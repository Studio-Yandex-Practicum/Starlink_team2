import datetime as dt
from typing import Dict, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import rich

from backend.core.config import settings
from backend.crud.admin import get_user
from backend.models.admin import Admin

router = APIRouter()


class OAuth2PasswordBearerWithCookie(OAuth2):
    """Этот класс взят напрямую из FastAPI.

    Единственное изменение — аутентификация берется из cookie,
        а не из заголовка!
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ) -> None:
        """Build an instance of OAuth2PasswordBearerWithCookie."""
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={
                "tokenUrl": tokenUrl,
                "scopes": scopes,
            },
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """ВАЖНО: эта строка отличается от FastAPI.

        Здесь мы используем
        `request.cookies.get(settings.COOKIE_NAME)` вместо
        `request.headers.get("Authorization").
        """
        authorization: Optional[str] = request.cookies.get(
            settings.COOKIE_NAME,
        )
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=settings.NOT_AUTHENTICATED,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def create_access_token(data: Dict) -> str:
    """Создание токена."""
    to_encode = data.copy()
    expire = dt.datetime.now() + dt.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(
    username: str,
    plain_password: str,
) -> Admin | bool:
    """Аутентификация пользователя."""
    user = await get_user(username)
    if not user or not crypto.verify(plain_password, user.hashed_password):
        return False
    return user


async def decode_token(token: str) -> Admin:
    """Декодирование токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    """Декодирование токена."""
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        rich.print(e)
        raise credentials_exception
    return await get_user(username)


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
) -> Admin:
    """Получите текущего пользователя из файлов cookie в запросе.

    Используйте эту функцию, когда хотите заблокировать маршрут, чтобы только
    аутентифицированные пользователи могли видеть доступ к маршруту.
    """
    return await decode_token(token)


async def get_current_user_from_cookie(request: Request) -> Admin:
    """Получите текущего пользователя из файлов cookie в запросе.

    Используйте эту функцию из других маршрутов,
        чтобы получить текущего пользователя.
    Хорошо для представлений,
        которые должны работать как для вошедших в систему,
            так и для не вошедших в систему пользователей.
    """
    token = request.cookies.get(settings.COOKIE_NAME, '')
    return await decode_token(token)


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, str]:
    """Логин с токеном."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"username": user.username})

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True,
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}

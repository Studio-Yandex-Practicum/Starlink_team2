from telebot.states import State, StatesGroup


class MailRegistrationState(StatesGroup):
    """Стейт для проверки регистрации почты."""

    mail = State()

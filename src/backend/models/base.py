from datetime import datetime

from core.db import preBase
from sqlalchemy import Column, DateTime


class AbstractModelForTime(preBase):

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    edited_at = Column(DateTime)

    def __repr__(self):
        return f'{self.created_at=}; {self.edited_at=}.'

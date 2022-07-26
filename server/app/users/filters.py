from typing import Optional

from app.db.filters import BaseFilter


class UserFilter(BaseFilter):
    name: Optional[str]

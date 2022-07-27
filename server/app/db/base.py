from sqlalchemy.orm import configure_mappers

from app.users.models import *  # noqa
from app.auth.models import *  # noqa
from app.partners.models import * # noqa

configure_mappers()

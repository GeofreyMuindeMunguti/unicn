"""add default admin

Revision ID: 809ce1c8e6e5
Revises: 52a57e95531a
Create Date: 2022-07-31 12:18:04.198480

"""
import datetime
import uuid

from alembic import op
import sqlalchemy as orm
from app.core.config import get_app_settings

settings = get_app_settings()


# revision identifiers, used by Alembic.
revision = '809ce1c8e6e5'
down_revision = '52a57e95531a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    now = datetime.datetime.now()
    op.execute(f"INSERT INTO users(id, name, email, created_at) VALUES ('{settings.DEFAULT_USER_ID}','SUPER-ADMIN', '{settings.DEFAULT_USER_EMAIL}', '{now}')")
    op.execute(f"INSERT INTO partners(id, name, owner_id, created_at) VALUES ('{settings.DEFAULT_ADMIN_ID}', 'TACTIVE CONSULTING', '{settings.DEFAULT_USER_ID}', '{now}')")
    op.execute(f"INSERT INTO partnermembers(id, user_id, partner_id, role, created_at) VALUES ('{str(uuid.uuid4())}','{settings.DEFAULT_USER_ID}', '{settings.DEFAULT_ADMIN_ID}', 'SUPER_ADMIN','{now}')")


def downgrade() -> None:
    op.execute(f"DELETE FROM partners WHERE id='{settings.DEFAULT_ADMIN_ID}'")
    op.execute(f"DELETE FROM users WHERE id='{settings.DEFAULT_USER_ID}'")
    op.execute(f"DELETE FROM partnermembers WHERE user_id='{settings.DEFAULT_USER_ID}' AND partner_id='{settings.DEFAULT_ADMIN_ID}'")

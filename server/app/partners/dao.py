from app.db.dao import CRUDDao, ChangedObjState
from app.exceptions.custom import DaoException, InvalidStateException
from app.partners.constants import PartnerMemberRoles
from app.partners.models import Partner, PartnerMember
from sqlalchemy.orm import Session, joinedload, selectinload
from app.partners.serializer import PartnerCreateSerializer, PartnerUpdateSerializer, PartnerMemberCreateSerializer, \
    PartnerMemberUpdateSerializer
from app.users.serializer import UserCreateSerializer


class PartnerDao(
    CRUDDao[
        Partner,
        PartnerCreateSerializer,
        PartnerUpdateSerializer
    ]
):
    def on_pre_create(
        self, db: Session, pk: str, values: dict, orig_values: dict
    ) -> None:
        if self.get(db, name=orig_values["name"]):
            raise DaoException(
                resource="Partner",
                message="Partner with such details already exists"
            )

        from app.users.dao import user_dao

        if owner := orig_values.pop("owner", None):
            user_obj = UserCreateSerializer(**owner)
            if not user_dao.get(db, email=owner["email"]):
                user = user_dao.create(db, obj_in=user_obj)
                user_dao.send_invitation(db, user_id=user.id, partner_name=orig_values.get(("name", "TACTIVE CONSULTING")))

                values["owner_id"] = user.id

    def on_post_create(
        self, db: Session, db_obj: Partner
    ) -> None:
        partner_member_dao.create(
            db, obj_in=PartnerMemberCreateSerializer(partner_id=db_obj.id, user_id=db_obj.owner_id, role=PartnerMemberRoles.PARTNER_ADMIN.value)
        )

    def deactivate(self, db: Session, obj_id: str) -> Partner:
        try:
            partner = self.get_not_none(db, id=obj_id)
            return self.update(db, obj_in={"is_active": False}, db_obj=partner)
        except InvalidStateException:
            raise DaoException(
                resource="PARTNER",
                message="Partner not found!"
            )

    def activate(self, db: Session, obj_id: str) -> Partner:
        try:
            partner = self.get_not_none(db, id=obj_id)
            return self.update(db, obj_in={"is_active": True}, db_obj=partner)
        except InvalidStateException:
            raise DaoException(
                resource="PARTNER",
                message="Partner not found!"
            )


partner_dao = PartnerDao(Partner, load_options=[joinedload(Partner.owner), selectinload(Partner.members)])


class PartnerMemberDao(
    CRUDDao[
        PartnerMember,
        PartnerMemberCreateSerializer,
        PartnerMemberUpdateSerializer
    ]
):
    pass


partner_member_dao = PartnerMemberDao(PartnerMember)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import deps
from app.core.deps import get_super_admin_member
from app.db.pagination import Page, PaginationQueryParams
from app.exceptions.custom import HttpErrorException, DaoException
from app.partners.dao import partner_dao
from app.partners.models import PartnerMember
from app.partners.serializer import PartnerCreateSerializer, PartnerSerializer

router = APIRouter(prefix="/partner")


@router.post("/", response_model=PartnerSerializer)
def create_partner(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: PartnerCreateSerializer,
    admin_member: PartnerMember = Depends(get_super_admin_member),
) -> PartnerSerializer:
    try:
        return partner_dao.create(db, obj_in=obj_in)
    except DaoException as e:
        raise HttpErrorException(
            status_code=403,
            error_code="FAILED CREATING PARTNER",
            error_message=f"{e.message}"
        )


@router.get("/", response_model=Page[PartnerSerializer])
def get_partners(
    db: Session = Depends(deps.get_db),
    pagination: PaginationQueryParams = Depends(),
    admin_member: PartnerMember = Depends(get_super_admin_member),
    _=Depends(deps.get_current_user),
) -> Page[PartnerSerializer]:
    return partner_dao.get_multi_paginated(db, params=pagination)


@router.get("/{bp_id}/", response_model=PartnerSerializer)
def get_by_id(
    db: Session = Depends(deps.get_db),
    *,
    bp_id: str,
    admin_member: PartnerMember = Depends(get_super_admin_member),
    _=Depends(deps.get_current_user),
) -> PartnerSerializer:
    return partner_dao.get_not_none(
        db, id=bp_id
    )

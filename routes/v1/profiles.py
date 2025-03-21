from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from typing import List, Optional

from core.deps import (
    get_current_user,
    is_admin,
    is_investor_or_admin,
)
from uuid import UUID


from schemas.exports import (
    ProfileSchema,
    ProfileUpdateSchema
)

from schemas.user import UserSchema, UserWithRoles
from models.profile import ProfileModel

from services.exports import (
    profile_service
)

router = APIRouter()

# =============================================================================
#                                   GET ALL 
# =============================================================================
@router.get(
    "/", 
    response_model=List[ProfileSchema]
)
async def get_all_profiles(
    current_user: UserSchema = Depends(is_admin)
):
    """
    Return All
    """
    return await profile_service.get_all()

# ==================================================================
#                                   CREATE   
# ==================================================================
@router.post(
    "/", 
    status_code=201
)
async def create_profile(
    data: ProfileSchema = Depends(),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    CREATE

    * Required field:
        - user_uuid
        - first_name
        - last_name
        - document_identification
        - birth_date
        - document_type
        - terms_conditions
        - bank_name
        - bank_account
        - bank_iban
        - profession
        - company
    """

    profile = profile_service.get(data.user_uuid)

    if not profile:
        return await profile_service.create( data)
    raise HTTPException(
        detail="Já existe um Perfil associado neste Utitlizador", 
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )

# ==================================================================
#                                   UPDATE   
# ==================================================================
@router.patch(
    "/", 
    status_code=200
)
async def update_profile(
    data: ProfileUpdateSchema,
    current_user: UserWithRoles = Depends(get_current_user)
):
    """
    UPDATE

    * Optional field:
        - user_uuid
        - first_name
        - last_name
        - document_identification
        - birth_date
        - document_type
        - terms_conditions
        - bank_name
        - bank_account
        - bank_iban
        - profession
        - company
    """

    profile:ProfileSchema = await profile_service.get_current_profile(current_user.uuid)

    if profile:
        return await profile_service.update(current_user.uuid, data)
    raise HTTPException(
        detail="Não existe um Perfil associado neste Utitlizador", 
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )

# ==================================================================
@router.get(
    "/{profile_uuid}",
    status_code=201
)
async def get_profile(
    profile_uuid: UUID,
    current_user: UserSchema = Depends(get_current_user)
):
    return await profile_service.get(profile_uuid)

# ==================================================================
@router.patch(
    "/approve/{profile_uuid}",
    status_code=201
)
async def approve(
    profile_uuid: UUID,
    current_user: UserSchema = Depends(is_admin)
):
    """
    Approve Profile
    """
    return await profile_service.approve(profile_uuid)

# ==================================================================
@router.get(
    "/my/current-profile"
)
async def current_profile(
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Return My Profile
    """
    return await profile_service.get_current_profile(current_user.uuid)


# ==================================================================
@router.patch(
    "/upload_avatar", 
    status_code=200
)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    CHANGE AVATAR

    * Optional field:
        - avatar
    """

    profile: ProfileSchema = await profile_service.get_current_profile(current_user.uuid)

    if profile:
        return await profile_service.upload_avatar(profile.uuid, file)
    raise HTTPException(
        detail="Não existe um Perfil associado neste Utitlizador", 
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )
















# ==================================================================
@router.patch(
    "/updating_finances",
    status_code=201
)
async def updating_finances(
    profile_uuid: UUID,
    current_user: UserSchema = Depends(is_admin)
):
    """
    Updating finances - Profile
    """
    return await profile_service.updating_finances(profile_uuid, current_user)

# ==================================================================

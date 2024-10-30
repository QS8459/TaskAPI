from fastapi import APIRouter, Depends, status, HTTPException;
from src.core.service.account.auth import get_current_user;
from src.core.service.profile.profile import get_profile_service;
from src.core.schemas.profile import ProfileDetailSchema, ProfileUpdateSchema;

profile_router = APIRouter(prefix="/profile", tags = ['profile']);

@profile_router.get('/me/',
                    status_code= status.HTTP_200_OK,
                    response_model=ProfileDetailSchema
                    )
async def get_profile(
        profile_service = Depends(get_profile_service),
        current_user = Depends(get_current_user),
):
    try:
        r = await profile_service.get_profile_by_acc_id(current_user.id)
        return r;
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}"
        )

@profile_router.put('/{pk}/',
                    status_code= status.HTTP_202_ACCEPTED,
                    response_model = ProfileUpdateSchema
)
async def edit_profile(
        pk,
        data: ProfileUpdateSchema,
        profile_service = Depends(get_profile_service),
        current_user = Depends(get_current_user),
):
    try:
        print("Private key",pk);
        print("Dict",data);
        r = await profile_service.get_and_update(pk, **data.dict());
        return r;

    except HTTPException as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'{e}'
        )

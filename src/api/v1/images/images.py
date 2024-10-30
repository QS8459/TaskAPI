from typing import Annotated;

from fastapi import APIRouter, Depends, File, status, Request;
from src.core.service.account.auth import get_current_user;
from src.core.service.images.images import get_image_service;
import os;

router = APIRouter(prefix="/image", tags = ['image'])

@router.post("/upload/",
            status_code= status.HTTP_202_ACCEPTED
            )
async def upload_image(
        request: Request,
        file: Annotated[bytes, File()],
        image_service = Depends(get_image_service),
        current_user = Depends(get_current_user)
                       ):
    print(file.content_type)
    return {'file_size':len(file)};


from typing import List, Annotated;
from pydantic.types import UUID;
from fastapi import APIRouter, Depends, HTTPException, status;
from src.core.schemas.account import (
    AddAccount, AccountDetail,
    AccountLoginSchema,
    Token,
    VerifyBody
);
from fastapi.security import OAuth2PasswordRequestForm;
from src.core.service.account.account import get_account_service;
from src.core.service.account.auth import generate_access_token, get_current_active_user, get_current_user;
from src.core.service.v_code.v_code import v_code_service;
router = APIRouter(prefix = "/account", tags = ['account']);

@router.post("/signup/",
            status_code= status.HTTP_201_CREATED,
            response_model = AccountDetail )
async def add_account(
    account_data:AddAccount,
    account_service = Depends(get_account_service),
    code_service = Depends(v_code_service)
):
    try:
        req = await account_service.add_account(**account_data.dict());
        if req:
            await code_service.generate_code(req.email, req.id);
        return req;
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"{e}",
        );

@router.post('/verify_account/',
             response_model=AccountDetail,
             status_code = status.HTTP_200_OK)
async def verify_account(
        data:VerifyBody,
        code_service = Depends(v_code_service),
        account_service = Depends(get_account_service)
):
    try:
        activation = await code_service.verify_user(data.id, data.code);
        if activation:
            return await account_service.activate_user(activation.get("user_id"))
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"{e}"
        )


@router.get("/all/",
            status_code= status.HTTP_200_OK,
            response_model = List[AccountDetail])
async def get_all_accounts(
        account_service = Depends(get_account_service),
        current_user = Depends(get_current_user)
):
    try:
        result = await account_service.get_all();
        return result;
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"{e}",
        );

@router.post("/login/",
             status_code= status.HTTP_200_OK,
            response_model= Token,
             )
async def account_login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        account_service = Depends(get_account_service)
):
    try:
        credential = AccountLoginSchema(email = form_data.username, password = form_data.password);

        user = await account_service.auth_user(credential)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        );
        access_token = generate_access_token(data = {
            "sub": user.email
        },
        expiration_delta=None);
        return access_token;
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"{e}",
        );

@router.get("/me/")
async def me(current_user=Depends(get_current_user)):
    return current_user;

@router.get("/{pk}/",
            status_code = status.HTTP_200_OK,
            response_model = AccountDetail)
async def get_account(
        pk: UUID,
        account_service = Depends(get_account_service)
):
    try:
        result = await account_service.get_by_id(pk);
        return result;
    except ValueError as e:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"{e}",
        );

@router.delete("/{pk}/",
               status_code = status.HTTP_204_NO_CONTENT)
async def delete_account(
        pk: UUID,
        account_service = Depends(get_account_service)
):
    try:
        result = await account_service.delete(pk);
        return None;
    except ValueError as e:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"{e}",
        );
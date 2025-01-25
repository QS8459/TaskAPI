from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import traceback
from src.logger import log


async def logger(request: Request, call_next):
    try:
        response = await call_next(request)
    except (HTTPException, ValueError, Exception) as e:
        log.error(
            f"EXCEPTION HAPPENED PLEASE CHECK here is error message {e}\n"
            f"{traceback.format_exc()}"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Something went terribly wrong"},
        )
    return response

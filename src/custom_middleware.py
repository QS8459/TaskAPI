from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.logger import log

async def logger(request: Request, call_next):
    try:
        log.info(call_next.__name__)
        response = await call_next(request)
    except (HTTPException, ValueError, Exception) as e:
        log.error(f"EXCEPTION HAPPENED PLEASE CHECK here is error message {e}")
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"detail":"Something went terribly wrong"}
        )
    return response

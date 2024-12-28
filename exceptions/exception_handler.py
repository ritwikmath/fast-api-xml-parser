from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from exceptions.custom_exceptions import CustomException
from main import app
from fastapi.exceptions import RequestValidationError


@app.exception_handler(CustomException)
def handle_custom_exception(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.message
    )


@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    print(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    errors = [{"field": "->".join(err['loc']), "message": err['msg']} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"message": "Validation Error", "details": errors},
    )


@app.exception_handler(Exception)
def handle_http_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

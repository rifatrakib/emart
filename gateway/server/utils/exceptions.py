from fastapi import HTTPException, status


def handle_400_bad_request(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"msg": msg},
    )


def handle_401_unauthorized(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": msg},
    )


def handle_403_forbidden(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"msg": msg},
    )


def handle_404_not_found(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": msg},
    )


def handle_410_gone(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_410_GONE,
        detail={"msg": msg},
    )


def handle_422_unprocessable_entity(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"msg": msg},
    )

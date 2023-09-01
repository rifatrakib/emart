from fastapi import HTTPException, status


def raise_401_unauthorized(message: str = "Not authorized") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": message},
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_403_forbidden(message: str = "Forbidden") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"msg": message},
    )


def raise_404_not_found(message: str = "Not found") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": message},
    )


def raise_409_conflict(message: str = "Conflict") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"msg": message},
    )


def raise_422_unprocessable_entity(message: str = "Unprocessable entity") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"msg": message},
    )

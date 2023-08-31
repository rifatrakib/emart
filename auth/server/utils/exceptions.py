from fastapi import HTTPException, status


def raise_422_unprocessable_entity(message: str = "Unprocessable entity") -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"msg": message},
    )

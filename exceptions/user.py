from fastapi import HTTPException, status

DEACTIVATED_USER_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail={
        "error": "Unprocessable Entity",
        "message": "The user is deactivated!"
    }
)


USER_NOT_FOUND_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "error": "Not Found",
        "message": "User Not Found!"
    }
)

USER_NO_CONTENT_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail={
        "error": "No Content",
        "message": "No Content For User!"
    }
)

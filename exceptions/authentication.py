from fastapi import HTTPException, status

CREDENTIAL_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "error": "Unauthorized",
        "message": "The credential could not be authenticated"
    },
    headers={"WWW-Authenticate": "Bearer"},
)

AGENT_CREDENTIAL_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "error": "Unauthorized",
        "message": "The agent credential service could not be authenticated"
    },
    headers={"WWW-Authenticate": "Bearer"},
)

TOKEN_NOT_PROVIDED_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "error": "Unauthorized",
        "message": "Token not provided"
    }
)

INVALID_TOKEN_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "error": "Bad Request",
        "message": "Invalid Token!"
    }
)

DEACTIVATED_WALLET_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail={
        "error": "Unprocessable Entity",
        "message": "The token is deactivated!"
    }
)

NOT_FOUND_EXCEPTION: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "error": "Not Found",
        "message": "Not Found!"
    }
)
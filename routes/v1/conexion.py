"""
---
"""

from fastapi import APIRouter, Response, status
from core.config import settings
# from providers.exports import gb
import requests

router = APIRouter()


# GET current user
@router.get("/")
def is_online():
    """
    is_online:
        - endpoint to verify if api/v1 still online
    """
    # value = gb.get_feature_value("can-see-reference-section", "fallback")
    # print(value)
    # print(settings.ENV.lower not in ("prd", "production"))
    # if gb.is_on("can-see-reference-section"):
    #     print("Feature is enabled!")
    return Response(status_code=status.HTTP_200_OK)

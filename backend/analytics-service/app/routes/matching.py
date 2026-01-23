from fastapi import APIRouter, Depends, Header
from typing import List
from uuid import UUID

from app.services.matching_service import (
    recommend_matches,
    recommend_nearest_farmers
)
from app.schemas.matching import MatchResponse, NearestFarmersRequest, RecommendationsRequest
from app.clients.auth_client import get_token_from_header, require_roles, get_current_user

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.post("/recommendations", response_model=MatchResponse)
def recommendations(
    data: RecommendationsRequest, 
    authorization: str = Header(...),
    user=Depends(require_roles(["buyer"]))
):
    token = get_token_from_header(authorization)

    return recommend_matches(
        crop=data.crop,
        listing_ids=data.listing_ids,
        token=token,
        user_id=user["id"]
    )

@router.post("/nearest-farmers")
def nearest_farmers(
    data: NearestFarmersRequest,
    user=Depends(require_roles(["buyer"]))
):
    return {
        "buyer_id": data.buyer_id,
        "nearest_farmers": recommend_nearest_farmers(data.buyer_id)
    }

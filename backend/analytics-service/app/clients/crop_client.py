import requests
from uuid import UUID
from fastapi import HTTPException
from app.core.config import settings

def get_listing(listing_id: UUID, token: str) -> dict:
    url = f"{settings.LISTING_SERVICE_URL}/{listing_id}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Listing not found")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Listing service error")

    return response.json()


def get_listing_price(listing_id: UUID, token: str) -> float:
    return get_listing(listing_id, token)["price"]

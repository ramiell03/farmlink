import httpx
import requests
from uuid import UUID
from fastapi import HTTPException
from app.core.core import settings

def get_listing_price(listing_id: UUID, token: str) -> float:
    url = f"{settings.LISTING_SERVICE_URL}/{listing_id}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized to access listing")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Listing not found")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Listing service error")

    return response.json()["price"]

def get_listing_ids_by_crop(crop: str, token: str) -> list[str]:
    url = f"{settings.LISTING_SERVICE_URL}/by-crop/{crop}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Listing service error")

    return [item["id"] for item in response.json()]


def get_listing_ids_by_farmer(farmer_id: str, token: str) -> list[str]:
    url = f"{settings.LISTING_SERVICE_URL}/by-farmer/{farmer_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.get(url, headers=headers, timeout=15)
    
    if res.status_code != 200:
        return []
    
    return [item["id"] for item in res.json()]

def get_listing_by_id(listing_id: UUID, token: str) -> dict:
    url = f"{settings.LISTING_SERVICE_URL}/{listing_id}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Listing not found")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Listing service error")

    return response.json()

def update_listing_quantity(
    listing_id: UUID,
    quantity: int,
    available: bool,
    token: str
):
    url = f"{settings.LISTING_SERVICE_URL}/{listing_id}"

    payload = {
        "quantity": quantity,
        "available": available
    }

    response = requests.patch(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Failed to update listing"
        )
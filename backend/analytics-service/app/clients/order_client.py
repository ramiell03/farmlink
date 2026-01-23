import httpx
from typing import List, Dict
from uuid import UUID
from app.core.config import settings  

def get_orders_for_crop(crop: str, token: str) -> List[Dict]:
    order_service_url = settings.ORDER_SERVICE_URL.rstrip("/")
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = httpx.get(
            f"{order_service_url}/by-crop/{crop}",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        print(f"[Order Client] Request error: {e}")
        return []
    except httpx.HTTPStatusError as e:
        print(f"[Order Client] HTTP error: {e}")
        return []

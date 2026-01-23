from uuid import UUID
from typing import List
from sqlalchemy.orm import Session

from app.algorithms.priority_queue import MaxPriorityQueue
from app.services.scoring_service import farmer_score
from app.clients.crop_client import get_listing
from app.schemas.matching import FarmerRecommendation
from app.models.recommendation import Recommendation
from app.db.database import SessionLocal


def recommend_matches(
    crop: str,
    listing_ids: List[UUID],
    token: str,
    user_id: UUID
):
    db: Session = SessionLocal()
    pq = MaxPriorityQueue()

    for listing_id in listing_ids:
        listing = get_listing(listing_id, token)

        score = farmer_score(
            price=listing["price"],
            quantity=listing["quantity"]
        )

        pq.push(score, listing)

    recommendations: List[FarmerRecommendation] = []

    while not pq.is_empty() and len(recommendations) < 5:
        listing = pq.pop()

        score = farmer_score(
            price=listing["price"],
            quantity=listing["quantity"]
        )

        db.add(
            Recommendation(
                user_id=user_id,
                target_id=listing["farmer_id"],
                crop=crop,
                score=score
            )
        )

        recommendations.append(
            FarmerRecommendation(
                farmer_id=listing["farmer_id"],
                price=listing["price"],
                quantity=listing["quantity"],
                score=score
            )
        )

    db.commit()
    db.close()

    return {
        "crop": crop,
        "recommendations": recommendations
    }


def recommend_nearest_farmers(buyer_id: str):
    return []

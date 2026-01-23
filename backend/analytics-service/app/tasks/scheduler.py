import asyncio
import logging
from app.services.analytics_service import recompute_analytics

logger = logging.getLogger(__name__)


class AnalyticsScheduler:
    def __init__(self, interval: int):
        self.interval = interval
        self._running = False

    async def start(self):
        if self._running:
            return

        self._running = True
        logger.info("Analytics scheduler started")

        while self._running:
            try:
                await recompute_analytics()
                logger.info("Analytics recomputation completed")
            except Exception as e:
                logger.exception("Analytics recomputation failed")

            await asyncio.sleep(self.interval)

    def stop(self):
        self._running = False
        logger.info("Analytics scheduler stopped")

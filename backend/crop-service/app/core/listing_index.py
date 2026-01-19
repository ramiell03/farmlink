import heapq

class ListingIndex:
    def __init__(self):
        self.by_crop ={}
        self.quality_heap = []
        
    def add_listing(self, crop_id, listing):
        self.by_crop.setdefault(crop_id, []).append(listing)
        heapq.heappush(self.quality_heap, (-listing.average_quality, listing.id))
        
    def top_quality(self, limit=5):
        return heapq.nsmallest(limit, self.quality_heap)
    
    def autocomplete(self, query: str, limit=10):
        query = query.lower()
        results = []
        for crop_name in self.by_crop:
            if crop_name.startswith(query):
                results.append(crop_name)
        return results[:limit]
    
listing_index = ListingIndex()
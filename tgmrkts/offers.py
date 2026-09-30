"""Offers object of MRKT client"""

class Offers:
    def __init__(self, client):
        self._client = client

    async def create(self, price: int, giftSaleId: str):
        payload = {
            "price": price,
            "giftSaleId": giftSaleId
        }
        response = await self._client.http.post("offers/create", json=payload)
        response.raise_for_status()
        return await response.json()

    async def cancel(self, offerId: str):
        response = await self._client.http.post(f"offers/cancel?offerId={offerId}")
        response.raise_for_status()
        return await response.json()

    async def activities(self, *, count: int = 20, isActive: bool = True, filters: list = ["Offers", "ChannelOffers", "GiftsCollectionOffers"]):
        response = await self._client.http.get("activities/with-totals", params={"count": count, "isActive": str(isActive).lower(), "filters": filters})
        response.raise_for_status()
        return await response.json()
    
    async def myOffersByGift(self, id: str, count: int = 20):
        response = await self._client.http.get(f"offers/by-gift/{id}?count={count}")
        response.raise_for_status()
        return await response.json()
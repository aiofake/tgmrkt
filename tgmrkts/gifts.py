'''Gifts object of MRKT client'''

from typing import *

class Gifts:
    def __init__(self, client):
        self._client = client

    async def saling(
        self,
        *,
        count: int = 20,
        cursor: str = "",
        collectionNames: list[str] | None = None,
        modelNames: list[str] | None = None,
        backdropNames: list[str] | None = None,
        symbolNames: list[str] | None = None,
        number: int | None = None,
        isNew: bool | None = None,
        isPremarket: bool | None = None,
        luckyBuy: bool | None = None,
        giftType: str | None = None,
        craftable: bool | None = None,
        isCrafted: bool | None = None,
        tgCanBeCraftedFrom: bool | None = None,
        removeSelfSales: bool | None = None,
        isTransferable: bool | None = None,
        availableForStaking: bool | None = None,
        forGame: bool | None = None,
        minPrice: int | None = None,
        maxPrice: int | None = None,
        ordering: str = "Price",
        lowToHigh: bool = True,
        query: str | None = None,
        **kwargs
    ) -> dict:
        payload = {
            "count": count,
            "cursor": cursor,
            "collectionNames": collectionNames or [],
            "modelNames": modelNames or [],
            "backdropNames": backdropNames or [],
            "symbolNames": symbolNames or [],
            "number": number,
            "isNew": isNew,
            "isPremarket": isPremarket,
            "luckyBuy": luckyBuy,
            "giftType": giftType,
            "craftable": craftable,
            "isCrafted": isCrafted,
            "tgCanBeCraftedFrom": tgCanBeCraftedFrom,
            "removeSelfSales": removeSelfSales,
            "isTransferable": isTransferable,
            "availableForStaking": availableForStaking,
            "forGame": forGame,
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "ordering": ordering,
            "lowToHigh": lowToHigh,
            "query": query,
            **kwargs
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self._client.http.post("gifts/saling", json=payload)
        response.raise_for_status()
        return await response.json()

    async def buy(self, *, ids: list):
        response = await self._client.http.post("gifts/buy", json={"ids": ids})
        response.raise_for_status()
        return await response.json()
        
    async def sale(self, *, ids: list, price: int):
        response = await self._client.http.post("gifts/sale", json={"ids": ids, "price": price})
        response.raise_for_status()
        return await response.json()
    
    async def collections(self) -> list[dict]:
        response = await self._client.http.get("gifts/collections")
        response.raise_for_status()
        return await response.json()

    async def models(self, collections: list[str]) -> list[dict]:
        response = await self._client.http.post("gifts/models", json={"collections": collections})
        response.raise_for_status()
        return await response.json()

    async def backdrops(self, collections: list[str]) -> list[dict]:
        response = await self._client.http.post("gifts/backdrops", json={"collections": collections})
        response.raise_for_status()
        return await response.json()

    async def inventory(
        self,
        *,
        isListed: bool | None = None,
        count: int = 20,
        cursor: str = "",
        collectionNames: list[str] | None = None,
        modelNames: list[str] | None = None,
        backdropNames: list[str] | None = None,
        symbolNames: list[str] | None = None,
        number: int | None = None,
        isNew: bool | None = None,
        isPremarket: bool | None = None,
        luckyBuy: bool | None = None,
        giftType: str | None = None,
        craftable: bool | None = None,
        isCrafted: bool | None = None,
        tgCanBeCraftedFrom: bool | None = None,
        removeSelfSales: bool | None = None,
        isTransferable: bool | None = None,
        availableForStaking: bool | None = None,
        forGame: bool | None = None,
        minPrice: int | None = None,
        maxPrice: int | None = None,
        ordering: str = "None",
        lowToHigh: bool = False,
        query: str | None = None,
        **kwargs
    ) -> dict:
        payload = {
            "isListed": isListed,
            "count": count,
            "cursor": cursor,
            "collectionNames": collectionNames or [],
            "modelNames": modelNames or [],
            "backdropNames": backdropNames or [],
            "symbolNames": symbolNames or [],
            "number": number,
            "isNew": isNew,
            "isPremarket": isPremarket,
            "luckyBuy": luckyBuy,
            "giftType": giftType,
            "craftable": craftable,
            "isCrafted": isCrafted,
            "tgCanBeCraftedFrom": tgCanBeCraftedFrom,
            "removeSelfSales": removeSelfSales,
            "isTransferable": isTransferable,
            "availableForStaking": availableForStaking,
            "forGame": forGame,
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "ordering": ordering,
            "lowToHigh": lowToHigh,
            "query": query,
            **kwargs
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self._client.http.post("gifts", json=payload)
        response.raise_for_status()
        return await response.json()

    async def history(self, *, limit: int = 20, type: str = "Gift", **kwargs) -> dict:
        response = await self._client.http.get("history", json={"limit": limit, "type": type, **kwargs})
        response.raise_for_status()
        return await response.json()
    
    async def feed(
        self,
        *,
        count: int = 20,
        cursor: str = "",
        collectionNames: list[str] | None = None,
        modelNames: list[str] | None = None,
        backdropNames: list[str] | None = None,
        number: int | None = None,
        type: list[str] | None = None,          # "listing", "sale", "return", "unlisting", "change_price", "upload"
        minPrice: int | None = None,
        maxPrice: int | None = None,
        ordering: str = "Latest",
        lowToHigh: bool = False,
        query: str | None = None,
        **kwargs
    ) -> dict:
        payload = {
            "count": count,
            "cursor": cursor,
            "collectionNames": collectionNames or [],
            "modelNames": modelNames or [],
            "backdropNames": backdropNames or [],
            "number": number,
            "type": type or [],
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "ordering": ordering,
            "lowToHigh": lowToHigh,
            "query": query,
            **kwargs
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        response = await self._client.http.post("feed", json=payload)
        response.raise_for_status()
        return await response.json()
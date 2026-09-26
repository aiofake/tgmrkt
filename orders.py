"""Orders object of MRKT client"""
from aiohttp import ClientResponseError

class Orders:
    def __init__(self, client):
        self._client = client


    async def create(
        self,
        *,
        collectionName: str = None,
        modelName: str = None,
        backdropName: str = None,
        symbolName: str = None,
        priceMinNanoTONs: int = 500000000,
        priceMaxNanoTONs: int = 1000000000,
        quantity: int = 1,
        isTransferable: bool = False,
        **kwargs
    ):
        payload = {
            "collectionName": collectionName,
            "modelName": modelName,
            "backdropName": backdropName,
            "symbolName": symbolName,
            "priceMinNanoTONs": priceMinNanoTONs,
            "priceMaxNanoTONs": priceMaxNanoTONs,
            "quantity": quantity,
            "isTransferable": isTransferable,
            **kwargs
        }
        response = await self._client.http.post("orders/create", json=payload)
        response.raise_for_status()
        return await response.json()


    async def cancel(self, orderId: str):
        try:
            response = await self._client.http.post(f"orders/cancel/{orderId}")
            response.raise_for_status()
            return True
        except ClientResponseError:
            return False
        except Exception as e:
            raise e


    async def list(
        self,
        *, 
        collectionNames: list[str],
        modelNames: list[str] = [],
        backdropNames: list[str] = [],
        symbolNames: list[str] = [],
        availableForStaking: bool = None,
        minPrice: float = None,
        maxPrice: float = None,
        ordering: str = "Price",
        lowToHigh: bool = False,
        query: str = None,
        cursor: str = "",
        count: int = 20,
        **kwargs
    ) -> list[dict]:
        payload = {
            "collectionNames": collectionNames,
            "modelNames": modelNames,
            "backdropNames": backdropNames,
            "symbolNames": symbolNames,
            "availableForStaking": availableForStaking,
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "ordering": ordering,
            "lowToHigh": lowToHigh,
            "query": query,
            "cursor": cursor,
            "count": count,
            **kwargs
        }
        response = await self._client.http.post("orders", json=payload)
        response.raise_for_status()
        return await response.json()

    
    async def fill(self, *, orderId: str, giftIds: str):
        response = await self._client.http.post("orders/fill", json={"orderId": orderId, "giftIds": giftIds})
        response.raise_for_status()
        return await response.json()


    async def getMyOrders(
        self,
        *, 
        collectionNames: list = [],
        modelNames: list = [],
        backdropNames: list = [],
        symbolNames: list = [],
        availableForStaking: bool = None, 
        minPrice: float = None, 
        maxPrice: float = None, 
        ordering: str = "PublicationTime",
        lowToHigh: bool = False,
        query: str = None,
        cursor: str = "", 
        count: int = 20,
        **kwargs
    ):
        payload = {
            "collectionNames": collectionNames,
            "modelNames": modelNames,
            "backdropNames": backdropNames,
            "symbolNames": symbolNames,
            "availableForStaking": availableForStaking,
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "ordering": ordering,
            "lowToHigh": lowToHigh,
            "query": query,
            "cursor": cursor,
            "count": count,
            **kwargs
        }
        response = await self._client.http.post("orders/get-my-orders", json=payload)
        response.raise_for_status()
        return await response.json()


    async def allCollectionTop(self):
        response = await self._client.http.get("orders/all-collection-top")
        response.raise_for_status()
        return await response.json()


    async def giftsHistory(self, *, st_from: str = "", limit: int = 20, **kwargs):
        payload = {
            "from": st_from,
            "limit": limit,
            **kwargs
        }
        response = await self._client.http.post("orders/gifts-history", json=payload)
        response.raise_for_status()
        return await response.json()


    async def top(self, *, collectionName: str, modelName: str = None, backdropName: str = None, symbolName: str = None):
        payload = {
            "collectionName": collectionName,
            "modelName": modelName,
            "backdropName": backdropName,
            "symbolName": symbolName
        }
        response = await self._client.http.post("orders/top", json=payload)
        response.raise_for_status()
        return await response.json()
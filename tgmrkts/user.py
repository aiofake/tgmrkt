'''User-related operations for the MRKT client'''

from typing import *

class User:
    def __init__(self, client):
        self._client = client

    async def me(self):
        response = await self._client.http.get("me")
        response.raise_for_status()
        return await response.json()
    
    async def balance(self):
        response = await self._client.http.get("balance")
        response.raise_for_status()
        return await response.json()

    async def withdraw(self, nanoTONs: int, walletAddress: str):
        response = await self._client.http.post("wallet/withdraw/tons", json={"nanoTONs": nanoTONs, "wallet": walletAddress})
        response.raise_for_status()
        return await response.json()

    async def transactions(self):
        response = await self._client.http.get("transactions/await")
        response.raise_for_status()
        return await response.json()
    
    '''Experimental method to autoWithdraw'''
    async def autoWithdraw(self, nanoTONs: int = None):
        if not nanoTONs:
            balance = await self.balance()
            nanoTONs = balance.get("balance").get("hard")

        wallet = await self.me().get("wallet").get("ton")
        response = await self._client.http.post("wallet/withdraw/tons", json={"nanoTONs": nanoTONs, "wallet": wallet})
        response.raise_for_status()
        return await response.json()

    async def configs(self):
        response = await self._client.http.get("configs")
        response.raise_for_status()
        return await response.json()

    async def get_locale(self, locale: str):
        response = await self._client.http.get("get_locale", json={"locale": locale})
        response.raise_for_status()
        return await response.json()

    async def tasks(self):
        response = await self._client.http.get("tasks/new")
        response.raise_for_status()
        return await response.json()
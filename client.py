"""Main object of MRKT client"""

import random
from aiohttp import ClientSession
from .gifts import Gifts
from .orders import Orders
from .offers import Offers
from .user import User
from .auth import get_token, refresh_token


class MrktClient:
    def __init__(
        self,
        token: str | None = None,
        *,
        session: str | None = None,
        workdir: str = ".",
        proxy: str | None = None,
        packed: bool = True,
        headers: dict | None = None,
    ):
        self.token = token
        self._session = session
        self.workdir = workdir
        self.proxy = proxy
        self.headers = headers or {}
        self._closed = False
        self.http: ClientSession | None = None

        if packed:
            self.gifts = Gifts(self)
            self.orders = Orders(self)
            self.offers = Offers(self)
        self.user = User(self)

    def _setup_http(self):
        chrome, edge = random.randint(120, 145), random.randint(120, 145)

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "content-type": "application/json",
            "origin": "https://cdn.tgmrkt.io",
            "priority": "u=1, i",
            "referer": "https://cdn.tgmrkt.io/",
            "sec-ch-ua": f'"Not=A?Brand";v="8", "Chromium";v="{chrome}", "Microsoft Edge";v="{edge}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": random.choice(['"Windows"', '"macOS"', '"Linux"']),
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-fetch-storage-access": "active",
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome}.0.0.0 Safari/537.36 Edg/{edge}.0.0.0",
        }
        if self.token:
            headers["authorization"] = f"Bearer {self.token}"
            headers["cookie"] = f"access_token={self.token}"
        self.headers.update(headers)

        self.http = ClientSession(
            base_url="https://api.tgmrkt.io/api/v1/",
            headers=self.headers,
            proxy=self.proxy,
        )
        self._closed = False

    async def auth(self, tgWebAppData: str) -> str:
        if not self.http:
            self._setup_http()
        response = await self.http.post("auth", json={"data": tgWebAppData})
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        if not token:
            raise ValueError(f"Auth failed: {data}")
        return token

    async def start(self) -> "MrktClient":
        if not self.token and self._session:
            self.token = await refresh_token(session=self._session, workdir=self.workdir, proxy=self.proxy)
        if not self.http and self.token:
            self._setup_http()
        return self

    @classmethod
    async def session(
        cls, 
        session: str, 
        *, 
        workdir: str = ".", 
        proxy: str | None = None, 
        **kwargs
    ):
        token = await refresh_token(session, workdir=workdir, proxy=proxy)
        return cls(token=token, workdir=workdir, proxy=proxy, **kwargs)

    @classmethod
    async def init_data(
        cls,
        init_data: str,
        *,
        workdir: str = ".",
        proxy: str | None = None,
        impersonate: str = "chrome124",
        **kwargs,
    ) -> "MrktClient":
        token = await get_token(init_data, proxy=proxy)
        return cls(token=token, workdir=workdir, proxy=proxy, impersonate=impersonate, **kwargs)

    def set_token(self, token: str) -> None:
        self.token = token
        self.headers["authorization"] = f"Bearer {token}"
        self.headers["cookie"] = f"access_token={token}"

        if self.http is None:
            self._setup_http()
        else:
            self.http.headers.update({
                "authorization": f"Bearer {token}",
                "cookie": f"access_token={token}",
            })

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if not self._closed and self.http:
            await self.http.close()
            self._closed = True
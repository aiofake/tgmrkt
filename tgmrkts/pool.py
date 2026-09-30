import asyncio
from typing import *

from .client import MrktClient
from .utils import get_tokens


class MrktPool:
    def __init__(
        self,
        *,
        tokens: list[str] | None = None,
        sessions: list[str] | None = None,
        workdir: str = ".",
        tasks: list[tuple[str, dict]] | None = None,
        proxy: str | None = None,
        unlimited: bool = False
    ):
        self.clients: list["MrktClient"] = []
        self._tasks = tasks
        self.proxy = proxy
        self.workdir = workdir
        self._kwargs = {
            "proxy": self.proxy,
            "workdir": self.workdir
        }
        self._unlimited = unlimited

        if tokens and sessions:
            raise ValueError("Client can not run with tokens and sessions both")
        
        if tokens:
            self.clients = [MrktClient(token=token, **self._kwargs) for token in tokens]
        elif sessions:
            self._load_sessions(sessions)
        else:
            raise ValueError("Client can not run without tokens or sessions")

    @classmethod
    async def from_sessions(
        cls,
        sessions: list[str],
        *,
        workdir: str = ".",
        proxy: str | None = None,
        concurrency: int = 5,
        **kwargs: Any,
    ) -> "MrktPool":
        tokens = await get_tokens(
            sessions,
            workdir=workdir,
            proxy=proxy,
            concurrency=concurrency,
        )
        return cls(
            tokens=tokens,
            workdir=workdir,
            proxy=proxy,
            **kwargs,
        )

    def _load_sessions(self, sessions: list[str]):
        async def load():
            tokens = await get_tokens(sessions, workdir=self.workdir, proxy=self.proxy)
            self.clients = [MrktClient(token=t, **self._kwargs) for t in tokens]

        self._token_future = load()

    async def start(self):
        if not self.clients and hasattr(self, "_token_future"):
            await self._token_future
            self.clients = [MrktClient(token=t, **self._kwargs) for t in self.clients]

    async def map(
            self,
            coro_func: Callable[[MrktClient], Awaitable[Any]],
            *,
            concurrency: int = 5,
        ) -> list[Any | Exception]:
            if concurrency < 1 and not self._unlimited:
                raise ValueError("concurrency must be greater than zero")
    
            sem = asyncio.Semaphore(concurrency)
    
            async def worker(client):
                async with sem:
                    return await coro_func(client)
    
            return await asyncio.gather(*(worker(c) for c in self.clients), return_exceptions=True)

    async def close(self):
        if self.clients:
            await asyncio.gather(*[c.close() for c in self.clients], return_exceptions=True)
            self.clients.clear()

    async def __aenter__(self) -> "MrktPool":
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
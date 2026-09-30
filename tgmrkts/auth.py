async def get_token(init_data: str, *, proxy: str | None = None) -> str:
    from .client import MrktClient

    async with MrktClient(token=None, proxy=proxy) as client:
        return await client.auth(init_data)


async def refresh_token(session: str, *, workdir: str = ".", proxy: str | None = None) -> str:
    from .utils import get_init_data

    init_data = await get_init_data(session, workdir=workdir, proxy=proxy)
    return await get_token(init_data, proxy=proxy)
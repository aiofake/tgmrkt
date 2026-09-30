import asyncio
import urllib.parse
import pyrogram
from .auth import refresh_token


def _pyrogram_proxy(proxy: str | dict | None) -> dict | None:
    if proxy is None or isinstance(proxy, dict):
        return proxy

    parsed = urllib.parse.urlsplit(proxy if "://" in proxy else f"http://{proxy}")
    if not parsed.hostname or parsed.port is None:
        raise ValueError("proxy must contain a hostname and port")

    scheme = parsed.scheme.lower()
    if scheme not in {"http", "socks4", "socks5"}:
        raise ValueError(f"Unsupported Pyrogram proxy scheme: {scheme}")

    result = {
        "scheme": scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
    }
    if parsed.username:
        result["username"] = urllib.parse.unquote(parsed.username)
    if parsed.password:
        result["password"] = urllib.parse.unquote(parsed.password)
    return result


async def get_init_data(
    session: str,
    workdir: str = ".",
    proxy: str | dict | None = None,
    username: str = "mrkt",
) -> str:
    async with pyrogram.Client(
        session,
        workdir=workdir,
        proxy=_pyrogram_proxy(proxy),
    ) as cli:
        bot = await cli.resolve_peer(username)
        url = await cli.get_main_web_app(bot.user_id, bot.user_id)
        query = url.split("tgWebAppData=")[1].split("tgWebAppVersion")[0]
        try:
            return query
        except (KeyError, IndexError) as exc:
            raise ValueError("Telegram WebApp URL does not contain tgWebAppData") from exc


async def get_tokens(
    sessions: list[str],
    *,
    workdir: str = ".",
    proxy: str | dict | None = None,
    concurrency: int = 5
) -> list[str]:
    if concurrency < 1:
        raise ValueError("concurrency must be greater than zero")

    sem = asyncio.Semaphore(concurrency)

    async def worker(session: str):
        async with sem:
            return await refresh_token(session, workdir=workdir, proxy=proxy)

    results = await asyncio.gather(*(worker(s) for s in sessions), return_exceptions=True)

    tokens = []
    for res in results:
        if isinstance(res, Exception):
            print(f"[!] Session {res} failed: {res}")
        else:
            tokens.extend(res if isinstance(res, list) else [res])
    return tokens
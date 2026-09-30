# MRKT Python Client

An asynchronous Python client for the [MRKT](https://t.me/mrkt) API.

## Features

- Authenticated API access with `MrktClient`
- Multi-account requests with `MrktPool`
- Gifts, orders, offers, and user API methods
- Access-token and Telegram-session authentication
- Optional proxy support

## Installation

```bash
python -m pip install tgmrkts
```

Python 3.10 or newer is required. `aiohttp` and `kurigram` are installed as
package dependencies; `kurigram` is used for Telegram-session authentication.

## Quick Start

```python
import asyncio

from tgmrkts import MrktClient


async def get_orders(client: MrktClient, collection: str) -> None:
    async with client as api:
        orders = await api.orders.list(
            collectionNames=[collection],
            count=10,
        )
        print(orders)


client = MrktClient(token="YOUR_ACCESS_TOKEN")
asyncio.run(get_orders(client, "Plush Pepe"))
```

The HTTP session is created lazily when the client enters the async context, so the client can safely be created before `asyncio.run()`.

You can also create it inside the coroutine:

```python
async def main() -> None:
    async with MrktClient(token="YOUR_ACCESS_TOKEN") as api:
        print(await api.gifts.collections())


asyncio.run(main())
```

Always close clients with `async with` or `await client.close()`.

## Authentication

### Access token

```python
client = MrktClient(token="YOUR_ACCESS_TOKEN")
```

### Telegram session

```python
import asyncio

from tgmrkts import MrktClient


async def main() -> None:
    client = await MrktClient.session(
        "my_telegram_session",
        workdir=".",
    )
    async with client as api:
        print(await api.user.me())


asyncio.run(main())
```

A proxy can be passed with `proxy="http://host:port"`.

## API Examples

### Gifts

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as api:
    listings = await api.gifts.saling(
        collectionNames=["Plush Pepe"],
        count=20,
        ordering="Price",
        lowToHigh=True,
    )
    inventory = await api.gifts.inventory(isListed=False)
```

Available methods include `collections`, `models`, `backdrops`, `saling`, `inventory`, `history`, `feed`, `buy`, and `sale`.

### Orders

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as api:
    orders = await api.orders.list(
        collectionNames=["Plush Pepe"],
        count=10,
    )
    top_orders = await api.orders.top(collectionName="Plush Pepe")
```

Available methods include `create`, `cancel`, `list`, `fill`, `getMyOrders`, `allCollectionTop`, `giftsHistory`, and `top`.

### Offers

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as api:
    activities = await api.offers.activities(count=20)
    offers = await api.offers.myOffersByGift("GIFT_ID")
```

Available methods include `create`, `cancel`, `activities`, and `myOffersByGift`.

### User

```python
async with MrktClient(token="YOUR_ACCESS_TOKEN") as api:
    profile = await api.user.me()
    balance = await api.user.balance()
    transactions = await api.user.transactions()
```

## Multiple Accounts

```python
import asyncio

from tgmrkts import MrktPool


async def get_balance(client) -> dict:
    async with client as api:
        return await api.user.balance()


async def main() -> None:
    async with MrktPool(tokens=["TOKEN_1", "TOKEN_2"]) as pool:
        results = await pool.map(get_balance, concurrency=2)
        for result in results:
            print(result)


asyncio.run(main())
```

`MrktPool.map()` returns exceptions as results. Check them before using the response:

```python
for result in results:
    if isinstance(result, Exception):
        print(f"Request failed: {result}")
```

Create a pool from Telegram sessions:

```python
pool = await MrktPool.from_sessions(
    ["account_1", "account_2"],
    workdir=".",
    concurrency=2,
)
```

## Configuration

`MrktClient` supports these main options:

- `token`: an existing TGMRKT access token
- `session`: a Telegram session name
- `workdir`: directory containing session files
- `proxy`: optional HTTP or SOCKS proxy
- `headers`: additional HTTP headers
- `packed`: attach gifts, orders, and offers API objects

## Development

Install the development dependencies and run the tests/build checks:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m build
python -m twine check dist/*
```

GitHub Actions runs these checks for pushes and pull requests. Before the first
release, configure a Trusted Publisher on both PyPI and TestPyPI with owner
`aiofake`, repository `tgmrkt`, workflow
`.github/workflows/pypi-publish.yml`, and environments `pypi` and `testpypi`
respectively. Run the publish workflow manually to publish to TestPyPI; publish
a GitHub Release to publish to PyPI. Increment the version in `pyproject.toml`
for every release.

## License

Released under the MIT License. See [LICENSE](LICENSE).

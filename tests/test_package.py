from tgmrkts import MrktClient, MrktPool


def test_public_package_imports():
    assert MrktClient.__name__ == "MrktClient"
    assert MrktPool.__name__ == "MrktPool"


def test_client_can_be_created_without_network_access():
    client = MrktClient(token="test-token")

    assert client.token == "test-token"
    assert client.http is None
    assert client.gifts is not None
    assert client.orders is not None
    assert client.offers is not None

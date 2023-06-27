from starlette import status
from httpx import AsyncClient

test_data = {
    "username": "test",
    "email": "test@gmail.com",
    "password": "string"
}

wallet_address = "0xbd103d3f4f345cae4ab7f6df1ece2ee3a3e62f46"

response_text = '{"ok":true,"result":{"addresses":[{"id":1,"address":"0xbd103d3f4f345cae4ab7f6df1ece2ee3a3e62f46"}]}}'


async def test_wallet_routs(ac: AsyncClient):

    await ac.post("/register/", json=test_data)
    response = await ac.post("/login/", json=test_data)

    cookie = response.headers["set-cookie"]

    response = await ac.post(
        "/wallet/addWallet",
        json={"address": wallet_address},
        headers={"Cookie": cookie})

    assert response.status_code == status.HTTP_200_OK

    response = await ac.get(
        "/wallet/getWallets",
        headers={"Cookie": cookie}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.text == response_text

    response = await ac.get(
        f"/wallet/{wallet_address}/getTransactions/",
        params={
            "token_amount": 10,
            "limit": 10
        },
        headers={"Cookie": cookie},
    )
    assert response.status_code != 404

    response = await ac.get(
        f"/wallet/{wallet_address}/getBalance/",
        headers={"Cookie": cookie},
    )
    assert response.status_code != 404

    

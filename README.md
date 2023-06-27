Wallet Check API is a API designed to assist users in managing and monitoring Ethereum wallets.

### Features

Add and manage multiple Ethereum wallets  
Track wallet transactions  
Display token balances  
Get a list of wallets associated with a user  
Delete a wallet from the user's list  


### How it Works

The API might interact with users via the frontend interface and store user data, including wallet addresses, in a database. Each user can add multiple wallet addresses associated with their account, and each address can have multiple users.

User can require transactions and token balances of any wallet

### How to run?
add .env file

```
DATABASE_DRIVER=postgresql+asyncpg
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_HOSTNAME==
DATABASE_PORT=
DATABASE_NAME=

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRATION_TIME=
REFRESH_TOKEN_EXPIRATION_TIME=
COOKIE_SECURE=
COOKIE_CSRF=
COOKIE_SAMESITE=
COOKIE_DOMAIN=
JWT_SECRET_KEY=

ETHERSCAN_API_KEY=

```
```
git clone https://github.com/Kem0111/Wallet_Check_API.git
```

```
docker-compose up -d
```

Go to the localhost:8000/docs and try it
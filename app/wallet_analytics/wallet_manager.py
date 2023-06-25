from .wallet_balance import WalletTokens
from .wallet_transactions import TokenTransactions


class WalletManager:

    async def get_transactions(self, address, limit, token_amount):

        transactions = TokenTransactions(address, limit=limit,
                                         min_token_amount=token_amount)

        result = {"transactions": []}

        async for tx in transactions.get_result():
            result["transactions"].append(
                {
                    'date': tx['datetime_obj'],
                    'transaction': tx['tx_hash'],
                    'sendler': tx['from_address'],
                    'receiver': tx['to_address'],
                    'sum': tx['value']
                }
            )
        return result

    async def get_balance(self, address):
        wallet_tokens = WalletTokens(address)

        result = {"balance": []}

        async for token_result in wallet_tokens.get_result():
            result["balance"].append(token_result)

        return result


wallet_manager = WalletManager()

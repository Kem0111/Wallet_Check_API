

from .wallet_transactions import TokenTransactions


class WalletManager:

    async def get_transactions(self, address, limit, token_amount):
        transactions = TokenTransactions(address, count=limit,
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


wallet_manager = WalletManager()

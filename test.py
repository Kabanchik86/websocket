from okx.Trade import TradeAPI
import okx.PublicData as PublicData

flag = "0"  # Production trading: 0, Demo trading: 1

#accountDataAPI = AccountAPI(api_key=apiKey, api_secret_key=secretKey, passphrase=passfrase, flag='0', domain = 'https://www.okx.com')
tradeAPI = TradeAPI(api_key=apiKey, api_secret_key=secretKey, passphrase=passfrase, flag='0', domain = 'https://www.okx.com')

#result = accountDataAPI.get_account_balance()
# order = tradeAPI.place_order(
#     instId="TON-USDT",
#     tdMode="cash",
#     side="buy",
#     ordType="market",
#     sz="0.1",
#     tgtCcy="base_ccy"
# )
# print(order)
# result = tradeAPI.get_fills()
# total_sz = 0.0
# for item in result['data']:
#     if item['ordId'] == '3296686009829335040':
#         total_sz += float(item['fillSz'])
#         print(item)
#         print(item['fillSz'])

# Retrieve funding rate history
publicDataAPI = PublicData.PublicAPI(flag=flag)
result = publicDataAPI.funding_rate_history(
    instId="APR-USDT-SWAP",
)
print(result)
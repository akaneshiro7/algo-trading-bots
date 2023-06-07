import keys, datetime, sys, config
from alpaca_trade_api.rest import REST

api = REST(key_id=keys.API_KEY, secret_key=keys.SECRET_KEY, base_url=config.BASE_URL)

if not api.get_clock().is_open:
    sys.exit("market is not open")

api.cancel_all_orders()
api.close_all_positions()

print("{} liquidated positions".format(datetime.datetime.now().isoformat()))
import config
import alpaca_trade_api as tradeapi
import psycopg2 
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
# cursor = connection.cursor()

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# # test query
# cursor.execute("SELECT * FROM stock")
# stocks = cursor.fetchall()
# for stock in stocks:
#     print(stock["symbol"])

api = tradeapi.REST(config.API_KEY, config.API_SECRET, api_version='v2', base_url=config.API_URL)
assets = api.list_assets()
# print(type(assets), type(assets[0]), assets[0], getattr(assets[0], 'class'))
for asset in assets:
    print(asset.symbol, asset.name, asset.exchange)
    cursor.execute("""
        INSERT INTO stock (symbol, name, exchange, is_etf)
        VALUES (%s, %s, %s, False)
    """, (asset.symbol, asset.name, asset.exchange)
    )

# save to postgres
connection.commit()

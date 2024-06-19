import config
import csv
import os
import psycopg2 
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("SELECT * FROM stock WHERE is_etf = TRUE")

rows = cursor.fetchall()
# row is an ETF
for row in rows: 
    if row["symbol"] in os.listdir("data"):
        # data dir contains {etf_name}/{date}.csv files
        rel_path = f"data/{row['symbol']}/"
        date_files = os.listdir(f"data/{row['symbol']}")
        dates = [f[:-4] for f in date_files]
        for file, date in zip(date_files, dates):
            print(file, rel_path + file, date)
            # read CSV
            with open(rel_path + file, 'r') as f:
                reader = csv.reader(f)
                # skip 1st line
                next(reader)
                for line in reader:
                    # stock symbol is 4th col
                    if len(line) > 1 and line[3].isupper(): # if ticker exists
                        ticker = line[3]
                        print(ticker)
                        shares = line[5].replace(',', '') # remove comma
                        weight = line[7][:-1] # remove % sign

                        # insert into SQL database
                        cursor.execute("""
                            SELECT * FROM stock
                            WHERE symbol = %s          
                        """, (ticker,)
                        )
                        stock = cursor.fetchone()
                        if stock:
                            cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (row['id'], stock['id'], date, shares, weight)
                        )
connection.commit()
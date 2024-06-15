
-- base table
CREATE TABLE stock (
    id SERIAL PRIMARY KEY, -- auto-incrementing integer
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);

-- compound id
-- e.g. (1,3) for ARKG, CRSP; (1,4) ARKG, EDIT; 
CREATE TABLE etf_holding (
    etf_id INTEGER NOT NULL,
    holding_id INTEGER NOT NULL,
    dt DATE NOT NULL,
    shares NUMERIC,
    weight NUMERIC,
    PRIMARY KEY (etf_id, holding_id, dt),
    -- foreign key constraint
    CONSTRAINT fk_etf FOREIGN KEY (etf_id) REFERENCES stock(id),
    CONSTRAINT fk_holding FOREIGN KEY (holding_id) REFERENCES stock(id)
);

CREATE TABLE stock_price (
    stock_id INTEGER NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL, -- date and time
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, dt),
    -- foreign key constraint
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock(id)
);

-- index
CREATE INDEX ON stock_price (stock_id, dt DESC);

-- from timescaledb
SELECT create_hypertable('stock_price', 'dt');
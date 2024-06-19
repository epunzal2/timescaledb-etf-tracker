
-- manually set ARK etfs
UPDATE
	stock
SET
	is_etf = TRUE
WHERE
	stock.symbol IN('ARKK', 'ARKQ', 'PRNT', 'IZRL', 'ARKG', 'ARKF', 'ARKW');

UPDATE
    stock
SET
    is_etf = TRUE
WHERE 
    stock.symbol IN ('PINK');
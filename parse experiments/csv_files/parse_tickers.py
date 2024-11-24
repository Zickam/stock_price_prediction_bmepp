tickers = {}
with open("tickers.csv") as file:
    for line in file.readlines()[1:]:
        line = line.strip()
        ticker, company_description = line.split(",", 1)
        tickers[ticker] = company_description
print(tickers)
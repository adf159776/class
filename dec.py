import requests
from datetime import datetime
def log2(func):
    def wrap(*args,**kwargs):
        print(f"{func.__name__}")
        return func(*args,**kwargs)
    return wrap


@log2
def get_symbols_info(ticker, comparisons):
    result = {}
    headers = {
        'x-api-key': "7P4Qtfr5yX2UrRtwaOlYIaHzZQJuiYry5ENaIgbn"
    }
    url = f"https://yfapi.net/v8/finance/chart/{ticker}"
    querystring = {"comparisons": comparisons, "range": "5d", "interval": "1d"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()["chart"]["result"][0]
    for index in range(len(data["timestamp"])):
        timestamp = datetime.fromtimestamp(data["timestamp"][index]).strftime('%Y-%m-%d')
        stock_info_mapping = {}

        for k in ["high", "low", "open", "close"]:
            temp_dict = {}
            temp_dict[k] = round(data["indicators"]["quote"][0][k][index], 2)
            stock_info_mapping[ticker] = temp_dict
        for comparison in data["comparisons"]:
            temp = {}
            for k in ["high", "low", "open", "close"]:
                temp[k] = comparison[k][index]
                stock_info_mapping[comparison["symbol"]] = temp
        result[timestamp] = stock_info_mapping

    return result

if __name__ == '__main__':
    print(get_symbols_info("AAPL", "TSLA"))

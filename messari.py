import requests

class MessariData:
    def __init__(self, asset, metric, year) -> None:
        self.asset = asset
        self.metric = metric
        self.url = f"https://data.messari.io/api/v1/assets/{self.asset}/metrics/{self.metric}/time-series"
        self.params = {"start":f"{year}-01-01T01:00:00.000Z",
                    "end":f"{year}-12-31T01:00:00.000Z",
                    "interval":"1d",
                    "columns":"close",
                    "timestamp-format":"rfc3339"}

    def get_asset_timeseries(self, params={}):
        if params is not None:
            self.params.update(params)
        try:
            response = requests.request("GET", self.url, params=self.params)
        except Exception as e:
            raise e
        return response.json()


if __name__ == "__main__":
    test_md = MessariData('bitcoin', 'price', 2021)
    response = test_md.get_asset_timeseries({"start":"2021-01-01T01:00:00.000Z",
                    "end":f"2021-01-02T01:00:00.000Z",
                    "interval":"1d",
                    "columns":"close",
                    "timestamp-format":"rfc3339"})

    # asserting data in response keys
    assert "data" in response.keys()

    # checking token symbol
    assert response["data"]["symbol"] == "BTC"

    # check value
    assert response["data"]["values"][0][1] == 32200.200908880128
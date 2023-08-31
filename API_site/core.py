from API_site.util.Useful_funcs import Utils
from API_site.util.site_api_handler import SiteApiInterface
from config_data.config import SiteSettings

site = SiteSettings()
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": site.RAPID_API_KEY.get_secret_value(),
    "X-RapidAPI-Host": site.HOST_API
}

url = "https://{api}".format(api=site.HOST_API)

querystring = {"q": "new york", "locale": "ru_RU",
               "langid": "1033", "siteid": "300000001"}
payload_list = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "destination": {"regionId": "3000"},
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2023
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2023
    },
    "rooms": [
        {
            "adults": 2,
            "children": []
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
        "max": 10000,
        "min": 50
    }}
}
payload_detail = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "propertyId": "3075306"
}

site_api = SiteApiInterface()
utils_func = Utils()


if __name__ == "__main__":
    site_api()
    utils_func()

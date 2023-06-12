import requests

def get_address_from_coords(lon, lat):
    PARAMS = {
        "apikey":"555bc789-2362-40fb-bfbf-c7c01038f989",
        "format":"json",
        "lang":"ru_RU",
        "kind":"house",
        "geocode": f"{lon},{lat}"
    }

    #отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str
    except Exception as e:
        return "error"

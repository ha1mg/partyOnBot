import requests


from config import APIKEY
def get_coords_from_address(address):
    try:
        PARAMS = {
            "apikey":APIKEY,
            "format":"json",
            "lang":"ru_RU",
            "kind":"house",
            "geocode": f"{address}"
        }

        #отправляем запрос по адресу геокодера.
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        location = json_data['response']['GeoObjectCollection']["featureMember"][0]['GeoObject']['Point']['pos']
        return location
    except Exception as e:
        return f"Error occurred: {e}"

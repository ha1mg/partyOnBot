import requests

#создаем функцию get_address_from_coords с параметром coords, куда мы будем посылать координаты и получать готовый адрес.
def get_address_from_coords(coords):
    #заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
    PARAMS = {
        "apikey":"555bc789-2362-40fb-bfbf-c7c01038f989",
        "format":"json",
        "lang":"ru_RU",
        "kind":"house",
        "geocode": coords
    }

    #отправляем запрос по адресу геокодера.
    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        #получаем данные
        json_data = r.json()
        #вытаскиваем из всего пришедшего json именно строку с полным адресом.
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        #возвращаем полученный адрес
        return address_str
    except Exception as e:
        #если не смогли, то возвращаем ошибку
        return "error"

# if __name__ == '__main__':
#     #даем запрос на получение адреса с координатами 37.617585, 55.751903
#     address_str = get_address_from_coords("37.617585,55.751903")
#     #распечатываем адрес
#     print(address_str)
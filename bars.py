import json
import math


def load_data(filepath):
    try:
        with open(filepath, encoding='utf-8') as file:
            file_data = file.read()
        return json.loads(file_data)
    except FileNotFoundError:
        print('Файл не найден')


def get_biggest_bar(bars):
    return max(bars, key=lambda n: n['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars, key=lambda n: n['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda bar_properties: get_distance(
        longitude,
        latitude,
        bar_properties['geometry']['coordinates'][0],
        bar_properties['geometry']['coordinates'][1])
               )


def get_distance(cur_longitude, cur_latitude, place_longitude, place_latitude):
    # радиус сферы (Земли)
    rad = 6372795
    # в радианах
    lat1 = float(cur_latitude) * math.pi / 180
    lat2 = place_latitude * math.pi / 180
    long1 = float(cur_longitude) * math.pi / 180
    long2 = place_longitude * math.pi / 180

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    distance = ad * rad
    return distance

if __name__ == '__main__':
    json_obj = load_data('bars.json')
    all_bars = json_obj['features']
    biggest_bar = get_biggest_bar(all_bars)
    smallest_bar = get_smallest_bar(all_bars)
    print('{} : количество посадочных мест {}'.format(
        biggest_bar['properties']['Attributes']['Name'],
        biggest_bar['properties']['Attributes']['SeatsCount'])
    )
    print('{} : количество посадочных мест {}'.format(
        smallest_bar['properties']['Attributes']['Name'],
        smallest_bar['properties']['Attributes']['SeatsCount'])
    )
    print('Поиск ближайшего бара по координатам')
    place_lat, place_long = input('Введите коодинаты через пробел: ').split()
    closest_bar = get_closest_bar(all_bars, place_lat, place_long)
    print('Ближайший бар: {}, находится по адресу: {}'.format(
        closest_bar['properties']['Attributes']['Name'],
        closest_bar['properties']['Attributes']['Address']
    ))

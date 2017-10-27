import json
import math
import sys


def load_data(filepath):
    try:
        with open(filepath, encoding='utf-8') as file:
            file_data = file.read()
        return json.loads(file_data)
    except FileNotFoundError:
        return None


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
    # All calculations are taken from here: http://gis-lab.info/qa/great-circles.html
    earth_sphere_radius = 6372795
    lat1, lat2, long1, long2 = map(math.radians,
                                   [
                                       float(cur_latitude),
                                       place_latitude,
                                       float(cur_longitude),
                                       place_longitude
                                   ])
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    distance = ad * earth_sphere_radius
    return distance


def print_bar_info(bar):
    print('{} находится по аресу - {} : количество посадочных мест {}'.format(
        bar['properties']['Attributes']['Name'],
        bar['properties']['Attributes']['Address'],
        bar['properties']['Attributes']['SeatsCount'])
    )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_obj = load_data(sys.argv[1])
        all_bars = data_obj['features']
        biggest_bar = get_biggest_bar(all_bars)
        smallest_bar = get_smallest_bar(all_bars)
        print_bar_info(biggest_bar)
        print_bar_info(smallest_bar)
        print('Поиск ближайшего бара по координатам')
        try:
            place_lat, place_long = input('Введите коодинаты через пробел: ').split()
            closest_bar = get_closest_bar(all_bars, place_lat, place_long)
            print_bar_info(closest_bar)
        except ValueError:
            print('Неверные координаты')
    else:
        print('Укажите имя файла: python bars.py <filename>')

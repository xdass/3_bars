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
    radius = 6372795 # Earth sphere radius in meters
    lat1, lat2, long1, long2 = map(math.radians, # Convert coords to radians
                                   [
                                       float(cur_latitude),
                                       place_latitude,
                                       float(cur_longitude),
                                       place_longitude
                                   ])
    # cos and sin of latitude
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    # longitude difference
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    
    # calculating the length of a large circle
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    distance = ad * radius
    return distance


if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_obj = load_data(sys.argv[1])
        all_bars = data_obj['features']
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
        try:
            place_lat, place_long = input('Введите коодинаты через пробел: ').split()
            closest_bar = get_closest_bar(all_bars, place_lat, place_long)
            print('Ближайший бар: {}, находится по адресу: {}'.format(
                closest_bar['properties']['Attributes']['Name'],
                closest_bar['properties']['Attributes']['Address']
            ))
        except ValueError:
            print('Неверные координаты')
    else:
        print('Укажите имя файла: python bars.py <filename>')

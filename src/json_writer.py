import json


def writeJSONtoFile(fileName, object):
    with open(fileName, mode='a', encoding='utf-8') as write_file:
        # экономия памяти на пробелах:
        json.dump(object, write_file, ensure_ascii=False, separators=(',', ':'))
        # или более удобный для человека вид:
        # json.dump(object, write_file, indent=4, ensure_ascii=False, separators=(',', ':'))
        write_file.write(',')

# -*- coding: utf-8 -*-
import sqlite3


def return_charm_values(num, c, read_translation_data):
    line = c[num + 1]
    line = line.split(',')
    slots, skill1, points1, skill2, points2, = line
    if not points2:
        points2 = 0
    skill1 = translate_skill(skill1, read_translation_data)
    skill2 = translate_skill(skill2, read_translation_data)
    line = [num + 1, skill1, skill2, points1, points2, slots]
    return line


def return_relic_values(num, r, read_translation_data):
    # Format: itemType,  Blademaster/Gunner, Points, Skill, Defense, Fire Res, Water res, Ice Res, Thndr Res, Drgn Res
    line = r[num]
    line = line.split(',')
    if len(line) == 5:
        item_type, hunter_type, points, skill, defence = line
        item_type = convert_item_type(item_type)
        hunter_type = convert_hunter_type(hunter_type)
        skill = translate_skill(skill, read_translation_data)
        line = [num + 1, item_type, hunter_type, skill, points, defence, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL']
    else:
        del line[-1]
        item_type, hunter_type, points, skill, defence, fire, water, ice, thunder, dragon = line
        item_type = convert_item_type(item_type)
        hunter_type = convert_hunter_type(hunter_type)
        skill = translate_skill(skill, read_translation_data)
        line = [num + 1, item_type, hunter_type, skill, points, defence, fire, water, thunder, ice, dragon]
    return line


def translate_skill(skill, read_translation_data):
    if skill:
        for i in read_translation_data:
            if skill in i:
                i = i.split(';')
                if i[0] == skill:
                    return i[1]
                elif i[1] == skill:
                    return i[0]
                else:
                    pass
    else:
        return ''


def convert_hunter_type(num):
    numbers = {'1': 0, '2': 1, '3': 1}
    return numbers[num]


def convert_item_type(num):
    slot_numbers = {'0': 0, '1': 3, '2': 2, '3': 1, '4': 4, '5': 6}
    return slot_numbers[num]


def charms_convert():
    conn = sqlite3.connect('charms.db')
    db = conn.cursor()
    db.execute('DELETE FROM charms;')
    charms = open("mycharms.txt", 'r', encoding='UTF-8', newline=None)
    c = charms.read().splitlines()
    translate = open('Skilllist Eng-JP.csv', 'r', encoding='UTF-8')
    read_translation_data = translate.read().splitlines()
    read_translation_data[0] = 'Amplify;増幅'
    for i in range(len(c) - 1):
        values = return_charm_values(i, c, read_translation_data)
        line = 'INSERT INTO charms VALUES (' \
               + str(values[0]) \
               + ',\"' \
               + values[1] \
               + '\",\"' \
               + values[2] \
               + '\",' \
               + str(values[3]) \
               + ',' \
               + str(values[4]) \
               + ',' \
               + str(values[5]) \
               + ');'
        db.execute(line)
    db.execute('DELETE FROM sqlite_sequence;')
    db.execute('INSERT INTO sqlite_sequence VALUES (\"charms\",\"' + str(len(c)) + '\");')
    conn.commit()
    conn.close()
    charms.close()
    return None


def relics_convert():
    conn = sqlite3.connect('relics.db')
    db = conn.cursor()
    db.execute('DELETE FROM relics;')
    relics = open('mygear.txt', 'r', encoding='UTF-8', newline=None)
    r = relics.read().splitlines()
    translate = open('Skilllist Eng-JP.csv', 'r', encoding='UTF-8')
    read_translation_data = translate.read().splitlines()
    read_translation_data[0] = 'Amplify;増幅'
    for i in range(len(r) - 1):
        values = return_relic_values(i, r, read_translation_data)
        line = 'INSERT INTO relics VALUES (' \
               + str(values[0]) \
               + ',' \
               + str(values[1]) \
               + ',' \
               + str(values[2]) \
               + ',\"' \
               + values[3] \
               + '\",' \
               + values[4] \
               + ',' \
               + values[5] \
               + ',' \
               + values[6] \
               + ',' \
               + values[7] \
               + ',' \
               + values[8] \
               + ',' \
               + values[9] \
               + ',' \
               + values[10] \
               + ');'
        db.execute(line)
    db.execute('INSERT INTO sqlite_sequence VALUES (\"relics\",\"' + str(len(r)) + '\");')
    conn.commit()
    conn.close()
    relics.close()
    return None


charms_convert()
relics_convert()

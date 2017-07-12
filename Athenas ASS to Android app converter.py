# -*- coding: utf-8 -*-
import sqlite3
charms = open("mycharms.txt", 'r', encoding='UTF-8', newline=None)
c = charms.read()
c = c.splitlines()
translate = open('Skilllist Eng-JP.csv', 'r', encoding='UTF-8')
read_data = translate.read()
read_data = read_data.splitlines()
read_data[0] = 'Amplify;増幅'


def return_charm_values(num):
    line = c[num+1]
    line = line.split(',')
    slots = line[0]
    skill1 = line[1]
    points1 = line[2]
    skill2 = line[3]
    points2 = line[4]
    if not points2:
        points2 = 0
    for i in read_data:
        if i.split(';')[0] == skill1:
            skill1 = i.split(';')[1]
        elif i.split(';')[0] == skill2:
            skill2 = i.split(';')[1]
    line = [num+1, skill1, skill2, points1, points2, slots]
    return line


def magic():
    conn = sqlite3.connect('charms.db')
    db = conn.cursor()
    db.execute('DELETE FROM charms;')
    for i in range(len(c)-1):
        athenas_values = return_charm_values(i)
        line = 'INSERT INTO charms VALUES ('\
               + str(athenas_values[0])\
               + ',\"'\
               + athenas_values[1]\
               + '\",\"'\
               + athenas_values[2]\
               + '\",'\
               + str(athenas_values[3])\
               + ','\
               + str(athenas_values[4])\
               + ','\
               + str(athenas_values[5])\
               + ');'
        print(line)
        db.execute(line)
    conn.commit()
    conn.close()
    charms.close()
    return None
magic()

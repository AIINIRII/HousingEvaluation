import pymysql

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


def ratio_transform(ratioStr: str):
    el_num_str = ratioStr.split("梯")[0]
    pe_num_str = ratioStr.split("梯")[1].split("户")[0]
    el_num = float(chinese2digits(el_num_str))
    pe_num = float(chinese2digits(pe_num_str))
    ratio = pe_num / el_num
    print(f"{ratioStr} with ratio {ratio}")
    return ratio


def ratio_modify():
    sqlR = "SELECT house_id, elevator_ratio FROM house_info;"
    sqlW = "UPDATE house_info SET elevator_ratio_value=%s WHERE house_id=%s;"
    SQL_USERNAME = "root"
    SQL_PWD = "632632"
    HOST = "localhost"
    DATABASE = "housing_evaluation"
    db = pymysql.connect(host=HOST, user=SQL_USERNAME, password=SQL_PWD, database=DATABASE)
    curR = db.cursor()
    curW = db.cursor()
    curR.execute(sqlR)
    for row in curR.fetchall():
        if row[1] is not None:
            curW.execute(sqlW, (ratio_transform(row[1]), row[0]))
    db.commit()


def insert_floor():
    sql = "INSERT INTO floor_type(type_id, type_name) values(%s, %s);"
    SQL_USERNAME = "root"
    SQL_PWD = "632632"
    HOST = "localhost"
    DATABASE = "housing_evaluation"
    db = pymysql.connect(host=HOST, user=SQL_USERNAME, password=SQL_PWD, database=DATABASE)
    cur = db.cursor()
    floor_type = ['未知', '地下室', '底层', '低楼层', '中楼层', '高楼层', '顶层']
    i = 0
    for n in floor_type:
        cur.execute(sql, (str(i), str(n)))
        i += 1
    db.commit()


def insert_room():
    sql = """SELECT DISTINCT q.rooms_type
           FROM (SELECT *
           FROM house_info
           WHERE house_title is not NULL
           AND house_price is not NULL
           AND house_type is not NULL
           AND house_finish is not NULL
           AND house_area is not NULL
           AND house_towards is not NULL
           AND have_elevator is not NULL
           AND completion_time is not NULL
           AND trading_date is not NULL
           AND elevator_ratio is not NULL
           AND rooms_type is not NULL
           AND place_name is not NULL) AS q"""
    SQL_USERNAME = "root"
    SQL_PWD = "632632"
    HOST = "localhost"
    DATABASE = "housing_evaluation"
    db = pymysql.connect(host=HOST, user=SQL_USERNAME, password=SQL_PWD, database=DATABASE)
    cur = db.cursor()
    cur2 = db.cursor()
    cur.execute(sql)
    sqlW = "INSERT INTO rooms_type(type_name) VALUES (%s);"
    for row in cur.fetchall():
        cur2.execute(sqlW, row[0])
    db.commit()


def modify_floor():
    SQL_USERNAME = "root"
    SQL_PWD = "632632"
    HOST = "localhost"
    DATABASE = "housing_evaluation"
    sqlR = "SELECT house_id, house_floor FROM house_info;"
    sqlW = "UPDATE house_info SET total_floor=%s, floor_type=%s WHERE house_id=%s;"
    db = pymysql.connect(host=HOST, user=SQL_USERNAME, password=SQL_PWD, database=DATABASE)
    cur = db.cursor()
    cur.execute(sqlR)
    cur2 = db.cursor()
    all_type = set()
    floor_type_dic = dict.fromkeys(['未知', '地下室', '底层', '低楼层', '中楼层', '高楼层', '顶层'])
    i = 0
    for key in floor_type_dic.keys():
        floor_type_dic[key] = i
        i += 1

    for row in cur.fetchall():
        id = row[0]
        floor = str(row[1])  # 顶层(共6层)
        if floor.find("(") != -1:
            total_floor = int(floor.split("(共")[1].split("层)")[0])
        else:
            print(f"the id: {id}, floor: {floor} can not be executed.")
            total_floor = 0
        if floor.find("(") != -1:
            floor_type = floor.split("(")[0]
        else:
            print(floor)
            floor_type = floor
        floor_type = floor_type_dic[floor_type]
        cur2.execute(sqlW, (total_floor, floor_type, id))
    db.commit()


if __name__ == '__main__':
    ratio_modify()

import datetime
import random
from typing import List

import numpy as np
import pymysql

# [-0.10850329  0.90898802 -0.10850329 -0.10850329  0.06291047 -0.61744586]
# [ 0.78383962  0.1752551   0.78383962  0.78383962 -0.95955633 -0.35217959]

total_len = 362
form_len = 355
def dataRandomSlice(queryList: List, seed):
    id = [i for i in range(0, len(queryList))]
    random.seed(seed)
    random.shuffle(id)
    train_dev_len = int(len(queryList) * 0.8)
    print(f"We have {train_dev_len} train data, {len(queryList) - train_dev_len} test data.")
    train_index = id[:train_dev_len]
    test_index = id[train_dev_len:]
    assert len(test_index) + len(train_index) == len(id)
    train_data = [queryList[i] for i in train_index]
    test_data = [queryList[i] for i in test_index]
    return train_data, test_data


def saveData(train_data, test_data, dataFolder):
    np.save(f"{dataFolder}/train_data", train_data)
    np.save(f"{dataFolder}/test_data", test_data)


def generateDataSlice(seed=2020, dataFolder="../data/"):
    queryList = dataQuery()
    train_data, test_data = dataRandomSlice(queryList, seed)
    saveData(train_data, test_data, dataFolder)


def loadData(dataFolder):
    train_data = np.load(f"{dataFolder}/train_data.npy")
    test_data = np.load(f"{dataFolder}/test_data.npy")
    return train_data, test_data


def list2dic(dataSet):
    dataDicesSet = []
    for data in dataSet:
        dataDices = []
        for row in range(len(data)):
            dataDic = dict.fromkeys(['id', 'title', 'floor', 'price', 'type', 'finish',
                                     'area', 'towards', 'elevator', 'completion_time', 'trading_date',
                                     'elevator_ratio', 'rooms_type', 'place_name', 'place_id', 'total_floor',
                                     'floor_type', 'elevator_ratio_value'])
            i = 0
            for key in dataDic.keys():
                dataDic[key] = data[row][i]
                i += 1
            dataDices.append(dataDic)
            # print(f"row: {row}")
            # for key, value in dataDic.items():
            #     print(f"key: {key}, value: {value}")
        dataDicesSet.append(dataDices)
    return dataDicesSet


def one_hot(i: str, max: int):
    nums = i.split(" ")
    for num in nums:
        num = num.strip()
        i = int(num)
    result = np.zeros((max, 1), dtype=float)
    result[i, 0] = 1.0
    return result


def data2time(data: str):
    # 2010.01.02
    num = data.split('.')
    # print(num)
    if len(num) == 3:
        date = datetime.date(int(num[0]), int(num[1]), int(num[2]))
    else:
        date = datetime.date(int(num[0]), int(num[1]), 1)
    return date.toordinal()


def packData(dataDicesSet):
    resultSet = []
    # used_key = ['id', 'title', 'floor', 'price', 'type', 'finish','area', 'towards', 'elevator', 'completion_time',
    #             'trading_date','elevator_ratio', 'room_type', 'place_name', 'place_id', 'total_floor', 'floor_type']
    X_used_key = ['type', 'finish', 'area', 'towards', 'elevator', 'rooms_type', 'completion_time', 'trading_date',
                  'place_id', 'total_floor', 'floor_type', 'elevator_ratio_value']
    Xs = []
    Ys = []
    for dataDices in dataDicesSet:
        X = np.zeros((len(dataDices), total_len))  # 355 + 7
        Y = np.zeros((len(dataDices), 1))
        i = 0
        for row in dataDices:
            resultList = np.zeros((0, 1))
            nkey = 'type'
            if nkey in X_used_key:
                narr = one_hot(row[nkey], 4)
                # print(resultList.shape, narr.shape)
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'towards'
            if nkey in X_used_key:
                narr = one_hot(row[nkey], 8)
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'place_id'
            if nkey in X_used_key:
                narr = one_hot(row[nkey], 297)
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'floor_type'
            if nkey in X_used_key:
                narr = one_hot(row[nkey], 7)
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'rooms_type'
            if nkey in X_used_key:
                narr = one_hot(row[nkey], 38)
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'elevator'
            if nkey in X_used_key:
                narr = np.array([[int(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            # print(resultList.shape)
            nkey = 'finish'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'area'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'finish'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'completion_time'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'total_floor'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'elevator_ratio_value'
            if nkey in X_used_key:
                narr = np.array([[float(row[nkey])]])
                resultList = np.concatenate([resultList, narr], axis=0)
            nkey = 'trading_date'
            if nkey in X_used_key:
                narr = np.array([[float(data2time(row[nkey]))]])
                resultList = np.concatenate([resultList, narr], axis=0)
            Y[i, 0] = float(row['price'])
            # print(resultList.shape)
            X[i, :] = np.squeeze(resultList)
            i += 1
        X_nof = X[:, :form_len]
        X_f = X[:, form_len:]
        X_f_std = X_f.std(axis=0)
        X_f_mean = X_f.mean(axis=0)
        X_f = (X_f - X_f_mean) / X_f_std
        X = np.concatenate((X_nof, X_f), axis=1)
        # print(X[0, form_len:])
        Xs.append(X)
        Ys.append(Y)

    return (Xs[0], Ys[0]), (Xs[1], Ys[1])


def dealData(dataFolder="../data/"):
    train_data, test_data = loadData(dataFolder)
    dataSet = [train_data, test_data]
    dataDicesSet = list2dic(dataSet)
    (X_train, Y_train), (X_test, Y_test) = packData(dataDicesSet)
    np.save(f"../data/X_train_{total_len}", X_train)
    np.save(f"../data/Y_train_{total_len}", Y_train)
    np.save(f"../data/X_test_{total_len}", X_test)
    np.save(f"../data/Y_test_{total_len}", Y_test)


def dataQuery():
    SQL_USERNAME = "root"
    SQL_PWD = "632632"
    HOST = "localhost"
    DATABASE = "housing_evaluation"
    sql = ("\n"
           "            SELECT *\n"
           "            FROM house_info\n"
           "            WHERE house_title is not NULL\n"
           "              AND house_price is not NULL\n"
           "              AND house_type is not NULL\n"
           "              AND house_finish is not NULL\n"
           "              AND house_area is not NULL\n"
           "              AND house_towards is not NULL\n"
           "              AND have_elevator is not NULL\n"
           "              AND completion_time is not NULL\n"
           "              AND trading_date is not NULL\n"
           "              AND elevator_ratio is not NULL\n"
           "              AND rooms_type is not NULL\n"
           "              AND place_name is not NULL\n"
           "            ;\n"
           "            ")
    db = pymysql.connect(host=HOST, user=SQL_USERNAME, password=SQL_PWD, database=DATABASE)
    cur = db.cursor()
    cur.execute(sql)
    queryList = []
    for row in cur.fetchall():
        queryList.append(row)
    return queryList


if __name__ == '__main__':
    generateDataSlice(2020, "../data/")
    dealData()

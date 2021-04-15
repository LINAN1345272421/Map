import time
import traceback

import pymysql
import requests
from flask import json


def get_conn():
    """
    :return: 连接，游标192.168.1.102
    """
    # 创建连接
    conn = pymysql.connect(host="10.92.5.115",
                    user="root",
                    password="123456",
                    db="yiqing",
                    charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询结果以((),(),)形式
    """
    conn,cursor = get_conn();
    cursor.execute(sql)
    res=cursor.fetchall()
    close_conn(conn,cursor)
    return res

def update_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  #  0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)' #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  #  0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_history():
    """
        插入历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])

        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_world():
    """
    更新 world 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[2]  #  0 是历史数据字典,1 最新详细数据列表,2世界数据
        conn, cursor = get_conn()
        sql = "insert into world(update_time,country,continent,confirmAdd,confirm,suspect,dead,heal,nowConfirm) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from world order by id desc limit 1)' #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        print(li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据(world)")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕(world)")
        else:
            print(f"{time.asctime()}已是最新数据！(world)")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    url_his = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'  # 加上这个history大兄弟++++++++
    url_world ='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)  # json字符串转字典
    data_all = json.loads(res['data'])

    # 再加上history的配套东东++++++++
    r_his = requests.get(url_his, headers)
    res_his = json.loads(r_his.text)
    data_his = json.loads(res_his['data'])

    #world数据
    r_world = requests.get(url_world, headers)
    res_world = json.loads(r_world.text)
    data_world = res_world['data']

    history = {}  # 历史数据
    #     for i in data_all["chinaDayList"]:
    #         ds = "2020." + i["date"]
    #         tup = time.strptime(ds, "%Y.%m.%d")
    #         ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
    #         confirm = i["confirm"]
    #         suspect = i["suspect"]
    #         heal = i["heal"]
    #         dead = i["dead"]
    #         history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    #     for i in data_all["chinaDayAddList"]:
    #         ds = "2020." + i["date"]
    #         tup = time.strptime(ds, "%Y.%m.%d")
    #         ds = time.strftime("%Y-%m-%d", tup)
    #         confirm = i["confirm"]
    #         suspect = i["suspect"]
    #         heal = i["heal"]
    #         dead = i["dead"]
    #         history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    # 通过上面的代码肯定不行了，里面只有当日详细数据，修改也很简单，改一下循环遍历的数据源即可：++++
    for i in data_his["chinaDayList"]:
        ds = "2021." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_his["chinaDayAddList"]:
        ds = "2021." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    # 下面就不用动了
    details = []  # 当日详细数据
    update_time = data_all["lastUpdateTime"]
    data_country = data_all["areaTree"]  # list 25个国家
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    world=[]
    for i in data_world:
        ds = i['y']+"."+i['date']
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        world.append([ds,i['name'],i['continent'],i['confirmAdd'],i['confirm'],i['suspect'],i['dead'],i['heal'],i['nowConfirm']])

    return history, details,world

def get_c1_data():
    """

    :return: 大屏主数据
    """
    sql="select sum(confirm),"\
        "(select suspect from history order by ds desc limit 1),"\
        "sum(heal),"\
        "sum(dead) "\
        "from details "\
        "where update_time=(select update_time from details order by update_time desc limit 1)"
    res=query(sql)
    return res[0]

def get_world_c1_data():
    """

    :return: 大屏主数据
    """
    sql="select sum(confirm),"\
        "sum(heal), "\
        "sum(dead), "\
        "sum(nowConfirm) "\
        "from world "\
        "where update_time=(select update_time from world order by update_time desc limit 1)"
    res=query(sql)
    return res[0]

def get_c2_data():
    """
    :return:  返回各省数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm),sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_b1_data():
    """
    :return:  返回各省数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res

def get_query_data(year,month,day):
    Year=str(year)
    Month=str(month)
    Day=str(day)
    ds = Year+"." + Month+"."+Day
    print(ds)
    tup = time.strptime(ds, "%Y.%m.%d")
    print(tup)
    ds = time.strftime("%Y-%m-%d", tup)
    Year=str(year)
    Month=str(month)
    Day=str(int(day)+1)
    ds1 = Year+"." + Month+"."+Day
    print(ds1)
    tup1 = time.strptime(ds1, "%Y.%m.%d")
    print(tup1)
    ds1 = time.strftime("%Y-%m-%d", tup1)
    print(ds1)
    sql = 'select province,sum(confirm) from details '\
          'where update_time between '+"'"+ds+"'"+' and '+"'"+ds1+"'"+' group by province'
    res = query(sql)
    print(res)
    return res

def get_b2_data():
    """
    :return:  返回各省数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm),sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    print(res)
    return res

def get_l1_data():
    """
	:return:返回每天历史累计数据
    """
    sql = "select ds,confirm,dead from history"
    res = query(sql)
    print(res)
    return res

def get_l2_data():
    """
    :return:返回每天新增确诊和死亡数据
    """
    sql = "select ds,heal_add,dead_add from history"
    res = query(sql)
    print(res)
    return res

def get_r1_data():
    sql='select city,confirm from'\
        '(select city ,confirm from details '\
        'where update_time=(select update_time from details order by update_time desc limit 1) '\
        'and province not in ("湖北","北京","上海","天津","重庆") '\
        'union all '\
        'select province as city , sum(confirm) from details '\
        'where update_time=(select update_time from details order by update_time desc limit 1) '\
        'and province in ("北京","上海","天津","重庆") group by province) as a '\
        'order by confirm desc limit 5'
    res=query(sql)
    return res

def get_city_data(name):
    sql='select city ,confirm ,heal ,dead from details '\
        'where update_time=(select update_time from details order by update_time desc limit 1) '\
        'and province='+'"'+name+'"'+' and city not in ("境外输入","地区待确认") '
    res=query(sql)
    return res

def get_r2_data():
    sql='select province,confirm from details where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) and city="境外输入" order by confirm desc limit 5'
    res=query(sql)
    return res

def get_world_bar_data():
    sql='select country,confirm from world where update_time=(select update_time from world ' \
          'order by update_time desc limit 1) order by confirm desc limit 8'
    res=query(sql)
    return res

def get_all_world_data():
    sql='select country,confirm,heal,dead from world where update_time=(select update_time from world ' \
          'order by update_time desc limit 1) '
    res=query(sql)
    return res

def get_china_data():
    sql='select confirm,heal,dead from history where ds=(select update_time from world ' \
          'order by ds desc limit 1) limit 1'
    res=query(sql)
    Res=('中国',res[0][0],res[0][1],res[0][2])
    return Res

def get_query_like1(fromyear,frommonth,fromday,toyear,tomonth,today,
                    continent,country,province,city):
    Year=str(fromyear)
    Month=str(frommonth)
    Day=str(fromday)
    ds = Year+"." + Month+"."+Day
    print(ds)
    tup = time.strptime(ds, "%Y.%m.%d")
    print(tup)
    ds = time.strftime("%Y-%m-%d", tup)
    Year=str(toyear)
    Month=str(tomonth)
    Day=str(today)
    ds1 = Year+"." + Month+"."+Day
    print(ds1)
    tup1 = time.strptime(ds1, "%Y.%m.%d")
    print(tup1)
    ds1 = time.strftime("%Y-%m-%d", tup1)
    if(province!="" or city!="" or country=="中国"):
        sql = "select update_time,province,sum(confirm),sum(heal),sum(dead) from details " \
              "where (update_time between " + "'" + ds + "' and '" + ds1 + "'" + ") "
        if (province != "" and city ==""):
            sql="select update_time,province,city,confirm,heal,dead from details " \
              "where (update_time between " + "'" + ds + "' and '" + ds1 + "'" + ") "
            sql = sql + "and (province like " + '"%' + province + '%") '
        if (province!="" and city != ""):
            sql = "select update_time,province,city,confirm,heal,dead from details " \
                  "where (update_time between " + "'" + ds + "' and '" + ds1 + "'" + ") "
            sql = sql + "and (city like " + '"%' + city + '%") '
            sql = sql + "and (province like " + '"%' + province + '%") '
        if(country=="中国" and province=="" and city==""):
            sql=sql+"group by  province , update_time"
    if(province=="" and city=="" and country!="中国"):
        sql = "select update_time,country,confirm,heal,dead,nowconfirm from world " \
              "where (update_time between " + "'" + ds + "' and '" + ds1 + "'" + ") "
        if (continent != ""):
            sql = sql + "and (continent like " + '"%' + continent + '%") '
        if (country != ""):
            sql = sql + "and (country like " + '"%' + country + '%") '
    print("查询（带日期）")
    print(sql)
    res = query(sql)
    print(res)
    return res

def get_query_like2(continent,country,province,city):
    if(province!="" or city!="" or country=="中国"):
        sql = "select update_time,province,sum(confirm),sum(heal),sum(dead) from details where 1=1 "
        if (province != "" and city==""):
            sql="select update_time,province,city,confirm,heal,dead from details where 1=1 "
            sql = sql + "and (province like " + '"%' + province + '%") '
        if (city != "" and province !=""):
            sql = "select update_time,province,city,confirm,heal,dead from details where 1=1 "
            sql = sql + "and (city like " + '"%' + city + '%") '
            sql=sql+"and (province like " + '"%' + province + '%") '
        if(country=="中国" and province=="" and city==""):
            sql=sql+"group by  province , update_time"
    if(province=="" and city=="" and country!="中国"):
        sql = "select update_time,country,confirm,heal,dead,nowconfirm from world where 1=1 "
        if (continent != ""):
            sql = sql + "and (continent like " + '"%' + continent + '%") '
        if (country != ""):
            sql = sql + "and (country like " + '"%' + country + '%") '
    print(sql)
    print("查询（无日期）")
    res = query(sql)
    print(res)
    return res

if __name__ == "__main__":
    update_world()
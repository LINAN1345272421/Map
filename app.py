import operator

from flask import Flask, request, jsonify
from flask import render_template
import utils

app = Flask(__name__)

@app.route('/all')
def update_all():
    utils.update_history()
    utils.update_details()
    return "1"

@app.route('/tem')
def hello_world():
    return render_template("index.html")

@app.route('/c1')
def get_c1_data():
    data=utils.get_c1_data()
    return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/c2')
def get_c2_data():
    name=request.values.get("name")
    res=[]
    if(name=="全国"):
        res=[]
        for tup in utils.get_c2_data():
            res.append({"name": addname(tup[0]), "value": int(tup[1]),"cityCode":getcode(tup[0]),"heal": int(tup[2]),"dead": int(tup[3])})
    else:
        res=[]
        for tup in utils.get_city_data(delname(name)):
            res.append({"name":addcityname(tup[0]),"value":int(tup[1]),"heal": int(tup[2]),"dead": int(tup[3])})
    print(res)
    return jsonify({"data":res})

@app.route('/b1')
def get_b1_data():
    name=[]
    value=[]
    for tup ,v in utils.get_b1_data():
        name.append(tup)
        value.append(v)
    return jsonify({"name":name,"value":value})

@app.route('/query')
def get_query_data():
    year=request.values.get("year")
    print(year)
    month=request.values.get("month")
    print(month)
    day=request.values.get("day")
    print(day)
    name=[]
    value=[]
    for tup ,v in utils.get_query_data(year,month,day):
        name.append(tup)
        value.append(v)
    return jsonify({"name":name,"value":value})

@app.route('/b2')
def get_b2_data():
    list=[]
    name=[]
    value = []
    for n ,c,h,d in utils.get_c2_data():
        list.append({"name":n,"value":round((h/c)*100,2)})
    list.sort(key=operator.itemgetter('value'))
    for n in list:
        name.append(n["name"])
        value.append(n["value"])
    return jsonify({"name":name,"value":value})

@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,dead=[],[],[]
    for a,b,c in data:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        dead.append(c)
    return jsonify({"day":day,"confirm":confirm,"dead":dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day,heal_add,dead_add=[],[],[]
    for a,b,c in data:
        day.append(a.strftime("%m-%d"))
        heal_add.append(b)
        dead_add.append(c)
    return jsonify({"day":day,"heal_add":heal_add,"dead_add":dead_add})

@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    list=[]
    for a,b, in data:
        list.append({"name":a,"value":b})
    return jsonify({"data":list})

@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data()
    list=[]
    for a,b, in data:
        list.append({"name":a,"value":b})
    return jsonify({"data":list})


def addname(name):
    list=["北京","天津","上海","重庆"]
    list2=["内蒙古","西藏"]
    list3=["香港","澳门"]
    list4=["河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西",
           "山东","河南","湖北","湖南","广东","海南","四川","贵州","云南",
           "陕西","甘肃","青海","台湾"]
    if(name in list):
        return name+"市"
    if(name in list2):
        return name+"自治区"
    if(name=="新疆"):
        return "新疆维吾尔自治区"
    if(name=="宁夏"):
        return "宁夏回族自治区"
    if(name=="广西"):
        return "广西壮族自治区"
    if(name in list3):
        return name+"特别行政区"
    if(name in list4):
        return name+"省"

def delname(name):
    list=["北京市","天津市","上海市","重庆市"]
    list2=["内蒙古自治区","西藏自治区"]
    list5=["宁夏回族自治区","广西壮族自治区"]
    list3=["香港特别行政区","澳门特别行政区"]
    list4=["河北省","山西省","辽宁省","吉林省","黑龙江省","江苏省","浙江省","安徽省","福建省","江西省",
           "山东省","河南省","湖北省","湖南省","广东省","海南省","四川省","贵州省","云南省",
           "陕西省","甘肃省","青海省","台湾省"]
    if(name in list):
        return name[0:len(name)-1]
    if(name in list2):
        return name[0:len(name)-3]
    if(name in list3):
        return name[0:len(name)-5]
    if(name in list4):
        return name[0:len(name)-1]
    if(name in list5):
        return name[0:len(name)-5]
    if(name=="新疆维吾尔自治区"):
        return "新疆"

def getcode(name):
    if(name=="全国"):
        return 100000
    if(name=="北京"):
        return 110000
    if(name=="天津"):
        return 120000
    if(name=="河北"):
        return 130000
    if(name=="山西"):
        return 140000
    if(name=="内蒙古"):
        return 150000
    if(name=="辽宁"):
        return 210000
    if(name=="吉林"):
        return 220000
    if(name=="黑龙江"):
        return 230000
    if(name=="上海"):
        return 310000
    if(name=="江苏"):
        return 320000
    if(name=="浙江"):
        return 330000
    if(name=="安徽"):
        return 340000
    if(name=="福建"):
        return 350000
    if(name=="江西"):
        return 360000
    if(name=="山东"):
        return 370000
    if(name=="河南"):
        return 410000
    if(name=="湖北"):
        return 420000
    if(name=="湖南"):
        return 430000
    if(name=="广东"):
        return 440000
    if(name=="广西"):
        return 450000
    if(name=="海南"):
        return 460000
    if(name=="重庆"):
        return 500000
    if(name=="四川"):
        return 510000
    if(name=="贵州"):
        return 520000
    if(name=="云南"):
        return 530000
    if(name=="西藏"):
        return 540000
    if(name=="陕西"):
        return 610000
    if(name=="甘肃"):
        return 620000
    if(name=="青海"):
        return 630000
    if(name=="宁夏"):
        return 640000
    if(name=="新疆"):
        return 650000
    if(name=="台湾"):
        return 710000
    if(name=="香港"):
        return 810000
    if(name=="澳门"):
        return 820000

def addcityname(name):
    if(name[len(name)-1]=='区'):
        return name
    if(name[len(name)-1]=='县'):
        return name
    return name+"市"

if __name__ == '__main__':
    app.run()

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

@app.route('/all_world')
def update_all_world():
    utils.update_history()
    utils.update_details()
    utils.update_world()
    return "1"

@app.route('/tem')
def hello_world():
    return render_template("index.html")

@app.route('/c1')
def get_c1_data():
    data=utils.get_c1_data()
    print("中国统计")
    print(data)
    return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route('/world_c1')
def get_world_c1_data():
    data=utils.get_world_c1_data()
    print("世界统计:")
    print(data)
    return jsonify({"confirm":data[0],"heal":data[1],"dead":data[2],"nowConfirm":data[3]})

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
    print("下砖数据")
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
    print("非湖北地区TOP5")
    print(list)
    return jsonify({"data":list})

@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data()
    list=[]
    for a,b, in data:
        list.append({"name":a,"value":b})
    print("境外输入TOP5")
    print(list)
    return jsonify({"data":list})

@app.route("/world_bar")
def get_world_bar_data():
    data = utils.get_world_bar_data()
    list=[]
    name=[]
    value=[]
    for a,b, in data:
        list.append({"name":a,"value":b})
        name.append(a)
        value.append(b)
    print("世界确诊TOP8")
    print(list)
    return jsonify({"name":name,"value":value})

@app.route("/all_world_data")
def get_all_world_data():
    data=[]
    for a in utils.get_all_world_data():
        data.append({"name":trans_world(a[0]),"value":a[1],"heal":a[2],"dead":a[3]})
    i=utils.get_china_data()
    data.append({"name":"China","value":i[1],"heal":i[2],"dead":i[3]})
    print("世界地图数据")
    print(data)
    return jsonify({"data":data})

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
    if(name[len(name)-1]=='市'):
        return name
    return name+"市"

def trans_world(name):
    if(name=="阿富汗"):
        return "Afghanistan"
    if(name=="安哥拉"):
        return "Angola"
    if(name=="阿尔巴尼亚"):
        return "Albania"
    if(name=="阿联酋"):
        return "United Arab Emirates"
    if(name=="阿根廷"):
        return "Argentina"
    if(name=="亚美尼亚"):
        return "Armenia"
    if(name=="法属南半球和南极领地"):
        return "French Southern and Antarctic Lands"
    if(name=="澳大利亚"):
        return "Australia"
    if(name=="奥地利"):
        return "Austria"
    if(name=="阿塞拜疆"):
        return "Azerbaijan"
    if(name=="布隆迪"):
        return "Burundi"
    if(name=="比利时"):
        return "Belgium"
    if(name=="贝宁"):
        return "Benin"
    if(name=="布基纳法索"):
        return "Burkina Faso"
    if(name=="孟加拉国"):
        return "Bangladesh"
    if(name=="保加利亚"):
        return "Bulgaria"
    if(name=="巴哈马"):
        return "The Bahamas"
    if(name=="波黑"):
        return "Bosnia and Herz."
    if(name=="白俄罗斯"):
        return "Belarus"
    if(name=="伯利兹"):
        return "Belize"
    if(name=="百慕大"):
        return "Bermuda"
    if(name=="玻利维亚"):
        return "Bolivia"
    if(name=="巴西"):
        return "Brazil"
    if(name=="文莱"):
        return "Brunei"
    if(name=="不丹"):
        return "Bhutan"
    if(name=="博茨瓦纳"):
        return "Botswana"
    if(name=="加拿大"):
        return "Canada"
    if(name=="瑞士"):
        return "Switzerland"
    if(name=="智利"):
        return "Chile"
    if(name=="中国"):
        return "China"
    if(name=="象牙海岸"):
        return "Ivory Coast"
    if(name=="喀麦隆"):
        return "Cameroon"
    if(name=="刚果（金）"):
        return "Dem. Rep. Congo"
    if(name=="刚果（布）"):
        return "Congo"
    if(name=="哥伦比亚"):
        return "Colombia"
    if(name=="哥斯达黎加"):
        return "Costa Rica"
    if(name=="古巴"):
        return "Cuba"
    if(name=="北塞浦路斯"):
        return "Northern Cyprus"
    if(name=="塞浦路斯"):
        return "Cyprus"
    if(name=="捷克"):
        return "Czech Rep."
    if(name=="德国"):
        return "Germany"
    if(name=="吉布提"):
        return "Djibouti"
    if(name=="丹麦"):
        return "Denmark"
    if(name=="多米尼加共和国"):
        return "Dominican Republic"
    if(name=="阿尔及利亚"):
        return "Algeria"
    if(name=="厄瓜多尔"):
        return "Ecuador"
    if(name=="埃及"):
        return "Egypt"
    if(name=="厄立特里亚"):
        return "Eritrea"
    if(name=="西班牙"):
        return "Spain"
    if(name=="爱沙尼亚"):
        return "Estonia"
    if(name=="埃塞俄比亚"):
        return "Ethiopia"
    if(name=="芬兰"):
        return "Finland"
    if(name=="斐"):
        return "Fiji"
    if(name=="福克兰群岛"):
        return "Falkland Islands"
    if(name=="法国"):
        return "France"
    if(name=="加蓬"):
        return "Gabon"
    if(name=="英国"):
        return "United Kingdom"
    if(name=="格鲁吉亚"):
        return "Georgia"
    if(name=="加纳"):
        return "Ghana"
    if(name=="几内亚"):
        return "Guinea"
    if(name=="冈比亚"):
        return "Gambia"
    if(name=="几内亚比绍"):
        return "Guinea-Bissau"
    if(name=="赤道几内亚"):
        return "Eq. Guinea"
    if(name=="希腊"):
        return "Greece"
    if(name=="格陵兰"):
        return "Greenland"
    if(name=="危地马拉"):
        return "Guatemala"
    if(name=="法属圭亚那"):
        return "French Guiana"
    if(name=="圭亚那"):
        return "Guyana"
    if(name=="洪都拉斯"):
        return "Honduras"
    if(name=="克罗地亚"):
        return "Croatia"
    if(name=="海地"):
        return "Haiti"
    if(name=="匈牙利"):
        return "Hungary"
    if(name=="印度尼西亚"):
        return "Indonesia"
    if(name=="印度"):
        return "India"
    if(name=="爱尔兰"):
        return "Ireland"
    if(name=="伊朗"):
        return "Iran"
    if(name=="伊拉克"):
        return "Iraq"
    if(name=="冰岛"):
        return "Iceland"
    if(name=="以色列"):
        return "Israel"
    if(name=="意大利"):
        return "Italy"
    if(name=="牙买加"):
        return "Jamaica"
    if(name=="约旦"):
        return "Jordan"
    if(name=="日本本土"):
        return "Japan"
    if(name=="哈萨克斯坦"):
        return "Kazakhstan"
    if(name=="肯尼亚"):
        return "Kenya"
    if(name=="吉尔吉斯斯坦"):
        return "Kyrgyzstan"
    if(name=="柬埔寨"):
        return "Cambodia"
    if(name=="科索沃"):
        return "Kosovo"
    if(name=="科威特"):
        return "Kuwait"
    if(name=="老挝"):
        return "Laos"
    if(name=="黎巴嫩"):
        return "Lebanon"
    if(name=="利比里亚"):
        return "Liberia"
    if(name=="利比亚"):
        return "Libya"
    if(name=="斯里兰卡"):
        return "Sri Lanka"
    if(name=="莱索托"):
        return "Lesotho"
    if(name=="立陶宛"):
        return "Lithuania"
    if(name=="卢森堡"):
        return "Luxembourg"
    if(name=="拉脱维亚"):
        return "Latvia"
    if(name=="摩洛哥"):
        return "Morocco"
    if(name=="摩尔多瓦"):
        return "Moldova"
    if(name=="马达加斯加"):
        return "Madagascar"
    if(name=="墨西哥"):
        return "Mexico"
    if(name=="北马其顿"):
        return "Macedonia"
    if(name=="马里"):
        return "Mali"
    if(name=="缅甸"):
        return "Myanmar"
    if(name=="黑山"):
        return "Montenegro"
    if(name=="蒙古"):
        return "Mongolia"
    if(name=="莫桑比克"):
        return "Mozambique"
    if(name=="毛里塔尼亚"):
        return "Mauritania"
    if(name=="马拉维"):
        return "Malawi"
    if(name=="马来西亚"):
        return "Malaysia"
    if(name=="纳米比亚"):
        return "Namibia"
    if(name=="新喀里多尼亚"):
        return "New Caledonia"
    if(name=="尼日尔"):
        return "Niger"
    if(name=="尼日利亚"):
        return "Nigeria"
    if(name=="尼加拉瓜"):
        return "Nicaragua"
    if(name=="荷兰"):
        return "Netherlands"
    if(name=="挪威"):
        return "Norway"
    if(name=="尼泊尔"):
        return "Nepal"
    if(name=="新西兰"):
        return "New Zealand"
    if(name=="阿曼"):
        return "Oman"
    if(name=="巴基斯坦"):
        return "Pakistan"
    if(name=="巴拿马"):
        return "Panama"
    if(name=="秘鲁"):
        return "Peru"
    if(name=="菲律宾"):
        return "Philippines"
    if(name=="巴布亚新几内亚"):
        return "Papua New Guinea"
    if(name=="波兰"):
        return  "Poland"
    if(name=="波多黎各"):
        return "Puerto Rico"
    if(name=="葡萄牙"):
        return "Portugal"
    if(name=="巴拉圭"):
        return "Paraguay"
    if(name=="卡塔尔"):
        return "Qatar"
    if(name=="罗马尼亚"):
        return "Romania"
    if(name=="俄罗斯"):
        return "Russia"
    if(name=="卢旺达"):
        return "Rwanda"
    if(name=="西撒哈拉"):
        return "W. Sahara"
    if(name=="沙特阿拉伯"):
        return "Saudi Arabia"
    if(name=="苏丹"):
        return "Sudan"
    if(name=="南苏丹"):
        return "South Sudan"
    if(name=="塞内加尔"):
        return "Senegal"
    if(name=="所罗门群岛"):
        return "Solomon Islands"
    if(name=="塞拉利昂"):
        return "Sierra Leone"
    if(name=="萨尔瓦多"):
        return "El Salvador"
    if(name=="索马里兰"):
        return "Somaliland"
    if(name=="索马里"):
        return "Somalia"
    if(name=="塞尔维亚"):
        return "Serbia"
    if(name=="苏里南"):
        return "Suriname"
    if(name=="斯洛伐克"):
        return "Slovakia"
    if(name=="斯洛文尼亚"):
        return "Slovenia"
    if(name=="瑞典"):
        return "Sweden"
    if(name=="斯威士兰"):
        return "Swaziland"
    if(name=="叙利亚"):
        return "Syria"
    if(name=="乍得"):
        return "Chad"
    if(name=="多哥"):
        return "Togo"
    if(name=="泰国"):
        return "Thailand"
    if(name=="塔吉克斯坦"):
        return "Tajikistan"
    if(name=="土库曼斯坦"):
        return "Turkmenistan"
    if(name=="东帝汶"):
        return "East Timor"
    if(name=="特里尼达和多巴哥"):
        return "Trinidad and Tobago"
    if(name=="突尼斯"):
        return "Tunisia"
    if(name=="土耳其"):
        return "Turkey"
    if(name=="乌干达"):
        return "Uganda"
    if(name=="乌克兰"):
        return "Ukraine"
    if(name=="乌拉圭"):
        return "Uruguay"
    if(name=="美国"):
        return "United States"
    if(name=="乌兹别克斯坦"):
        return "Uzbekistan"
    if(name=="委内瑞拉"):
        return "Venezuela"
    if(name=="越南"):
        return "Vietnam"
    if(name=="瓦努阿图"):
        return  "Vanuatu"
    if(name=="西岸"):
        return "West Bank"
    if(name=="也门"):
        return "Yemen"
    if(name=="南非"):
        return "South Africa"
    if(name=="赞比亚"):
        return "Zambia"
    if(name=="津巴布韦"):
        return "Zimbabwe"
    if(name=="新加坡"):
        return "Singapore Rep."
    if(name=="多米尼加"):
        return "Dominican Rep."
    if(name=="巴勒斯坦"):
        return "Palestine"
    if(name=="巴哈马"):
        return "Bahamas"
    if(name=="东帝汶"):
        return "Timor-Leste"
    if(name=="几内亚比绍"):
        return "Guinea-Bissau"
    if(name=="科特迪瓦"):
        return "Côte d'Ivoire"
    if(name=="锡亚琴冰川"):
        return "Siachen Glacier"
    if(name=="英属印度洋领土"):
        return "Br. Indian Ocean Ter."
    if(name=="波斯尼亚和黑塞哥维那"):
        return "Bosnia and Herz."
    if(name=="中非共和国"):
        return "Central African Rep."
    if(name=="北塞浦路斯"):
        return "N. Cyprus"
    if(name=="捷克"):
        return "Czech Rep."
    if(name=="韩国"):
        return "Korea"
    if(name=="老挝"):
        return "Lao PDR"
    if(name=="朝鲜"):
        return "Dem. Rep. Korea"
    if(name=="西撒哈拉"):
        return "W. Sahara"
    if(name=="南苏丹"):
        return "S. Sudan"
    if(name=="所罗门群岛"):
        return "Solomon Is."
    if(name=="塞尔维亚"):
        return "Serbia"
    if(name=="坦桑尼亚"):
        return "Tanzania"




@app.route('/tem2')
def hello_world2():
    return render_template("index2.html")

@app.route('/query2')
def get_query_data2():
    fromyear=request.values.get("fromyear")
    frommounth=request.values.get("frommounth")
    fromday=request.values.get("fromday")
    toyear=request.values.get("toyear")
    tomounth=request.values.get("tomounth")
    today=request.values.get("today")

    continent=request.values.get("continent")
    country=request.values.get("country")
    province=request.values.get("province")
    city=request.values.get("city")
    Data=[]
    if(fromday!=""):
        for data in \
                utils.get_query_like1(fromyear,frommounth,fromday,toyear,tomounth,today,
                    continent,country,province,city):
            Data.append(data)
    else:
        for data in \
                utils.get_query_like2(continent,country,province,city):
            Data.append(data)
    return jsonify({"data":Data})

@app.route('/tem3')
def hello_world_android():
    return render_template("android.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

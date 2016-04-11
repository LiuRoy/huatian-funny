# -*- coding=utf8 -*-
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['huatian']
mongo_collection = mongo_db['user']

BUY_HOUSE = {
    u'0': u'--',
    u'1': u'已购房',
    u'2': u'租房',
    u'3': u'单位宿舍',
    u'4': u'和家人住一起',
}
BUY_CAR = {
    u'0': u'--',
    u'1': u'已购车',
    u'2': u'未购车',
}
SALARY = {
    u'-1': u'2000以下',
    u'1': u'2000-4000',
    u'2': u'4000-6000',
    u'3': u'6000-10000',
    u'4': u'10000-15000',
    u'5': u'15000-20000',
    u'6': u'20000-50000',
    u'7': u'50000以上'
}
EDUCATION = {
    u'1': u'大专以下',
    u'2': u'大专',
    u'3': u'本科',
    u'4': u'硕士',
    u'5': u'博士',
}
INDUSTRY = {
    u'0': u'--',
    u'1': u'计算机/互联网/通信',
    u'2': u'公务员/事业单位',
    u'3': u'教师',
    u'4': u'医生',
    u'5': u'护士',
    u'6': u'空乘人员',
    u'7': u'生产/工艺/制造',
    u'8': u'商业/服务业/个体经营',
    u'9': u'金融/银行/投资/保险',
    u'10': u'文化/广告/传媒',
    u'11': u'娱乐/艺术/表演',
    u'12': u'律师/法务',
    u'13': u'教育/培训/管理咨询',
    u'14': u'建筑/房地产/物业',
    u'15': u'消费零售/贸易/交通物流',
    u'16': u'酒店旅游',
    u'17': u'现代农业',
    u'18': u'在校学生',
}
POSITION = {
    u'0': u'--',
    u'1': u'普通职员',
    u'2': u'中层管理者',
    u'3': u'高层管理员',
    u'4': u'企业主',
    u'5': u'学生',
}
SATISFY = {
    0: u'不满意',
    1: u'满意'
}
# -*- coding=utf8 -*-
"""
    打分程序
"""

import io
from urllib2 import urlopen
from tkMessageBox import showwarning
from Tkinter import Tk, Label, Button, Radiobutton, IntVar
from tkFont import Font
from PIL import Image, ImageTk
from extension import mongo_collection, BUY_HOUSE, BUY_CAR,\
    EDUCATION, INDUSTRY, SALARY, POSITION

master = None
tk_image = None

offset = 0
user, photo, url, buy_house, buy_car, age, height, salary, education, company, \
industry, school, position, satisfy, appearance = [None for i in range(15)]


def get_user(offset=0):
    """mongo中读取用户信息"""
    global user
    user = mongo_collection.find_one({}, skip=offset, limit=1, sort=[('url', -1)])


def init_master():
    """初始化主窗口"""
    global master
    master = Tk()
    master.title(u'花田')
    master.geometry(u'630x530')
    master.resizable(width=False, height=False)


def place_image(image_ur):
    """获取用户头像"""
    global tk_image
    image_bytes = urlopen(image_ur).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)


def set_appearance():
    """设置头像评分"""
    mongo_collection.update({'url': user['url']},
                            {'$set': {'appearance': appearance.get()}})


def set_satisfy():
    """设置是否满意"""
    mongo_collection.update({'url': user['url']},
                            {'$set': {'satisfy': satisfy.get()}})


def update():
    """更新页面"""
    global user, offset, photo, url, buy_house, buy_car, age, height, salary, \
        education, company, industry, school, position, satisfy, appearance
    image_url = u'{}&quality=85&thumbnail=410y410'.format(user['avatar'])
    place_image(image_url)

    print offset

    photo['image'] = tk_image
    url['text'] = user['url']
    buy_house['text'] = BUY_HOUSE.get(user['house']) or user['house']
    buy_car['text'] = BUY_CAR.get(user['car']) or user['car']
    age['text'] = user['age']
    height['text'] = user['height']
    salary['text'] = SALARY.get(user['salary']) or user['salary']
    education['text'] = EDUCATION.get(user['education']) or user['education']
    company['text'] = user['company'] if user['company'] else u'--'
    industry['text'] = INDUSTRY.get(user['industry']) or user['industry']
    school['text'] = user['school'] if user['school'] else u'--'
    position = POSITION.get(user['position']) or user['position']

    satisfy.set(int(user.get(u'satisfy', -1)))
    appearance.set(int(user.get(u'appearance', -1)))


def init():
    """初始化页面"""
    global user, offset, photo, url, buy_house, buy_car, age, height, salary, \
        education, company, industry, school, position, satisfy, appearance
    get_user(offset)
    image_url = u'{}&quality=85&thumbnail=410y410'.format(user['avatar'])
    place_image(image_url)

    photo = Label(master, image=tk_image)
    photo.place(anchor=u'nw', x=10, y=40)
    url = Label(master, text=user['url'], font=Font(size=20, weight='bold'))
    url.place(anchor=u'nw', x=10, y=5)
    buy_house = Label(master, text=BUY_HOUSE.get(user['house']) or user['house'])
    buy_house.place(anchor=u'nw', x=490, y=50)
    buy_car = Label(master, text=BUY_CAR.get(user['car']) or user['car'])
    buy_car.place(anchor=u'nw', x=490, y=75)
    age = Label(master, text=user['age'])
    age.place(anchor=u'nw', x=490, y=100)
    height = Label(master, text=user['height'])
    height.place(anchor=u'nw', x=490, y=125)
    salary = Label(master, text=SALARY.get(user['salary']) or user['salary'])
    salary.place(anchor=u'nw', x=490, y=150)
    education = Label(master, text=EDUCATION.get(user['education']) or user['education'])
    education.place(anchor=u'nw', x=490, y=175)
    company = Label(master, text=user['company'] if user['company'] else u'--')
    company.place(anchor=u'nw', x=490, y=200)
    industry = Label(master, text=INDUSTRY.get(user['industry']) or user['industry'])
    industry.place(anchor=u'nw', x=490, y=225)
    school = Label(master, text=user['school'] if user['school'] else u'--')
    school.place(anchor=u'nw', x=490, y=250)
    position = Label(master, text=POSITION.get(user['position']) or user['position'])
    position.place(anchor=u'nw', x=490, y=275)

    satisfy = IntVar()
    satisfy.set(int(user.get(u'satisfy', -1)))
    satisfied = Radiobutton(master, text=u"满意", variable=satisfy,
                            value=1, command=set_satisfy)
    not_satisfied = Radiobutton(master, text=u"不满意", variable=satisfy,
                                value=0, command=set_satisfy)
    satisfied.place(anchor=u'nw', x=450, y=10)
    not_satisfied.place(anchor=u'nw', x=510, y=10)

    appearance = IntVar()
    appearance.set(int(user.get(u'appearance', -1)))
    for i in range(1, 11):
        score_i = Radiobutton(master, text=str(i), variable=appearance,
                              value=i, command=set_appearance)
        score_i.place(anchor=u'nw', x=i * 40 - 30, y=460)


def handle_previous():
    """上一个用户"""
    global offset
    if offset <= 0:
        showwarning(u'error', u'已经是第一个')

    offset -= 1
    get_user(offset)
    update()


def handle_next():
    """下一个用户"""
    global offset

    offset += 1
    get_user(offset)
    if not user:
        showwarning(u'error', u'已经是第后一个')
        return
    update()


def add_assembly():
    """添加组件"""
    init()

    buy_house_static = Label(master, text=u'购房: ', font=Font(size=15))
    buy_house_static.place(anchor=u'nw', x=440, y=50)
    buy_car_static = Label(master, text=u'购车: ', font=Font(size=15))
    buy_car_static.place(anchor=u'nw', x=440, y=75)
    age_static = Label(master, text=u'年龄: ', font=Font(size=15))
    age_static.place(anchor=u'nw', x=440, y=100)
    height_static = Label(master, text=u'身高: ', font=Font(size=15))
    height_static.place(anchor=u'nw', x=440, y=125)
    salary_static = Label(master, text=u'工资: ', font=Font(size=15))
    salary_static.place(anchor=u'nw', x=440, y=150)
    education_static = Label(master, text=u'学历: ', font=Font(size=15))
    education_static.place(anchor=u'nw', x=440, y=175)
    company_static = Label(master, text=u'公司: ', font=Font(size=15))
    company_static.place(anchor=u'nw', x=440, y=200)
    industry_static = Label(master, text=u'行业: ', font=Font(size=15))
    industry_static.place(anchor=u'nw', x=440, y=225)
    school_static = Label(master, text=u'学校: ', font=Font(size=15))
    school_static.place(anchor=u'nw', x=440, y=250)
    position_static = Label(master, text=u'职位: ', font=Font(size=15))
    position_static.place(anchor=u'nw', x=440, y=275)
    previous = Button(master, text=u'上一个', command=handle_previous)
    previous.place(anchor=u'nw', x=10, y=490)
    next = Button(master, text=u'下一个', command=handle_next)
    next.place(anchor=u'nw', x=520, y=490)


if __name__ == '__main__':
    init_master()
    add_assembly()
    master.mainloop()

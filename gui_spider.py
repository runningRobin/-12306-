# -*- coding:utf8 -*-
from Tkinter import *
from ScrolledText import ScrolledText
import urllib2
import ssl
import json
from city import *
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
}

is_show_title = 0
def getlist(from_station, to_station, train_date):
    req = urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' %(train_date, from_station, to_station))
    req.headers = headers
    html = urllib2.urlopen(req)
    dict = json.loads(html.read())
    return dict

def dosearch():
    global is_show_title
    is_show_title = 0
    z_tpye = {32:sw, 25:td, 31:yd, 30:rd, 21:gr, 23:rw, 28:yw, 24:rz, 29:yz}
    select_type = []
    for i in z_tpye:
        if z_tpye[i].get() == '1':
            select_type.append(i)

    text.delete(0.0, END)
    from_city = entry_from_city.get().encode('utf-8')
    to_city = entry_to_city.get().encode('utf-8')
    train_date = entry_date.get().encode('utf-8')
    from_station = city_name[from_city]
    to_station = city_name[to_city]
    # from_station = 'BJP'
    # to_station = 'XHP'
    # train_date = '2017-05-30'
    for i in getlist(from_station, to_station, train_date)['data']['result']:
        str_info = i.split('|')
        showtext(select_type, str_info)

def showtext(select_type, str_info):
    global is_show_title
    z_tpye_name = {32:u'商务', 25:u'特等座', 31:u'一等座', 30:u'二等座', 21:u'高级软卧', 23:u'软卧', 28:u'硬卧', 24:u'软座', 29:u'硬座'}
    str_len = len(str_info[3])
    str_show = u'|---车次---|-发车时间-|-到站时间-|'
    str_info_show = ''
    if str_len == 5:
        str_info_show = u'|--' + str_info[3] + u'--|--' + str_info[8] + u'---|--' + str_info[9] + u'--|'
    elif str_len == 4:
        str_info_show = u'|---' + str_info[3] + u'--|--' + str_info[8] + u'---|--' + str_info[9] + u'--|'
    elif str_len == 3:
        str_info_show = u'|---' + str_info[3] + u' ---|--' + str_info[8] + u'---|--' + str_info[9] + u'--|'
    elif str_len == 2:
        str_info_show = u'|---' + str_info[3] + u'--|--' + str_info[8] + u'---|--' + str_info[9] + u'--|'
    for i in select_type:
        if str_info[i]:
            str_show += u'--' + z_tpye_name[i] + u'--|'
            str_info_show += u'---' + str_info[i] + u'---|'
        else:
            str_show += u'--' + z_tpye_name[i]+u'--|'
            str_info_show += u'---无---|'
    if is_show_title == 0:
        text.insert(END, str_show+'\n')
        is_show_title += 1
    str_info_show += '\n'
    text.insert(END, str_info_show)

root = Tk()
root.title('12306抢票小工具')
root.geometry('+600+100')

label_from_city = Label(root, text='出发城市', font=('微软雅黑', 10))
label_from_city.grid(row=0, column=0, ipady=10)
entry_from_city = Entry(root)
entry_from_city.grid(row=0, column=1, ipady=3)

label_to_city = Label(root, text='目的城市', font=('微软雅黑', 10))
label_to_city.grid(row=0, column=2, ipady=10)
entry_to_city = Entry(root)
entry_to_city.grid(row=0, column=3, ipady=3)

label_date = Label(root, text='出发日期', font=('微软雅黑', 10))
label_date.grid(row=0, column=4, ipady=10)
entry_date = Entry(root)
entry_date.grid(row=0, column=5, ipady=3)

sw = StringVar()
td = StringVar()
yd = StringVar()
rd = StringVar()
gr = StringVar()
rw = StringVar()
yw = StringVar()
rz = StringVar()
yz = StringVar()
sw.set(0)
td.set(0)
yd.set(0)
rd.set(0)
gr.set(0)
rw.set(0)
yw.set(0)
rz.set(0)
yz.set(0)

check_type_sw = Checkbutton(root, text='商务座', variable=sw)
check_type_sw.grid(row=1, column=0, columnspan=5, sticky='w',padx=10)
check_type_td = Checkbutton(root, text='特等座', variable=td, pady=10)
check_type_td.grid(row=1, column=0, columnspan=5, sticky='w', padx=70)
check_type_yd = Checkbutton(root, text='一等座', variable=yd)
check_type_yd.grid(row=1, column=0, columnspan=5, sticky='w', padx=130)
check_type_rd = Checkbutton(root, text='二等座', variable=rd)
check_type_rd.grid(row=1, column=0, columnspan=5, sticky='w', padx=190)
check_type_gr = Checkbutton(root, text='高级软卧', variable=gr)
check_type_gr.grid(row=1, column=0, columnspan=5, sticky='w', padx=250)
check_type_rw = Checkbutton(root, text='软卧', variable=rw)
check_type_rw.grid(row=1, column=0, columnspan=5, sticky='e', padx=200)
check_type_yw = Checkbutton(root, text='硬卧', variable=yw)
check_type_yw.grid(row=1, column=0, columnspan=5, sticky='e', padx=150)
check_type_yz = Checkbutton(root, text='软座', variable=rz)
check_type_yz.grid(row=1, column=0, columnspan=5, sticky='e', padx=100)
check_type_yz = Checkbutton(root, text='硬座', variable=yz)
check_type_yz.grid(row=1, column=0, columnspan=5, sticky='e', padx=50)

button = Button(root, text='Start', font=('微软雅黑', 10), command=dosearch)
button.grid(row=1, column=5, columnspan=2, ipadx=10)

text = ScrolledText(root, font=('微软雅黑', 10))
text.grid(row=2, columnspan=6)

root.mainloop()

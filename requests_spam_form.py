import re
import string
import random
import requests
import threading
import tkinter as tk
from tkinter import messagebox


def random_string(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

s = requests.session()


if __name__ == '__main__':
    url_in = str(input("Nhập Link muốn Spam: ")).strip()
    #url_in = str( prompt('Nhap Link: ')).strip()

    #url_in = 'https://docs.google.com/forms/d/e/1FAIpQLSdij99or2kqhGneofj2945weO6UO2eOvQkChh879ZJXsJGAqA/viewform'
    url = s.get(url_in).url
    url_rsp = 'https://docs.google.com/forms/u/0/d/e/'+url.split('/')[-2]+'/formResponse'

    contentext = s.get(url_rsp).text
    pram = "<title>(.*?)</title>"
    try:
        titlee = re.findall(pram, contentext, re.DOTALL)[0]
    except Exception as e:
        print(f"Lỗi: {e}")
    if titlee:
        print("FROM SPAM - TÊN FORM VỪA NHẬP:")
        print('--------------------------------------------------')
        print(titlee.center(50, '|'))
        print('--------------------------------------------------\n')
    else:
        print("link lỗi !!!")
    max_spam = int(input("Nhập số lần muốn Spam: "))
    pattern = r'data-params="%.@.(.*?)<span class'

    dta ={}
    cau_tra_loi ={}
    matches = re.findall(pattern, contentext, re.DOTALL)
    for mat in matches:

        mat = mat.split(']]')[0]
        pattern = r',&quot;(.*?)&quot.*?\[\[(\d+)'
        mattch = re.findall(pattern, mat)
        cauhoi, id_q= mattch[0]
        pattern = r"&quot;(.*?)&quot"

        cautraloi = re.findall(pattern, mat)[2:]
        if "[false,true]" in mat:
            ngay_thang_nam = True
            dta['entry.' + id_q + '_year'] = "year"
            dta['entry.' + id_q + '_month'] = "month"
            dta['entry.' + id_q + '_day'] = "day"
            # _year
            # _month
            # _day
        elif ",[false]," in mat:
            ngay_gio = True
            dta['entry.' + id_q + '_hour'] = "hour"
            dta['entry.' + id_q + '_minute'] = "minute"
            # _hour:
            # _minute
        elif len(cautraloi) == 0:
            dta['entry.' + id_q] = "No information!"
        else:
            dta['entry.'+id_q] = cautraloi

        # print(id_q, data)
        # print(mattch)
        # input()
    # print(dta)
    # input()
    def random_data():
        data_send = {}
        for key, value in dta.items():

            if "year" in key:
                value = int(random.randint(1890, 2077))
            elif "month" in key:
                value = int(random.randint(1, 12))
            elif "day" in key:
                value = int(random.randint(1, 28))
            elif "minute" in key:
                value = int(random.randint(1, 59))
            elif "hour" in key:
                value = int(random.randint(1, 24))
            elif value != "No information!":
                value = random.choice(value)

            data_send[key] = value
            # print("key", key)
            # print('value', value)

        # print(data_send)
        # input()
        return data_send
    def attack():
        global total_runs
        global max_spam
        if total_runs >= max_spam:
            # print("Đã đạt đến số lần gửi tối đa. Dừng chương trình.")
            return  # Dừng vòng lặp và kết thúc thread
        for _ in range(30):
            try:
                if total_runs >= max_spam:
                    #print("Đã đạt đến số lần gửi tối đa. Dừng chương trình.")
                    return  # Dừng vòng lặp và kết thúc thread
                s.post(url_rsp,data=random_data())
                total_runs += 1
                #print(aa.text)
                if total_runs >= max_spam:
                    # print("Đã đạt đến số lần gửi tối đa. Dừng chương trình.")
                    return  # Dừng vòng lặp và kết thúc thread
                if total_runs <= max_spam:
                    print(f"Đang gửi lần thứ: {total_runs}".center(50, '-'))

            except Exception as e:
                print(f"Lỗi: {e}")

    total_runs = 0
    for _ in range(10000):
        threading.Thread(target=attack).start()


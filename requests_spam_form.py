import string
import random
import requests
import threading
import tkinter as tk
from tkinter import messagebox
import re  # Thêm dòng này để import module re

def random_string(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

s = requests.session()

if __name__ == '__main__':
    url_in = 'https://docs.google.com/forms/d/e/1FAIpQLSdij99or2kqhGneofj2945weO6UO2eOvQkChh879ZJXsJGAqA/viewform'
    url = s.get(url_in).url.split('/')[-2]
    url_rsp = 'https://docs.google.com/forms/u/0/d/e/'+url+'/formResponse'

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

    pattern = r',null,8,'
    numpage = re.findall(pattern, contentext)
    hstorypage = False
    if len(numpage):
        hstorypage = "0"
        for i in range(1, len(numpage) + 1):
            hstorypage += ',' + str(i)

    pattern = f'FB_PUBLIC_LOAD_DATA(.*?){url}'
    dulieu = re.findall(pattern, contentext, re.DOTALL)[0]
    pattern = "\[\d+,\"(.*?)\",null,(\d+)"
    cauhoii = re.findall(pattern, dulieu, re.DOTALL)

    pattern_Get_id = r'\[\[(\d+),'
    pattern_get_cau_tl = r'\[\"(.*?)\"'
    # print(dulieu)
    # input()
    dta = {}
    for (y, z) in cauhoii:
        if int(z) != 8:
            tltracno = dulieu.split(y)[1]
            id_q = re.findall(pattern_Get_id, tltracno)[0]
            if int(z) == 9:
                ngay_thang_nam = True
                dta['entry.' + id_q + '_year'] = "year"
                dta['entry.' + id_q + '_month'] = "month"
                dta['entry.' + id_q + '_day'] = "day"
            elif int(z) == 10:
                ngay_gio = True
                dta['entry.' + id_q + '_hour'] = "hour"
                dta['entry.' + id_q + '_minute'] = "minute"
            elif int(z) == 0:
                dta['entry.' + id_q] = "No information!"
            else:
                cautraloi = re.findall(pattern_get_cau_tl, tltracno.split(']]')[0])
                dta['entry.' + id_q] = cautraloi

    def random_data():
        data_send = {}
        global hstorypage
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
        if hstorypage:
            data_send['pageHistory'] = hstorypage
        return data_send

    def attack():
        global total_runs
        global max_spam
        if total_runs >= max_spam:
            return
        for _ in range(30):
            try:
                if total_runs >= max_spam:
                    return
                s.post(url_rsp,data=random_data())
                total_runs += 1
                if total_runs >= max_spam:
                    return
                if total_runs <= max_spam:
                    print(f"Đang gửi lần thứ: {total_runs}".center(50, '-'))

            except Exception as e:
                print(f"Lỗi: {e}")

    total_runs = 0
    for _ in range(10000):
        threading.Thread(target=attack).start()

"""
作者： 子轩
时间： 2023/2/18
声明： 请勿用于商业用途

"""

import base64
import json
import os
import sys
from os.path import join, abspath

import cv2
import numpy as np
import requests

from utils import plt_img_info, acc_loc_poem, get_acc_poem, get_poem, inference_dir

M4 = 1024 * 1024 * 4  # 图片大小限制  高精度 10M  标准 4M
M10 = 1024 * 1024 * 10  # 图片大小限制  高精度 10M  标准 4M

requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')


def detect_rescale_img(img_path, st_size=M4):
    stats = os.stat(img_path)
    if stats.st_size > st_size:
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        new_img = cv2.resize(img, (0, 0), fx=0.8, fy=0.8, interpolation=cv2.INTER_NEAREST)
        # cv2.imwrite(img_path, new_img) # 本地图片覆盖更新 含有中文路径无法使用
        cv2.imencode('.jpg', new_img)[1].tofile(img_path)  # 保存含有中文路径的图片
        stats = os.stat(img_path)
        if stats.st_size > st_size:
            print(stats.st_size)
            detect_rescale_img(img_path, st_size)
    else:
        pass


class BaiduOcr():
    def __init__(self, api_key, sec_key):
        # 注册百度ocr文字识别获取以下两个密钥
        self.api_api = (api_key, sec_key)
        self.API_KEY = self.api_api[0][0]
        self.SECRET_KEY = self.api_api[1][0]
        self.get_access_token()

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}

        self.ACCESS_TOKEN = str(requests.post(url, params=params).json().get("access_token"))

    def img_2_base64(self, img_path, st_size=M4):
        detect_rescale_img(img_path, st_size)

        with open(img_path, 'rb') as fin:
            image_data = fin.read()
            base64_data = base64.b64encode(image_data)
            return base64_data

    def img_2_word_basic_loc(self, img_path, st_size=M4):
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=" + self.ACCESS_TOKEN
        payload = {
            "image": self.img_2_base64(img_path, st_size)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_dict = json.loads(response.text)
        return json_dict

    def img_2_word_acc_loc(self, img_path, st_size=M10):
        url_acc = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + self.ACCESS_TOKEN
        payload = {
            "image": self.img_2_base64(img_path, st_size)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url_acc, headers=headers, data=payload)
        json_dict = json.loads(response.text)
        return json_dict
    def connect_test(self, img_path, acc_loc):
        if acc_loc:
            json_dict_1 = self.img_2_word_acc_loc(img_path)
        else:
            json_dict_1 = self.img_2_word_basic_loc(img_path)
        print(json_dict_1)
        connected_flag = False

        if list(json_dict_1.keys())[0] not in ['error_code', 'error_msg']:
            connected_flag = True
        try:
            msg = json_dict_1['error_msg']
        except:
            msg = ""
        return connected_flag, msg

    def inference(self, img_path, img_save_path, acc_loc=False, dpi=300):

        if acc_loc:
            json_dict_1 = self.img_2_word_acc_loc(img_path)
        else:
            json_dict_1 = self.img_2_word_basic_loc(img_path)  # 带位置坐标
        print(json_dict_1)
        if list(json_dict_1.keys())[0] in ['error_code']:
            connect_flag = False
            for value in range(len(self.api_api[0])):

                self.API_KEY = self.api_api[0][value]
                self.SECRET_KEY = self.api_api[1][value]
                self.get_access_token()

                connect_flag, msg = self.connect_test(img_path, acc_loc)




if __name__ == '__main__':
    import datetime

    date = str(datetime.date.today())

    """
    注意：imgs_save 中保存的是临时图片，默认100张后清空
    注意：生成的文件 和记录保存在word_save 中，请不要删除csv文件，此为project log

    需要更改的值
    imgs_dir :  照片所在文件夹的绝对地址
    acc_loc： bool类型， 选择是高精度（True）(每个账户每月500张)，还是普通精度（False）
    task_name : 同一个task name会记录已经完成的照片，可以中断后继续。任意起名即可
    以下为需要给定的超参数

    """
    s = json.load(open("setting_test.json", "r", encoding="utf-8"))
    API_KEY = s['API_KEY']
    SECRET_KEY = s['SECRET_KEY']
    imgs_dir = s['imgs_dir']
    acc_loc = s['acc_loc']
    word_save_dir = s['word_save']
    img_temp_dir = s['img_temp']
    dpi = s['dpi']
    if s['path_sort_way'] == 'string':
        sort_way = 1

    elif s['path_sort_way'] == 'int':
        sort_way = 2
    else:
        print("sort_Way must be string or int ")
        sys.exit()

    project = BaiduOcr(API_KEY, SECRET_KEY)  # 创建一个实例对象

    for imgsdir in imgs_dir:
        task_name = os.path.basename(imgsdir) + date
        inference_dir(project, imgsdir, word_save_dir, img_temp_dir, task_name=task_name, acc_loc=acc_loc, dpi=dpi,
                      sort_way=sort_way)

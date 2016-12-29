# -*- coding: utf-8 -*-
import requests
from PIL import Image
from svmutil import *
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

base_path = 'xxxx'


def get_bin_table():
    threshold = 80
    table = []
    for ii in range(256):
        if ii < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


# 判断像素点是黑点还是白点
def getflag(img, x, y):
    tmp_pixel = img.getpixel((x, y))
    if tmp_pixel > 228:  # 白点
        tmp_pixel = 0
    else:  # 黑点
        tmp_pixel = 1
    return tmp_pixel


# 黑点个数
def sum_9_region(img, x, y):
    width = img.width
    height = img.height
    flag = getflag(img, x, y)
    # 如果当前点为白色区域,则不统计邻域值
    if flag == 0:
        return 0
    # 如果是黑点
    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            total = getflag(img, x, y + 1) + getflag(img, x + 1, y) + getflag(img, x + 1, y + 1)
            return total
        elif x == width - 1:  # 右上顶点
            total = getflag(img, x, y + 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y + 1)
            return total
        else:  # 最上非顶点,6邻域
            total = getflag(img, x - 1, y) + getflag(img, x - 1, y + 1) + getflag(img, x, y + 1) \
                    + getflag(img, x + 1, y) \
                    + getflag(img, x + 1, y + 1)
            return total
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            total = getflag(img, x + 1, y) + getflag(img, x + 1, y - 1) + getflag(img, x, y - 1)
            return total
        elif x == width - 1:  # 右下顶点
            total = getflag(img, x, y - 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y - 1)
            return total
        else:  # 最下非顶点,6邻域
            total = getflag(img, x - 1, y) + getflag(img, x + 1, y) + getflag(img, x, y - 1) + getflag(img, x - 1,
                                                                                                       y - 1) + getflag(
                img, x + 1, y - 1)
            return total
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            total = getflag(img, x, y - 1) + getflag(img, x, y + 1) + getflag(img, x + 1, y - 1) + getflag(img, x + 1,
                                                                                                           y) + getflag(
                img, x + 1, y + 1)
            return total
        elif x == width - 1:  # 右边非顶点
            total = getflag(img, x, y - 1) + getflag(img, x, y + 1) + getflag(img, x - 1, y - 1) + getflag(img, x - 1,
                                                                                                           y) + getflag(
                img, x - 1, y + 1)
            return total
        else:  # 具备9领域条件的
            total = getflag(img, x - 1, y - 1) + getflag(img, x - 1, y) + getflag(img, x - 1, y + 1) + getflag(img, x,
                                                                                                               y - 1) \
                    + getflag(img, x, y + 1) + getflag(img, x + 1, y - 1) + getflag(img, x + 1, y) + getflag(img, x + 1,
                                                                                                             y + 1)
            return total


# 下载图片
def downloads_pic(pic_path):
    for picname in range(1, 50):
        url = 'http://crm.commchina.net/ValIDAteCode.aspx'
        res = requests.get(url, stream=True)
        with open(pic_path + str(picname) + '.jpg', 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()


def to36(n):
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = []
    while n != 0:
        a.append(loop[n % 36])
        n /= 36
    a.reverse()
    out = ''.join(a)
    return out


# 分割图片
def spiltimg(img):
    # 按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见原理图
    # :param img:
    # :return:
    child_img_list = []
    for index in range(5):
        x = 6 + index * (8 + 1)  # 见原理图
        y = 5
        child_img = img.crop((x, y, x + 9, img.height - 2))
        child_img_list.append(child_img)
    return child_img_list


def toGrey(im):
    imgry = im.convert('L')  # 转化为灰度图
    table = get_bin_table()
    out = imgry.point(table, '1')
    return out


def greyimg(image):
    width = image.width
    height = image.height
    box = (0, 0, width, height)
    imgnew = image.crop(box)
    for i in range(0, height):
        for j in range(0, width):
            num = sum_9_region(image, j, i)
            if num < 2:
                imgnew.putpixel((j, i), 255)  # 设置为白色
            else:
                imgnew.putpixel((j, i), 0)  # 设置为黑色
    return imgnew


def get_feature(img):
    # 获取指定图片的特征值,
    # 1. 按照每排的像素点,高度为12,则有12个维度,然后为8列,总共20个维度
    # :return:一个维度为20（高度）的列表
    width, height = img.size
    pixel_cnt_list = []
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) <= 100:  # 黑色点
                pix_cnt_x += 1
        pixel_cnt_list.append(pix_cnt_x)
    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) <= 100:  # 黑色点
                pix_cnt_y += 1
        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list


# 验证码灰度化并且分割图片
# param 待分割图片入境  分割后图片路径
def begin(pic_path, split_pic_path):
    listdir = os.listdir(pic_path)
    print len(listdir)
    for f in listdir:
        if os.path.isfile(pic_path + f):
            print pic_path + f
            if f.endswith(".jpg"):
                pic = Image.open(pic_path + f)
                pic = toGrey(pic)
                # pic.save(split_pic_path + f)
                pic.save("new_code.jpg")
                pic = Image.open("new_code.jpg")
                newpic = greyimg(pic)
                newpic.save(split_pic_path + f)
                childs = spiltimg(newpic)
                count = 0
                for c in childs:
                    c.save(split_pic_path + f.split(".")[0] + "-" + str(count) + '.jpg')
                    count += 1


def train(filename, merge_pic_path):
    if os.path.exists(filename):
        os.remove(filename)
    result = open(filename, 'a')
    for f in os.listdir(merge_pic_path):
        if f != '.DS_Store' and os.path.isdir(merge_pic_path + f):
            for img in os.listdir(merge_pic_path + f):
                if img.endswith(".jpg"):
                    pic = Image.open(merge_pic_path + f + "/" + img)
                    pixel_cnt_list = get_feature(pic)
                    if ord(f) >= 97:
                        line = str(ord(f)) + " "
                    else:
                        line = f + " "
                    for i in range(1, len(pixel_cnt_list) + 1):
                        line += "%d:%d " % (i, pixel_cnt_list[i - 1])
                    result.write(line + "\n")
    result.close()


def train_new(filename, path_new):
    if os.path.exists(filename):
        os.remove(filename)
    result_new = open(filename, 'a')
    for f in os.listdir(path_new):
        if f != '.DS_Store' and f.endswith(".jpg"):
            pic = Image.open(path_new + f)
            pixel_cnt_list = get_feature(pic)
            # if ord(f) >= 97:
            # 	line = str(ord(f)) + " "
            # else:
            line = "0 "
            for i in range(1, len(pixel_cnt_list) + 1):
                line += "%d:%d " % (i, pixel_cnt_list[i - 1])
            result_new.write(line + "\n")
    result_new.close()


# 模型训练
def train_svm_model(filename):
    y, x = svm_read_problem(base_path + filename)
    model = svm_train(y, x)
    svm_save_model(base_path + "svm_model_file", model)


# 使用测试集测试模型
def svm_model_test(filename):
    yt, xt = svm_read_problem(base_path + '/' + filename)
    model = svm_load_model(base_path + "svm_model_file")
    p_label, p_acc, p_val = svm_predict(yt, xt, model)  # p_label即为识别的结果
    cnt = 0
    results = []
    result = ''
    for item in p_label:  # item:float
        if int(item) >= 97:
            result += chr(int(item))
        else:
            result += str(int(item))
        cnt += 1
        if cnt % 4 == 0:
            results.append(result)
            result = ''
    return results


if __name__ == "__main__":
    print "start..."
    # downloads_pic('pic/')
    begin('pic/', 'done/')

#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys,getopt
import os.path
import time
from itertools import islice

#首先输入文件应该是按时间排好序的，文件的排序工作不应该在统计脚本里执行
#业务基本就是我自己的理解

#函数依据type统计reader输出到writer
def tongji(reader, type, writer):
    limit = 10 if type == '1' else 16 #根据统计类型截取更新时间
    patch = ' 00:00:00' if type == '1' else ':00'
    #初始话bar时间、开盘价、最高价、最低价、收盘价、成交量
    bartime = ''
    baropen = 0
    barupper = 0
    barlower = 0
    barlast = 0
    barvolume = 0
    for line in reader:
        update = line[2][0:limit]
        open = line[6]
        upper = line[9]
        lower = line[8]
        last = line[3]
        volume = line[4]
        if update != bartime:
            if bartime != '':
                bartime = "%s%s" % (bartime, patch)
                writer.writerow([bartime, baropen, barupper, barlower, barlast, barvolume])
            baropen = open
            barupper = upper 
            barlower = lower 
            barlast = last
            barvolume = int(volume)
        else: 
            barupper = upper if upper > barupper else barupper
            barlower = lower if lower < barlower else barlower
            barlast = last
            barvolume += int(volume)
        bartime = update
        
    if bartime != '': 
        bartime = "%s%s" % (bartime, patch)
        writer.writerow([bartime, baropen, barupper, barlower, barlast, barvolume])

try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:l:') #获得输入参数
except getopt.GetoptError:
    print('-l or -f has no parameter')
    exit(0)

optsdict = dict(opts) # 得到参数字典

if '-l' not in optsdict.keys():
    print('lack of -l')
    exit(0)
if '-f' not in optsdict.keys():
    print('lack of -f')
    exit(0)

type = optsdict['-l'] #得到统计类型
if not type in ('1', '2'): #校验统计类型
    print('wrong type') 
    exit(0)

input = optsdict['-f'] #得到输入文件
if not os.path.isfile(input): #校验输入文件
    print("%s not exist" % input)
    exit(0)
filename = os.path.split(input)[1] #得到文件名
path = os.path.split(input)[0] #得到文件路径

newfile = open("%s/%s_%s.csv" % (path, filename.split('.')[0], type), 'w') #打开新文件用于存储统计结果
writer = csv.writer(newfile)
writer.writerow(['bartime', 'baropen', 'barupper', 'barlower', 'barlast', 'barvolume']) #将表头写入新文件
csvfile = open('./600588.csv','r') #打开源文件
reader = csv.reader(islice(csvfile, 1, None)) #去掉源文件表头
tongji(reader, type, writer) #调用tongji函数
csvfile.close() #关闭源文件
newfile.close(); #关闭新文件

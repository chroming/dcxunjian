# -*- coding:gbk -*-
#作者sikx@dcits.com

import re
print("              ******************************************")
print("                       TOP系统巡检填写小助手V1")
print("              ******************************************")
print("                                                           ")

#本程序仅用于获取AIX系统巡检抓包中TOP系统所需填写的信息。
#抓包中需要有命令prtconf,ifconfig,topas,iostat,df -g,errpt,lsvg等

print(" ")
#log = open(name,'r')

def readfile():
    name = raw_input("请输入当前目录下日志文件名(包括扩展名): ")
    try:
        log = open(name,'r')
        logt = log.read()
        log.close()
        return logt
    except:
        print("文件读取失败!请检查后重试！")
        return readfile()
##    finally:
##        if log:
##            log.close()
##    #print logt

logt = readfile()

get_machine_id = re.findall(r'Machine Serial Number\:\ (\w{5,10})',logt,re.S)
try:
    if get_machine_id[0] == get_machine_id[1]:
        machine_id = get_machine_id[0]
    else:
        machine_id = get_machine_id
except:
    try:
        machine_id = get_machine_id[0]
    except:
        machine_id = None

get_ip = re.findall(r'ifconfig.*?inet\ ((?:\d{1,3}\.){3}\d{1,3})',logt,re.S)

#get_topas = re.match(r'topas.*?Kernel.*?Idle\ {4,6}(\d{1,3}\.{0,1}\d{0,1}).*?MEMORY.*?Comp\ {4,7}(\d{1,3}\.{0,1}\d{0,1})PAGING\ SPACE.*?Used\ {4,7}(\d{1,3}\.{0,1}\d{0,1})',logt,re.S)
#print get_topas
#get_CPU = get_topas[0]
#get_memory = get_topas[1]
#get_pagingspace = get_topas[2]

get_rootvg = re.findall(r'lsvg \-l rootvg(.*?)\#',logt,re.S)[0]

get_rootnum = re.findall(r' {2,20}(\d{1,5}) {2,20}(\d{1,5}) {2,20}(\d{1,5})',get_rootvg,re.S)
x = 0
y = 0
for ii in get_rootnum:
    if int(ii[1]) == 2*int(ii[0]):
        x = x + 1
    else:
        if int(ii[1]) == int(ii[0]):
            y = y + 1
if x > y:
    rootvgmi = "是"
else:
    if x==0 and y==0:
        rootvgmi = "获取失败"
    else:
        rootvgmi = "否"

get_stale = re.findall(r'lsvg -o\s*(.*?)#',logt,re.S)
if get_stale == []:
    stale = "否"
else:
    stale = "是"

get_cpu= re.findall(r'topas.*?Kernel\ {4,10}\d.*?Idle\ {4,10}([1-9]\S*)',logt,re.S)[0]
cpu = 100 - float(get_cpu)

get_memory = re.findall(r'topas.*?MEMORY.*?Comp\ {4,10}(\d\S*)',logt,re.S)[0]
#print get_memory

get_pagingspace = re.findall(r'topas.*?PAGING\ SPACE.*?Used\ {4,10}(\d\S*)',logt,re.S)[0]
#print get_pagingspace

#get_iostat = re.findall(r'iostat.*?idle.*?((?:\d{1,3}\.{0,1}\d{0,1}\ {1,20}){6})',logt,re.S)[0]
get_iostat = re.findall(r'iostat.*?tty.*?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)',logt,re.S)[0]
#print get_iostat
iostat = 100 - float(get_iostat[4])

try:
    get_errpt = re.findall(r'errpt.*?DESCRIPTION(.*?)\#',logt,re.S)[0]
except:
    get_errpt = None

#get_df = re.findall(r'sort.*?(\d{1,3}%)',logt,re.S)[0]
#get_df = re.findall(r'sort\ \-rn\ \+3(.*?)\#',logt,re.S)[0]
get_df = re.findall(r'(df -.*?)\#',logt,re.S)[0] 
print(" ")
print(" ")
print("本机IP是：%s"%get_ip)
print("本机序列号是：%s"%machine_id)
print("********************************************")
print("本机是否有操作系统镜像： %s"%rootvgmi)
print("本机是否有stale状态逻辑卷： %s"%stale)
print("********************************************")
print("本机CPU使用： %s"%cpu)
print("本机IO使用： %s"%iostat)
print("本机内存使用： %s"%get_memory)
print("本机PAGING SPACE： %s"%get_pagingspace)
print("********************************************")
print("本机空间占用： %s"%get_df)
print("********************************************")
print("本机报错： %s"%get_errpt)

raw_input("按Enter退出")



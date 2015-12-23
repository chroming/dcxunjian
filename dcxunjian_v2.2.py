# -*- coding:utf-8 -*-
#作者sikx@dcits.com
#v2版改进：
#已完成：对无法获取数据数据提示获取失败；修改错误的stale计算方式；修改只能获取第一条ip的问题
#仍需改进：topas没有时需要其他命令代替；多次返回结果应使用平均值计算；

import re
print("              ******************************************")
print("                       TOP系统巡检填写小助手V2.2")
print("              ******************************************")
print("                                                           ")

#本程序仅用于获取AIX系统巡检抓包中TOP系统所需填写的信息。
#抓包中需要有命令prtconf,ifconfig,topas,iostat,df -g,errpt,lsvg等

print(" ")
#log = open(name,'r')

#获取信息通用函数
def check_func(zz):
    get_data = re.findall(r'%s'%zz,logt,re.S)
    try:
        get_data[0]
        return get_data
    except:
        return ('获取失败！')

#读取文件
def readfile():
    name = raw_input("请输入当前目录下日志文件名(包括扩展名): ")
    try:
        log = open('/tmp/%s'%name,'r')
        logt = log.read()
        log.close()
        return logt
    except:
        print("文件读取失败!请检查后重试！")
        return readfile()




def get_func(logt):
    #获取序列号
    get_machine_id = check_func('Machine Serial Number\:\ (\w{5,10})')
    try:
        if get_machine_id[0] == get_machine_id[1]:
            machine_id = get_machine_id[0]
        else:
            machine_id = get_machine_id
    except:
        try:
            machine_id = get_machine_id[0]
        except:
            machine_id = '获取失败！'

    #获取IP
    get_ip = check_func('inet\ ((?:\d{1,3}\.){3}\d{1,3})')

    #查看rootvg镜像状态
    get_rootvg = check_func('lsvg \-l rootvg(.*?)\#')[0]
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

    #判断本机是否有stale状态逻辑卷
    get_stale = check_func('STALE\ PVs\:\s*(\d)')[0]
    if int(get_stale) == 0:
        stale = "正常"
    else:
        stale = "异常"

    #判断是否有TOPAS
    try:
        get_topas = re.findall(r'(topas\: *not)',logt)[0]
        cpu = get_memory = get_pagingspace = "获取失败！"
    #如果有获取以下信息
    except:
        try:

            get_cpu= check_func('topas.*?Kernel\ {4,10}\d.*?Idle\ {4,10}([1-9]\S*)',logt)[0]
            cpu = 100 - float(get_cpu)

            get_memory = check_func('topas.*?MEMORY.*?Comp\ {4,10}(\d\S*)',logt)[0]

            get_pagingspace = check_func('topas.*?PAGING\ SPACE.*?Used\ {4,10}(\d\S*)',logt)[0]
        except:
            cpu = get_memory = get_pagingspace = "获取失败！"

    # except:
    #
    #     get_cpu= check_func('topas.*?Kernel\ {4,10}\d.*?Idle\ {4,10}([1-9]\S*)')[0]
    #     cpu = 100 - float(get_cpu)
    #
    #     get_memory = check_func('topas.*?MEMORY.*?Comp\ {4,10}(\d\S*)')[0]
    #
    #     get_pagingspace = check_func('topas.*?PAGING\ SPACE.*?Used\ {4,10}(\d\S*)')[0]

    get_iostat = check_func('iostat.*?tty.*?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)')[0]

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
    Choicenum =raw_input('输入1继续程序，输入其他退出，请输入代码： ')
    if Choicenum == str(1):
        logt = readfile()
        get_func(logt)

logt = readfile()
get_func(logt)

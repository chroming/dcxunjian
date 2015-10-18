# -*- coding:gbk -*-
#����sikx@dcits.com
#v2��Ľ���
#����ɣ����޷���ȡ����������ʾ��ȡʧ�ܣ��޸Ĵ����stale���㷽ʽ���޸�ֻ�ܻ�ȡ��һ��ip������
#����Ľ���topasû��ʱ��Ҫ����������棻��η��ؽ��Ӧʹ��ƽ��ֵ���㣻

import re
print("              ******************************************")
print("                       TOPϵͳѲ����дС����V2.2")
print("              ******************************************")
print("                                                           ")

#����������ڻ�ȡAIXϵͳѲ��ץ����TOPϵͳ������д����Ϣ��
#Ӧ����ֱ�ӻ�ȡ�����ļ�����������־����
#ץ������Ҫ������prtconf,ifconfig,topas,iostat,df -g,errpt,lsvg��

print(" ")
#log = open(name,'r')

#��ȡ��Ϣͨ�ú���
def check_func(zz,logt):
    get_data = re.findall(r'%s'%zz,logt,re.S)
    if get_data == []:
        return('��ȡʧ�ܣ�')
    else:
        return get_data
 

#��ȡ�ļ�
def readfile():
    name = raw_input("�����뵱ǰĿ¼����־�ļ���(������չ��): ")
    try:
        log = open('%s'%name,'r')
        logt = log.read()
        log.close()
        return logt
    except:
        print("�ļ���ȡʧ��!��������ԣ�")
        return readfile()




def get_func(logt):
    #��ȡ���к�
    get_machine_id = check_func('Machine Serial Number\:\ (\w{5,10})',logt)
    try:
        if get_machine_id[0] == get_machine_id[1]:
            machine_id = get_machine_id[0]
        else:
            machine_id = get_machine_id
    except:
        try:
            machine_id = get_machine_id[0]
        except:
            machine_id = '��ȡʧ�ܣ�'

    #��ȡIP
    get_ip = check_func('inet\ ((?:\d{1,3}\.){3}\d{1,3})',logt)

    #�鿴rootvg����״̬
    get_rootvg = check_func('lsvg \-l rootvg(.*?)\#',logt)[0]
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
        rootvgmi = "��"
    else:
        if x==0 and y==0:
            rootvgmi = "��ȡʧ��"
        else:
            rootvgmi = "��"

    #�жϱ����Ƿ���stale״̬�߼���
    get_stale = check_func('STALE\ PVs\:\s*(\d)',logt)[0]
    if int(get_stale) == 0:
        stale = "����"
    else:
        stale = "�쳣"

    #�ж��Ƿ���TOPAS
    try:
        get_topas = re.findall(r'(topas\: *not)',logt)[0]
        cpu = get_memory = get_pagingspace = "��ȡʧ�ܣ�"
    #����л�ȡ������Ϣ
    except:
        try:

            get_cpu= check_func('topas.*?Kernel\ {4,10}\d.*?Idle\ {4,10}([1-9]\S*)',logt)[0]
            cpu = 100 - float(get_cpu)

            get_memory = check_func('topas.*?MEMORY.*?Comp\ {4,10}(\d\S*)',logt)[0]

            get_pagingspace = check_func('topas.*?PAGING\ SPACE.*?Used\ {4,10}(\d\S*)',logt)[0]
        except:
            cpu = get_memory = get_pagingspace = "��ȡʧ�ܣ�"

    get_iostat = check_func('iostat.*?tty.*?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)\ *?(\d\S*)',logt)[0]
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
    print("����IP�ǣ�%s"%get_ip)
    print("�������к��ǣ�%s"%machine_id)
    print("********************************************")
    print("�����Ƿ��в���ϵͳ���� %s"%rootvgmi)
    print("�����Ƿ���stale״̬�߼��� %s"%stale)
    print("********************************************")
    print("����CPUʹ�ã� %s"%cpu)
    print("����IOʹ�ã� %s"%iostat)
    print("�����ڴ�ʹ�ã� %s"%get_memory)
    print("����PAGING SPACE�� %s"%get_pagingspace)
    print("********************************************")
    print("�����ռ�ռ�ã� %s"%get_df)
    print("********************************************")
    #raw_input('��Enter����ʾerrpt����')
    print("�������� %s"%get_errpt)
    Choicenum =int(raw_input('����1�����������������˳�����������룺 '))
    if Choicenum == 1:
        logt = readfile()
        get_func(logt)

        
logt = readfile()
get_func(logt)

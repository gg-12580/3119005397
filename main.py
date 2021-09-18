# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 00:25:53 2020

@author: hp
"""

# _*_ coding:utf-8 _*_
"""
Created on Mon Sep 21 17:16:17 2020

@author: hp
"""


"""
本代码主要使用Levenshtein距离算法实现文章查重功能，以下是对算法的简介：
Levenshtein距离又称作编辑距离（Edit Distance），是指两个字符之间，有一个转变成另一个所需的最少编辑操作次数
通过编辑距离来判断两个字符串是否相等以及所需步长，动态规划算法得出相应查重率
"""
import Levenshtein
import time
import re
import sys

def main():
    #开始测量程序所需时间
    start_time = time.time()

    try:
        orig_path, add_path, answer_path= sys.argv[1:4]
    except BaseException:
        print("Error: 输入命令错误")
    else:
        # 判断命令行参数有没有错误
        try:
            orig = open(orig_path,'r',encoding='UTF-8')
            orig_context = orig.read()   
        except IOError:
            print("Error: 没有从该路径：{}找到文件/读取文件失败".format(orig_path))
            conditio_one=0
        else:
            conditio_one=1
            orig.close()

        # 判断抄袭文件路径等是否出错
        try:
            orig_add = open(add_path,'r',encoding='UTF-8')
            add_context = orig_add.read()  
        except IOError:
            print("Error: 没有从该路径：{}找到文件/读取文件失败".format(add_path))
            conditio_two=0
        else:
            conditio_two=1
            orig_add.close()

        # 判断答案文件路径等是否出错
        try:
            answer_txt=open(answer_path,'w',encoding='UTF-8')
        except BaseException:
            print("Error: 创建文件：{}失败".format(answer_path))
            conditio_three=0
        else:
            conditio_three=1
      
            
        # 如果输入命令行参数没有错误则运行
        if(conditio_one&conditio_two&conditio_three):
            final_orig = remove_symbol(orig_context)  # 调用remove_symbol函数除去影响
            final_add = remove_symbol(add_context)
            ratio = Levenshtein.ratio(final_orig, final_add)  #利用Levenshtein包里的函数算出相似度
            dist = Levenshtein.distance(final_orig, final_add) #利用Levenshtein包里的函数算出转换所需步长

            # 得知程序运行所需时间
            end_time = time.time()
            time_required=end_time - start_time

            #控制台输出，方便得知状态和答案
            print('查重率：%.2f' %ratio)
            print("输出文件到:"+answer_path)
            print ('程序所耗时间：%.2f s'%(time_required))

            #写入答案文件
            answer_txt.write("源文件:"+orig_path+'\n')
            answer_txt.write("抄袭文件:"+add_path+'\n')
            answer_txt.write('转换所需步长：'+str(dist)+'\n')
            answer_txt.write('查重率：%.2f' %ratio+'\n')
            answer_txt.write('程序所耗时间：%.2f s'%(time_required)+'\n')
            answer_txt.close()

def remove_symbol(context): # 利用正则除去标点符号等等的影响
    remove_rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  #只保留数字，大小写字母以及中文
    result = remove_rule.sub('', context)
    return result 

if __name__ == '__main__':
    main()
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
reload(sys)
def foo():
    str="function"
    print(str);

def foo1(num):
    print('num' ,num);

def foo2(name ,age):
    print('name' ,name);
    print('age' ,age);

if __name__=="__main__":
    # print("main")
    # foo2('yuhui' ,30)
    # foo1(6)
    # foo()

    # str='Runoob'
#
# print(str)                 # 输出字符串
# print(str[0:-1])           # 输出第一个到倒数第二个的所有字符
# print(str[0])              # 输出字符串第一个字符
# print(str[2:5])            # 输出从第三个开始到第五个的字符
# print(str[2:])             # 输出从第三个开始的后的所有字符
# print(str * 2)             # 输出字符串两次
# print(str + '你好')        # 连接字符串
#
# print('------------------------------')
#
# print('hello\nrunoob')      # 使用反斜杠(\)+n转义特殊字符
# print(r'hello\nrunoob')     # 在字符串前面添加一个 r，表示原始字符串，不会发生转义
# x="a"
# y="b"
# # 换行输出
# print( x )
# print( y )
#
# print('---------')
# # 不换行输出
# print( x, end=" " )
# print( y, end=" " )
# print()
# from sys import argv,path  #  导入特定的成员
#
# print('================python from import===================================')
# print('path:',path) # 因为已经导入path成员，所以此处引用时不需要加sys.path
    list=[1,2,3,4]
    it = iter(list)    # 创建迭代器对象
    for x in it:
        print (x, end=",")
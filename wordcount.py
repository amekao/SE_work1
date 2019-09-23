# /usr/bin/python3
# -*- coding: utf-8 -*-
# author: Wu Zihao
# time: 2019/9/16
# function:

import sys
import re
import os
from fnmatch import fnmatch
import win32ui


def char_count(o_f):
    """
    计算总字符数
    :param o_f: 输入已open的文件
    :return:返回总字符数
    """
    o_f.seek(0)
    content = o_f.read()
    char_num = len(content)

    return char_num


def complex_char_count(o_f):
    """
    计算详细字符数
    :param o_f: 输入已open的文件
    :return:返回数码数，字母数，空格数，换行符数，制表符数，标点数
    """
    digit_num = 0
    alpha_num = 0
    other_num = 0

    o_f.seek(0)
    content = o_f.read()

    for char in content:
        if char.isdigit():  # 数字计数
            digit_num += 1
        elif char.isalpha():  # 字母计数
            alpha_num += 1
        else:
            other_num += 1  # 标点，空格，制表换行符
    space_num = content.count(' ')  # 空格
    newline_num = content.count('\n')  # 换行符
    tab_num = content.count('\t')  # 制表符
    dot_num = other_num - space_num - newline_num - tab_num  # 标点符号

    return digit_num, alpha_num, space_num, newline_num, tab_num, dot_num


def line_count(o_f):
    """
    计算总行数
    :param o_f:输入已open的文件
    :return: 返回总行数
    """
    o_f.seek(0)
    line_num = len(o_f.readlines())
    return line_num


def complex_line_count(o_f):
    """
    计算复杂行数（/**/的注释无法识别）
    :param o_f: 输入已open的文件
    :return: 返回注释行数，空白行数，代码行数
    """
    o_f.seek(0)
    content = o_f.readlines()

    anno_line = 0
    void_line = 0
    code_line = 0

    for line in content:
        line = line.strip()  # 去掉首尾空白
        if line.startswith('//') or line.startswith('{//') or line.startswith('}//'):
            anno_line += 1  # 注释行
        elif len(line) == 1 or line.startswith('{') or line.startswith('}'):
            void_line += 1  # 空白行
        else:
            code_line += 1  # 其余均归为代码行

    return anno_line, void_line, code_line


def word_count(o_f):
    """
    计算单词数
    :param o_f:输入已open的文件
    :return: 返回单词数
    """
    o_f.seek(0)
    content = o_f.read()
    words = re.split(r'[^a-zA-Z]+', content)
    while '' in words:
        words.remove('')  # 去掉无用的''
    # print(words)
    word_num = len(words)
    return word_num


def traverse_file(f_p, f_n):
    """
    递归遍历指定路径指定后缀的文件
    :param f_p: 指定路径 或 待比较的路径+名字
    :param f_n: 指定后缀(如 '*.c')
    :return: 以全局变量的形式返回文件列表
    """
    # 全局变量dicList，存放py文件名
    global dicList

    # 当前目录下的文件列表

    file_list = os.listdir(f_p)

    for file in file_list:  # 以列表的形式返回该目录下的所有文件
        newpath = os.path.join(f_p, file)  # 将每一个文件拼接成绝对路径

        # 判断是否为目录
        if os.path.isdir(newpath) is True:
            traverse_file(newpath, f_n)  # 若为目录则递归
        # 判断是否为文件
        elif os.path.isfile(newpath) is True:
            if fnmatch(newpath, f_n):   # 如果是文件则判断是否为相应后缀文件
                dicList.append(newpath)


def output(f_i):
    """
    依据cblaw五个标志位输出对应信息
    :param f_i: 输入文件路径和名字
    :return: 打印出对应信息
    """
    try:
        open_file = open(f_i, "r")  # 先以GBK打开，测试读一下看是否乱码
        test_read = open_file.read()
        open_file.seek(0)
    except FileNotFoundError:
        print("找不到该文件")
        sys.exit()
    except UnicodeDecodeError:
        open_file = open(f_i, "r", encoding='UTF-8') # 若乱码，则重新以UTF-8打开
    except:
        print("文件打开失败，请重新运行程序")
        sys.exit()
    print(f_i)
    if c_mode is True:
        print(f'字数: {char_count(open_file)}')
    if b_mode is True:
        c_list = complex_char_count(open_file)
        print(f'数字: {c_list[0]}  字母: {c_list[1]}  空格：{c_list[2]}  '
              f'换行符: {c_list[3]}  制表符: {c_list[4]}  标点：{c_list[5]}')
    if l_mode is True:
        print(f'行数: {line_count(open_file)}')
    if a_mode is True:
        l_list = complex_line_count(open_file)
        print(f'注释行: {l_list[0]}  空白行: {l_list[1]}  代码行: {l_list[2]}')
    if w_mode is True:
        print(f'词数: {word_count(open_file)}')

    open_file.close()


if __name__ == '__main__':
    print('''
**************************************************************
***            功能:对输入的文本文件进行字符计数           ***
**************************************************************
--------------------------------------------------------------
普通参数： -c -w -l -b -a 可随意组合叠加使用
    -c  返回文件字符数
    -w  返回文件词数
    -l  返回文件行数
    -b  返回文件详细字符数（数字/字母/空格/换行符/制表符/标点）
    -a  返回文件详细行数（代码行/空行/注释行）  
特殊参数：-s -x
    -s  寻找指定路径下所有符合通配符的文件并计算
    -x  弹出文件选择窗口，-c -w -l -b -a五种统计信息全显示
--------------------------------------------------------------
用法示例：
    wc.exe -w -b -a file.py  
    返回文件file.py的词数，详细字符数，详细行数
    wc.exe -s -a /dir/*.c
    返回在路径dir下所有后缀为c的文件的详细行数
    wc.exe -x
    弹出窗口直接选择
--------------------------------------------------------------
版本：--v2.0  2019-9-23 22:26:59
作者：Wu Zihao  3117004671
--------------------------------------------------------------
            ''')
    # 赋初值
    c_mode, w_mode, l_mode, a_mode, b_mode = False, False, False, False, False
    s_mode = False
    file_info = ''
    file_name = '*.c'  # 默认为c文件
    file_path = os.getcwd()  # 默认为当前路径下

    dicList = []  # 存放遍历后文件列表

    if len(sys.argv) == 1:
        print("请参照上面的说明,使用正确的参数重新运行程序")
        sys.exit()

    sys.argv.pop(0)  # 去掉列表中0号单元

    if '-x' in sys.argv:
        dlg = win32ui.CreateFileDialog(1)  # 参数1表示打开文件对话框
        dlg.DoModal()
        file_info = dlg.GetPathName()  # 获取选择的文件名称

        c_mode, w_mode, l_mode, a_mode, b_mode = True, True, True, True, True
        output(file_info)
    else:
        if '-s' in sys.argv:
            s_mode = True
            sys.argv.remove('-s')
        if '-c' in sys.argv:
            c_mode = True
            sys.argv.remove('-c')
        if '-w' in sys.argv:
            w_mode = True
            sys.argv.remove('-w')
        if '-l' in sys.argv:
            l_mode = True
            sys.argv.remove('-l')
        if '-a' in sys.argv:
            a_mode = True
            sys.argv.remove('-a')
        if '-b' in sys.argv:
            b_mode = True
            sys.argv.remove('-b')

        # 在argv中获取用户想输入的路径和名字
        if len(sys.argv) != 0:
            file_info = sys.argv.pop(0)  # 如果用户没输入路径+名字，则使用默认的
        if len(os.path.basename(file_info)) != 0:
            file_name = os.path.basename(file_info)  # 非空则赋上文件名字
        if len(os.path.abspath(os.path.dirname(file_info))) != 0:
            file_path = os.path.abspath(os.path.dirname(file_info))  # 非空则附上文件绝对路径

        if len(sys.argv) > 0:
            print("异常：参数输入错误！")
            sys.exit()

        if s_mode is True:  # s_mode相当于批量操作了
            traverse_file(file_path, file_name)
            print(f'在{file_path}路径下遍历到{len(dicList)}个文件：')
            for file in dicList:
                print(f'{dicList.index(file)+1}. ', end='')  # 输出序号
                output(file)

        else:  # 发现使用通配操作可以让用户体验更好，所以这里也是使用fnmatch进行匹配
            file_name = '*'+ file_name # 遍历时要fnmatch，而file_path会不断加路径，给filename前面加上通配符*
            traverse_file(file_path, file_name)
            if len(dicList) == 0:
                print("提示：找不到符合名称的文件，程序退出！")
                sys.exit()
            else:
                for file in dicList:
                    output(file)

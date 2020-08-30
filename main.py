#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transform Arab number of base 10 format to Simple Chinese way. By @xiaobit
0. number range ±e17, '十万兆', extremes not inclusive, can expand if need.
1. transform '± 2020.0' as '正负二千零二十点零'
2. not support scientific format, like 1.0e-1
3. ON/OFF insignificant figures

More exampls, if `digit[0]` is '零':
' ± -000.000100'            >> 正负零零零点零零零一零零
'10101010101'               >> 一百零一亿零一百零一万零一百零一
'-10080038703101.0'         >> 负十兆零八百亿零三千八百七十万三千一百零一点零
'-12970000000001001.1'      >> 负一万二千九百七十兆零一千零一点一
‘99999999999999999’         >> 九万九千九百九十九兆九千九百九十九亿九千九百九十九万九千九百九十九
"""

import sys
import re


digit = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
unit = ["", "十", "百", "千", "万", "亿", "兆"]  # 兆=10^12
unit_minor = ["十", "百", "千", "万"]  # "万" only apply for "兆"
decimal_dot = '点'
sign_positive = '正'
sign_negative = '负'
plus_minus = '正负'


def int2zh(num):
    """num is string,
    either the integer part of a float or just an integer itself
    return the counterpart string of its Chinese version.
    """
    if num == '':
        return ''
    if float(num) == 0:
        return digit[0]

    digit_count = 0
    s = ''
    p0 = [0]  # if "万", "亿", "兆" is ZERO, record digit_count position

    num_list = list(num)
    while len(num_list) > 0:
        d = int(num_list.pop())
        if (d % 10) > 0:
            if (digit_count <= 4):
                s += f"{unit[digit_count]}{digit[d % 10]}"
            elif digit_count in range(5, 8):
                if re.search(unit[4], s) is None:
                    s += unit[4]
                s += f"{unit_minor[digit_count - 5]}{digit[d % 10]}"

            elif (digit_count == 8):
                s += f"{unit[5]}{digit[d % 10]}"
            elif digit_count in range(9, 12):
                if re.search(unit[5], s) is None:
                    s += unit[5]
                s += f"{unit_minor[digit_count - 9]}{digit[d % 10]}"

            elif (digit_count == 12):
                s += f"{unit[6]}{digit[d % 10]}"
            elif digit_count in range(13, 17):
                if re.search(unit[6], s) is None:
                    s += unit[6]
                s += f"{unit_minor[digit_count - 13]}{digit[d % 10]}"
            else:
                raise ValueError('Overflow!')

        else:
            # When to add digit ZERO is tricky!
            if len(s) > 0:
                if s[-1] != digit[0]:
                    if digit_count in [4, 8, 12]:
                        p0.append(digit_count)
                    else:
                        s += digit[0]

        digit_count += 1
    # print('List special ZERO positions: ', p0)
    return re.sub("^一十", '十', s[::-1])


def getzeros(num):
    """get leading zeros for a number string `num`.
    return a tuple `(leadingzeros, otherdigits)`
    """
    leadingzeros = ''
    otherdigits = ''
    for i in range(len(num)):
        if num[i] != '0':
            otherdigits = num[i:]
            break
        leadingzeros += num[i]
    return leadingzeros, otherdigits


def getsign(num):
    """input the raw num string, return a tuple (sign_num, num_abs).
    """
    sign_num = ''
    if num.startswith('±'):
        sign_num = plus_minus
        num_abs = num.lstrip('±+-')
    else:
        try:
            temp = float(num)
            if (temp < 0) and (sign_num == ''):
                sign_num = sign_negative
            elif (temp > 0) and (sign_num == ''):
                if ('+' in num):
                    sign_num = sign_positive
            else:
                if num.startswith('-'):
                    sign_num = sign_negative
                if num.startswith('+'):
                    sign_num = sign_positive
            num_abs = num.lstrip('+-')
        except ValueError:
            raise
    return sign_num, num_abs


def num2zh(num, sep='', significant=False):
    """main function. Default separators `sep` of digits is None.
    Set `significant` as True to exclude insignificant figures.
    """
    sign_num = ''

    if sep:
        num = ''.join(num.split(sep))
    num = re.sub('\s+', '', num)  # reassure no space

    sign_num, num = getsign(num)

    if '.' in num:
        integers, remainders = num.split('.')
        if integers.isdigit():
            leadingzeros, otherdigits = getzeros(integers)
            if insignificant:
                str_int = len(leadingzeros)*digit[0] + int2zh(otherdigits)
            else:
                str_int = int2zh(integers)
        else:
            str_int = ''

        str_remainder = ''.join([digit[int(x)] for x in remainders])
        return sign_num + str_int + decimal_dot + str_remainder
    else:
        if num.isdigit():
            leadingzeros, otherdigits = getzeros(num)
            if insignificant:
                return sign_num+ len(leadingzeros)*digit[0] + int2zh(otherdigits)
            else:
                return sign_num + int2zh(num)
        else:
            print('Thank you!')


if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            break
        print(num2zh(line.strip()))

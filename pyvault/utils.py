#-*- coding: utf-8 -*-

def constant_time_compare(s1, s2):
    if len(s1) != len(s2):
        return False

    result = 0
    for x, y in zip(s1, s2):
        result |= ord(x) ^ ord(y)
    return result == 0

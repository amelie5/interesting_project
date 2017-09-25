# -*- coding: utf-8 -*-

__author__ = 'amelie'

def transfer(a_list,b_list):
    ret_list = list((set(a_list).union(set(b_list))) ^ (set(a_list) ^ set(b_list)))
    print(ret_list)
    return len(ret_list)


a_list = [4,2,3,1]
b_list = [1,4,5]
print(transfer(a_list,b_list))

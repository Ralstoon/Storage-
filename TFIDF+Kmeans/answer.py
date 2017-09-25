# coding=utf-8
import os
import sys
import codecs

from numpy import unicode



# 功能:合并实体名称和聚类结果 共类簇2类


# source1 = open("BH_EntityName.txt", 'r')
# source2 = open("Cluster_Result.txt", 'r')


#########################################################################
#                        第一部分 合并实体名称和类簇

# lable = []  # 存储408个类标 20个类
# content = []  # 存储408个实体名称
# name = source1.readline()
# # 总是多输出空格 故设置0 1使其输出一致
# num = 1
# while name != "":
#     name = unicode(name.strip('\r\n'), "utf-8")
#     if num == 1:
#         res = source2.readline()
#         res = res.strip('\r\n') #strip(s) 方法用于移除字符串头尾指定的字符(默认为空格)
#
#         value = res.split(' ')
#         no = int(value[0]) - 1  # 行号
#         va = int(value[1])  # 值
#         lable.append(va)
#         content.append(name)
#
#         print(name, res)
#         result1.write(name + ' ' + res + '\r\n')
#         num = 0
#     elif num == 0:
#         num = 1
#     name = source1.readline()
#
# else:
#     print('OK')
#     source1.close()
#     source2.close()
#     result1.close()
#
# # 测试输出 其中实体名称和类标一一对应
# i = 0
# while i < len(lable):
#     print(content[i], (i + 1), lable[i])
#     i = i + 1

#########################################################################
#                      第二部分 合并类簇 类1 ..... 类2 .....

def Merge_show(names,clf_labels):
    # 定义定长20字符串数组 对应20个类簇
    output = [''] * 20
    result2 = codecs.open("ZBH_Cluster_Merge.txt", 'w', 'utf-8')

    # 统计类标对应的实体名称
    i = 0
    while i < len(clf_labels):
        output[clf_labels[i]] += names[i] + ' '
        i = i + 1

    # 输出
    i = 0
    while i < 20:
        # print('#######')
        result2.write('#######\r\n')
        # print('Label: ' + str(i))
        result2.write('Cluster: ' + str(i) + '\r\n')
        # print(output[i])
        result2.write(output[i] + '\r\n')
        i = i + 1

    result2.close()
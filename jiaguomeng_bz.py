# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:50:13 2019

@author: sqr_p
"""

import numpy as np
from tqdm import tqdm
import itertools
from queue import PriorityQueue as PQ
from scipy.special import comb

buffs_100 = {
    '木屋': ['木材厂'],
    '居民楼': ['便利店'],
    '钢结构房': ['钢铁厂'],
    '花园洋房': ['商贸中心'],
    '空中别墅': ['民食斋'],

    '便利店': ['居民楼'],
    '五金店': ['零件厂'],
    '服装店': ['纺织厂'],
    '菜市场': ['食品厂'],
    '学校': ['图书城'],
    '图书城': ['学校', '造纸厂'],
    '商贸中心': ['花园洋房'],
    '加油站': ['人民石油'],

    '木材厂': ['木屋'],
    '食品厂': ['菜市场'],
    '造纸厂': ['图书城'],
    '钢铁厂': ['钢结构房'],
    '纺织厂': ['服装店'],
    '零件厂': ['五金店'],
    '企鹅机械': ['零件厂'],
    '人民石油': ['加油站']
}

buffs_50 = {'零件厂': ['企鹅机械']}

buffs_com = {'人才公寓': [.2, .4, .6],
             '中式小楼': [.2, .4, .6],
             '空中别墅': [.2, .4, .6],
             '民食斋': [.2, .4, .6],
             '媒体之声': [.05, .1, .15],
             '电厂': [.2, .4, .6],
             '平房': [.2, .4, .6],
             '企鹅机械': [.1, .2, .3]}
buffs_ind = {'人才公寓': [.2, .4, .6],
             '中式小楼': [.2, .4, .6],
             '空中别墅': [.2, .4, .6],
             '民食斋': [.2, .4, .6],
             '媒体之声': [.05, .1, .15],
             '电厂': [.2, .4, .6],
             '企鹅机械': [.1, .2, .3]}
buffs_res = {'人才公寓': [.2, .4, .6],
             '中式小楼': [.2, .4, .6],
             '空中别墅': [.2, .4, .6],
             '民食斋': [.2, .4, .6],
             '媒体之声': [.05, .1, .15],
             '电厂': [.2, .4, .6],
             '纺织厂': [.15, .3, .5],
             '企鹅机械': [.1, .2, .3]
             }
#

# TODO !!!

residence = '木屋 居民楼 钢结构房 平房'.split()
commercial = '便利店 五金店 服装店 菜市场 学校 图书城 民食斋'.split()
industry = '木材厂 食品厂 造纸厂 电厂 钢铁厂 纺织厂 零件厂'.split()

OneStars = '电厂 钢铁厂 零件厂 民食斋 木屋'.split()
TwoStars = '纺织厂 平房 便利店 服装店 图书城 菜市场 学校 木材厂 造纸厂'.split()
TriStars = '居民楼 食品厂 钢结构房 五金店'.split()

star = dict()
for item in OneStars:
    star[item] = 1
for item in TwoStars:
    star[item] = 2
for item in TriStars:
    star[item] = 3

startDict = {1: 1, 2: 2, 3: 6, 4: 24}

######星级 * 照片 * 政策 * 任务
'''
 我这里的照片加成是全体40%+在线40%+住宅150%+商业150%+工业60%
 所以住宅和商业建筑的照片加成系数为 1+0.4+0.4+1.5=3.3
 工业建筑的照片加成系数为 1+0.4+0.4+0.6=2.4

 我的政策加成为 全体100% + 商业300% + 住宅300% + 工业150%
 加上家国之光的10%加成
 政策加成系数为 商业住宅 1+1+3+.1 = 5.1
             工业     1+1+1.5+.1 = 3.6

 最后在住宅上乘上和谐家园的任务加成 1.3
'''
# TODO: 自动计算

# TODO !!!
start = dict()
for item in commercial:  # 商业
    start[item] = startDict[star[item]] * (0.2 + 0.3 + 1 + 1 + 3 + 0.2 + 0.05 + 0.05) * 1.1
for item in industry:  # 工业
    start[item] = startDict[star[item]] * (1 + 0.2 + 1 + 0.2 + 0.05 + 0.05) * 1.7
for item in residence:  # 住宅
    start[item] = startDict[star[item]] * (1 + 1 + 3 + 0.2 + 0.4 + 0.05 + 0.05) * 1.1

# 收益调整
start['平房'] *= 1.1
start['民食斋'] *= 1.52

# 任务加成调整!!!!!
# TODO !!!
# start['加油站'] *= 2
start['服装店'] *= 2
start['五金店'] *= 2.5


# start['小型公寓'] *= 2


def calculateComb(buildings):
    buildtuple = buildings[0] + buildings[1] + buildings[2]
    starts = [start[x] for x in buildtuple]
    results = [1] * 9
    for item in buildtuple:
        if item in buffs_100:
            for buffed in buffs_100[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]
        if item in buffs_50:
            for buffed in buffs_100[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item] * 0.5
        if item in buffs_com:
            results[0:3] = np.add(results[0:3], buffs_com[item][star[item] - 1])
        if item in buffs_ind:
            results[3:6] = np.add(results[3:6], buffs_ind[item][star[item] - 1])
        if item in buffs_res:
            results[6:9] = np.add(results[6:9], buffs_res[item][star[item] - 1])
    return (np.sum([v * results[i] for i, v in enumerate(starts)]),
            [v * results[i] / startDict[star[buildtuple[i]]] for i, v in enumerate(starts)])


#
results = PQ()


#
class Result(object):
    def __init__(self, priority, builds):
        self.priority = priority
        self.builds = builds
        return

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority


print('Total iterations:', comb(len(commercial), 3) * comb(len(industry), 3) * comb(len(residence), 3))

for item in tqdm(itertools.product(itertools.combinations(commercial, 3), itertools.combinations(industry, 3),
                                   itertools.combinations(residence, 3))):
    prod = calculateComb(item)
    #    if prod > Max:
    #        print('\n', prod, item)
    #        Max = prod
    results.put(Result(-prod[0], (item, prod[1])))
    pass

cdict = dict()
# for i in range(2):
#    cdict[i] = results.get()
#    print(-cdict[i].priority, cdict[i].builds)
print('==============')
Rec = results.get()
print('最优策略：', Rec.builds[0])
print('各建筑加成倍率', np.round(Rec.builds[1], 2))
print('升级优先级', np.round([x * star[Rec.builds[0][i // 3][i % 3]] for i, x in enumerate(Rec.builds[1])], 2))
print('==============')
Rec = results.get()
print('次优策略：', Rec.builds[0])
print('各建筑加成倍率', np.round(Rec.builds[1], 2))
print('升级优先级', np.round([x * star[Rec.builds[0][i // 3][i % 3]] for i, x in enumerate(Rec.builds[1])], 2))

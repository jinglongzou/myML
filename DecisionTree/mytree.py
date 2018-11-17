#函数首字母大写，变量首字母小写

import numpy
from math import log
#数据集是带标签，以表格形式存储，最后一列为标签,当为二分类时，标签值为1或0

def SplitDataSet(dataSet,i,featValue):
    subDataSet = []
    for example in dataSet:
        if example[i] == featValue:
            reduceFeatData = example[:i]
            reduceFeatData.extend(example[i+1:])
            subDataSet.append(reduceFeatData)
    return subDataSet

def CalcShannonEnt(subDataSet):
    num = len(subDataSet)
    #统计该特征值下对应的每个标签的数目
    labelCounts = {}
    for example in subDataSet:
        currentLabel = example[-1] #获取标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0        #创建一个标签计数的键
        labelCounts[currentLabel] +=1
    #计算香农熵
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/float(num)
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def ChooseBestFeature(dataSet):
    numFeat = len(dataSet[0]) - 1
    baseEntropy = CalcShannonEnt(dataSet)
    bestInfoGain = 0.0;bestFeat = -1
    for i in range(numFeat):
        #得到一个特征下的所有值
        featValues = [example[i] for example in dataSet]
        featSet = set(featValues)
        newEntropy = 0.0
        for featValue in featSet:
            subDataSet = SplitDataSet(dataSet,i,featValue)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * CalcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (bestInfoGain < infoGain):
            bestInfoGain = infoGain
            bestFeat = i
    return bestFeat
#当所有特征用完时
def majorityLabel(dataSet):
    import operator
    classCounts = {}
    for example in dataSet:
        currentLabel = example[-1]
        if currentLabel not in classCounts.keys():
            classCounts[currentLabel] = 0
        classCounts[currentLabel] += 1
        sortedClassCounts = sorted(sortedClassCounts.items(),key = operator.itemgetter(1),reverse = True)
        return sortedClassCounts[0][0]
#创建树的过程就是利用数据集训练的过程
def CreateTree(dataSet,featLabels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityLabel(dataSet)
    bestFeat = ChooseBestFeature(dataSet)
    bestFeatLabel = featLabels[bestFeat]
    mytree = {bestFeatLabel:{}}
    del(featLabels[bestFeat])#删除已经使用的特征标签
    featValues = [example[bestFeat] for example in dataSet]
    featSet = set(featValues)
    #针对每个特征值得到该最好特征下的子类，并对每个子类再次创建子树
    for featValue in featSet:
        #subDataSet = SplitDataSet(dataSet,bestFeat,featValue)
        subFeatLabels = featLabels[:]
        mytree[bestFeatLabel][featValue] = CreateTree(SplitDataSet(dataSet,bestFeat,featValue),subFeatLabels)
    return mytree

#通过逐级比对特征的键值来分类，当键值相同时则进一步分类，直到树不是字典，即到树的叶节点了
def classify(inputTree,featLabels,testExample):
    firstFeatStr = list(inputTree.keys())[0]
    secondTree = inputTree[firstFeatStr]
    featIndex = featLabels.index(firstFeatStr)
    for key in secondTree.keys():
        if testExample[featIndex] == key:
            if type(secondTree[key]).__name__ == 'dict':
                classLabel = classify(secondTree[key],featLabels,testExample)
            else:
                classLabel = secondTree[key]
    return classLabel

def Test():
    #测试树
    #1、读取数据集，并提取出特征标签
    fr = open(r'lenses.txt')
    lenses = [line.strip().split('\t') for line in fr.readlines()]
    featLabels = ['age','prescript','atigmatic','tearrate']
    lensesTree = CreateTree(dataSet,featLabels)
    print(lensesTree)

"""
总结：写代码过程中犯的了很多粗心错误，
    1、变量名不一致；
    2、使用的函数名不正确；
    3、写代码没有考虑到对象的类型特性,如使用for时，区域循环，使用的是列表中的元素；index循环使用的是索引值
    4、通过打印变量可以分析错误
"""

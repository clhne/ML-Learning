#-*-coding:utf-8-*-
import numpy as np

def distance(X):
    return np.sqrt(sum(X**2))

def PCA(dataMat, topNfeat):
    #使矩阵的均值为0
    meanVals = np.mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals
    #获得协方差矩阵
    covMat = np.cov(meanRemoved, rowvar=0)
    #求协方差矩阵的特征值及相应的特征向量
    eigVals, eigVects = np.linalg.eigh(np.mat(covMat))
    #根据特征值大小进行排序，并取前N大的特征向量
    eigValInd = np.argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:,eigValInd]
    #进行重建
    lowDataMat = meanRemoved * redEigVects
    reconMat = (lowDataMat * redEigVects.T) + meanVals

    reconMat = reconMat.real
    rate = []
    #计算经过PCA之后的余弦相似度
    for i in range(len(dataMat)):
        rate.append(sum((np.array(dataMat[i])[0])*(np.array(reconMat[i])[0]))/(distance(np.array(dataMat[i])[0])*distance(np.array(reconMat[i])[0])))

    return reconMat,rate

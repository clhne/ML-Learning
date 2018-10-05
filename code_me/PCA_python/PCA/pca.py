#-*-coding:utf-8-*-
#PCA对数据进行降维

from numpy import *

def confloat(x):
    r=[float(i) for i in x]
    return r

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [confloat(line) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat=9999999):
    #计算平均值
    meanVals = mean(dataMat, axis=0)
    #去平均值
    meanRemoved = dataMat - meanVals #remove mean
    #计算协方差矩阵
    covMat = cov(meanRemoved, rowvar=0)

    #计算特征值和特征向量
    eigVals,eigVects = linalg.eig(mat(covMat))

    #对特征值进行排序，从小到大排序
    eigValInd = argsort(eigVals)            #sort, sort goes smallest to largest

    #获得最大的topFeat 特征值
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #cut off unwanted dimensions

    #获取对应的特征向量
    redEigVects = eigVects[:,eigValInd]       #reorganize eig vects largest to smallest

    #将数据转换到新的特征空间
    lowDDataMat = meanRemoved * redEigVects#transform data into new dimensions
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat

def replaceNanWithMean():
    datMat = loadDataSet('secom.data', ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i]) #values that are not NaN (a number)
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal  #set NaN values to mean
    return datMat

datMat=loadDataSet('testSet.txt')
#
lowDataMat,reconMat=pca(datMat,2)
print(lowDataMat)
#
# #将降维后的数据和原始数据一起绘制出来
import  matplotlib
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(datMat[:,0].flatten().A[0],datMat[:,1].flatten().A[0],marker='^',s=90)
ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
plt.show()
print(datMat[:,0].flatten().A[0])

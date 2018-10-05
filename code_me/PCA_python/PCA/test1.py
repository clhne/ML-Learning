#-*-coding:utf-8-*-
#对半导体材料数据降维
from pca import *
dataMat=replaceNanWithMean()

lowDataMat,reconMat=pca(dataMat,6)
print(lowDataMat)
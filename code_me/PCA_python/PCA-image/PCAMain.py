#-*-coding:utf-8-*-
from PCA import *
import matplotlib.pyplot as plt

def loadDataSet(filename, delim='\t'):
    fr = open(filename)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    dataArr = [list(map(float, line)) for line in stringArr]
    return np.mat(dataArr)

n = 1000 #number of points to create

dataMat = loadDataSet('./data/testSet.txt')
reconMat, rate = PCA(dataMat, 1)
fig = plt.figure()
ax = fig.add_subplot(121)
ax.scatter(np.array(dataMat[:,0]), np.array(dataMat[:,1]), marker='^', s=20)
plt.xlabel('hours of direct sunlight')
plt.ylabel('liters of water')
plt.title('Before PCA')



ax = fig.add_subplot(122)
ax.scatter(np.array(dataMat[:,0]), np.array(dataMat[:,1]), marker='^', s=20)
ax.scatter(np.array(reconMat[:,0]), np.array(reconMat[:,1]), marker='s', s=20, c='red')
plt.xlabel('hours of direct sunlight')
plt.ylabel('liters of water')
plt.title('After PCA')

plt.show()
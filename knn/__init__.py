from knn import *

if __name__ == '__main__':
    returnMat, classLabelVector = file2matrix("datingTestSet.txt")
    print (classify0([43757, 7.6, 0.134296], returnMat, classLabelVector, 10))

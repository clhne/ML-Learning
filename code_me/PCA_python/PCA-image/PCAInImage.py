#-*-coding:utf-8-*-
import matplotlib.pyplot as plt
from PIL import Image
from PCA import *
import os
from tqdm import tqdm

def GetFiles(path):
    for root,dirs,files in os.walk(path):
        return files

def loadDataSet(filename, delim='\t'):
    fr = open(filename)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    dataArr = [list(map(float, line)) for line in stringArr]
    return np.mat(dataArr)

def PictureToData(path):
    #将图片数据集转化为矩阵
    pictureList = GetFiles(path)
    width = 0
    height = 0
    file = open("./data/pictures.data", 'w')
    for picture in tqdm(pictureList):
        im = Image.open(path+'/'+picture)
        im = im.convert("L")
        width, height = im.size
        data = im.getdata()
        data = np.array(data, dtype='double')
        for elem in data.tolist():
            file.write(str(elem) + " ")
        file.write("\n")
    file.close()
    return [width,height]


if __name__ == "__main__":

    [width, height] = PictureToData('./at33')# 获取图片大小
    data = loadDataSet("./data/pictures.data",delim=' ')#加载图片数据集
    new_data, rate = PCA(data, 10)
    print(rate)
    num = 0
    file = open("./data/PCApictures.data", 'w')
    pictureList = GetFiles('./at33')
    for picture in new_data:
        for i in picture.tolist()[0]:
            file.write(str(i)+' ')
        file.write('\n')
        pictureMat = picture.reshape((height,width))
        new_im = Image.fromarray(pictureMat.astype(np.uint8))
        new_im.save('./newPicture/PCA_'+pictureList[num])
        num += 1
    file.close()
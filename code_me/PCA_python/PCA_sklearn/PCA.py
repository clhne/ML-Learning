#-*-coding:utf-8-*-
from sklearn.datasets import load_iris
iris=load_iris()
x=iris['data']
y=iris['target']
#print(x)
#print(y)
from sklearn.preprocessing import StandardScaler
x=StandardScaler().fit_transform(x)
#print(x)
# 4维降到2维
from sklearn.decomposition import PCA
import pandas as pd
pca=PCA(n_components=2)
data=pca.fit_transform(x)
data_df=pd.DataFrame(data=data,columns=['pc1','pc2'])
target_df=pd.DataFrame(data=iris.target,columns=['target'])
final_df=pd.concat([data_df,target_df],axis=1)
print(final_df)
#对2D数据可视化
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
plt.xlabel('pc1')
plt.ylabel('pc2')
plt.title("2 components's PCA",size=20)
targets=['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
colors=['r','g','b']
flower_datas=[final_df[final_df['target']==0],
              final_df[final_df['target']==1],
              final_df[final_df['target']==2]]
for flower_data,color in zip(flower_datas,colors):
    plt.scatter(flower_data.pc1,flower_data.pc2,c=color,s=50)
    plt.legend(targets,loc='lower right')
    plt.grid()
plt.show()
#可以从图中看出，降维后数据仍然可以很好地区分
import numpy as np
import mlpy
import matplotlib.pyplot as plt

basePath = "/home/youngcoma/Dropbox/newFallDetect/experiment"

##
## @@ INPUT: read calculated_data from file @@ ##
##	dataDict Format: _id:{SVM, TA, AV, label} 
cal_dataFileName = 'test1_data.txt'
data = np.loadtxt("{}/calculated_data/{}".format(basePath,cal_dataFileName), delimiter=',')
base_id, attrs, label = data[:, 0].astype(np.int), data[:,1:4], data[:, 4].astype(np.int)

# dataDict = dict(zip(base_id, attrs))
# print 'calculated_data preview: \n{}\n\r'.format(dataDict)


pca = mlpy.PCA()
pca.learn(attrs)

z = pca.transform(attrs, k=2)

plt.set_cmap(plt.cm.Paired)
fig1 = plt.figure(1)
title = plt.title("PCA on {} dataset".format(cal_dataFileName))
plot = plt.scatter(z[:, 0], z[:, 1], c=label)
labx = plt.xlabel("First component")
laby = plt.ylabel("Second component")
plt.show()
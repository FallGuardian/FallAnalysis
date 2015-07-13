import numpy as np
import mlpy
import matplotlib.pyplot as plt # required for plotting

data = np.loadtxt('./data/data_all_549.csv', delimiter=',')
x, y = data[:, 1:4], data[:, 4].astype(np.int)
print x
pca = mlpy.PCA()
pca.learn(x)
z = pca.transform(x, k=2)

plt.set_cmap(plt.cm.Paired)
fig1 = plt.figure(1)
title = plt.title("PCA on ./data/data_all_549.csv dataset")
plot = plt.scatter(z[:, 0], z[:, 1], c=y)
labx = plt.xlabel("First component")
laby = plt.ylabel("Second component")
plt.show()


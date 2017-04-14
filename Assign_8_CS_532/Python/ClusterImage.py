from sevenhtml import *

blognames, words, data=readfile('2blogdata.txt')
clust=hcluster(data)
printclust(clust, labels=blognames)

drawdendrogram(clust, blognames, jpeg='2blogclust.jpg')

print ('Centroid = 5', end='\n')
kclust= kcluster(data, k=5)
for i in range(5):
    print('Cluster %d' % i, *[blognames[x] for x in kclust[i]], sep='\t')

print('Centroid = 10', end='\n')
kclust= kcluster(data, k=10)
for i in range(10):
    print('Cluster %d' % i, *[blognames[x] for x in kclust[i]], sep='\t')

print('Centroid = 20', end='\n')
kclust= kcluster(data, k=20)
for i in range(20):
    print('Cluster %d' % i, *[blognames[x] for x in kclust[i]], sep='\t')

print('2d Coords', end='\n')
coords= scaledown(data)
draw2d(coords, blognames, jpeg='2blog2d.jpg')

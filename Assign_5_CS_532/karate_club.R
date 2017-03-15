
require(graphics)
library(igraph)

pdf('Desktop/karate_club_cluster_edge_2.pdf')
karate_graph<-read.graph('Desktop/karate_club.graphml', format='graphml')
karate_eb<-cluster_edge_betweenness(karate_graph)
colors<-c('light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'red', 'light blue', 'light blue', 'light blue', 'light blue', 'red', 'red', 'light blue', 'light blue', 'red', 'light blue', 'red', 'light blue', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red','red')
plot(karate_eb, karate_graph, col=colors)
legend(x=0, legend=c("officers", "Mr. Hi"), fill=c('red', 'light blue'))
dev.off()

require(graphics)
library(igraph)

pdf('Desktop/karate_club_cluster_eigen_2.pdf')
karate_graph<-read.graph('Desktop/karate_club.graphml', format='graphml')
karate_eb<-cluster_leading_eigen(karate_graph)
colors<-c('light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'light blue', 'red', 'light blue', 'light blue', 'light blue', 'light blue', 'red', 'red', 'light blue', 'light blue', 'red', 'light blue', 'red', 'light blue', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red','red')
plot(karate_eb, karate_graph, col=colors, main="Karate Club Community Prediction Using Leading Eigen")
legend(x=0, legend=c("officers", "Mr. Hi"), fill=c('red', 'light blue'))
dev.off()


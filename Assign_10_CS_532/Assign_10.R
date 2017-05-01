require(graphics)

pdf("Desktop/mem_data.pdf")

data_table<-read.table(file="Desktop/Assign_10_CS_532/data_set.txt", header=T, sep="\t")

diff_data<-c(data_table$diff)

max_diff<-max(diff_data)

num_zero_diff<- length(diff_data[diff_data==0])



plot(diff_data, xlim= c(1, 1025), ylim=c(-100,1000), pch=20, col='blue', main="Time Maps", xlab="Difference in Number of Mementos", ylab="URIs", type='h')

text(c(1000,1000,1000,1000,1000,1000),c(850,800,700,650,550,500), labels=c("Total URIs", length(diff_data), "No Change", num_zero_diff, "Max Difference", max_diff), pos=2, col='black')

dev.off()



require(graphics)
pdf("Desktop/mem_data.pdf")
data_table<-read.table(file="Desktop/data_set.txt", header=T, sep="\t")
mem_data<-c(data_table$mem)
max_mem<-max(mem_data)
num_zero_mem<- length(mem_data[mem_data==0])
h<-hist(mem_data, plot=F, breaks=max_mem)
plot(h$mids, h$counts, log='xy', xlim= c(1, max_mem), ylim=c(1,20), pch=20, col='blue', main="Mementos", xlab="Num of Mementos", ylab="URIs", type='h')
text(c(3000,3000,3000,3000),c(18,16.4,14.4,13), labels=c("Total URIs", length(mem_data), "Without Mementos", num_zero_mem), pos=2, col='black')
dev.off()


require(graphics)
pdf("Desktop/age_data.pdf")
data_table<-read.table(file="Desktop/data_set.txt", header=T, sep="\t")
num_na<-length(data_table$age[data_table$age=='NA'])
num_uri<-length(data_table$mem)
num_zero_mem<- length(data_table$mem[data_table$mem==0])
data<-data_table[!data_table$mem=='0' & !data_table$age=='NA',]
max_age<-max(data$age)
max_mem<-max(data$mem)
plot(data$age, data$mem, log="xy", pch=20, col='blue', main="Age vs Mementos", xlab="Age of URI", ylab="Number of Mementos", type='p' )
text(c(1000,1000,1000,1000,1000,1000),c(18000,13300,9750,7000,4700,3500), labels=c("Total URIs", num_uri, "No Mementos", num_zero_mem, "No Date Est", num_na), pos=2, col='black')
dev.off()



library(ggplot2)

setwd("/Users/echo/Documents/Lab/MyProject/AndroidGetSlow/log/")

data = read.csv("pro_log/all", sep = "\t")
# print(str(data))

ggplot(data, aes(latency, colour = type)) +
  stat_ecdf() +
  theme_bw()
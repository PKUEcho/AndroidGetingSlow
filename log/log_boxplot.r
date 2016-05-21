library(ggplot2)

setwd("/Users/echo/Documents/Lab/MyProject/AndroidGetSlow/log/")

data = read.csv(
  "pro_log/com.eg.android.AlipayGphone-.AlipayLogin", sep = "\t")

theme_set(theme_grey(base_size = 28)) 

p <- ggplot(data, aes(type, latency))
p +
  geom_boxplot() +
  geom_jitter(width = 0.1) +
  theme_bw() +
  theme(axis.title.x = element_text(size=35),
        axis.title.y = element_text(size=35),
        axis.text.x = element_text(size=30),
        axis.text.y = element_text(size=30))
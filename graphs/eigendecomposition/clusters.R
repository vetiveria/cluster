
# Packages
packages <- c("ggplot2", "plotly", "data.table")
prepare <- function(x){
  if (!require(x, character.only = TRUE)) {
    install.packages(x, dependencies = TRUE)
    library(x, character.only = TRUE)
  }
}
isready <- lapply(packages, prepare)



# Data
principals <- fread(file = "../../warehouse/principals.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                    colClasses = c("character", "numeric", "numeric", "numeric", "numeric", "factor"))
accumulations <- fread("https://raw.githubusercontent.com/briefings/sars/master/fundamentals/hopkins/warehouse/accumulations.csv", 
                       header = TRUE, select = c("COUNTYGEOID", "deathRate", "positiveRate"), 
                       colClasses = c(COUNTYGEOID="character", deathRate="numeric", positiveRate="numeric"), 
                       encoding = "UTF-8", data.table = TRUE)



# Cases whereby SARS-CoV-2 data is recorded in 'accumulations'
readings <- principals[accumulations, on = "COUNTYGEOID"]
readings[, .N]



# ... missing
missing <- principals[!accumulations, on = "COUNTYGEOID"]



# Draw
fig <- plot_ly(principals, x = ~C01, y = ~C02, z = ~C03, color = ~label, 
               colors = c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900'))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'PC 1'), 
                                   yaxis = list(title = 'PC 2'),
                                   zaxis = list(title = 'PC 3')))
htmlwidgets::saveWidget(fig, "clusters.html")


fig <- plot_ly(readings, x = ~C01, y = ~C02, z = ~C03)
fig <- fig %>% add_markers(size = ~deathRate, color = ~label, colors = c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900'))
fig <- fig %>% layout(scene = list(xaxis = list(title = 'PC 1'), 
                                   yaxis = list(title = 'PC 2'),
                                   zaxis = list(title = 'PC 3')))
htmlwidgets::saveWidget(fig, "contexts.html")


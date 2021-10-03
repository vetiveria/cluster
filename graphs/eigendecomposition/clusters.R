
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
principals <- fread(file = "../warehouse/baseline/principals.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                    colClasses = c("character", "numeric", "numeric", "numeric", "numeric", "factor"))

accumulations <- fread("https://raw.githubusercontent.com/briefings/sars/master/fundamentals/hopkins/warehouse/accumulations.csv", 
                       header = TRUE, select = c("COUNTYGEOID", "deathRate", "positiveRate"), 
                       colClasses = c(COUNTYGEOID="character", deathRate="numeric", positiveRate="numeric"), 
                       encoding = "UTF-8", data.table = TRUE)

gazetter <- fread("https://raw.githubusercontent.com/briefings/sars/master/fundamentals/hopkins/warehouse/gazetteer.csv", 
                  header = TRUE, select = c("STUSPS", "STATE", "COUNTYGEOID", "COUNTY"), 
                  colClasses = c(STUSPS="character", STATE="character", COUNTYGEOID="character", COUNTY="character"), 
                  encoding = "UTF-8", data.table = TRUE)


# Cases whereby SARS-CoV-2 data is recorded in 'accumulations'
readings <- principals[accumulations, on = "COUNTYGEOID"]
readings <- gazetter[readings, on = "COUNTYGEOID"]
readings[, .N]



# ... missing
missing <- principals[!readings, on = "COUNTYGEOID"]



# Draw [file.path(getwd(), , )]
fig <- plot_ly(readings, x = ~C02, y = ~C03, z = ~C04, color = ~label, 
               colors = c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900'), 
               text = ~paste(COUNTY, ', ', STATE))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'PC 2'), 
                                   yaxis = list(title = 'PC 3'),
                                   zaxis = list(title = 'PC 4')))
htmlwidgets::saveWidget(fig, 'clusters.html')



fig <- plot_ly(readings, x = ~C02, y = ~C03, z = ~C04, color = ~label,
               colors = c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900'), 
               marker = list(symbol = 'circle', size = ~deathRate/25, sizemode = 'diameter'), 
               text = ~paste(COUNTY, ', ', STATE))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'PC 2'), 
                                   yaxis = list(title = 'PC 3'),
                                   zaxis = list(title = 'PC 4')))
htmlwidgets::saveWidget(fig, 'contexts.html')


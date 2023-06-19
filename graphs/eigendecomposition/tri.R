
# Functions
source("functions/packages.R")
source("functions/gazetteer.R")


# Ensure that the required packages are available
packages()


# Data
principals <- fread(file = "../../warehouse/kidney/principals.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                    colClasses = c("character", "numeric", "numeric", "numeric", "numeric", "factor"))
gazetteer <- gazetteer()
data <- principals[gazetteer[, !c("COUNTYFP", "STATEFP")], on = "COUNTYGEOID"]


# Draw
fig <- plot_ly(data, x = ~C01, y = ~C02, z = ~C03, color = ~label, 
               colors = c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900'), 
               text = ~paste(county, ', ', STUSPS))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'PC 1'), 
                                   yaxis = list(title = 'PC 2'),
                                   zaxis = list(title = 'PC 3')))
htmlwidgets::saveWidget(fig, 'kidney.html')
# Functions
source("functions/packages.R")
source("functions/gazetteer.R")
source("functions/chemicals.R")



# Ensure that the required packages are available
packages()



# Data
cluster <- fread("https://raw.githubusercontent.com/vetiveria/cluster/develop/warehouse/releases/00.csv", 
                 header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                 colClasses = c(COUNTYGEOID = "character", label = "factor", tri_chem_id = "numeric", quantity_kg = "numeric"))

gazetteer <- gazetteer()
gazetteer <- gazetteer[, !c("STATEFP", "COUNTYFP")]

chemicals <- chemicals()



# Structure: via right join
baseline <- gazetteer[cluster, on = "COUNTYGEOID"]
baseline <- chemicals[baseline, on = "tri_chem_id"]
rm(cluster, gazetteer, chemicals)



# https://plotly.com/r/box-plots/
fig <- plot_ly(baseline, x = ~chemical, y = ~quantity_kg, type = "box", boxpoints = "all", jitter = 0.2)

htmlwidgets::saveWidget(fig, paste0("distributions", ".html"))


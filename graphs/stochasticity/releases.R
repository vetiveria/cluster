
# Packages
packages <- c("ggplot2", "plotly", "data.table", "tsne")
prepare <- function(x){
  if (!require(x, character.only = TRUE)) {
    install.packages(x, dependencies = TRUE)
    library(x, character.only = TRUE)
  }
}
isready <- lapply(packages, prepare)



# Data
original <- fread(file = "../../../segments/warehouse/design/original.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, colClasses = c(COUNTYGEOID="character"))
principals <- fread(file = "../../warehouse/principals.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                    colClasses = c("character", "numeric", "numeric", "numeric", "numeric", "factor"))



# Traing Data Matrix
trainingdata <- data.matrix(original[, !c("COUNTYGEOID")], rownames.force = NA)



# Initial number of 'dimensionality reduction' feature space projections 
initial_dims <- 16



# Label colours
colours <- colors(distinct = TRUE)
paints <- c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900')



# Variables & Parameters
labels <- principals$label
epoch <- 100
start <- Sys.time()



# Call Back
epoch_callback <- function(x, y){
  
  name <- as.integer(difftime(Sys.time(), start, units = "secs"))
  namestr <- formatC(name, width = 13, format = "d", flag = "0")
  
  
  # join
  projections <- as.data.table(x, keep.rownames = FALSE) 
  colnames(projections) <- c("tSNE1", "tSNE2", "tSNE3")
  update <- data.table(principals, projections)
  
  
  # write
  fwrite(update, file = paste0("data/", namestr, ".csv"))
  
  
  # illustrate
  fig <- plot_ly(data.table(projections), x = ~tSNE1, y = ~tSNE2, z = ~tSNE3, color = labels, 
                 colors = paints[1 + as.numeric(as.character(labels))])
  fig <- fig %>% add_markers()
  fig <- fig %>% layout(scene = list(xaxis = list(title = 'tSNE 1'), 
                                     yaxis = list(title = 'tSNE 2'),
                                     zaxis = list(title = 'tSNE 3')))
  htmlwidgets::saveWidget(fig, paste0(namestr, ".html"))
  
}



# Model
model <- tsne(trainingdata, initial_config = NULL, k = 3, initial_dims = initial_dims, max_iter = 1000,
     epoch_callback = epoch_callback, epoch = epoch)









# Functions
source("functions/packages.R")
source("functions/gazetteer.R")
source("functions/tSNE3DGraph.R")


# Ensure that the required packages are available
packages()


# Data
principals <- fread(file = "../../warehouse/principals.csv", header = TRUE, encoding = "UTF-8", data.table = TRUE, 
                    colClasses = c("character", "numeric", "numeric", "numeric", "numeric", "factor"))
trainingdata <- data.matrix(principals[, !c("COUNTYGEOID", "label")], rownames.force = NA)
gazetteer <- gazetteer()


# Labels
labels <- principals$label


# Label colours
colours <- c('#000000', '#BF382A', '#0C4B8E', '#808000', '#993300', '#ff9900')


# Variables: Initial number of 'dimensionality reduction' feature space projections
variables <- as.list(c(8, 200, Sys.time()))
names(variables) <- c("initial_dims", "epoch", "start")



# Structuring
structure <- function(matrix) {
  
  projections <- as.data.table(matrix, keep.rownames = FALSE)
  colnames(projections) <- c("tSNE1", "tSNE2", "tSNE3")
  
  projections <- data.table(principals, projections)
  projections <- projections[gazetteer[, !c("COUNTYFP")], on = "COUNTYGEOID"]
  projections
  
}


# tSNE Callback Function
epoch_callback <- function(x){
  
  # Use elapsed time to create file names
  elapsed <- as.integer(as.integer(Sys.time()) - variables$start)
  namestr <- formatC(elapsed, width = 9, format = "d", flag = "0")
  
  # Saving the data of, and illustrating, the latest tSNE estimates
  latest <- structure(matrix = x)
  tSNE3DGraph(data = latest, fileName = namestr)
}


# tSNE Algorithm
estimates <- tsne(trainingdata, initial_config = NULL, k = 3, initial_dims = variables$initial_dims, max_iter = 400,
     epoch_callback = epoch_callback, epoch = variables$epoch)
tSNE3DGraph(data = structure(matrix = estimates), fileName = "estimates")



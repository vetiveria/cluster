packages <- function(){
  
  # List of packages
  packages <- c("ggplot2", "plotly", "data.table", "tsne")
  
  # Prepare
  prepare <- function(x){
    if (!require(x, character.only = TRUE)) {
      install.packages(x, dependencies = TRUE)
      library(x, character.only = TRUE)
    }
  }
  isready <- lapply(packages, prepare)
  
}
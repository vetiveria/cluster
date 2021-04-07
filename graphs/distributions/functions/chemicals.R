chemicals <- function() {
  
  source("functions/data.R")
  
  url <- "https://raw.githubusercontent.com/vetiveria/spots/master/resources/references/chemicalsOfTRI.csv"
  select <- c("tri_chem_id", "name")
  colClasses <- c(tri_chem_id = "character", name = "character")
  fieldNames <- c("tri_chem_id", "chemical")
  
  
  data(url = url, select = select, colClasses = colClasses, fieldNames = fieldNames)
  
}
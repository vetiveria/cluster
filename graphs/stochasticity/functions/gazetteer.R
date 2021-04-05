gazetteer <- function(){
  
  
  source("functions/data.R")
  
  
  getCounties <- function(){
    url <- "https://raw.githubusercontent.com/discourses/hub/develop/data/countries/us/geography/counties/counties.csv"
    select <- c("STATEFP", "COUNTYFP", "GEOID" , "NAME")
    colClasses <- c(STATEFP="character", COUNTYFP="character", GEOID="character", NAME="character")
    fieldNames <- c("STATEFP", "COUNTYFP", "COUNTYGEOID", "county")
    
    data(url = url, select = select, colClasses = colClasses, fieldNames = fieldNames)
  }
  counties <- getCounties()
  
  
  getStates <- function(){
    url <- "https://raw.githubusercontent.com/discourses/hub/develop/data/countries/us/geography/states/states.csv"
    select <- c("STATEFP", "STUSPS", "NAME")
    colClasses <- c(STATEFP="character", STUSPS="character", NAME="character")
    fieldNames <- c("STATEFP", "STUSPS", "state")
    
    data(url = url, select = select, colClasses = colClasses, fieldNames = fieldNames)
  }
  states <- getStates()
  
  
  counties[states, on = "STATEFP"]
  
  
}
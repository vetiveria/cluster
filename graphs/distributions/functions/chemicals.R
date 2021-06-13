chemicals <- function() {
  
  source("functions/data.R")
  
  url <- "https://raw.githubusercontent.com/vetiveria/spots/develop/resources/references/chemicalsEnvirofacts.csv"
  select <- c("TRI_CHEM_INFO.TRI_CHEM_ID",	"TRI_CHEM_INFO.CHEM_NAME", "TRI_CHEM_INFO.CAAC_IND",	"TRI_CHEM_INFO.CARC_IND", 
              "TRI_CHEM_INFO.R3350_IND")
  colClasses <- c(TRI_CHEM_INFO.TRI_CHEM_ID = "character", TRI_CHEM_INFO.CHEM_NAME = "character", TRI_CHEM_INFO.CAAC_IND = "numeric",
                  TRI_CHEM_INFO.CARC_IND = "numeric", TRI_CHEM_INFO.R3350_IND = "numeric")
  fieldNames <- c("tri_chem_id", "chemical", "air_pollutant", "carcinogenic", "R3350_pollutant")
  
  
  data(url = url, select = select, colClasses = colClasses, fieldNames = fieldNames)
  
}
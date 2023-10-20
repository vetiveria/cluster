
data <- function(url, select, colClasses, fieldNames){
  data <- fread(url, header = TRUE, encoding = "UTF-8", data.table = TRUE, select = select, colClasses = colClasses)
  colnames(data) <- fieldNames
  data
}

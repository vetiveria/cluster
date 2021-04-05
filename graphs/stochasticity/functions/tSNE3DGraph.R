
tSNE3DGraph <- function(data, fileName){
  
  fig <- plot_ly(data.table(data), x = ~tSNE1, y = ~tSNE2, z = ~tSNE3, color = labels, colors = colours, text = ~paste(county, ', ', state))
  fig <- fig %>% add_markers()
  fig <- fig %>% layout(scene = list(xaxis = list(title = 'tSNE 1'), 
                                     yaxis = list(title = 'tSNE 2'),
                                     zaxis = list(title = 'tSNE 3')))
  htmlwidgets::saveWidget(fig, paste0(fileName, ".html"))
  
  fwrite(data, file = paste0("data/", fileName, ".csv"))
  
}
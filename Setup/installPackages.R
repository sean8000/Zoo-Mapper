#library (ks)
#library (rgl)
#library (misc3d)
#library (readxl)
#library (dplyr)
#library (htmlwidgets)
#library(ggplot2)
#library(pandoc)
#library(rjson)  
#You must install all of these libraries in order to run kde
dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)  # create personal library
.libPaths(Sys.getenv("R_LIBS_USER"))  # add to the path

install.packages('ks', repos='https://cloud.r-project.org/')
install.packages('rgl', repos='https://cloud.r-project.org/')
install.packages('misc3d', repos='https://cloud.r-project.org/')
install.packages('readxl', repos='https://cloud.r-project.org/')
install.packages('dplyr', repos='https://cloud.r-project.org/')
install.packages('htmlwidgets', repos='https://cloud.r-project.org/')
install.packages('ggplot2', repos='https://cloud.r-project.org/')
install.packages('pandoc', repos='https://cloud.r-project.org/')
install.packages('rjson', repos='https://cloud.r-project.org/')



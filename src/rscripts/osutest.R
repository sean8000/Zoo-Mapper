library(maptools)
library(rgdal)
library(misc3d)
library(sf)
library(sm)
#readShapeLines(file.choose())
#readShapePoints(file.choose())
#readShapePoly(file.choose())


#https://blogs.oregonstate.edu/geo599spatialstatistics/2014/05/06/working-shapefile-data-r/

  
shape <- readShapePoints(file.choose())
#summary(shape)
#shape <- readOGR("C:/Users/jtayl/Desktop/testr/shapes/shapes.shp")
#summary(shape)
#shape <- st_read("C:/Users/jtayl/Desktop/testr/shapes/shapes.shp")
summary(shape)

x <- shape$coords.x1
y <- shape$coords.x2
z <- shape$coords.x3

#mx <- x/1000
#my <- y/1000

#mz <- z/1000

#with(shape, {
 # d <- kde3d(mx, my, mz, h=0.2, n = 150, lims=c(range(mx),range(my),range(mz)))
  #contour3d(d$d, 0.02, d$x, d$y, d$z,
   #         color = "red", color2 = "gray", scale=TRUE
  #)
#})

m <- cbind(x,y,z)
sm.density(m, panel=TRUE, panel.plot = TRUE)

#writes the shapefile
writePointsShape(shape, file.choose()) 

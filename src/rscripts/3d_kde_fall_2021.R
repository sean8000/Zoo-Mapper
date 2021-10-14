library(ks)
library(rgl)
library(misc3d)
library(sm)
library(rpanel)
library(maptools)
library(spatstat)
library(sf)


# Read shark 1205 data for depth, long, and lat into shark_1205
shark_1205 <- read.csv("C:/Users/Kevin/Documents/R/shark_1205.csv")[ ,c('DepthM', 'LongUTM', 'LatUTM')]

# shape <- st_read(file.choose())

#print(shape)

x <- shark_1205$LongUTM
y <- shark_1205$LatUTM
z <- shark_1205$DepthM

mx <- x/1000
my <- y/1000
mz <- z/1000

 with(shark_1205, {
  d <- kde3d(x, y, z, h=0.2, n=100, lims=c(range(x), range(y), range(z)))
  contour3d(d$d, 0.04, d$x, d$y, d$z, color = "red", color2="gray", scale=TRUE)
 })

m <- cbind(x,y,z)
sm.density(m, panel=TRUE, panel.plot = TRUE)

p3 <- pp3(x,y,z, as.box3(range(x), range(y), range(z)))
dists <- nndist.pp3(p3)

# writePointsShape(dists, file.choose())
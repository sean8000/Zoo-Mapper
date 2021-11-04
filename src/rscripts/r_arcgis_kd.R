library(ks)
library(rgl)
library(misc3d)
library(sm)
library(rpanel)
library(maptools)
library(spatstat)
library(sf)
library(arcgisbinding)
library(csv)

arc.check_product()
shark_data <- arc.open("C:/Users/Kevin/Documents/CISC498/MarinelandDemo/Marineland Demo/Marineland_ZooMonitor_3D_MBV_Depths.shp")
# shark_data_df <- read.csv("C:/Users/Kevin/Documents/GitHub/Zoo-Mapper/src/main/resources/FinalShark_1205_forR.csv")
shark_data_df <- arc.select(shark_data)

#View(shark_data_df)

x <- shark_data_df$UTMx
y <- shark_data_df$UTMy
z <- shark_data_df$DepthM_MBV

# For scaling, might not be useful
mx <- x/1000
my <- y/1000
mz <- z/1000


with(shark_data_df, {
  d <- kde3d(x, y, z, h=0.1, n=100, lims=c(range(x), range(y), range(z)))
  contour3d(d$d, 0.01, d$x, d$y, d$z, color = "red", color2="gray", scale=TRUE)
})

m <- cbind(x,y,z)
sm.density(m, panel=TRUE, panel.plot = TRUE)

p3 <- pp3(x,y,z, as.box3(range(x), range(y), range(z)))
dists <- nndist.pp3(p3)
shark_data_df$nndist <- dists

# arc.write("C:/Users/Kevin/Documents/CISC498/shark-test.shp", shark_data_df)

#arc.write("C:/Users/Kevin/Documents/CISC498/shark-test.shp", shark_data_df)

arc.write(file.choose(), shark_data_df)

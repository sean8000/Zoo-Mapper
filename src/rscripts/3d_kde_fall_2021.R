library(ks)
library(rgl)
library(misc3d)
library(dplyr)
library(htmlwidgets)
library(ggplot2)
library(arcgisbinding)
library(sf)

options(stringsAsFactors=FALSE)

arc.check_product()

# Define Functions
calcKernelVol <- function(fhat, perc) { # Calculates perc% kernel volume
  ct <- contourLevels(fhat, cont=perc, approx=TRUE)
  vol.voxel <- prod(sapply(fhat$eval.points, diff)[1,]) # Calculate volume of single voxel
  no.voxel <- sum(fhat$estimate>ct) # Calculate number of voxels
  vol <- no.voxel*vol.voxel # Calculate total volume as product
  return(vol) }

calcIntersect <- function(fhat1, fhat2, perc) { # Calculates volume of intersection of perc% volumes
  ct1 <- contourLevels(fhat1, cont=perc, approx=TRUE) 
  ct2 <- contourLevels(fhat2, cont=perc, approx=TRUE) 
  vol.voxel <- prod(sapply(fhat1$eval.points, diff)[1,]) 
  no.voxel <- sum(fhat1$estimate>ct1 & fhat2$estimate>ct2) 
  intersect <- no.voxel*vol.voxel
  return(intersect) }

genLabel <- function(m, n, pilot) { # Generate label for KDE settings
  return(paste("M",m,",N",n,",",pilot,sep="")) }

KDETrialSingle <- function(data, if2D, percs, m, n, pilot, imgDir, colorSingle, opacitySingle, display2D){
  band <- Hpi(data, nstage=n, pilot=pilot)*m # Generate bandwith matrix
  fhat <- kde(data, H=band) # Generate KDE
  if(typeof(fhat$x) == "list"){
    fhat$x <- data.matrix(fhat$x)
  }
  if(if2D){
    imgName <- paste(imgDir, "/", genLabel(m,n,pilot), ".html", sep="")
    png(imgName)
    plot(fhat, display=display2D, cont=percs, asp=1, col=colorSingle)
    dev.off()
  }
  else{
    imgName <- paste(imgDir, "/", genLabel(m,n,pilot), "lhtml", sep="")
    plot(fhat, display="rgl", cont=percs, asp=1, col=colorSingle, alpha=opacitySingle)
    scene <- scene3d()
    saveWidget(rglwidget(scene), file=imgName)
    rgl.close()
  }
  vols <- vector()
  for(perc in percs){
    vols <- append(vols, calcKernelVol(fhat,perc))
  }
  return(vols)
}

# load data
raw_shark_data <- arc.open("C:/Users/Kevin/Documents/CISC498/MarinelandDemo/Marineland Demo/Marineland_ZooMonitor_3D_MBV_Depths.shp")
shark_data_df<- arc.select(shark_data)

# pre-processing
shark_data = select(shark_data_df, "UTMx", "UTMy", "DepthM_MBV")
colnames(shark_data) <- c("X", "Y", "Z")
shark_data <- na.omit(shark_data)






























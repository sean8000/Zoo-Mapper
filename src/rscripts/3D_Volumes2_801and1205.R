# Load required libraries
library (ks)
library (rgl)
library (misc3d)
library(readxl)
library(dplyr)
library(htmlwidgets)

# Define functions
calcKernelVol <- function(fhat, perc) { # Calculates perc% kernel volume
  ct <- contourLevels(fhat, cont=perc, approx=TRUE)
  vol.voxel <- prod(sapply(fhat$eval.points, diff)[1,]) 
  no.voxel <- sum(fhat$estimate>ct) 
  vol<- no.voxel*vol.voxel
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

genBounds <- function(data1, data2) { # Generate bounds for two volumes
  data <- rbind(data1, data2)
  mins <- c(min(data$X), min(data$Y), min(data$Z))
  maxs <- c(max(data$X), max(data$Y), max(data$Z))
  bounds <- c(mins, maxs)
  return(bounds) }

KDETrialSingle <- function(data, percs, m, n, pilot, imgDir) { # Tries KDE with given settings for single volumes
  band <- Hpi(data, nstage=n, pilot=pilot)*m
  fhat <- kde(data, H=band)
  if(typeof(fhat$x) == "list") { fhat$x  <- data.matrix(fhat$x) }
  imgName <- paste(imgDir,"/",genLabel(m,n,pilot),".html",sep="")
  plot(fhat, display="rgl", cont=percs, asp=1)
  scene <- scene3d()
  saveWidget(rglwidget(scene), file=imgName)
  rgl.close()
  vols <- vector()
  for(perc in percs) { vols <- append(vols, calcKernelVol(fhat,perc)) }
  return(vols) }

KDETrialDouble <- function(data1, data2, percs, m, n, pilot, imgDir) { # Tries KDE with given settings for two volumes
  band1 <- Hpi(data1, nstage=n, pilot=pilot)*m
  band2 <- Hpi(data2, nstage=n, pilot=pilot)*m
  bounds <- genBounds(data1, data2)
  fhat1 <- kde(data1, H=band1, xmin=bounds[1:3], xmax=bounds[4:6])
  if(typeof(fhat1$x) == "list") { fhat1$x  <- data.matrix(fhat1$x) }
  fhat2 <- kde(data2, H=band2, xmin=bounds[1:3], xmax=bounds[4:6])
  if(typeof(fhat2$x) == "list") { fhat2$x  <- data.matrix(fhat2$x) }
  imgName <- paste(imgDir,"/",genLabel(m,n,pilot),".html",sep="")
  plot(fhat1, display="rgl", cont=percs, asp=1)
  plot(fhat2, display="rgl", cont=percs, asp=1, add=TRUE, col=cm.colors(length(percs)))
  scene <- scene3d()
  saveWidget(rglwidget(scene), file=imgName)
  rgl.close()
  vols <- vector()
  for(perc in percs) {
    vols <- append(vols, calcKernelVol(fhat1, perc))
    vols <- append(vols, calcKernelVol(fhat2, perc))
    vols <- append(vols, calcIntersect(fhat1, fhat2, perc)) }
  return(vols) }

KDESingle <- function(data, percs, ms, ns, pilots, imgDir) { # Performs KDE for single volume with all combinations of settings
  volumes <- data.frame(matrix(ncol=1+length(percs), nrow=0))
  colnames(volumes) <- c("Label", paste(percs))
  for(m in ms) {
    for(n in ns) {
      for(pilot in pilots) {
        vols <- KDETrialSingle(data, percs, m, n, pilot, imgDir)
        row <- data.frame(c(genLabel(m,n,pilot), as.list(vols)))
        colnames(row) <- c("Label", paste(percs))
        volumes <- rbind(volumes, row) }}}
  return(volumes) }

KDEDouble <- function(data1, data2, percs, ms, ns, pilots, imgDir) { # Performs KDE for two volumes with all combinations of settings
  volumes <- data.frame(matrix(ncol=1+3*length(percs), nrow=0))
  prefixes <- c("V1", "V2", "V&")
  volnames <- c(outer(prefixes, paste(percs), paste))
  colnames(volumes) <- c("Label", volnames)
  for(m in ms) {
    for(n in ns) {
      for(pilot in pilots) {
        vols <- KDETrialDouble(data1, data2, percs, m, n, pilot, imgDir)
        row <- data.frame(c(genLabel(m,n,pilot), as.list(vols)))
        colnames(row) <- c("Label", volnames)
        volumes <- rbind(volumes, row) }}}
  return(volumes)
}

prepData <- function(raw, name, nameCol, xCol, yCol, zCol, zIncr) { # Transforms the data into a usable form
  data <- raw[raw[nameCol] == name,] # Select only rows corrsponding to desired animal
  data <- select(data, xCol, yCol, zCol) # Select coordinate columns as X,Y,Z
  data <- na.omit(data) # Remove rows with missing data
  colnames(data) <- c("X", "Y", "Z") # Rename columns to X,Y,Z
  data[,3] <- data[,3] + runif(nrow(data), -zIncr, 0) # Add noise to Z
  return(data) }

run <- function(raw, excluded, nameCol, xCol, yCol, zCol, zIncr, percs, ms, ns, pilots, dir) { # Runs program
  names <- unique(raw[nameCol])
  colnames(excluded) <- nameCol
  names <- anti_join(names, excluded, by=nameCol)
  if(! dir.exists(dir)) { dir.create(dir) }
  for(i in 1:nrow(names)) {
    name <- as.character(names[i,])
    data <- prepData(raw, name, nameCol, xCol, yCol, zCol, zIncr)
    imgDir <- paste(dir,"/",name,sep="")
    if(! dir.exists(imgDir)) { dir.create(imgDir) }
    volumes <- KDESingle(data, percs, ms, ns, pilots, imgDir)
    print(paste(name,":",sep=""))
    print(volumes) }
  if(nrow(names) > 1) {
    for(i in 1:(nrow(names)-1)) {
      name1 <- as.character(names[i,])
      data1 <- prepData(raw, name1, nameCol, xCol, yCol, zCol, zIncr)
      for(j in (i+1):nrow(names)) {
        name2 <- as.character(names[j,])
        data2 <- prepData(raw, name2, nameCol, xCol, yCol, zCol, zIncr)
        tag <- paste(name1,"&",name2)
        imgDir <- paste(dir,"/",tag,sep="")
        if(! dir.exists(imgDir)) { dir.create(imgDir) }
        volumes <- KDEDouble(data1, data2, percs, ms, ns, pilots, imgDir)
        print(paste(tag,":",sep=""))
        print(volumes) }}}
}

# Set parameters
# zIncr is top and middle depths
dir <- "C:/Users/nancy/Desktop/R"
nameCol <- "Focal_Shar"
excluded <- data.frame(c("Calibration"))
xCol <- "LongUTM"
yCol <- "LatUTM"
zCol <- "DepthM"
zIncr <- 4.571777 - 3.047851
percs <- c(0,95)
ms <- c(1,5)
ns <- c(1)
pilots <- c("samse", "unconstr", "dscalar", "dunconstr")

# Load data 
path <- "C:/Users/nancy/Desktop/R/FinalShark_1205_forR.xls"
raw <- read_excel(path,sheet=1)

# Run Program
run(raw, excluded, nameCol, xCol, yCol, zCol, zIncr, percs, ms, ns, pilots, dir)
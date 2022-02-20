#This script is based on the blog posts from the link below.
#https://smathermather.com/2017/02/16/quantitative-analysis-of-gorilla-movement-and-r-stat-part-3-monkey/

# Load the adehabitatHR library
# Load appropriate libraries for loading and manipulating data
library(sp) # Spatial data objects in R
library(rgdal) # Geospatial Data Abstraction Library
library(adehabitatHR) # Adehabitat HomeRange
library(readr) # File read capacity
library(rgeos) # Geometric calculation to be used later
library(maptools) # more spatial stuff

#add data
loc_int_tot <-
  read.csv("C:/Users/jtayl/Desktop/testr/el.csv") #reads in the csv of elephant location data

# We need to add a data filter here... .
# For now, we assign just the columns we need for HR calculation
# This filters out all of the unecessary data and works with just the xy data and the id of the elephant
loc_int_totf <- loc_int_tot[,c('X','Y', 'id')]

# Use sp library to assign coordinates and projection
coordinates(loc_int_totf) <- c("X", "Y")

#to make this work with another data set just replace X, Y, and id  with the names of the corresponding columns are from your data set and set the path
# to your dataset in the read statement

# utmzone needs to be fixed
# proj4string acquired at spatialreference.org
proj4string(loc_int_totf) <- CRS("+proj=utm +zone=35 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs") 

# Estimating the utilization distribution using "reference" bandwidth
kud <- kernelUD(loc_int_totf,grid=400,extent=.4)

# Calculates the homerange area taken up from 50-95% at 5% increments
#outputs sizes in m2
kernel.area(kud, percent = seq(50, 95, by = 5),
            unin = c("m"),
            unout = c("m2"), standardize = FALSE)

# Display the utilization distribution
image(kud)

# Estimate the homerange from the utilization distribution
#homerange <- getverticeshr(kud,95)
plot(homerange,col = rgb(red = 1, green = 0, blue = 0, alpha = 0.5), #plots the location data
     pch = 16, cex = 4)

# Calculate home range sizes
# outputs sizes in hectares
as.data.frame(homerange)

# Calculate home range sizes for every 5% from 50-95%
#ii <- kernel.area(kud, percent=seq(1, 99, by=1))
#plot(ii)

# Write out data
#writeOGR(homerange, getwd(),      #this currently does not work a shapefile is created but nothing gets displayed upon import into ArcPro
#         "homerange", driver="ESRI Shapefile")


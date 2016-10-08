#Antena Data Analysis
# Set path for data directory
setwd('')
getwd() # check the data folder path
# get R libraries
library(sp)
library(gstat)
# read data from .csv file
data <- read.csv('new.csv', header=TRUE)
data <- na.omit(data)
head(data)
summary(data)
hist(data$SignalStrength)

# Define co-ordinates
coordinates(data) <- c('Lon','Lat')
proj4string(data) <- CRS("+proj=longlat +datum=WGS84") # CRS("+init=epsg:4326")

# Spatial plots
# 1. bubble plot
bubble(data, "SignalStrength", col=c("#00ff0088", "#00ff0088"), main = "signal strength")

# bounding box selection
bbPoints <- bbox(data)
# check class of points
class(bbPoints)
class(data)
# construct a grid of locations to predict at
grid <- expand.grid(x=seq(bbPoints[1:1],bbPoints[3:3],0.001), y=seq(bbPoints[2:2],bbPoints[4:4],0.001))
plot(grid)
# convert grid to a SpatialPoints object
coordinates(grid) <- c('x','y')
proj4string(grid) <- CRS("+proj=longlat +datum=WGS84") # CRS("+init=epsg:4326")
summary(grid)
# and tell sp that this is a grid
gridded(grid) <- TRUE

# 1. IDW Spatial Interpolation
sampinterp.idw <- idw(SignalStrength~1, data, grid, idp=4)
# plot spatial interpolation
spplot(sampinterp.idw,'var1.pred', scales=list(draw=TRUE))

# Save layer as geotiff
require(raster)
r = raster(sampinterp.idw["var1.pred"])
plot(r)
# check file name
writeRaster(r,"r_9.tiff","GTiff")

# TODO:
# 2. Kriging Interpolation
#sampinterp.idw <- krige(SignalStrength~1, data, grid) # Working ?? 

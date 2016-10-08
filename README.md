GSMCoverage
===========
GSMCoverage is compilation of Python and R code for analyzing the GSM Signal (.log) file obtained from Android app. Antennas. It has two main components, A. Geo-coded GSM Signal Extractor (based on Python implementation), B. Geospatial Signal Data Analysis tool (based on R software)


A. Geocoded Signal Extractor
===========
The Antennas app. provides interface to capture the GPS enabled GSM/CDMA signal strength. This signal strength is logged periodically in a log file. The Geo-coded Signal Extractor comprises of three different ways to extract the data from .log file. 


1. A method for extracting the best signal strength for best location (Best location is given by GPS reading)
	A. In PgSQL .SQL format 
	B. .csv format

	
2. A method for extracting all GSM signal strengths (i.e. from sampled available networks) for best location (Best location is given by GPS reading)
	A. In PgSQL .sql format 
	B. .csv format

3. A method for extracting all GSM signal strengths (i.e. from sampled available networks) with all details for best location (Best location is given by GPS reading)
	Each row comprises of 
	Operator ID, network ID/Antena ID/CID, Sampling Time, Latitude, Longitude, Signal Strength 


B. Antenna Signal Data Processing tool
===========
R Script to convert .csv into raster Geotiff file (csvToGeotiff.R). 


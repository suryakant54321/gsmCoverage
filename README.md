gsmCoverage
===========
Py GSM Signal Extractor
-----------------------
It comprises of following major sections 
1. A method for extracting the best signal strength for best location (Best location is given by GPS reading)
	A. In PgSQL .SQL format 
	B. .csv format
2. A method for extracting all GSM signal strengths (i.e. from sampled available networks) for best location (Best location is given by GPS reading)
	A. In PgSQL .sql format 
	B. .csv format
3. A method for extracting all GSM signal strengths (i.e. from sampled available networks) with all details for best location (Best location is given by GPS reading)
	Each row comprises of 
	Operator ID, network ID/Antena ID/CID, Sampling Time, Latitude, Longitude, Signal Strength 
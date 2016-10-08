#/usr/bin/python
# -*- coding: utf-8 -*-
"""
# Objectives: Extract content from log files.
"""
import os, re, time, shutil, string
# Set / change configurations to extract details
from LibGSMConfig import *
# import modules to extract perticular information
from LibGSMProcess import *
import time
# Extract data from all log files
MyGSMallFiles = ProcessMyAllFiles(InDirName, OutDirName)
#
print ("Total %s Files found\n")%(len(MyGSMallFiles))
#print "Number of samples in this file are %s"%(len(DataTemp))
TotalDataPoints = 0
for fileData in range(0,len(MyGSMallFiles)):
    DataTemp = MyGSMallFiles[fileData]
    print(len(DataTemp))
    TotalDataPoints = TotalDataPoints + len(DataTemp)
    for i in range(0,len(DataTemp)):
        #print DataTemp[i][0][0]
        # Generate one SQL File
        if CreatePgSQLfile == "TRUE":          
            # 1. Consider one location at best strength
            GenMyBsBl = GetBsBl(DataTemp[i])
            # Generate SQL lines
            MySQLout = GenerateSQL(GenMyBsBl, SQLTableName)#from lat, lon and signal strength
            WriteSQLfile = open(SQLfileName, "a").write(MySQLout)
        # Generate one CSV File
        if CreateCSVfile == "TRUE":
            # 1. Consider one location at best strength
            GenMyBsBl = GetBsBl(DataTemp[i])
            CSVData = ("%s,%s,%s\n")%(GenMyBsBl[0],GenMyBsBl[1],GenMyBsBl[2])
            WriteCSVfile = open(CSVfileName, "a").write(CSVData)
        # 2. Consider all networks at best location
        if ExtractAllGSM =="TRUE":
            GenMyAllNetworks = GetAllNetBestLoc(DataTemp[i])
            #print len(GenMyAllNetworks)
            for data in range(0,len(GenMyAllNetworks)):
                SQLDataString = GenerateSQL(GenMyAllNetworks[data], AllSQLTableName)
                WriteSQLfileU = open(AllSQLFileName, "a").write(SQLDataString)
                AllCSVdataString = ("%s,%s,%s\n")%(GenMyAllNetworks[data][0],GenMyAllNetworks[data][1],GenMyAllNetworks[data][2])
                #print AllCSVdataString
                WriteCSVfileU = open(AllCSVFileName, "a").write(AllCSVdataString)
        # 3. Extract dateTime, networkAntena, gps_source, phone_type, network_type, operator_id,
        # and Lat, Lon, SignalStrength
        if ExtractAllDetails == "TRUE":
            ExtractLogDetails = GetAllLogDetails(DataTemp[i]) 
            #print len(ExtractLogDetails)
            for MyD in range (0, len(ExtractLogDetails)):
                GetSQLDetailString = GenerateDetailSQL(ExtractLogDetails[MyD], DetailsSQL)
                WriteSQLfileD = open(DetailsSQLFile, "a").write(GetSQLDetailString)
                # e.g. dateTime, networkAntena, gps_source, phone_type, network_type, operator_id, Lat, Lon, SignalStrength
                shrt = ExtractLogDetails[MyD]
                DetailCSVString = ("%s,%s,%s,%s,%s,%s,%s,%s,%s\n")%(shrt[3], shrt[4],shrt[5],shrt[6],shrt[7],shrt[8],shrt[0],shrt[1],shrt[2])
                #print DetailCSVString
                WriteCSVfileD = open(DetailsCSVFileName, "a").write(DetailCSVString)
print ("Total %s samples are retrived \n")%(TotalDataPoints)

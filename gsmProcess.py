import os, re, time, shutil, string
from LibGSMProcess import * 
#
InDirName = "new"
OutDirName = "done"
####
# Section 1
# A. Dynamic Settings for SQL write
CreatePgSQLfile = "TRUE"
#****
if CreatePgSQLfile == "TRUE":
    SQLfileName = "data.sql"
    SQLTableName = "myGSMdata"
    PgSQLTable = ("CREATE TABLE %s \n (gid serial NOT NULL,\n signal_strength numeric,\n geog geography(MultiPoint,4326)) \n WITH (OIDS=TRUE); \n ALTER TABLE %s OWNER TO postgres;\n")%(SQLTableName, SQLTableName)
    WriteSQLfile = open(SQLfileName, "a").write(PgSQLTable)
# B. Dynamic Settings for CSV write
CreateCSVfile = "TRUE"
#****
if CreateCSVfile == "TRUE":
    CSVfileName = "new.csv"
    FirstCSVLine = "Lat,Lon,SignalStrength\n"
    WriteCSVfile = open(CSVfileName, "a").write(FirstCSVLine)
####
# Section 2
# For extracting all GSM signales sampled by a device
# Create SQL and CSV together
ExtractAllGSM = "TRUE"
if ExtractAllGSM == "TRUE":
    AllSQLTableName = "myTable"
    AllSQLFileName = "myPgSQL.sql"
    AllPgSQLTable = ("CREATE TABLE %s \n (gid serial NOT NULL,\n signal_strength numeric,\n geog geography(MultiPoint,4326)) \n WITH (OIDS=TRUE); \n ALTER TABLE %s OWNER TO postgres;\n")%(AllSQLTableName, AllSQLTableName)
    AllWriteSQLfile = open(AllSQLFileName, "a").write(AllPgSQLTable)
    AllCSVFileName = "myAll.csv"
    AllFirstCSVLine = "Lat,Lon,SignalStrength\n"
    AllWriteCSVfile = open(AllCSVFileName, "a").write(AllFirstCSVLine)

####
# Section 3
# For Extracting all details of GSM sampling


#**************************************************   
# Extract data from all log files
MyGSMallFiles = ProcessMyAllFiles(InDirName, OutDirName)

#
print len(MyGSMallFiles)
#print "Number of samples in this file are %s"%(len(DataTemp))
for fileData in range(0,len(MyGSMallFiles)):
    DataTemp = MyGSMallFiles[fileData]
    #TotalDataPoints = TotalDataPoints + len(DataTemp)
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
        # To Do
        # 3. Store date, network antena / source id, lat, lon and signal strength
#print ("Total %s samplings are retrived")%(TotalDataPoints)

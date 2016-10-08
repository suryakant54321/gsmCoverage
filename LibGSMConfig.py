#/usr/bin/python
# -*- coding: utf-8 -*-
"""
# Author: Suryakant Sawant
# Date:
# Objectives: 
# 1. Read all log files of Antennas folder
# 2. Extract location, signal strength information from log files
# 3. Convert extracted information into required format 
#    (i.e. CSV, SQL table, etc.) with required parameters
"""
InDirName = "new"
OutDirName = "done"
####
# Section 1
# A. Dynamic Settings for SQL write
CreatePgSQLfile = "FALSE"
#****
if CreatePgSQLfile == "TRUE":
    SQLfileName = "data.sql" # Change if required
    SQLTableName = "myGSMdata"
    PgSQLTable = ("CREATE TABLE %s \n (gid serial NOT NULL,\n signal_strength numeric,\n geog geography(MultiPoint,4326)) \n WITH (OIDS=TRUE); \n ALTER TABLE %s OWNER TO postgres;\n")%(SQLTableName, SQLTableName)
    WriteSQLfile = open(SQLfileName, "a").write(PgSQLTable)
#
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
ExtractAllGSM = "FALSE"
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
ExtractAllDetails = "FALSE"
if ExtractAllDetails == "TRUE":
    DetailsSQL = "myTable"
    DetailsSQLFile = "myPgSQLDetails.sql"
    DetailsPgSQLTable = ("CREATE TABLE %s \n (gid serial NOT NULL, \n time_stamp timestamp with time zone NOT NULL, \n network_antena character varying(10), \n gps_source character varying(2), \n phone_type character varying(10), \n network_type character varying(10), \n operator_id character varying(10),\n signal_strength numeric, \n geog geography(MultiPoint,4326)) \n WITH (OIDS=TRUE); \n ALTER TABLE %s OWNER TO postgres; \n")%(DetailsSQL, DetailsSQL)
    DetailsWriteSQL = open(DetailsSQLFile, "a").write(DetailsPgSQLTable)
    DetailsCSVFileName = "myAllDetails.csv"
    DetailsFirstCSVLine = "dateTime, phone_type, network_type, operator_id, networkAntena, gps_source, Lat, Lon, SignalStrength\n"
    DetailsWriteCSV = open(DetailsCSVFileName, "a").write(DetailsFirstCSVLine)
#**************************************************   

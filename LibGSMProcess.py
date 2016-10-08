#/usr/bin/python
# -*- coding: utf-8 -*-
"""
Objectives: Extract content from log files.
"""
from details import *   
import os, re, time, shutil, string
os.chdir(os.getcwd())

# Open one by one file from given directory and returns the multilist 
def ProcessMyAllFiles(InDirName, OutDirName):
    AllFilesData = []
    for fils in os.listdir(InDirName):
	print(fils)
        if fils.endswith(".log"):
            currentPath = ("%s/%s")%(InDirName,fils)
            movePath = OutDirName
            #print(movePath)
            sampleBlock = 0
            aa = -1
            DataAll = []
            DataTemp = []
            for Uline in open(currentPath):
                if Uline != '\n':#given line is not blank 
                    Uline2 = re.split(",",Uline)
                    #Uline2 = Uline2.rstrip('\n')
                    GSMrecord = GetGSMrecord(Uline2)
                    ActiveGSM = GetActiveGSM(Uline2)
                    GSMlines = GetGSMlines(Uline2)
                    NetLocation = GetNetLocation(Uline2)
                    BestLocation = GetBestLocation(Uline2)
                    if GSMrecord != None:
                        DataTemp.append(sampleBlock)
                        aa = aa+1
                        DataAll = []
                        DataAll.append(GSMrecord)
                    if ActiveGSM != None:
                        DataAll.append(ActiveGSM)
                    if GSMlines != None:
                        DataAll.append(GSMlines)
                    if NetLocation != None:
                        DataAll.append(NetLocation)
                    if BestLocation != None:
                        DataAll.append(BestLocation)
                        DataTemp[aa]=DataAll
            AllFilesData.append(DataTemp)
            shutil.move(currentPath, movePath)
    return AllFilesData
# Colllect IMP part one by one
def GetGSMrecord(LineData):
    myRecord = []
    if LineData[0] =='Record':
        myRecord.append(LineData[1])
        myRecord.append(LineData[2])
        myRecord.append(LineData[3])
        myRecord.append(LineData[4])
        myRecord.append(LineData[5].rstrip('\n'))
        return myRecord
# Get active GSM
def GetActiveGSM(activeLine):
    ActiveGSMdetails = []
    #print activeLine[0]
    if activeLine[0] == 'ACTIVE GSM':
        ActiveGSMdetails.append(activeLine[1])
        ActiveGSMdetails.append(activeLine[2])
        ActiveGSMdetails.append(activeLine[3].rstrip('\n'))
        return ActiveGSMdetails
# Get GSM lines if any
def GetGSMlines(gsmLine):
    myGSMline = []
    if gsmLine[0] =='GSM':
        myGSMline.append(gsmLine[1])
        myGSMline.append(gsmLine[2])
        myGSMline.append(gsmLine[3])
        myGSMline.append(gsmLine[4])
        myGSMline.append(gsmLine[5].rstrip('\n'))
        return myGSMline
# Get network location
def GetNetLocation(NetLoc):
    myNetLocation=[]
    if NetLoc[0]=='Network Location':
        myNetLocation.append(NetLoc[2])#Lat
        myNetLocation.append(NetLoc[3].rstrip('\n'))#Lon
        myNetLocation.append(NetLoc[1])#Provider
        return myNetLocation
# Get best location
def GetBestLocation(BestLoc):
    myBestLocation=[]
    if BestLoc[0]=='Best Location':
        myBestLocation.append(BestLoc[2])#Lat
        myBestLocation.append(BestLoc[3].rstrip('\n'))#Lon
        myBestLocation.append(BestLoc[1])#Provider
        return myBestLocation
# Generate SQL with best location best signal
# structure (1 Record, 1 ACTIVE GSM, 0 to n GSM, 1 Network Location, 1 Best Location)
# seperate only Active GSM and Best Location
def GetBsBl(GSMSampleBlock):
    dataInSQL = []
    #print (GSMSampleBlock[1],GSMSampleBlock[-1])
    SignalProcess = ProcessMe(GSMSampleBlock[1][2])
    SignalProcess[1] = removeGtLt(SignalProcess[1])
    if len(SignalProcess[1])>7:
        SignalProcess[1] = SignalProcess[1][2:5]
    else:
        SignalProcess[1] = SignalProcess[1][2:4]
    LatProcess = ProcessMe(GSMSampleBlock[-1][0])
    LonProcess = ProcessMe(GSMSampleBlock[-1][1])
    dataInSQL.append(LatProcess[1])
    dataInSQL.append(LonProcess[1])
    dataInSQL.append(SignalProcess[1])
    return dataInSQL
# Process for equal to sign
def ProcessMe(dataToProcess):
    ProcessedData = re.split("=",dataToProcess)
    return ProcessedData 
# Remove greater than less than sign
def removeGtLt(dataIn):
    table = string.maketrans( '', '', )
    DataIn = dataIn.translate(table,"<>")
    return DataIn
# Generate SQL from list for given table
def GenerateSQL(ListData, tableName):
    listLen = len(ListData)
    # e.g.
    # INSERT INTO field_obs_antena_3 VALUES (0, '2014-01-31 16:34:38.718' , NULL, NULL, 'N','75', GeometryFromText('MULTIPOINT ((78.210785 21.454251))',-4326));
    SQLstatement = ("INSERT INTO %s VALUES(0, '%s',GeometryFromText('MULTIPOINT (%s %s)',-4326));\n")%(tableName, ListData[2], ListData[1], ListData[0])
    return SQLstatement
# Generate all network for best location
# structure (1 Record, 1 ACTIVE GSM, 0 to n GSM, 1 Network Location, 1 Best Location)
def GetAllNetBestLoc(MyGSMsmBl):
    DataAllGood = []
    dataAllNetBest = []
    # to seperate samples with no other GSM signals
    if len(MyGSMsmBl)<5:
        mYSignal = ProcessMe(MyGSMsmBl[1][2])
        mYSignal[1] = removeGtLt(mYSignal[1])
        if len(mYSignal[1])>7:
            mYSignal[1] = mYSignal[1][2:5]
        else:
            mYSignal[1] = mYSignal[1][2:4]
        LatProcess = ProcessMe(MyGSMsmBl[-1][0])
        LonProcess = ProcessMe(MyGSMsmBl[-1][1])
        dataAllNetBest.append(LatProcess[1])
        dataAllNetBest.append(LonProcess[1])        
        dataAllNetBest.append(mYSignal[1])
        DataAllGood.append(dataAllNetBest)
    else:
        mYSignal = ProcessMe(MyGSMsmBl[1][2])
        mYSignal[1] = removeGtLt(mYSignal[1])
        if len(mYSignal[1])>7:
            mYSignal[1] = mYSignal[1][2:5]
        else:
            mYSignal[1] = mYSignal[1][2:4]
        LatProcess = ProcessMe(MyGSMsmBl[-1][0])
        LonProcess = ProcessMe(MyGSMsmBl[-1][1])
        dataAllNetBest.append(LatProcess[1])
        dataAllNetBest.append(LonProcess[1])        
        dataAllNetBest.append(mYSignal[1])
        DataAllGood.append(dataAllNetBest)
        # tricky part to extract the GSM data 
        GSMDataLength = len(MyGSMsmBl)-2
        GSMPureData = MyGSMsmBl[2:GSMDataLength]
        for aa in range(0,len(GSMPureData)):
            DataAllNewGSM = []
            GSMPureSig = ProcessMe(GSMPureData[aa][-1])
            GSMPureSig[1] = removeGtLt(GSMPureSig[1])
            if len(GSMPureSig[1])>7:
                GSMPureSig[1] = GSMPureSig[1][2:5]
            else:
                GSMPureSig[1] = GSMPureSig[1][2:4]
            DataAllNewGSM.append(LatProcess[1])
            DataAllNewGSM.append(LonProcess[1])
            DataAllNewGSM.append(GSMPureSig[1])
            DataAllGood.append(DataAllNewGSM)
    return DataAllGood
# Generate all network for best location with all other details
# structure (1 Record, 1 ACTIVE GSM, 0 to n GSM, 1 Network Location, 1 Best Location)
def GetAllLogDetails(AllDetailData):
    DataAllGood = []
    dataAllNetBest = []
    # process datetime
    DateTime = AllDetailData[0][0]
    DateTime = ProcessMe(DateTime)
    DateTime = removeGMT(DateTime[1])
    #print DateTime
    # phone Type
    PhoneType = AllDetailData[0][1]
    PhoneType = ProcessMe(PhoneType)
    PhoneType = PhoneType[1]
    #print PhoneType
    # network Type
    NetworkType = AllDetailData[0][2]
    NetworkType = ProcessMe(NetworkType)
    NetworkType = NetworkType[1]
    #print NetworkType
    # operator identification
    OperatorID = AllDetailData[0][4]
    OperatorID = ProcessMe(OperatorID)
    OperatorID = OperatorID[1]
    #print OperatorID
    # to seperate samples with no other GSM signals
    if len(AllDetailData)<5:
        # network Antena id (e.g. ACTIVE GSM, LAC=1377, CID=3533, Signal= >-52dBm)
        NetworkAntena = AllDetailData[1][1]
        NetworkAntena = ProcessMe(NetworkAntena)
        NetworkAntena = NetworkAntena[1]
        #print NetworkAntena
        #
        mYSignal = ProcessMe(AllDetailData[1][2])
        mYSignal[1] = removeGtLt(mYSignal[1])
        if len(mYSignal[1])>7:
            mYSignal[1] = mYSignal[1][2:5]
        else:
            mYSignal[1] = mYSignal[1][2:4]
        # Get latitude
        LatProcess = ProcessMe(AllDetailData[-1][0])
        # Get longitude
        LonProcess = ProcessMe(AllDetailData[-1][1])
        # Get gps_source
        myGPSsource = ProcessMe(AllDetailData[-1][2])
        #print (LatProcess,LonProcess, myGPSsource)
        #
        dataAllNetBest.append(LatProcess[1])
        dataAllNetBest.append(LonProcess[1])        
        dataAllNetBest.append(mYSignal[1])
        dataAllNetBest.append(DateTime)
        dataAllNetBest.append(PhoneType)
        dataAllNetBest.append(NetworkType)
        dataAllNetBest.append(OperatorID)
        dataAllNetBest.append(NetworkAntena)
        dataAllNetBest.append(myGPSsource[1])
        #        
        DataAllGood.append(dataAllNetBest)
    else:
        # network Antena id (e.g. ACTIVE GSM, LAC=1377, CID=3533, Signal= >-52dBm)
        NetworkAntena = AllDetailData[1][1]
        NetworkAntena = ProcessMe(NetworkAntena)
        NetworkAntena = NetworkAntena[1]
        #print ('my %s')%(NetworkAntena)
        #
        mYSignal = ProcessMe(AllDetailData[1][2])
        mYSignal[1] = removeGtLt(mYSignal[1])
        if len(mYSignal[1])>7:
            mYSignal[1] = mYSignal[1][2:5]
        else:
            mYSignal[1] = mYSignal[1][2:4]
        # Get latitude
        LatProcess = ProcessMe(AllDetailData[-1][0])
        # Get longitude
        LonProcess = ProcessMe(AllDetailData[-1][1])
        # Get gps_source
        myGPSsource = ProcessMe(AllDetailData[-1][2])
        #print (LatProcess,LonProcess, myGPSsource)
        #
        dataAllNetBest.append(LatProcess[1])
        dataAllNetBest.append(LonProcess[1])        
        dataAllNetBest.append(mYSignal[1])
        dataAllNetBest.append(DateTime)
        dataAllNetBest.append(PhoneType)
        dataAllNetBest.append(NetworkType)
        dataAllNetBest.append(OperatorID)
        dataAllNetBest.append(NetworkAntena)
        dataAllNetBest.append(myGPSsource[1])
        DataAllGood.append(dataAllNetBest)
        # tricky part to extract the GSM data 
        GSMDataLength = len(AllDetailData)-2
        GSMPureData = AllDetailData[2:GSMDataLength]
        for aa in range(0,len(GSMPureData)):
            DataAllNewGSM = []
            # GSM network Antena id (e.g. GSM, LAC=1377, CID=36392, PSC=-1, TYP=1, Signal= -103dBm)
            GSMNetworkAntena = GSMPureData[aa][1]
            GSMNetworkAntena = ProcessMe(GSMNetworkAntena)
            GSMNetworkAntena = GSMNetworkAntena[1]
            #print ('my pure %s')%(GSMNetworkAntena)
            # Signal Strength
            GSMPureSig = ProcessMe(GSMPureData[aa][-1])
            GSMPureSig[1] = removeGtLt(GSMPureSig[1])
            if len(GSMPureSig[1])>7:
                GSMPureSig[1] = GSMPureSig[1][2:5]
            else:
                GSMPureSig[1] = GSMPureSig[1][2:4]
            DataAllNewGSM.append(LatProcess[1])
            DataAllNewGSM.append(LonProcess[1])
            DataAllNewGSM.append(GSMPureSig[1])
            DataAllNewGSM.append(DateTime)
            DataAllNewGSM.append(PhoneType)
            DataAllNewGSM.append(NetworkType)
            DataAllNewGSM.append(OperatorID)
            DataAllNewGSM.append(GSMNetworkAntena)
            DataAllNewGSM.append(myGPSsource[1])
            DataAllGood.append(DataAllNewGSM)
    return DataAllGood

# Remove GMT timestamp
def removeGMT(DateTime):
    MyTable = string.maketrans( '', '', )
    DateTime = DateTime.translate(MyTable,'"')    
    MyDateTime = re.split(" GMT",DateTime)
    MyDateTime = MyDateTime[0]
    MyDateTime = re.split(":",MyDateTime)
    MyDateTime = ('%s:%s:%s.%s')%(MyDateTime[0],MyDateTime[1],MyDateTime[2],MyDateTime[3])
    return MyDateTime

# Generate Detail SQL from list for given table
def GenerateDetailSQL(ListData, tableName):
    #print (ListData)
    # e.g.
    # INSERT INTO field_obs_antena_3 VALUES (0, TimeStamp, network_antena, gps_source, phone_type, network_type, operator_id, signal_strength, GeometryFromText('MULTIPOINT ((78.210785 21.454251))',-4326));
    SQLstatement = ("INSERT INTO %s VALUES(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s',GeometryFromText('MULTIPOINT (%s %s)',-4326));\n")%(tableName, ListData[3], ListData[7], ListData[8], ListData[4], ListData[5], ListData[6], ListData[2], ListData[1], ListData[0])
    return SQLstatement

#************************************************
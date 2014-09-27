import os, re, time, shutil, string
os.chdir(os.getcwd())
#**************************************************
# 0. Open one by one file from given directory and returns the multilist 
def ProcessMyAllFiles(InDirName, OutDirName):
    AllFilesData = []
    for fils in os.listdir(InDirName):
        if fils.endswith(".log"):
            currentPath = ("%s/%s")%(InDirName,fils)
            movePath = OutDirName
            #print movePath
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
# 1: Colllect IMP part one by one
def GetGSMrecord(LineData):
    myRecord = []
    if LineData[0] =='Record':
        myRecord.append(LineData[1])
        myRecord.append(LineData[2])
        myRecord.append(LineData[3])
        myRecord.append(LineData[4])
        myRecord.append(LineData[5].rstrip('\n'))
        return myRecord
# 2: get active GSM
def GetActiveGSM(activeLine):
    ActiveGSMdetails = []
    #print activeLine[0]
    if activeLine[0] == 'ACTIVE GSM':
        ActiveGSMdetails.append(activeLine[1])
        ActiveGSMdetails.append(activeLine[2])
        ActiveGSMdetails.append(activeLine[3].rstrip('\n'))
        return ActiveGSMdetails
# 3: get GSM lines if any
def GetGSMlines(gsmLine):
    myGSMline = []
    if gsmLine[0] =='GSM':
        myGSMline.append(gsmLine[1])
        myGSMline.append(gsmLine[2])
        myGSMline.append(gsmLine[3])
        myGSMline.append(gsmLine[4])
        myGSMline.append(gsmLine[5].rstrip('\n'))
        return myGSMline
# 4: get network location
def GetNetLocation(NetLoc):
    myNetLocation=[]
    if NetLoc[0]=='Network Location':
        myNetLocation.append(NetLoc[2])
        myNetLocation.append(NetLoc[3].rstrip('\n'))
        return myNetLocation
# 5: get best location
def GetBestLocation(BestLoc):
    myBestLocation=[]
    if BestLoc[0]=='Best Location':
        myBestLocation.append(BestLoc[2])
        myBestLocation.append(BestLoc[3].rstrip('\n'))
        return myBestLocation
# 6: Generate SQL with best location best signal
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
# 7: Process for equal to sign
def ProcessMe(dataToProcess):
    ProcessedData = re.split("=",dataToProcess)
    return ProcessedData 
# 8: remove greater than less than sign
def removeGtLt(dataIn):
    table = string.maketrans( '', '', )
    DataIn = dataIn.translate(table,"<>")
    return DataIn
# 9: Generate SQL from list for given table
def GenerateSQL(ListData, tableName):
    listLen = len(ListData)
    # e.g.
    # INSERT INTO field_obs_antena_3 VALUES (0, '2014-01-31 16:34:38.718' , NULL, NULL, 'N','75', GeometryFromText('MULTIPOINT ((78.210785 21.454251))',-4326));
    SQLstatement = ("INSERT INTO %s VALUES(0, '%s',GeometryFromText('MULTIPOINT (%s %s)',-4326));\n")%(tableName, ListData[2], ListData[1], ListData[0])
    return SQLstatement
# 10: Generate all network for best location
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
#************************************************** 

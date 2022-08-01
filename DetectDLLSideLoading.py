import Utils
import DLLSideLoadedClass
import CBAPIendpoints

def DetetcDLLSideLoading(FilePath, confJson):


    # Create CB headers for all clients
    CB_headers = [
        {
            'X-Auth-Token': confJson["Clients"][x]["API-Key"],
            'Version': '12.0',
            'Accept': 'application / json',
            'Content-Type': 'application / json'
        } for x in range(len(confJson["Clients"]))
    ]

    # Read Data of DLL sideloading
    csvHeaders, csvRows = Utils.getCSVFromFile(FilePath)

    # Prepare CB EDR queries
    Results = []
    Queries = []

    ## Loop on all configured clients -- No threading
    for client in confJson["Clients"]:
        if client["Enabled"].upper() == "TRUE":
            for row in csvRows:
                if row[5].upper() == "TRUE":  # Row[5] is enabled value
                    DLLSideLoaded = DLLSideLoadedClass.DLLSideLoaded(row)
                    Queries.append(DLLSideLoaded.CheckDLLPath())
                    ProcessSearch = CBAPIendpoints.ProcessSearch(CB_headers[0], client["URL"],
                                                                 DLLSideLoaded.CheckDLLPath())
                    Results.append(ProcessSearch.Search())
                    del ProcessSearch

    return Queries, Results

def Output(Results, outputPath):
    TotalResults = 0
    TotalIncomplete = 0
    outputCSVHeader = ['DateTime', 'Sensorid', 'UserName', 'Uniqueid', 'ProcessPath', 'cmdline', 'ProcessMd5',
                       'ParentName', 'ParentMd5', 'ID in DataSheet', 'Incomplete Query']
    Utils.writeCSVFile(outputPath, "w", outputCSVHeader, "")
    Rows = []

    for i in range(len(Results)):
        TotalResults += Results[i]['total_results']
        TotalIncomplete += ({True: 1, False: 0}[Results[i]['incomplete_results']])
        if len(Results[i]['results']) == 0 and Results[i]['incomplete_results'] == True:
            Rows.append([0, 0, 0, 0, 0, 0, 0, 0, 0, i, Results[i]['incomplete_results']])
        else:
            for j in range(len(Results[i]['results'])):
                Rows.append([Results[i]['results'][j]['start'], Results[i]['results'][j]['sensor_id'],
                             Results[i]['results'][j]['username'], Results[i]['results'][j]['unique_id'],
                             Results[i]['results'][j]['path'], Results[i]['results'][j]['cmdline'],
                             Results[i]['results'][j]['process_md5'],
                             Results[i]['results'][j]['parent_name'], Results[i]['results'][j]['parent_md5'], i,
                             Results[i]['incomplete_results']])

    Utils.writeCSVFile(outputPath, "a", "", Rows)

    print("Total Processed Queries: " + str(len(Results)))
    print("Total Incomplete Queries: " + str(TotalIncomplete))
    print("Total Finding: " + str(TotalResults))

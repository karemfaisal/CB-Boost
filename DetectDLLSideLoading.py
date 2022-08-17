import Utils
import DllHijackRuleClass
import CBAPIendpoints
from cbapi.response import *
import gc
def DetetcDLLSideLoading(DLLrules, DetectSideLoadOpetions, profiles):


    # Read Data of DLL sideloading
    dllRules = Utils.getFilePathsRecursively(DLLrules, "yml")
    Data = Utils.getYamlFromFile("I:\\GIT\\CB-Boost\\HijackLibs\\yml\\microsoft\\built-in\\activeds.yml")

    # Prepare CB EDR queries
    Results = []
    Queries = []

    ## Loop on all configured clients -- No threading
    for profile in profiles:
        cb = CbResponseAPI(profile=profile)
        for rule in dllRules:
            DllHijackRule = DllHijackRuleClass.DllHijackRule(Utils.getYamlFromFile(rule))
            if DetectSideLoadOpetions == "DLLPath":
                Query = DllHijackRule.CheckDLLPath()
                if Query == "N/A":
                    del DllHijackRule
                    gc.collect()
                    continue
                Queries.append(Query)
                Results.append(cb.select(Process).where(Query))
                del DllHijackRule
                gc.collect()
            elif DetectSideLoadOpetions == "ProcessPath":
                Results.append(cb.select(Process).where(DllHijackRule.CheckProcessPath()))
                Queries.append(DllHijackRule.CheckProcessPath())
                del DllHijackRule
                gc.collect()
            else:
                Queries.append(DllHijackRule.CheckDLLPath())
                Results.append(cb.select(Process).where(DllHijackRule.CheckDLLPath()))
                Results.append(cb.select(Process).where(DllHijackRule.CheckProcessPath()))
                Queries.append(DllHijackRule.CheckProcessPath())
                del DllHijackRule
                gc.collect()
    del cb
    return Queries, Results

def Output(Results, outputPath):
    TotalResults = 0
    outputCSVHeader = ['DateTime', 'Sensorid', 'UserName', 'Uniqueid', 'ProcessPath', 'cmdline', 'ProcessMd5',
                       'ParentName', 'ParentMd5', 'ID in DataSheet']
    Utils.writeCSVFile(outputPath, "w", outputCSVHeader, "")
    Rows = []

    for i in range(len(Results)):
        TotalResults += len(Results[i])
        for j in range(len(Results[i])):
            Rows.append([Results[i][j].start.strftime("%m/%d/%Y, %H:%M:%S"), str(Results[i][j].sensor_id),
                            Results[i][j].username, Results[i][j].unique_id,
                            Results[i][j].path, Results[i][j].cmdline,
                            Results[i][j].process_md5,
                            Results[i][j].parent_name, Results[i][j].parent_md5, str(i)])
            Utils.writeCSVFile(outputPath, "a", "", Rows)
            Rows.clear()


    print("Total Processed Queries: " + str(len(Results)))
    print("Total Finding: " + str(TotalResults))

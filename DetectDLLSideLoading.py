import Utils
import DllHijackRuleClass
from cbapi.response import *
import gc
def DetetcDLLSideLoading(DLLrules, DetectSideLoadOpetions, profiles):


    # Read Data of DLL sideloading
    dllRules = Utils.getFilePathsRecursively(DLLrules, "yml")

    print("\n{} Rules are getting parsed!, Please wait".format(len(dllRules)))
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
    print("\n{} Queries are prepared!".format(len(Results)))
    return Queries, Results

def Output(Results, outputPath):

    TotalResults = 0
    outputCSVHeader = ['DateTime', 'Sensorid', 'UserName', 'Uniqueid', 'ProcessPath', 'cmdline', 'ProcessMd5',
                       'ParentName', 'ParentMd5', 'ID in DataSheet']
    Utils.writeCSVFile(outputPath, "w", outputCSVHeader, "")
    Rows = []
    Exception = []
    for i in range(len(Results)):
        try:
            TotalResults += len(Results[i])
            if i%5 == 0 :
                print("{} Queries are executed!".format(i+1))
                print("Current Resutls: {} ".format(TotalResults))
            for j in range(len(Results[i])):
                Rows.append([Results[i][j].start.strftime("%m/%d/%Y, %H:%M:%S"), str(Results[i][j].sensor_id),
                                Results[i][j].username, Results[i][j].unique_id,
                                Results[i][j].path, Results[i][j].cmdline,
                                Results[i][j].process_md5,
                                Results[i][j].parent_name, Results[i][j].parent_md5, str(i)])
                Utils.writeCSVFile(outputPath, "a", "", Rows)
        except Exception as e:
            print("Exception happend!!!:\n" + str(e) + "\n")
            Exception.append(str(e))
        Rows.clear()


    print("\nTotal Executed Queries: " + str(len(Results)))
    print("\nTotal Exceptions: " + str(len(Exception)))
    print("Total Finding: " + str(TotalResults))

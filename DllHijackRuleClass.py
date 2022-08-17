class DllHijackRule:
    ProcessName = []
    ProcessPath = []
    DLLName = ""
    DLLPath = []
    def __init__(self, Data):
        for x in Data['VulnerableExecutables']: self.ProcessName.append(x['Path'].split("\\")[-1])
        for x in Data['VulnerableExecutables']:
            if x['Type'] == "Sideloading" : self.ProcessPath.append(x['Path'].replace("%SYSTEM32","C:\\windows\\system32").replace("%SYSWOW64%","C:\\windows\\syswow64"))
        self.DLLName = Data['Name']
        if len(self.ProcessPath)> 0 :
            for x in Data['ExpectedLocations']: self.DLLPath.append(x.replace("%SYSTEM32%", "C:\\windows\\system32").replace("%SYSWOW64%", "C:\\windows\\syswow64") + "\\"+ self.DLLName)


    def CheckDLLPath(self):
        if len(self.DLLPath) == 0:
            return "N/A"
        Query = "modload:" + self.DLLName + " AND (-modload: " + self.DLLPath[0].lstrip().replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        for i in range(1,len(self.DLLPath)):
            Query += " or" + " -modload: " + self.DLLPath[i].lstrip().replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        Query += ")"

        return Query

    def CheckProcessPath(self):
        Query = "process_name:" + self.ProcessName + " AND (-path: " + self.ProcessPath[0].lstrip().replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        for i in range(1,len(self.ProcessPath)):
            Query += " or" + " -path: " + self.ProcessPath[i].lstrip().replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        Query += ")"
        return Query

    def __del__(self):
        self.ProcessName.clear()
        self.ProcessPath.clear()
        self.DLLPath.clear()
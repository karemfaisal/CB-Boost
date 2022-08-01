class DLLSideLoaded:
    ProcessName = ""
    ProcessPath = []
    DLLName = ""
    DLLPath = []
    Signature = ""
    def __init__(self, Data):
        self.ProcessName = Data[0].lstrip()
        self.ProcessPath = Data[1].split(",")
        self.DLLName = Data[2].lstrip()
        self.DLLPath = Data[3].split(",")
        self.Signature = Data[4].lstrip()

    def CheckDLLPath(self):
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
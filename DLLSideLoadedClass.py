class DLLSideLoaded:
    ProcessName = ""
    ProcessPath = []
    DLLName = ""
    DLLPath = []
    Signature = ""
    def __init__(self, Data):
        self.ProcessName = Data[0]
        self.ProcessPath = Data[1].split(",")
        self.DLLName = Data[2]
        self.DLLPath = Data[3].split(",")
        self.Signature = Data[4]

    def CheckDLLPath(self):
        Query = "modload:" + self.DLLName + " AND (-modload: " + self.DLLPath[0].replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        for i in range(1,len(self.DLLPath)):
            Query += " or" + " -modload: " + self.DLLPath[i].replace(" ","\\ ").replace("(","\\(").replace(")","\\)")
        Query += ")"
        return Query


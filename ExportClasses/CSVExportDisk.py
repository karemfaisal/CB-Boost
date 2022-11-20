import Utils

class CSVExportDisk():

    def export(self,destination,data):
        Utils.writeCSVFile(destination, "w", data[0], "")
        Utils.writeCSVFile(destination, "a", "", data[1:-1])
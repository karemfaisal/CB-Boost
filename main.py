from RuleClasses.GetActivity import *
import DetectDLLSideLoading
import argparse
import logging
import ExportClasses.CSVExportDisk
import Utils
parser = argparse.ArgumentParser()

####
if __name__ == '__main__':
    # Carbon Black Looging
    root = logging.getLogger()
    root.addHandler(logging.StreamHandler())
    logging.getLogger("cbapi").setLevel(logging.DEBUG)

    # define exporters
    csvexporter = ExportClasses.CSVExportDisk.CSVExportDisk()

    # Argument parser
    parser.add_argument("-r", "--rules",
                        help="path to the CB-Boost yaml file path")
    parser.add_argument("-p", "--profiles",
                        help="profiles name for running the API separated by ','  ex: Karem,Ali")
    args = parser.parse_args()

    # Get clients info
    profiles = []
    if args.profiles == None:
        profiles.append("default")
    else:
        profiles = args.profiles.split(",")


    # Check tool option
    if args.rules != None:
        # Yml rules parsing
        YMLObjects = Utils.getYamlFromFile(args.rules)

        for YmlObject in YMLObjects:
            if YmlObject['RuleClass'] == "GetActivity":
                if YmlObject['destinationFormat'].lower() == "CSV".lower():
                    GetActivityObj = GetActivity(YmlObject, csvexporter).execute()
    else:
        print("[Error!] Yaml rule file must be inserted")
        exit()






    #     if args.DLLrules != None:
    #         if args.output != None:
    #             outputPath = args.output
    #         else:
    #             outputPath = "Output-DLLSideLoad.csv"
    #
    #         Queries, Results = DetectDLLSideLoading.DetetcDLLSideLoading(args.DLLrules, args.DetectDllHijack, profiles)
    #         DetectDLLSideLoading.Output(Results, outputPath)
    #     else:
    #         print("Specify a csv file contains the data of DLL sideloading.")
    # else:
    #     print("specify an action!!")


    print ("End!")

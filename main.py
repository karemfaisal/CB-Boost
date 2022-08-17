import os.path

import Utils
import DetectDLLSideLoading
import argparse
from cbapi.response import *
parser = argparse.ArgumentParser()


parser.add_argument("-DDH", "--DetectDllHijack", choices=["DLLPath", "ProcessPath", "All"],
                    help="Detect DLL SideLoading/OrderHijacking attempts")
parser.add_argument("-f", "--file",
                    help="Path to the file used")
parser.add_argument("-dr", "--DLLrules",
                    help="Path to DLLHijack rules folder")
parser.add_argument("-p", "--profiles",
                    help="profiles name for running the API separated by ,  ex: Karem,Ali")
parser.add_argument("-o", "--output",
                    help="Path to the output file)")
args = parser.parse_args()

Data = Utils.getYamlFromFile("I:\\GIT\\CB-Boost\\HijackLibs\\yml\\microsoft\\built-in\\activeds.yml")
# Get clients info
profiles = []
if args.profiles == None:
    profiles.append("default")
else:
    profiles = args.profiles.split(",")

# Check tool option
if args.DetectDllHijack != None:
    if args.DLLrules != None:
        if args.output != None:
            outputPath = args.output
        else:
            outputPath = "Output-DLLSideLoad.csv"

        Queries, Results = DetectDLLSideLoading.DetetcDLLSideLoading(args.DLLrules, args.DetectDllHijack, profiles)
        DetectDLLSideLoading.Output(Results, outputPath)
    else:
        print("Specify a csv file contains the data of DLL sideloading.")
else:
    print("specify an action!!")


print ("End!")

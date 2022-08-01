import Utils
import DetectDLLSideLoading
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("-DSL", "--DetectSideLoad", choices=["DLLPath", "ProcessPath", "All"],
                    help="Detect DLL SideLoading/OrderHijacking attempts")
parser.add_argument("-f", "--file",
                    help="Path to the file used")
parser.add_argument("-c", "--config",
                    help="Path to the CB EDR's config file - default (CB.conf)")
parser.add_argument("-o", "--output",
                    help="Path to the output file)")
args = parser.parse_args()


# Get clients info
if args.config == "":
    confJson = Utils.getJsonFromFile("CB.conf")
else:
    confJson = Utils.getJsonFromFile(args.config)

# Check tool option
if args.DetectSideLoad != None:
    if args.file != None:
        if args.output != None:
            outputPath = args.output
        else:
            outputPath = "Output-DLLSideLoad.csv"
        Queries, Results = DetectDLLSideLoading.DetetcDLLSideLoading(args.file, args.DetectSideLoad, confJson)
        DetectDLLSideLoading.Output(Results, outputPath)
    else:
        print("Specify a csv file contains the data of DLL sideloading.")
else:
    print("specify an action!!")


print ("End!")

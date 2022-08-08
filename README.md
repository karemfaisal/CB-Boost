# CB-Boost
CB-Boost is a tool utilized Carbon Black API to run Incident response actions, and detection use cases that requires automation.

CB-Boost's detection use cases are not meant to be full detection use cases, but it only contains what requires programmatically analysis of the output of certain use cases. To create a simple use case just do it using watchlists.

CB-Boost's IR capabilities is coming soon!.




## Engine Capabilities

### Detection uses cases
* [x] Detect DLL sideLoading/SearchOrderHijacking depending on
  * [x] DLL Path
  * [x] Process Path

### Incident response
Coming Soon!




## How it works?

1. Update CB config "CB.conf" with CB EDR data.
2. for DLL Sideloading/SearchOrderHijacking,  Add any additional data to the DLLSideLoading csv file.
3. run the tool

```shell
python3 main.py -h
```

```shell
[*Output]
usage: main.py [-h] [-DSL {DLLPath,ProcessPath,All}] [-f FILE] [-c CONFIG]
               [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -DSL {DLLPath,ProcessPath,All}, --DetectSideLoad {DLLPath,ProcessPath,All}
                        Detect DLL SideLoading/OrderHijacking attempts
  -f FILE, --file FILE  Path to the file used
  -c CONFIG, --config CONFIG
                        Path to the CB EDR's config file - default (CB.conf)
  -o OUTPUT, --output OUTPUT
                        Path to the output file)
```

1. For DLL Sideloading/SearchOrderHijacking detection
```shell
python3 main.py -DSL DLLPath -f "DLLSideLoading data.csv" -c "CB.conf" -o "output-DLLSearOrderHijacking.csv"
```


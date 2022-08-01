# CB-Boost
This repository contains an engine that utilize Carbon Black EDR for boosting its IR and detection capabilities.



### Engine Capabilities

* [x] Detect DLL sideLoading/SearchOrderHijacking depending on
  * [ ] DLL Path
  * [ ] Process Path



### How to use

1. Update CB config "CB.conf" with CB EDR data.
2. Add any additonal data to the DLLSideLoading csv
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

```shell
python3 main.py -DSL DLLPath -f "DLLSideLoading data.csv" -c "CB.conf" -o "output-DLLSearOrderHijacking.csv"
```


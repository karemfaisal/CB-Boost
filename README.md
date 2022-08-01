# CB-Boost
This repository contains an engine that utilize Carbon Black EDR for boosting its IR and detection capabilities.



### Engine Capabilities

* [x] Detect DLL sideLoading/SearchOrderHijacking.



### How to use

```shell
python3 main.py -h
```

```shell
[*Output]
usage: main.py [-h] [-DSL] [-f FILE] [-c CONFIG] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -DSL, --DetectSideLoad
                        Detect DLL side loading attempts
  -f FILE, --file FILE  Path to the file used
  -c CONFIG, --config CONFIG
                        Path to the CB EDR's config file - default (CB.conf)
  -o OUTPUT, --output OUTPUT
                        Path to the output file)
```

```shell
python3 main.py -DSL -f "DLLSideLoading data.csv" -c "CB.conf" -o "output-DLLSearOrderHijacking.csv"
```


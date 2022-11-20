# CB-Boost
CB-Boost is a tool utilized Carbon Black API to run Incident response actions, and detection use cases that requires automation.

CB-Boost's detection use cases are not meant to be full detection use cases, but it only contains what requires programmatically analysis of the output of certain use cases. To create a simple use case just do it using watchlists.

CB-Boost's IR capabilities is coming soon!.



## Engine Capabilities

### Threat Hunting

* [x] TimeLine Activity 
* [ ] Osquery  (bypass the 200 device limitation)

### Detection uses cases
* [x] Detect DLL Hijacking [sideLoading/OrderHijacking].
  * [x] Integration with [HijackLibs](https://github.com/wietze/HijackLibs)
  * [x] Detection Based on the DLL Path
  * [x] Detection Based on The Process Path (not recommended)
* [ ] Detect Hidden Accounts


### Incident response

- [ ] Execute PowerShell/Command Prompt commands

- [ ] Upload & Run executables and retrieve the output. 

  


## How it works?

1. ``` git clone --recurse-submodules https://github.com/karemfaisal/CB-Boost```

2. ```pip install -r requirements```

3. ```cbapi-response configure```

   - Will promote you to enter the your CB-EDR Data [URI, Token, Profile Name]

   - cbapi-response could be found in the venv path or pip's scripts' path

**For DLLHijacking detection**

4. Point to the folder contains HijackLibs rules or minimal rules that you want to search for.

   ``` bash
   python3 main.py --rules rule.yml --profile "default"
   ```

   

```shell
python3 main.py -h
```

```shell
[*Output]
usage: main.py [-h] [-r RULES] [-p PROFILES]

optional arguments:
  -h, --help            show this help message and exit
  -r RULES, --rules RULES
                        path to the CB-Boost yaml file path
  -p PROFILES, --profiles PROFILES
                        profiles name for running the API separated by ',' ex:
                        Karem,Ali
```

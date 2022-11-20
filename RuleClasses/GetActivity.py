import math
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
from cbapi.response import *
from threading import Lock, current_thread
import Utils


class GetActivity():
    description = ""
    destination = ""
    destinationFormat = ""
    processQuery = ""
    startDateTime = ""
    endDateTime = ""
    requiredActivities = []
    CBprofile = ""
    threadLimit = 0
    Exporter = object
    exclusions = \
        {
            "Network": [],
            "DLL": [],
            "File": {
                "Operation": [],
                "Type": []
            },
            "Registry": {
                "Path": [],
                "Operation": []
            },
            "CrossProc": {
                "Type": [],
                "TargetProcess": [],
                "SubType": [],
                "AccessPriviledge": []
            }
        }
    outputColumns = ["Eventtype", "TimeStamp", "Hostname", "Username", "Path", "PID", "UniqueID", "Cmdline",
                     "parent_name", "remote_domain",
                     "remote_ip", "remote_port", "local_ip", "local_port", "protocol", "direction", "target_file",
                     "file_action",
                     "file_md5", "file_type", "registry_target", "registry_action", "crossproc_source",
                     "crossproc_target", "crossproc_priv", "crossproc_privcode"]
    processes = []
    Events = []
    Events.append(outputColumns)
    step = 0
    mutex = Lock()

    def __init__(self, YmlObj, exporter):
        self.processQuery = YmlObj['processQuery']
        self.startDateTime = YmlObj['startDateTime']
        self.endDateTime = YmlObj['endDateTime']
        self.requiredActivities.extend(YmlObj['requiredActivities'])
        self.threadLimit = YmlObj['threadLimit']
        self.destination = YmlObj['destination']
        self.destinationFormat = YmlObj['destinationFormat']
        self.description = YmlObj['description']
        self.Exporter = exporter

    def returnProcesses(self):
        cb = CbResponseAPI(profile=self.CBprofile)
        processes = cb.select(Process).where(self.processQuery).min_last_update(self.startDateTime).max_last_update(
            self.endDateTime)
        return processes

    def getEvents(self, start):
        Events = []
        i = 0
        # loop on processes
        for process in self.processes[start:start + self.step]:
            if "network".lower() in self.requiredActivities:
                for netconn in process.netconns:
                    try:
                        Events.append(("network connection",
                                       Utils.convert_timestamp(netconn.timestamp),
                                       process.hostname.lower(),
                                       process.username.lower(),
                                       process.path,
                                       process.process_pid,
                                       process.unique_id,
                                       process.cmdline,
                                       process.parent_name,
                                       netconn.domain,
                                       netconn.remote_ip,
                                       netconn.remote_port,
                                       netconn.local_ip,
                                       netconn.local_port,
                                       netconn.proto,
                                       netconn.direction))
                    except:
                        print("Error Network")

            # To-do: Complete variables of DLL load, and create associated CSV header
            if "DLL".lower() in self.requiredActivities:
                for modload in process.modloads:
                    try:
                        Events.append(("Module Load",
                                       Utils.convert_timestamp(netconn.timestamp),
                                       process.hostname.lower(),
                                       process.username.lower(),
                                       process.path,
                                       process.process_pid,
                                       process.unique_id,
                                       process.cmdline,
                                       process.parent_name,
                                       '', '', '', '', '', '', '',
                                       ))
                    except:
                        print("DLL append error")

            if "File".lower() in self.requiredActivities:
                for filemod in process.filemods:
                    try:
                        Events.append(("File Action",
                                       Utils.convert_timestamp(filemod.timestamp),
                                       process.hostname.lower(),
                                       process.username.lower(),
                                       process.path,
                                       process.process_pid,
                                       process.unique_id,
                                       process.cmdline,
                                       process.parent_name,
                                       '', '', '', '', '', '', '',
                                       filemod.path,
                                       filemod.type,
                                       filemod.md5,
                                       filemod.filetype
                                       ))
                    except:
                        print("Error File")
            if "Registry".lower() in self.requiredActivities:
                for regmod in process.regmods:
                    Events.append(("Registry",
                                   Utils.convert_timestamp(regmod.timestamp),
                                   process.hostname.lower(),
                                   process.username.lower(),
                                   process.path,
                                   process.process_pid,
                                   process.unique_id,
                                   process.cmdline,
                                   process.parent_name,
                                   '', '', '', '', '', '', '',  # network connection
                                   '', '', '', '',  # file action
                                   regmod.type,
                                   regmod.path,
                                   ))

            if "CrossProc".lower() in self.requiredActivities:
                for crossproc in process.crossprocs:
                    Events.append(("Cross Proc",
                                   Utils.convert_timestamp(crossproc.timestamp),
                                   process.hostname.lower(),
                                   process.username.lower(),
                                   process.path,
                                   process.process_pid,
                                   process.unique_id,
                                   process.cmdline,
                                   process.parent_name,
                                   '', '', '', '', '', '', '',  # network connection
                                   '', '', '', '',  # file action
                                   '', '',
                                   crossproc.source_path,
                                   crossproc.target_path,
                                   crossproc.privileges,
                                   crossproc.privilege_code
                                   ))

            i += 1
            if (i % 15 == 0):
                print(current_thread().getName())
                print("Progress : {0}/{1} Process".format(i, self.step))
                print("-------------")

        self.mutex.acquire()
        self.Events.extend(Events)
        self.mutex.release()

    def execute(self):
        self.processes = self.returnProcesses()
        processesChunks = [x for x in range(0, len(self.processes), math.ceil(len(self.processes) / self.threadLimit))]
        if len(processesChunks) > 1:
            self.step = processesChunks[1] - processesChunks[0]
        else:
            self.step = len(self.processes)

        # Execute Thread
        with ThreadPoolExecutor(self.threadLimit) as executor:
            futures = [executor.submit(self.getEvents, x) for x in
                       range(0, len(self.processes), math.ceil(len(self.processes) / self.threadLimit))]
            done, not_done = wait(futures, return_when=ALL_COMPLETED)

        self.exporter.export(self.destination, self.Events)

        print("end")

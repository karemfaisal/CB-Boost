import Utils
import urllib
import requests
requests.packages.urllib3.disable_warnings()

class ProcessSearch:
    query=""
    URL=""
    apiEndPoint="/api/v1/process?"
    CBHeaders = {}
    def __init__(self, CBHeaders, URL, Query):
        self.URL = URL
        self.query = urllib.parse.quote(Query)
        self.CBHeaders = CBHeaders

    def Search(self):
        return requests.request("GET", self.URL + self.apiEndPoint + "q=" + self.query, headers=self.CBHeaders,
                                verify=False).json()



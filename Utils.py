import json
import csv
import os

def getJsonFromFile(filePath):
    with open(filePath, "r") as file:
        jsonData = json.loads(file.read())
    return jsonData

def getCSVFromFile(filePath):
    with open(filePath, "r") as file:
        csvData = csv.reader(file)
        csvHeaders = next(csvData)
        csvRows = []
        for row in csvData:
            csvRows.append(row)
    return csvHeaders, csvRows

def writeCSVFile(filePath="",writeMode ="w", Headers = "", Rows=""):
    with open(filePath, writeMode, newline='', encoding='UTF8') as file:
        csvWriter = csv.writer(file)
        if Headers != "":
            csvWriter.writerow(Headers)
        if Rows != "":
            csvWriter.writerows(Rows)
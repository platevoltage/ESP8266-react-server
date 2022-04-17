#!/usr/bin/python

import os
import json


restPaths = []
fileDirectories = ["payload/manifest.json.h"]
varNames = ["_manifest_json"]
fileDirectoryChunk = "\n"
wifiChunk = "\n"
restPathChunk = "\n"

os.mkdir('react-server-test')
os.mkdir('react-server-test/payload')

def createIno():
    sourceFile = open("template/template.ino", "r")
    destinationFile = open("react-server-test/react-server-test.ino", "a")
    templateChunks = sourceFile.read().split("//XXX")
    templateChunks[0] += fileDirectoryChunk + wifiChunk
    templateChunks[1] += restPathChunk
    for chunk in templateChunks:
        destinationFile.write(chunk)

def createFileDirectoryChunk():
    for dir in fileDirectories:
        global fileDirectoryChunk
        fileDirectoryChunk += '#include "' + dir + '"\n'

def createRestPathChunk():
    for i in range(len(restPaths)):
        global restPathChunk
        restPathChunk += '\tserver.on(\"' + restPaths[i] + '\", [](){ server.send(200, \"' + getFileType(varNames[i]) + '\", ' + varNames[i] + '); });\n'

def getFileType(fileName):

    fileType = fileName.split("_")[-1]
    if fileType == "js":
        fileType = "javascript"
    return "text/" + fileType

def createWifiChunk():
    global wifiChunk
    wifiChunk += "#ifndef STASSID\n#define STASSID \"Can't stop the signal, Mal\"\n#define STAPSK  \"youcanttaketheskyfromme\"\n#endif"


def createAssetArray():
    sourceFile = open("./build/asset-manifest.json", "r")
    files = json.loads(sourceFile.read())["files"]
    projectName = files["index.html"].split("/")[1]
    print(projectName)
    restPaths.append("/" + projectName + "/manifest.json") #add manifest to restPaths
    for key in files:
       if files[key].split(".")[-1] != "map" and files[key].split(".")[-1] != "json": 
           dirSplit = files[key].split("/")
           tempString = "payload"
           
           for i in range(len(dirSplit)-2):
               tempString += "/" + dirSplit[i+2]

           fileDirectories.append(tempString + ".h")
           restPaths.append(files[key])
           varNames.append(convertFileNameToC(dirSplit[-1]))
    

def convertFileNameToC(fileName):
    varName = ""
    for x in fileName.split("."):
        if not any(chr.isdigit() for chr in x): 
            varName += "_" + x
    return varName

def createDirs(workingDirectory):
    
    sourceDirContents = os.listdir("./build/" + workingDirectory)

    for file in sourceDirContents:
        varName = ""
        
        for x in file.split("."):
            if not any(chr.isdigit() for chr in x): 
                varName += "_" + x
                
        
        fileExtension = file.split(".")[-1]
        if os.path.isdir("./build/" + workingDirectory + "/" + file):
            os.mkdir('react-server-test/payload/' + workingDirectory + "/" + file)
            createDirs(workingDirectory + "/" + file)
        elif fileExtension == "js" or fileExtension == "css" or fileExtension == "html" or file == "manifest.json":
            createFile('build/' + workingDirectory + "/" + file, 'react-server-test/payload/' + workingDirectory + "/" + file + ".h", varName)
            # print(varName)
            # varNames.append(varName)
            # fileDirectories.append("payload/" + workingDirectory + "/" + file + ".h")

def createFile(source, destination, varName):

    destinationFile = open(destination, "x")
    destinationFile = open(destination, "a")
    sourceFile = open(source, "r")
    destinationFile.write('static const char ' + varName + '[] PROGMEM = R"=====(\n')
    destinationFile.write(sourceFile.read())
    destinationFile.write('\n)=====";')

    destinationFile.close()



createDirs(".")
createAssetArray()
createFileDirectoryChunk()
createWifiChunk()
createRestPathChunk()
createIno()

print(fileDirectories)
print(restPaths)
print(varNames)
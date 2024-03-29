#!/usr/bin/python

import os
import json
import shutil


restPaths = []
fileDirectories = ["payload/manifest.json.h"]
varNames = ["_manifest_json"]
fileDirectoryChunk = "\n"
wifiChunk = "\n"
restPathChunk = "\n"
if __name__ == "__main__":
    ssid = ""
    password = ""
    sourceDirectory = "build/"
    destinationDirectory = "react-server/"
else:
    sourceDirectory = "upload/build/"
    destinationDirectory = "product/react-server/"


def createIno():
    sourceFile = open("inoTemplate/template.ino", "r")
    destinationFile = open(destinationDirectory + "react-server.ino", "a")
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
    wifiChunk += "#ifndef STASSID\n#define STASSID \"" + ssid + "\"\n#define STAPSK  \"" + password + "\"\n#endif"

def createAssetArray():
    sourceFile = open(sourceDirectory + "asset-manifest.json", "r")
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

def createRootDirectory():
    if not os.path.isdir(destinationDirectory):

        os.mkdir(destinationDirectory)
        os.mkdir(destinationDirectory + 'payload')
    elif __name__ == "__main__":
        confirm = input("'react-server' already exists and will be deleted, continue? [default: y]")
        if confirm == "y" or confirm == "" or confirm == "yes":
            shutil.rmtree(destinationDirectory)
            createRootDirectory()    
        else:
            return
        
def createDirs(workingDirectory):
    
    sourceDirContents = os.listdir("./" + sourceDirectory + workingDirectory)

    for file in sourceDirContents:
        varName = ""
        
        for x in file.split("."):
            if not any(chr.isdigit() for chr in x): 
                varName += "_" + x
                    
        fileExtension = file.split(".")[-1]
        if os.path.isdir("./" + sourceDirectory + workingDirectory + "/" + file):
            os.mkdir(destinationDirectory + 'payload/' + workingDirectory + "/" + file)
            createDirs(workingDirectory + "/" + file)
        elif fileExtension == "js" or fileExtension == "css" or fileExtension == "html" or file == "manifest.json":
            createFile(sourceDirectory + workingDirectory + "/" + file, destinationDirectory + 'payload/' + workingDirectory + "/" + file + ".h", varName)
 
def createFile(source, destination, varName):

    destinationFile = open(destination, "x")
    destinationFile = open(destination, "a")
    sourceFileContents = open(source, "r").read()
    sourceFileContentsLines = sourceFileContents.split('\n')
    tempLines = []

    for line in sourceFileContentsLines:
        if not line.startswith("/*") and not line.startswith("//"):
            tempLines.append(line)

    sourceFileContents = '\n'.join(tempLines)
    destinationFile.write('static const char ' + varName + '[] PROGMEM = R"=====(\n')
    destinationFile.write(sourceFileContents)
    destinationFile.write('\n)=====";')
    destinationFile.close()

def prompt():
    global ssid, password

    ssid = input("Wifi SSID? : ")
    password = input("Password? : ")

    confirm = input("is this correct? [default: y]")
    print(confirm)
    if confirm == "y" or confirm == "" or confirm == "yes":
        
        return
    else:
        prompt()


if __name__ == "__main__":
    prompt()
    createRootDirectory()
    createDirs(".")
    createAssetArray()
    createFileDirectoryChunk()
    createWifiChunk()
    createRestPathChunk()
    createIno()

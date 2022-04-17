#!/usr/bin/python

import os

# print(os.path.splitext('my_file.txt')[-1])
os.mkdir('payload_test')

# os.chdir('build')

# sourceDir = os.listdir("./static/")
# print(sourceDir)
# print(os.getcwd())
def createDirs(workingDirectory):

    sourceDir = os.listdir("./build/" + workingDirectory)
    # print(sourceDir)
    # print(workingDirectory)
    for i in sourceDir:
        varName = ""
        # print(i)
        
        for k in i.split("."):
            # print(k)
            if not any(chr.isdigit() for chr in k): 
                varName += "_" + k
        
        fileExtension = i.split(".")[-1]
        if os.path.isdir("./build/" + workingDirectory + "/" + i):
            # print('payload_test/' + workingDirectory + "/" + i)
            os.mkdir('payload_test/' + workingDirectory + "/" + i)
            # os.chdir(i)
            
            createDirs(workingDirectory + "/" + i)
        elif fileExtension == "js" or fileExtension == "css" or fileExtension == "html":
            createFile('build/' + workingDirectory + "/" + i,'payload_test/' + workingDirectory + "/" + i + ".h", varName)
            print(varName)

def createFile(source, destination, varName):

    destinationFile = open(destination, "x")
    destinationFile = open(destination, "a")
    # varName = "TTTTEEEESSSSST"
    sourceFile = open(source, "r")
    # print(source.read())
    destinationFile.write('static const char ' + varName + '[] PROGMEM = R"=====(\n')
    destinationFile.write(sourceFile.read())
    destinationFile.write('\n)=====";')

    destinationFile.close()



createDirs(".")

# print(os.listdir())
#!/usr/bin/python

import os

os.mkdir('payload_test')

# os.chdir('build')

# sourceDir = os.listdir("./static/")
# print(sourceDir)
print(os.getcwd())
def createDirs(workingDirectory):

    sourceDir = os.listdir("./build/" + workingDirectory)
    print(sourceDir)
    print(workingDirectory)
    for i in sourceDir:
        if os.path.isdir("./build/" + workingDirectory + "/" + i):
            print('payload_test/' + workingDirectory + "/" + i)
            os.mkdir('payload_test/' + workingDirectory + "/" + i)
            # os.chdir(i)
            
            createDirs(workingDirectory + "/" + i)
       


createDirs(".")

# print(os.listdir())
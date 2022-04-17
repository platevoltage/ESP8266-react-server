#!/usr/bin/python

import sys
print(sys.argv)
source = sys.argv[1]
destination = sys.argv[2]
varName = sys.argv[3]

destinationFile = open(destination, "x")
destinationFile = open(destination, "a")





sourceFile = open(source, "r")
# print(source.read())
destinationFile.write('static const char ' + varName + '[] PROGMEM = R"=====(\n')
destinationFile.write(sourceFile.read())
destinationFile.write('\n)=====";')

destinationFile.close()

#open and read the file after the appending:




# f.write('\n)=====";')
__author__ = 'rohitm92'

import glob
import os
import string
import re


def main():
    directory = "/Users/rohitm92/Desktop/Rohit/Stanford/Courses/CS 224W/Project/Repository/twitter/featnamesclean/"
    extension = "*.featnamesclean"
    outputFileName = "globalFeatureList"
    outputExtension = outputFileName
    fileList = getFileList(directory, extension)
    globalFeatureSet = set()
    sumFeatures = 0
    #Need to do the following for each file in fileList, not just fileList[0]
    for i in range(len(fileList)):
        sumFeatures = addFileToFeatureSet(fileList[i], globalFeatureSet, sumFeatures)
    print "Number of files: ", len(fileList)
    print "Number of features: ", sumFeatures
    print "Number of distinct features: ", len(globalFeatureSet)

    writeFeaturesToFile(globalFeatureSet, outputFileName, outputExtension, directory)

def writeFeaturesToFile(globalFeaureSet, fileName, extension, directory):
    f1=open(directory + fileName + "." + extension, 'w+')
    for item in globalFeaureSet:
        f1.write(item + '\n')
        #print item

def getFileList(directory, extension):
    os.chdir(directory)
    fileList = list()
    for file in glob.glob(extension):
        fileList.append(file)
    return fileList

def addFileToFeatureSet(filename, globalFeatureSet, sumFeatures):
    with open(filename) as f:
        for line in f:
            sumFeatures += 1
            splitLineList = line.split(' ')
            globalFeatureSet.add(splitLineList[1].rstrip())

    return sumFeatures

if __name__ == "__main__":
    main()
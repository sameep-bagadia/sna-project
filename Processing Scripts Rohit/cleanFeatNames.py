__author__ = 'rohitm92'

import glob
import os
import string
import re

def main():
    directory = "/Users/rohitm92/Desktop/Rohit/Stanford/Courses/CS 224W/Project/Repository/twitter/"
    newsubdir = directory + "featnamesclean/"
    os.mkdir(newsubdir)
    extension = "*.featnames"
    newExtension = "*.featnamesclean"
    fileList = getFileList(directory, extension)
    #Need to do the following for each file in fileList, not just fileList[0]
    for i in range(len(fileList)):
        featureListRaw = listFeaturesRaw(fileList[i])
        featureListClean = removeSpecialChar(featureListRaw)
        writeFeaturesToFile(featureListClean, fileList[i], extension[2:], newExtension[2:], newsubdir)

def writeFeaturesToFile(featureList, fileName, oldExtension, newExtension, directory):
    f1=open(directory + fileName.replace(oldExtension, newExtension), 'w+')
    for key in featureList:
        f1.write(str(key) + ' ' + featureList[key] + '\n')


def removeSpecialChar(featureListRaw):
    featureListClean = dict()
    for key in featureListRaw:
        featureListClean[key] = featureListRaw[key][0] + re.sub(r'[\W]+', '', featureListRaw[key])
    return featureListClean

def getFileList(directory, extension):
    os.chdir(directory)
    fileList = list()
    for file in glob.glob(extension):
        fileList.append(file)
    return fileList

def listFeaturesRaw(filename):
    featureListRaw = dict()
    with open(filename) as f:
        for line in f:
            splitLineList = line.split(' ')
            featureListRaw[int(splitLineList[0])] = splitLineList[1].rstrip()
    return featureListRaw



if __name__ == "__main__":
    main()
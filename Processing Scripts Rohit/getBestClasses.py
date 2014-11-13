__author__ = 'rohitm92'

import json
import string
import re
import urllib2


def main():
    directory = "/Users/rohitm92/Desktop/Rohit/Stanford/Courses/CS 224W/Project/Repository/twitter/featnamesclean/"
    inputFileName = "globalFeatureList"
    inputExtension = inputFileName
    outputFileName = "featureGenreMap"
    outputExtension = "json"


    globalFeatureSet = set()
    fileList = getFeatureSet(globalFeatureSet, directory, inputFileName, inputExtension)
    featureGenreMap = dict()
    getWefollowGenres(globalFeatureSet, featureGenreMap, directory, outputFileName, outputExtension)


def writeDictToFile(featureGenreMap, directory, outputFileName, outputExtension):
    f = []
    try:
        f = open(directory+outputFileName+'.'+outputExtension, 'a')
    except:
        f = open(directory+outputFileName+'.'+outputExtension, 'w+')
    json.dump(featureGenreMap, f)
    f.write('\n')
    f.close()

def getWefollowGenres(globalFeatureSet, featureGenreMap, directory, outputFileName, outputExtension):
    count = 0
    setSize = len(globalFeatureSet)

    for feature in globalFeatureSet:
        print "Features classified: ",count,'/',setSize
        count += 1
        if isTwitterUser(feature):
            featureList = genreOfFeature(feature[1:])
            #if len(featureList)>0:
                #print feature + ', prominent in : '
                #print featureList
            featureGenreMap[feature] = featureList
        else:
            featureGenreMap[feature] = list()

        #Write every 100 items to avoid data loss
        if count%100 == 0:
            print "Classified", count, " features. Writing to file."
            writeDictToFile(featureGenreMap, directory,  outputFileName, outputExtension)
            #Clear to avoid excess RAM usage as well as to avoid redundant data write
            featureGenreMap.clear()

    #Write any remaining features not written yet
    writeDictToFile(featureGenreMap, directory,  outputFileName, outputExtension)


def isTwitterUser(feature):
    if feature[0] == '@':
        return True
    elif feature[0] == '#':
        return False
    else:
        print "Found non-user, non-hashtag:", feature
        return False


def getFeatureSet(globalFeatureSet, directory, inputFileName, inputExtension):
    with open(directory+inputFileName+"."+inputExtension) as f:
        for line in f:
            globalFeatureSet.add(line.rstrip())

def genreOfFeature(feature):
    try:
        page = httpRequest(feature)
        stringSearched = '<h3><a href="/interest/'
        startIndices =  [m.start() for m in re.finditer(stringSearched, page)]
        endIndices = [string.find(page, '</a></h3>', startIdx) for startIdx in startIndices]
        features = list()
        for i in range(len(startIndices)):
            startIdx = startIndices[i]
            endIdx = endIndices[i]
            twiceLength = endIdx - startIdx - len(stringSearched)
            length = twiceLength/2 - 1
            features.append(page[endIdx-length:endIdx])
        return features
    except:
        #print feature, "not found"
        return list()

def httpRequest(feature):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request('http://www.wefollow.com/'+feature, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    return page

if __name__ == "__main__":
    main()
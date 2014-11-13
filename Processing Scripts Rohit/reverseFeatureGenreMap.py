__author__ = 'rohitm92'

import json

def main():
    filename = "/Users/rohitm92/Desktop/Rohit/Stanford/Courses/CS 224W/Project/Repository/twitter/featnamesclean/featureGenreMap.json"
    ofilename = "/Users/rohitm92/Desktop/Rohit/Stanford/Courses/CS 224W/Project/Repository/twitter/featnamesclean/genreFeatureMap.json"
    featureGenreMap = dict()
    addFileToFeatureSet(featureGenreMap, filename)

    genreFeatureMap = dict()
    reverseDictionary(featureGenreMap, genreFeatureMap)

    f = open(ofilename, 'w+')
    json.dump(genreFeatureMap, f)
    f.write('\n')
    f.close()


def addFileToFeatureSet(featureGenreMap, filename):
    with open(filename) as f:
        for line in f:
            featureGenreMap.update(json.loads(line))

def reverseDictionary(featureGenreMap, genreFeatureMap):
    for celebrity in featureGenreMap.keys():
        genres = featureGenreMap[celebrity]
        for genre in genres:
            try:
                celebrities = genreFeatureMap[genre.encode('ascii','ignore')]
                celebrities.append(celebrity.encode('ascii', 'ignore'))
                genreFeatureMap[genre.encode('ascii', 'ignore')] = celebrities
            except:
                celebrities = list()
                celebrities.append(celebrity.encode('ascii', 'ignore'))
                genreFeatureMap[genre.encode('ascii', 'ignore')] = celebrities


if __name__ == "__main__":
    main()
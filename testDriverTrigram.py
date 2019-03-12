from EWordEP import *
from EWordTP import *

# read file

filePath = 'emission_lemmaa.txt'
data = [i.strip('\n').split('\t') for i in open(filePath)]

dataEmission = []
# ========= susun data ==========
for i in range(len(data)):
    word = data[i][0]
    # print word
    tag = data[i][1]
    # print tag
    pembilang, penyebut = data[i][2], data[i][3]
    ew = EWordEP()
    ew.set(word, tag, pembilang, penyebut)
    dataEmission.append(ew)

# =============================
filePath = 'transition_lemmaTrigram.txt'
data = [
    i.strip('\n').replace("P(", "").replace("|", ",").replace(")=(", ",").replace(")", "").replace(" ", "").split(",")
    for i in open(filePath)]

dataTransition = []
for i in range(len(data)):
    tag = data[i][0]
    prevTag = data[i][1], data[i][2]

    pembilang, penyebut = data[i][3], data[i][4]

    ew = EWordTP()
    ew.set(tag, prevTag, pembilang, penyebut)
    dataTransition.append(ew)

firstWord = ""
secondWord = ""


def tagOf(word,known):
    word1 = []
    word2 = []


    for i in range(len(dataEmission)):
        if word == dataEmission[i].getWord():
            word1.append(dataEmission[i])
        if known == dataEmission[i].getWord():
            word2.append(dataEmission[i])


    maximum = 0
    trueTag = ""
    for i in range(len(word1)):
        for j in range(len(word2)):
            for k in range(len(dataTransition)):

                if dataTransition[k].getTag() == word1[i].getTag() and dataTransition[k].getPrevTag()[0] == word2[j].getTag():

                    skor = dataTransition[k].getScore() * word1[i].getScore()

                    if skor > maximum:
                        maximum = skor
                        trueTag = dataTransition[k].getTag()
    #print trueTag


    return trueTag

def tagOfTrigram(word,known1,known2):
    word1 = []
    word2 = []
    word3 = []

    for i in range(len(dataEmission)):
        if word == dataEmission[i].getWord():
            word1.append(dataEmission[i])
        if known1 == dataEmission[i].getWord():
            word2.append(dataEmission[i])
        if known2 == dataEmission[i].getWord():
            word3.append(dataEmission[i])


    maximum = 0
    trueTag = ""
    for i in range(len(word1)):
        for j in range(len(word2)):
            for k in range(len(word3)):
                for l in range(len(dataTransition)):

                    if dataTransition[l].getTag() == word1[i].getTag() and \
                       dataTransition[l].getPrevTag()[0] == word2[j].getTag() and \
                       dataTransition[l].getPrevTag()[1] == word3[j].getTag():
                        skor = dataTransition[l].getScore() * word1[i].getScore()

                        if skor > maximum:
                            maximum = skor
                            trueTag = dataTransition[k].getTag()
                            #print trueTag


    return trueTag


filePath = 'lemma_test.txt'
data = [i.strip('\n').strip('\r').lower() for i in open(filePath)]

data = [i for i in data if i]  # remove empty line in data

savefile = 'lemmatest_resultnosmooth.txt'
f = open(savefile, "w")

for i in range(len(data)):
    print i
    if i == 0:

        #print "awal kalimat"
        #print tagOf(data[i], ".")
        f.write(data[i]+"\t"+tagOf(data[i],".")+"\n")


    elif i ==1:
        #print "kata kedua"
        #print tagOf(data[i], ".")
        f.write(data[i] + "\t" + tagOf(data[i], data[i-1])+"\n")
    elif i ==len(data):
        f.write(data[i] + "\t" + "Z")

    else:
        print data[i],data[i-2],data[i - 1]
        #print data[i]
        #print tagOf(data[i], [data[i - 2],data[i-1]])
        f.write(data[i] + "\t" + tagOfTrigram(data[i], data[i-2],data[i - 1]))

f.write("\n")

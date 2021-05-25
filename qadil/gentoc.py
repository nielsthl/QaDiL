# -*- coding: utf-8 -*

import sys
import glob
import re
import csv
import io
import os

chapterdir = sys.argv[1]
ltoc = glob.glob(chapterdir+'/*.toc')


chapterlist=[]
dict={}
sectioncount = 1

def replaceatend(targ, repl, str):
    return re.sub(targ+'$', repl, str)

for f in ltoc:
     with open(f, "r") as fil:
        csvreader = csv.reader(fil, quotechar='@', skipinitialspace=True)
        chapterno=''
        fbasename = os.path.basename(f)

        for li in csvreader:
             if (li[0]=="chapterno"): 
                chapterlist.append(dict) 
                dict={}
                chapterno = li[1]
                
                dict["chapterno"]=chapterno
                dict["chapter"] = ""
                dict["chapterlink"] = ""
                dict["sections"] = [] 
                sectioncount = 1
                prefix = replaceatend(".toc", ".html", fbasename) + "#"
             else:
                if (li[0] == "chapter"):
                    dict["chapter"] = li[1]
                    dict["chapterlink"] = prefix+li[2]
                if (li[0] == "section"):
                    sectionpair = (chapterno+"."+str(sectioncount)+" "+li[1], prefix + li[2])
                    dict["sections"].append(sectionpair)
                    sectioncount += 1


#sectionschar = '&#9654' # Right triangle
#sectionschar = '&#9655' # Right triangle (hollow)
sectionschar = '&#10095' # Bf ">"

def formathtml(entry):
    label = 'kap' + entry["chapterno"]
    returnstr = ""
    returnstr += '<li><a class="kap" href="' + entry["chapterlink"]+'"><b>'+entry["chapterno"] + '</b> ' + entry["chapter"] +'</a></li>'
    returnstr += '<a href="#'+label+'" data-toggle="collapse"><span class="downtick">'+sectionschar+'</span></a>'
    returnstr += '<ul id="'+label+'" class="collapse">'
    for e in entry["sections"]:
        returnstr += '<li><a href="' + e[1]+'">'+e[0] + '</a></li>'
    returnstr += '</ul>'
    return returnstr




def chaptercmp(x):
    #
    # Hack to deal with appendices A, B, C, D, ...:
    #
    chapterstr = x["chapterno"]
    try:
        return int(chapterstr)
    except:
        return ord(chapterstr)

chapterlist.append(dict)
del chapterlist[0]

returnstr = ""
for e in sorted(chapterlist, key=chaptercmp):
    returnstr += formathtml(e)

regex = '<!-- Table of contents not generated -->'
regc = re.compile(regex)

    
htmlfiles = glob.glob(chapterdir+'/*.html')    
for f in htmlfiles:

    with open(f, "r") as fil:
        str = fil.read()
        
    str = regc.sub(returnstr, str)
    
    with open(f, "w") as fil:
        fil.write(str)

    

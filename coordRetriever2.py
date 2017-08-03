import json
import requests
from time import sleep, time
import traceback

i = 0
keyin = 0
startime = 0

def main(file1,file2):
    f2 = open(file2,'w',encoding="utf-8")
    affils = list(open(file1,'r',encoding="utf-8"))
    #print(str(affils))
    findCoords(affils,f2)
        
def findCoords(univList,fileWriter):
    global i
    global keyin
    global startime
    keys = list(open("keys.txt","r",encoding="utf-8"))
    keys = keys[:9]
    index = 0
    print(str(len(univList)))
    startime = time()
    for index,univName in enumerate(univList[:12600]):
        """
        try:
            univName,coords = univ.split("|",1)
        except ValueError:
            fileWriter.write(univ)

        if coords.find(",") != 0:
            #print(coords)
            fileWriter.write('"'+univName+'",'+coords)
        else:         
        """      
        try:
            coo = getLocation(removeSpaces(univName),keys[keyin])
        except IndexError:
            raise IndexError('You ran out of keys ya fool')
        fileWriter.write('"'+univName[:len(univName)-1]+'",'+str(coo['lat'])+','+str(coo['lng'])+"\n")
        if index % 100 == 0:
            print("ID: "+str(index))

def getLocation(univ,key):
    global i
    global keyin
    global startime
    reached = False
    while not reached:
        #print(univ)
        try:
            i += 1
            if(key[-1] == "\n"):
                key = key[:-1]
            r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+univ+'&key='+key)
            #print('https://maps.googleapis.com/maps/api/geocode/json?address='+univ+'&key='+key)
            if(i % 50 == 0):
                sleeptm = 60 - ((time() - startime) % 60)
                sleep(sleeptm)
                print("sleeping..."+str(sleeptm)+" seconds")
                if(i % 2450 == 0):
                    keyin += 1
            data = r.json()['results'][0]['geometry']['location']
            #print("zZ"+str(data)+"Zz")
            reached = True
        #except ValueError:
        #    print("hi i'm paul")
        except IndexError as voop:
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #print(format(voop)+"   "+str(exc_traceback.tb_lineno))
            #print(univ)
            try:
                univ = univ.split(',',1)[1]#[univ.index(',')+1]
            except ValueError:
                break
    else:
        return data
    return {'lat':'','lng':''}    
    
def removeEmail(univ):
    if univ.find("@") != -1:
        return univ[:univ.rfind(" ")]
    return univ

def removeSpaces(univ):
    while univ.find(" ") != -1:
        i = univ.find(" ")
        univ = univ[:i] + "%20" + univ[i+1:]
    return univ

if __name__ == "__main__":
    import sys
    main(str(sys.argv[1]),str(sys.argv[2]))
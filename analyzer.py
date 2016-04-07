import os
import subprocess
import time



if not os.path.isdir("myfifo"):
    subprocess.call("mkdir myfifo", shell=True)
else:
    subprocess.call("rm myfifo/*", shell=True)

def tsharkLogs():
    files = os.listdir("/tmp")
    for eachFile in files:
        if "myfifo" in eachFile:
            subprocess.call("tshark -i - < '/tmp/"+eachFile+"' > 'myfifo/"+eachFile+".txt'", shell=True)

def coutPackets():
    files = os.listdir("myfifo/")
    print files
    results = {}
    for i in range(1,61):
        results[i] = 0
    
    for eachFile in files:
        print "Starts: ",eachFile
        c = 0 
        f = open("myfifo/"+eachFile,"r")
        for eachLine in f:
            #c += 1
            #print "c: ", c
            eachLineList = eachLine.split(" ")
            while '' in eachLineList:
            	eachLineList.remove('')

            index = int(float(eachLineList[0]))+1

            if index < 0:
                 print "Index error: negtive integer"
                 exit(1)
            if index <= 59:
                results[index] += 1

        f.close()

    wf = open("analysis-result.txt","w")
    for k,v in results.items():
    	wf.writelines(str(v/2)+"\n")
    wf.close()
    print results

        



if __name__ == "__main__":
    tsharkLogs()
    coutPackets()
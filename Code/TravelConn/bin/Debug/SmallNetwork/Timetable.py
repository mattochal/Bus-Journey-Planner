import pyperclip
import random

def addtime(t,m):
    minutes = ( int(t[2:]) + m ) % 60
    hours = int(t[:2]) + (( int(t[2:]) + int(m) ) // 60)
    s = ""
    if (len(str(hours)) == 1):
        s += "0"
    s  += str(hours)
    if (len(str(minutes))== 1):
        s += "0"
    s += str(minutes)
    return s

def getTimetableTable(links,times,daycat,routeid,first,interval,until):
    courses = (until - first)*60//interval

    if len(str(first)) == 1:
        t1 = "0"+str(first)+"00"
    else:
        t1 = str(first) + "00"
        
    At = [t1]
    i = 0

    # first set of times for the first bus
    for t in times.split("\n"):
        At.append(addtime(At[i],int(t)))
        At.append(addtime(At[i],int(t)))
        i += 2
    At.pop()
    
    table = ""
    #print (links)
    #print ("links length = " + str(len(links.split("\n")))) 
    i = 0 
    for i in range(0, len(links.split("\n"))-1):
        #print("got here"  + str (i))
        table += "{0}\t{1}\t{2}\t{3}\t{4}".format(daycat,links.split("\n")[i].split()[0],100,At[2*i],At[(2*i)+1])
        table += "\n"

    #print (table)   
    for i in range(1,courses):
        for k in range(0, len(At)):
            At[k] = addtime(At[k],interval)
        for j in range(0, len(links.split("\n"))-1):
            #print("got here"  + str (j))
            table += "{0}\t{1}\t{2}\t{3}\t{4}".format(daycat,links.split("\n")[j].split()[0],100 + i,At[2*j],At[(2*j)+1])
            table += "\n"

    #print(table)
    #print(asdbfusndia)
    return (table)

#bus stop id , bus name , lat, long address
def getBusStoptable(busStops,table):
    entry = ""
    bigtable = ""
    for b in busStops.split():
        idn = ""
        for i in range(0,len(b)):
            idn += str(ord(b[i]))
        if idn not in table:
            table.append(idn)
            bigtable += ("{0}\t{1}\t{2}\t{3}\t{4}".format(idn,b,((int(idn)//4)*3 - 18)%100,(int(idn)%100),"address " + b) + "\n")

    return bigtable

def getLinkTable(busStops,busid):
    table = ""
    count = 1
    idb1 = ""
    
    for i in range(0,len(busStops.split()[0])):
        idb1 += str(ord(busStops.split()[0][i]))
            
    for i in range(1,len(busStops.split())):
        b = busStops.split()[i]
        idb2 = idb1
        idb1 = ""
        for i in range(0,len(b)):
            idb1 += str(ord(b[i]))
        table += ("{0}{1}\t{2}\t{3}\t{4}".format(busid,count,busid,idb2,idb1)) + "\n"
        count += 1
    return table
        
#Generates an atificial timetable

n = 10
alf = 10
buses = ""
for i in range(1,n+1):
    buses += "Bus {0}{1}\tA{2}\t{3}{4}\t".format(i,"A",i,chr(65+alf-1),i)
    for j in range(0,alf):
        buses += str(chr(65+j)) + str(i)
        if j != alf-1:
            buses += " "

    buses += "\n"
    
    buses += "Bus {0}{1}\t{2}{3}\tA{4}\t".format(i,"B",chr(65+alf-1),i,i)
    for j in range(0,alf):
        buses += str(chr(65+alf-1-j)) + str(i)
        if j != alf-1:
            buses += " "

    buses += "\n"

idcount = 0;
if n > 1:
    for i in range(0,alf):
        buses += "Bus {0}{1}\t{2}{3}\t{4}{5}\t".format(n+i+1,"A",chr(65+i),"1",chr(65+i),n)
        for j in range(0,n):
            buses += str(chr(65+i)) + str(j+1)
            if j != n-1:
                buses += " "
        buses += "\n"
        buses += "Bus {0}{1}\t{2}{3}\t{4}{5}\t".format(n+i+1,"B",chr(65+i),"1",chr(65+i),n)
        for j in range(0,n):
            buses += str(chr(65+i)) + str(n-j)
            if j != n-1:
                buses += " "
        if i != alf-1:
            buses += "\n"

print(buses)

busstops = ""
for i in range(0,alf):
    for j in range(1,n+1):
        busstops += chr(65+i) + str(j)+ "\t"+ str(i+1) +"\t"+str(j)+"\n"
        
print (busstops)
print(f)


"""buses =Bus 1A	A	H	A B C D E F G H
Bus 1B	H	A	H G F E D C B A
Bus 2A	X	J	X Y C Z W E I J
Bus 2B	J	X	J I E W Z C Y X
Bus 3A	R	Q	R C O L P Q
Bus 3B	Q	R	Q P L O C R
Bus 4A	E	K	E F G M L K
Bus 4B	K	E	K L M G F E"""

daycat = "1"
first = 6#h
interval = 15#min
pathmin = 3
pathmax = 6
until = 23#h

count = 1
bigtable = ""
busStopTable = ""
busstoplist = []
links = ""
linkTable = ""
timeTable = ""

for bus in buses.split("\n"):
    times = ""
    busname = bus.split("\t")[0]
    routeid = count
    busstops = bus.split("\t")[3]

    #bigtable += "-------------------- Bus Stops" + "\n"
    busStopTable += getBusStoptable(busstops,busstoplist)
    links = getLinkTable(busstops,routeid)
    linkTable += links
    
    for i in range(0,len(busstops.split())-2):
       times += str(random.randrange(pathmin,pathmax)) + "\n"   
    times += str(random.randrange(pathmin,pathmax))
    #print("get " + str(count))
    timeTable += getTimetableTable(links,times,daycat,routeid,first,interval,until)
    #bigtable += "-------------------- Bus Timetable" + "\n"
    count += 1
    
print (timeTable)

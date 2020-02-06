import numpy as np
import sys
import copy
import random

def covers(point , ref, m):
    for i in range(m):
        if point[i] >= ref[i]:
            return 0
    return 1

def CoverPoints( points , index, ref, m):

    n_index = []
    for i in index:
        if covers(points[i],ref,m):
            n_index.append(i)

    return n_index

def GetVolume(point,ref,m):

    vol = 1.0
    for i in range(m):
        vol *= abs(ref[i] - point[i])

    return vol

def SplitReferencePoint(point, ref , m):

    upper_ref = []
    for i in range(m):
        item = []
        for j in range(m):
            if (i == j):
                item.append(point[j])
            else:
                item.append(ref[j])
        upper_ref.append(item)
    return upper_ref

def HV(points, ref, index, m):
    tam = len(index)
    if tam == 1:
        return GetVolume(points[index[0]],ref,m)
    
    elif tam == 0:
        return 0

    else:

        VolList = []
        for i in range(len(index)):
            VolList.append(GetVolume(points[index[i]], ref, m ))
        vol_max = max(VolList)
        id_max = VolList.index(vol_max)

        RefPoints = SplitReferencePoint(points[index[id_max]], ref , m)
        #Eliminamos el punto maximo
        index.remove(index[id_max])

        tmp_hv = 0
        for ref_i in RefPoints:
            n_index = CoverPoints( points , index, ref_i, m)
            tmp_hv += HV(points, ref_i, n_index , m)
        return vol_max + tmp_hv


def UpperSubPoints(points,lower_ref,index,m):

    l = []
    for item in index:
        point = []
        for i in range(m):
            if lower_ref[i] > points[item][i]:
                point.append(lower_ref[i])
            else:
                point.append(points[item][i])
        l.append(point)        
    return l
        
def CoverPointsSubSet( points , ref, m):

    subpoints = []
    for i in range(len(points)):
        if covers(points[i],ref,m):
            subpoints.append(points[i])

    return subpoints
    
def SplitBoxBylowerRef(point, lower_ref,m):
    new_point = []
    for i in range(m):
        if lower_ref[i] > point[i]:
            new_point.append(lower_ref[i])
        else:
            new_point.append(point[i])
            
    return new_point
            


def readFile(name):

    f = open(name,'r')
    
    list = []
    for line in f:
        l = line.strip()
        l = l.split()
        if line.find("#") == -1:
            tmp = [float(i) for i in l]
            list.append(tmp)

    f.close()
    return list


"""
how to launch 
python indicators.py filename

"""
front = readFile(sys.argv[1])


m = len(front[0])
# set reference point

upper_ref = [6 for i in range(m)]
lower_ref = [0 for i in range(m)]
print "dim: ", m, "size of set: ", len(front)

index = [i for i in range(len(front))]
print "hv: ", HV(front, upper_ref, index, m)







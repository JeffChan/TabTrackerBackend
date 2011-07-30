from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect 
from django.conf import settings
from tabtracker.tabtrack.util import *

def index(request):
    return HttpResponse("SSSSSSSSSSSUP")

def adduser(request, fbID):
    if(len(User.objects.all().filter(facebookID=fbID))>0):
        return HttpResponse("suck.")
    else:
	    return HttpResponse(str(addUser(fbID)))

def getuser(request, fbID):
    return HttpResponse(str(getUser(fbID)))

def getuserdata(request, fbID):
    user = getUser(fbID)
    tabs = getAllTabs(user)
    ret = ""
    for tabID in tabs:
        tab = Tab.objects.get(id=tabID)
        uID = tab.userID1
        if(uID==user): uID = tab.userID2
        u = User.objects.get(id=uID)
        sign = 1 if uID<user else -1
        ret+=str(u.facebookID)+","+str(sign*tab.total)+" "
    return HttpResponse(ret)

def addtab(request, fbID1, fbID2):
    u1 = getUser(fbID1)
    u2 = getUser(fbID2)
    if(getTab(u1,u2)!=-1): return HttpResponse("suck.")
    else:
        return HttpResponse(str(addTab(getUser(fbID1), getUser(fbID2))))


def additem(request, tabID, amount):
    itemID = addItem(tabID,-1,"no description",long(amount))
    return HttpResponse(str(itemID))


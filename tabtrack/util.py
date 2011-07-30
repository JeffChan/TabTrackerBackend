import datetime

import models

def getAllTabs(user):
    query1 = Tab.objects.all().filter(userID1=user)
    query2 = Tab.objects.all().filter(userID2=user)
    ret = []
    for tab in query1:
        ret.append(tab.id)
    for tab in query2:
        ret.append(tab.id)
    return ret
    
def getAllItems(tab):
    query = Item.objects.all().filter(tabID=tab)
    ret = []
    for item in query:
        ret.append(item.id)
    return ret
        
def getEvent(tab):
    query = Event.objects.all().filter(tabID=tab)
    return query[0].id
    
def addItem(tab, event, desc, amount):
    item = Item(tabID=tab, eventID=event, description=desc, amountCents=amount)
    item.save()
    query = (Tab.objects.all().filter(id=tab))[0]
    query.total+=amount
    query.save()
    return query.id
    
def addTab(u1, u2):
    if(u1>u2): u1,u2=(u2,u1)
    tab = Tab(userID1=u1, userID2=u2, total=0)
    tab.save()
    return tab.id
    
def addEvent(desc):
    event = Event(description=desc, timestamp=datetime.datetime.now())
    event.save()
    return event.id
      
def getTotalOwed(user, tab):
    query = Item.objects.all().filter(tabID=tab)
    ret = 0
    for item in query:
        ret+=item.amountCents
    query = Tab.objects.all().filter(id=tab)
    tab = query[0]
    if(user==tab.userID2):
        ret*=-1
    return ret
    
def autoShuffle(tabID):   
    depthLimit = 5
    tab = (Tab.objects.all().filter(id=tabID))[0]    
    start = tab.userID1
    target = tab.userID2
    backtrack = {start:(-1,0,-1)}
    queue = [start]
    while True:
        while len(queue)>0 and target not in backtrack:
            user = queue.pop(0)
            depth = backtrack[user][1]
            if(depth>=depthLimit): continue
            query = Tab.objects.all().filter(total=0).filter(userID1=user))[0]
            for tab in query:
                u = tab.userID2
                if u in backtrack: continue
                backtrack[u] = (user, depth+1, tab.total)
                queue.append(u)
            query = Tab.objects.all().filter(total=0).filter(userID2=user))[0]
            for tab in query:
                u = tab.userID2
                if u in backtrack: continue
                backtrack[u] = (user, depth+1, tab.total)
                queue.append(u)
        if(target not in backtrack): break
        min = None
        user = target
        while(user!=start):
            user,depth,total = backtrack[user]
            if(min==None or abs(total)<abs(min)):
                min=total
        user = target
        eventID = addEvent("AUTO DEBT TRANSFER")
        while(user!=start):
            newuser,depth,total = backtrack[user]
            u1 = min(user,newuser)
            u2 = max(user,newuser)
            tab = (Tab.objects.all().filter(userID1=u1).filter(userID2=u2))[0]
            addItem(tab.id, eventID, "AUTO DEBT TRANSFER", -min)
            user = newuser
            
    
        
        
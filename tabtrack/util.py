import datetime

from models import *

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
        
def getEvent(item):
    query = Event.objects.all().filter(itemID=item)
    return query[0].id

def getUser(fbID):
    query = User.objects.all().filter(facebookID=fbID)
    if(len(query)==0): return -1
    else: return query[0].id

def getTab(id1, id2):
    query = Tab.objects.all().filter(userID1=min(id1,id2)).filter(userID2=max(id1,id2))
    if(len(query)==0): return -1
    else: return query[0].id

def addUser(fbID):
    user = User(facebookID=fbID)
    user.save()
    return user.id

def addItem(tab, event, desc, amount):
    if(event<0): event = addEvent(desc)
    item = Item(tabID=tab, eventID=event, description=desc, amountCents=amount)
    item.save()
    query = (Tab.objects.all().filter(id=tab))[0]
    query.total+=amount
    query.save()
    return item.id

def addItemUser(u1, u2, event, desc, amount):
    a = 1 if u1<u2 else -1
    t = (Tab.objects.filter(userID1=min(u1,u2)).filter(userID2=max(u1,u2)))[0]
    addItem(t.id,event,desc,a*amount)
    
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
    otab = (Tab.objects.all().filter(id=tabID))[0]    
    start = otab.userID1
    target = otab.userID2
    while True:
        otab = (Tab.objects.all().filter(id=tabID))[0]    
        if(otab.total==0): break
        backtrack = {start:(-1,0,-1)}
        queue = [start]
        while len(queue)>0 and target not in backtrack:
            user = queue.pop(0)
            depth = backtrack[user][1]
            if(depth>=depthLimit): continue
            query = Tab.objects.all().exclude(total=0).filter(userID1=user)
            for tab in query:
                u = tab.userID2
                if(u==target and user==start): continue
                if u in backtrack: continue
                backtrack[u] = (user, depth+1, tab.total)
                queue.append(u)
            query = Tab.objects.all().exclude(total=0).filter(userID2=user)
            for tab in query:
                u = tab.userID1
                if u in backtrack: continue
                backtrack[u] = (user, depth+1, tab.total)
                queue.append(u)
        if(target not in backtrack): break
        count = {}
        count[otab.total] = 1
        user = target
        while(user!=start):
            newuser,depth,total = backtrack[user]
            amount=total if user<newuser else -total
            if amount in count: count[amount]+=1
            else: count[amount]=1
            user = newuser
        minAmount = None
        for am in count:
            if(minAmount==None or count[am]>count[minAmount]):
                minAmount = am
        print minAmount, backtrack
        user = target
        desc = "AUTO DEBT TRANSFER"
        eventID = addEvent(desc)
        addItemUser(start,target,eventID,desc,-minAmount)
        print "adding",start,"to",target,-minAmount
        while(user!=start):
            newuser,depth,total = backtrack[user]
            addItemUser(user, newuser, eventID, desc,-minAmount)
            print "adding",user,"to",newuser,-minAmount
            user = newuser
            
    
def t1():
    u1=addUser("A")
    u2=addUser("B")
    u3=addUser("C")
    t12=addTab(u1,u2)
    t13=addTab(u1,u3)
    t23=addTab(u2,u3)
    e=addEvent("food")
    i1=addItem(t12,e,"i1",1000)
    i2=addItem(t13,e,"i2",1000)
    i3=addItem(t23,e,"i3",1000)
    print getTotalOwed(u1,t12), getAllItems(t12)
    autoShuffle(t12)
    print getTotalOwed(u1,t12), getAllItems(t12)
    
def t2(a1,a2,a3):
    u1=addUser("A")
    u2=addUser("B")
    u3=addUser("C")
    t12=addTab(u1,u2)
    t13=addTab(u1,u3)
    t23=addTab(u2,u3)
    e=addEvent("food")
    i1=addItem(t12,e,"i1",a1)
    i2=addItem(t13,e,"i2",a2)
    i3=addItem(t23,e,"i3",a3)
    print getTotalOwed(u1,t12), getAllItems(t12)
    autoShuffle(t12)
    print getTotalOwed(u1,t12), getAllItems(t12)
    
def t3(a1,a2,a3,a4):
    u1=addUser("A")
    u2=addUser("B")
    u3=addUser("C")
    u4=addUser("D")
    t12=addTab(u1,u2)
    t34=addTab(u4,u3)
    t23=addTab(u2,u3)
    t41=addTab(u4,u1)
    e=addEvent("food")
    i1=addItem(t12,e,"i1",a1)
    i2=addItem(t23,e,"i2",a2)
    i3=addItem(t34,e,"i3",a3)
    i4=addItem(t41,e,"i4",a4)
    print getTotalOwed(u1,t12), getAllItems(t12)
    autoShuffle(t12)
    print getTotalOwed(u1,t12), getAllItems(t12)


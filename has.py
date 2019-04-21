# Generation Algorithms

import random, sah, simpy

def reNormNeg(x): return (x-.5) * 2
ranran = lambda : reNormNeg(random.random())
def tabRasa(i = 1):
        l =  []
        for x in range(i):
                l.append(ranran())
        return l

def createID(n,l=0):
	name = ''
	a = ['q','w','e','r','t','y','u',
             'i','o','p','a','s','d','f',
             'g','h','j','k','l','z','x',
             'c','v','b','n','m']
	A = ['Q','W','E','R','T','Y','U',
             'I','O','P','A','S','D','F',
             'G','H','J','K','L','Z','X',
             'C','V','B','N','M']
	D = ['1','2','3','4','5','6','7','8','9','0']
	r = ['+','_']
	switch = {0:a,1:A,2:a+A,3:D,4:a+D,5:a+A+D,6:A+D,7:a+r,8:A+r,9:a+A+r,10:D+r,11:a+D+r,12:A+D+r,13:a+A+D+r}
	for i in range(n):
		name += random.choice(switch[l%14])
	return name

def addID(keys,N,T=0):
    while True:
        k = createID(N,T)
        if k in keys:
            pass
        else:
            return k


def populateDictionary(n, func):
    d = dict()
    for i in range(n):
        D = d.keys()
        N = addID(D,12,6)
        d[N] = func()
    return d

def initiateAgent():
    agent = dict()
    agent['f'] = random.randint(0,7)
    agent['buffer'] = tabRasa(4) #TODO: Make (4) class/global variable
    agent['weights'] = tabRasa(4) #TODO: Make (4) class/global variable
    agent['friends'] = []
    return agent

def initiatePopulation(n):
    return populateDictionary(n,initiateAgent) #TODO: log all nodes to DNA

def generateAgent(agent, name, env, events):
    return sah.Agent(agent['f'],
                     name,
                     env,
                     agent['buffer'],
                     agent['weights'],
                     agent['friends'],
                     events)

def generatePopulation(pop):
    generated = dict()
    generated['env'] = simpy.Environment()
    generated['events'] = dict() #TODO: Make class variable
    generated['agents'] = dict()
    for i in pop.keys():
        generated['agents'][i] = generateAgent(pop[i],
                                               i,
                                               generated['env'],
                                               generated['events'])
    return generated

def addNod(d,k,agent=initiateAgent()):
    D = d.keys()
    N = addID(D,12,6)
    d[N] = agent
    k['agents'][N] = generateAgent(agent,N,k['env'],k['events'])
    #TODO: log ADDNOD to DNA

def delNod(d,k,N):
    k['agents'].pop(N)
    k['events'].pop(N)
    d.pop(N)
    #TODO: log DELNOD to DNA

def addCon(d,k,a1,a2):
    w = ranran()
    k['agents'][a1].addFriend(a2,w)
    d[a1]['weights'] += [w]
    d[a1]['friends'] += [a2]
    #TODO: log ADDCON to DNA

def delCon(d,k,a1,a2):
    k['agents'][a1].delFriend(a2)
    f = d[a1]['friends'].index(a2)
    del d[a1]['friends'][f+4] #TODO: Make (4) class/global variable
    del d[a1]['weights'][f+4] #TODO: Make (4) class/global variable
    #TOD: log DELCON to DNA

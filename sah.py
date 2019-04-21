# Core Classes

import numpy, simpy, random, has


_funkies =  {0:numpy.sin,
             1:numpy.cos,
             2:numpy.tanh,
             3:numpy.rint,
             4:numpy.sign,
             5:lambda x: numpy.around(x,1),
             6:lambda x: max(x, x/(2*numpy.pi)),
             7:lambda x: x
             }


class Agent(object):
        
        def __init__(self, f, name, env, buffer, weights, friends, events):
                self.buffer = buffer
                self.weights = weights
                self.function = _funkies[f]
                self.name = name
                self.env = env
                self.action = env.process(self.run())
                self.friends = friends
                self.events = events
                self.events[name] = 0
        def addFriend(self,n,w):
                self.friends = self.friends + [n]
                self.weights = self.weights + [w]
        def delFriend(self,n):
                k = self.friends.index(n)
                del self.friends[k]
                del self.weights[k]
        def tapOut(self, duration):
                yield self.env.timeout(duration)
        def updateBuffer(self, _list,_item):
                l = _list
                l.pop(0)
                l.append(_item)
                return l

        def mainLoop(self, ins, wght, func, out):
                XXX = numpy.array(ins) * numpy.array(wght)
                YYY = numpy.sum(XXX)
                YYY = func(YYY)
                self.events[self.name] = YYY
                return self.updateBuffer(out, YYY)
        
        def run(self):
                while True:
                        fs = []
                        for i in self.friends:
                                try:
                                        fs.append(self.events[i])
                                except:
                                        fs.append(0)
                        self.buffer = self.mainLoop(self.buffer + fs,self.weights,self.function,self.buffer)
                        yield self.env.process(self.tapOut(2))

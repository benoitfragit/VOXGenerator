#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pickle

class ICommandSelector:
    def __query__(self, sentence):
        raise NotImplementedError('subclasses must override __query__()!')

class FuzzySelector(ICommandSelector):
    def __init__(self):
        self.__words__ = {}
        self.__tfidf__ = {}
    
    def __build__(self, name, dic, force_rebuild):
        if force_rebuild:
            self.__occurence__(dic)
            self.__frequency__(dic)
        
            self.__serialize__(name)
        else:
            if not self.__deserialize__(name):
                self.__build__(name, dic, True)             
    
    def __occurence__(self, dic):
        for key in dic:
            sentence = dic[key];
            words = sentence.split(" ")
            
            for word in words:
                if not self.__words__.has_key(word):
                    self.__words__[word] = 1
                else:
                    self.__words__[word] += 1
    
    def __frequency__(self, dic):
        for key in dic :
            self.__tfidf__[key] = []
            
            sentence = dic[key]
            words = sentence.split(" ")
    
            for word in self.__words__:
                freq = 0.0
                
                if word in words:
                    tf   = float(words.count(word))/float(len(words)) 
                    idf  = math.log(float(len(dic))/float(self.__words__[word] )) 
                    freq = tf * idf
                
                self.__tfidf__[key].append(freq)

            
            if sum( self.__tfidf__[key] ) != 0: 
                self.__tfidf__[key] = [ float(elm) / float( sum( self.__tfidf__[key] )) for elm in self.__tfidf__[key]]
    
    def __query__(self, sentence):
        words = sentence.split(" ")
        proj = []
        
        for word in self.__words__:
            query_freq = 0
            
            if word in words:
                query_freq = float(words.count(word))/float(len(words)) * math.log(float(len(self.__tfidf__))/float(self.__words__[word] ))
            
            proj.append(query_freq)

        first = True
        minDist = 0
        idx = -1

        for index in self.__tfidf__:
            ll = self.__tfidf__[index] # here we have a list            

            res = [ (ll_i - tab_i) * (ll_i - tab_i) for ll_i, tab_i in zip(ll, proj)] 
            dist = sum(res)
            
            if first == True or dist < minDist :
                minDist = dist
                idx = index
                first = False

        return idx

    def __serialize__(self, name):
        filepath = str(name) + ".bin"
        output = open(filepath, 'w')
        pickle.dump(self.__words__, output)
        pickle.dump(self.__tfidf__, output)
        output.close()    

    def __deserialize__(self, name):
        filepath = str(name) + ".bin"
        
        try:
            with open(filepath, 'rb') as inp:
                self.__words__ = pickle.load(inp)
                self.__tfidf__ = pickle.load(inp)
                inp.close()
                
                return True
                                   
        except IOError:
            print "The dic file " + filepath + " is not found" 
            return False
            
    def __show__(self):
        print "TFIDF Frequencies\n"
        for key in self.__tfidf__:
            liste = self.__tfidf__[key]
            
            st = str(key) + " "
            for item in liste:
                st += str(item) + " "
            
            print st + "\n"
        
        print "Words count\n"
        for w in self.__words__:
            print w, self.__words__[w]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

class Checksum:        
    def __haschanged__(self, f):
        checksum_file = f.split('.')[0] + ".md5"
        
        result = False
        if os.path.exists(checksum_file):
            result = self.__comparechecksum__(checksum_file, f)
        
        checksum = self.__computemd5checksum__(f)
        with open(checksum_file, "w") as fl:
            fl.write(str(checksum))
            fl.close()    
    
        return result
                
    def __comparechecksum__(self, checksum_file, f):
        first_line = ''
        
        with open(checksum_file, 'r') as md5file:
            first_line = md5file.readline()
            checksum   = self.__computemd5checksum__(f)
            
            if first_line == str(checksum):
                return False
        
        return True
    
    def __computemd5checksum__(self, f):
        hasher = hashlib.md5() 
        with open(f, "rb") as ff:
            buf = ff.read()
            hasher.update(buf)
            checksum = hasher.hexdigest()
            
            return checksum
        
        return 0x0

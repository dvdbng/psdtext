#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Busca y exporta textos en un psd de Adobe Photohop
# 

# [^a-zA-Z0-9<>\ [\]\-_\.\\{}/:+*ñáéíóúÁÉÍÓÚ|;@#$%&="' ]

import re
import sys

START = "/Text " + chr(40) + chr(254) + chr(255);

class export():
    def write(self,fn,str):
        pass
    def close(self):
        pass
    
class singleFileExport(export):
    def __init__(self):
        self.fn = "psd-text.txt"
        self.f = open(self.fn, "wb")
        self.last = ""
    def write(self,fn,str):
        if fn != self.last:
            self.last = fn
            self.f.write("\n\n\n====================================================\n")
            self.f.write("FILE: %s \n" % fn);
        self.f.write("\n\nCADENA:__")
        self.f.write(str.encode("utf-8"))
        self.f.write("__")
    def close(self):
        self.f.close()

class multipleFileExport(export):
    def __init__(self):
        self.f = None
        self.fn = ""
    def write(self,fn,str):
        if self.fn != fn:
            if self.f:
                self.f.close()
            self.f = open('psd_'+fn+'.txt',"wb")
            self.fn = fn
            self.f.write("\n\nCADENA:__")
            self.f.write(str.encode("utf-8"))
            self.f.write("__")
    def close(self)	:
        if self.f:
            self.f.close()

class consoleExport(export):
    def __init__(self):
        self.last = ""
    def write(self,fn,str):
        if fn != self.last:
            self.last = fn
            print("\n\n\n====================================================\n")
            print("FILE: %s \n" % fn);
        print("\n\nCADENA:__")
        print(str.encode("utf-8"))
        print("__")
    def close(self):
        pass

def parse(fn,export):
    print("PARSEANDO ARCHIVO %s" % fn)
    f = open(fn,"r");
    b = f.read()
    while b:
        p = b.find(START)
        if p>0:
            b = b[p+len(START):]
            str = ""
            
            fb = ord(b[0])
            while fb != 41:
                ch = unichr(fb*256 + ord(b[1]))
                if fb != 0:
                    print (fb*256 + ord(b[1]),ch)
                b = b[2:]
                str += ch
                fb = ord(b[0])
            export.write(fn,str)
        else:
            b=False




def main():
    ex = None
    p = sys.argv
    fi = 0
    for k in p:
        if fi == 1:
            if k == "-h" or k == "--help":
                print """Modo de uso:
    psdtext [output] [file]...  : Extract text from psd files
    psdtext [-h | --help]       : Show this help
    
    output is one of:
        single: Export text in a single file
        multiple: Export text in multiple files
        console: Print text in console
        
    output defaults to multiple"""
                return
            elif k  == "single":
                ex = singleFileExport()
            elif k == "console":
                ex = consoleExport()
            else:
                ex = multipleFileExport()
                if k != "multiple":
                    parse(k,ex)
        elif fi>1:
            parse(k,ex)
        fi += 1
        if ex:
            ex.close()
    

main()

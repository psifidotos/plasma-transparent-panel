#! /usr/bin/env python

import os, sys
import shutil, errno
from subprocess import call

def copyanything(src, dst):
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def get_immediate_subdirectories(a_dir):
    try:
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]
    except FileNotFoundError:
        return []

def show_themes():
    rootthemedir2 = "/usr/share/plasma/desktoptheme/"
    userthemedir2 = os.path.join(os.getenv("HOME"),".local/share/plasma/desktoptheme/")

    mainthemes2 = get_immediate_subdirectories(rootthemedir2)
    userthemes2 = get_immediate_subdirectories(userthemedir2)
    print(mainthemes)
    print(userthemes)

rootthemedir = "/usr/share/plasma/desktoptheme/"
userthemedir = os.path.join(os.getenv("HOME"),".local/share/plasma/desktoptheme/")

mainthemes = get_immediate_subdirectories(rootthemedir)
userthemes = get_immediate_subdirectories(userthemedir)

if len(sys.argv) == 1:
    print("no parameters")
    exit()

written=False
newthemepath = ""

if sys.argv[1] == "--list":
    show_themes()
else:
    if sys.argv[2]!="West" and sys.argv[2]!="North" and sys.argv[2]!="East" and sys.argv[2]!="South":
        print("Panel position can be: North, South, West, East")
        exit()
                      
    if sys.argv[1] in mainthemes:       
        print("main theme: "+sys.argv[1])
        originaltheme=rootthemedir+sys.argv[1]
        if sys.argv[1].startswith("breeze"):
            originaltheme= os.path.join(rootthemedir,"default")
        
        if len(sys.argv) > 2:
            newthemepath = userthemedir+sys.argv[1]+" - "+sys.argv[2]+" Transparent"
            copyanything(originaltheme,newthemepath)
            if sys.argv[1].startswith("breeze"):
                os.remove(os.path.join(newthemepath,"metadata.desktop"))
                
                shutil.copyfile(os.path.join(rootthemedir,sys.argv[1],"metadata.desktop"),os.path.join(newthemepath,"metadata.desktop"))
                shutil.copyfile(os.path.join(rootthemedir,sys.argv[1],"colors"),os.path.join(newthemepath,"colors"))
            written=True
    elif sys.argv[1] in userthemes:
        print("user theme: "+sys.argv[1])
        if len(sys.argv) > 2:
            newthemepath = userthemedir+sys.argv[1]+" - "+sys.argv[2]+" Transparent"
            copyanything(userthemedir+sys.argv[1],newthemepath)        
            written=True
    else:
        print("unknown theme")
        
if written==True:
    fname = os.path.join(newthemepath,"metadata.desktop")
    fnewname = os.path.join(newthemepath,"metadata.desktop.new")
    f=open(fname)
    fnew=open(fnewname,"w")
    
    for line in f:
        if line.startswith('Name='):
            fnew.write(line[:-1]+" - "+sys.argv[2]+" Transparent")
        elif line.startswith('Comment') or line.startswith('Name[') or line.startswith('Name ['):
            i=0 #do nothing
            #print("")
        else:
            fnew.write(line)
       
    f.close()
    fnew.close()
    os.remove(fname)
    os.rename(fnewname, fname)

    
    fname = os.path.join(newthemepath,"widgets/panel-background.svgz")
    try:
        os.rename(fname, os.path.join(newthemepath,"widgets/panel-background.svg.gz"))
    except FileNotFoundError:
        print("panel-background.svgz not found")
    else:
        fname = os.path.join(newthemepath,"widgets/panel-background.svg.gz")
        call(["gunzip",fname])
    
    fnewname = os.path.join(newthemepath,"widgets/panel-background-new.svg")
    fname = os.path.join(newthemepath,"widgets/panel-background.svg")
    f=open(fname)
    fnew=open(fnewname,"w")
    
    usersEnabledShadows = []
    usersDisabledShadows = []
    
    if(len(sys.argv)>=4):
        for x in range(3, len(sys.argv)):
            if(sys.argv[x].startswith("-")):
                usersDisabledShadows.append(sys.argv[x][1:])
            else:
                usersEnabledShadows.append(sys.argv[x])

    print("Disabled Shadows")
    edge=""
    if(sys.argv[2]=="North"):
        edge="north"
    elif(sys.argv[2]=="West"):
        edge="west"
    elif(sys.argv[2]=="East"):
        edge="east"
    elif(sys.argv[2]=="South"):
        edge="south"
    
    searchStr='id="'+edge
    containsThisPanel = False
    for line in f:
        if searchStr in line:
            containsThisPanel = True
    f.close()
    f=open(fname)
    
    excludeLines=False
    inlineItems=0
    bufferPreviousStr=""
    for line in f:
        if (line.startswith('</svg>')and(not containsThisPanel)):
             center = "south-center"
             edge = "south-top"
             minicenter = "south-mini-center"
             miniedge = "south-mini-top"
             if sys.argv[2] == 'West':
                 fnew.write('<!-- West panel transparency -->\n')
                 center="west-center"
                 edge="west-right"
                 minicenter="west-mini-center"
                 miniedge="west-mini-right"
             elif sys.argv[2] == 'East':
                 fnew.write('<!-- East panel transparency -->\n')
                 center="east-center"
                 edge="east-left"
                 minicenter="east-mini-center"
                 miniedge="east-mini-left"
             elif sys.argv[2] == 'North':
                 fnew.write('<!-- North panel transparency -->\n')
                 center="north-center"
                 edge="north-bottom"
                 minicenter="north-mini-center"
                 miniedge="north-mini-bottom"                 
             
             fnew.write('  <g id="'+center+'" style="opacity:0">\n')
             fnew.write('  <rect x="0" y="0" height="10" width="10" style="opacity:0"/> </g>\n')
             fnew.write('  <g id="'+edge+'"  style="opacity:0">\n')
             fnew.write('  <rect x="0" y="0" height="10" width="10" style="opacity:0"/> </g>\n')             
             fnew.write('  <g id="'+minicenter+'" style="opacity:0">\n')
             fnew.write('  <rect x="0" y="0" height="10" width="10" style="opacity:0"/> </g>\n')
             fnew.write('  <g id="'+miniedge+'"  style="opacity:0">\n')
             fnew.write('  <rect x="0" y="0" height="10" width="10" style="opacity:0"/> </g>\n')
             fnew.write(line)            
        elif (searchStr in line):
             pos1 = line.index('"')
             pos2 = line.index('"',pos1+1)
             splitted = line[0:pos2+1]
             if( 'style="' in bufferPreviousStr):
                        pos1=bufferPreviousStr.index('style="')
                        pos2=bufferPreviousStr.index('"',pos1+7)
                        remover = bufferPreviousStr[:pos1]+bufferPreviousStr[pos2+1:]
                        bufferPreviousStr = remover
             fnew.write(bufferPreviousStr + splitted)
             bufferPreviousStr = ""
             if "</g>" not in line and "/>" not in line:
                 excludeLines=True
             else:
                 fnew.write('" style="opacity:0"/>\n');
        else:
            if not excludeLines:
                newline=""
                endLine=False
                
                if line.endswith(">\n"):
                    newline= line[:-2]+' style="opacity:0">\n'
                else:
                    newline= line[:-1]+' style="opacity:0"\n'
                    endLine=True
                
                shadowIdLineFound=False
                if 'id="shadow-topleft"' in line and ((sys.argv[2] != "North" and sys.argv[2] != "West" and "topleft" not in usersEnabledShadows) or ("topleft" in usersDisabledShadows)):
                    print("topleft")
                    shadowIdLineFound = True
                elif 'id="shadow-top"' in line and ((sys.argv[2] != "North" and "top" not in usersEnabledShadows)or("top" in usersDisabledShadows)) :
                    print("top")
                    shadowIdLineFound = True
                elif 'id="shadow-topright"' in line and ((sys.argv[2] != "North" and sys.argv[2] != "East" and "topright" not in usersEnabledShadows)or("topright" in usersDisabledShadows)):
                    print("topright")
                    shadowIdLineFound = True
                elif 'id="shadow-right"' in line and ((sys.argv[2] != "East" and "right" not in usersEnabledShadows)or("right" in usersDisabledShadows)):
                    print("right")
                    shadowIdLineFound = True
                elif 'id="shadow-bottomright"' in line and ((sys.argv[2] != "East" and sys.argv[2] != "South" and "bottomright" not in usersEnabledShadows)or("bottomright" in usersDisabledShadows)):
                    print("bottomright")
                    shadowIdLineFound = True
                elif 'id="shadow-bottom"' in line and ((sys.argv[2] != "South" and "bottom" not in usersEnabledShadows)or("bottom" in usersDisabledShadows)):
                    print("bottom")
                    shadowIdLineFound = True
                elif 'id="shadow-bottomleft"' in line and ((sys.argv[2] != "South" and sys.argv[2] != "West" and "bottomleft" not in usersEnabledShadows)or("bottomleft" in  usersDisabledShadows)):
                    print("bottomleft")
                    shadowIdLineFound = True
                elif 'id="shadow-left"' in line and ((sys.argv[2] != "West" and "left" not in usersEnabledShadows)or("left" in usersDisabledShadows)):
                    print("left")
                    shadowIdLineFound = True
                    
                if shadowIdLineFound:
                    if( 'style="' in bufferPreviousStr):
                        pos1=bufferPreviousStr.index('style="')
                        pos2=bufferPreviousStr.index('"',pos1+7)
                        remover = bufferPreviousStr[:pos1]+bufferPreviousStr[pos2+1:]
                        bufferPreviousStr = remover
                    
                    if endLine == False:
                        fnew.write(bufferPreviousStr+newline)
                    else:
                        fnew.write(bufferPreviousStr)
                        excludeLines = True
                        
                    bufferPreviousStr=""
                else:
                    bufferPreviousStr = bufferPreviousStr + line
                        
                if ">" in line and not shadowIdLineFound:
                    fnew.write(bufferPreviousStr)
                    bufferPreviousStr=""
                #else:
                 #   fnew.write(line)
                 #   bufferPreviousStr=""
                        #fnew.write(line)   
                    
            elif excludeLines and "</g>" in line:
                p1=line.index("</g>")
                fnew.write(' style="opacity:0">\n')
                fnew.write('  <rect x="0" y="0" height="10" width="10" style="opacity:0"/> </g>\n')
                fnew.write(line[p1+4:])    
                excludeLines=False
                inlineItems=0
            elif excludeLines and "/>" in line:
                if(inlineItems==0):
                    p2=line.index("/>")
                    fnew.write(' style="opacity:0"/>\n')
                    excludeLines=False
                else:
                    inlineItems=inlineItems-1
            elif excludeLines and "<" in line:
                inlineItems=inlineItems+1
            
    f.close()
    fnew.close()
    os.remove(fname)
    os.rename(fnewname, fname)
    #os.system("gzip -S z "+fname.replace(" ","\ "))
    call(["gzip",fname])
    os.rename(fname+".gz", os.path.join(newthemepath,"widgets/panel-background.svgz"))
    
    call(["kbuildsycoca5","--noincremental"])
    






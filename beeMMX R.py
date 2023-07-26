import math
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog as fs
from tkinter import ttk
from PIL import ImageTk as it, Image as img
import os
import mutagen as mg
import keyboard as kb
import sys
import json
import shutil
import webbrowser as web
from datetime import date as dt, datetime as dtime
import darkdetect as drk
import scipy.io.wavfile as wave
import gzip as gz
import tktooltip as tip
import configparser as cfg
from discordrp import Presence
import time

if len(sys.argv)>1:
    os.chdir(os.path.dirname(sys.executable))

for i in os.listdir(os.path.join(os.getcwd(),'logs')):
    if os.path.splitext(os.getcwd()+'/logs/'+i)[1] == '.txt':
        with open(os.path.join(os.getcwd(),'logs',i),'rb') as log, gz.open(os.path.join(os.getcwd(),'logs',i)+'.gz','wb') as gzip:
            gzip.writelines(log)
        os.remove(os.path.join(os.getcwd(),'logs',i))

def openDir():
    web.open('file:///'+os.path.dirname(sys.executable))

def Image(name):
    return it.PhotoImage(img.open(os.path.join(os.getcwd(),'media/missing.png')) if (dt.today().day==1 and dt.today().month==4) or name.strip()=='' else (img.open(os.getcwd()+'/'+name)))

music = []

os.makedirs(os.path.join(os.getcwd(),'logs'),exist_ok=True)

fileList = os.listdir(os.path.join(os.getcwd(),'logs'))
if len(fileList)>10:
    for i in fileList:
        try:
            os.remove(os.path.join(os.getcwd(),'logs',i))
        except PermissionError:
            print('[Emptying log folder] Error: permission denied to file \'{}\'!'.format(i))
del(fileList)

sys.stdout = open(os.path.join(os.getcwd(),'logs',dtime.now().strftime('%d.%m.%Y_%H-%M-%S.txt')),'w')
sys.stderr = sys.stdout

class Style:
    def __init__(self,name,id,authors,ui_name,vanilla):
        self.name = name
        self.id = id
        self.authors = authors
        self.ui_name = ui_name
        self.vanilla = vanilla

class gelData:
    def __init__(self,files:dict[tuple | str]):
        self.files = files

class funnelData:
    def __init__(self,file:str,sync:bool=False):
        self.file=file
        self.sync=sync

class Track:
    def __init__(self,ID:str,short_title:str,title:str,description:str,authors:str,length:str,image:str,preview:str,music:str,sample:str,group:str,key:str,style:Style,noLarge:bool,gels:gelData|None,funnel:funnelData|None):
        self.id = ID
        self.short_title = short_title
        self.title = title
        self.desc = description
        self.authors = authors
        self.length = length
        self.image = image
        self.preview = preview
        self.music = music
        self.sample = sample
        self.group = group
        self.key = key
        self.style = style
        self.noLarge = noLarge
        self.gels = gels
        self.funnel = funnel

styles = {
    'bts':Style('Behind The Scenes','BEE2_BTS','TeamSpen210','',False),
    'over':Style('Overgrown','BEE2_OVERGROWN','TeamSpen210','',True),
    'clean':Style('Clean','BEE2_CLEAN','Valve, Carl Kenner, TeamSpen210','',True),
    'original_clean':Style('Clean (Original Textures)','BEE2_CLEAN_ORIGINAL','Valve','Original Clean',True),
    'grass_clean':Style('Grass Clean','BEE2_GRASS_CLEAN','joethegamer',"joethegamer's Grass Clean",False),
    'hybrid':Style('Hybrid','AXO_HYBRID','Valve, Axo',"Axo's Hybrid",False),
    'p1':Style('Portal 1 Style','BEE2_PORTAL_1','Carl Kenner, TeamSpen210, Valve','Portal 1',True),
    'cave':Style('Deep Cave','DDS_CAVE_STYLE','Drgregs',"Drgregs' Deep Cave",False),
    'rocky':Style('Rocky Cave','SUBSTYLE_CAVE_STYLE','Drgregs',"Drgregs' Rocky Cave",False),
    'dev':Style('Developer Style','DDS_DEV_STYLE','Drgregs',"Drgregs' Developer",False),
    'gray':Style('Solid Gray Dev','SUBSTYLE_DEV_STYLE','Drgregs',"Drgregs' Solid Gray Developer",False),
    'gmod':Style("Garry's Mod Style",'DDS_GMOD_STYLE','Facepunch, Drgregs',"Drgregs' GMod",False),
    'floor':Style('Unpolished Floor','SUBSTYLE_GMOD_STYLE','Facepunch, Drgregs',"Drgregs' Unpolished Floor",False),
    '50s':Style('1950s Old Aperture','BEE2_1950s','Carl Kenner, TeamSpen210, Critfish','1950s',True),
    '60s':Style('1960s Old Aperture','BEE2_1960s','Carl Kenner, TeamSpen210, Critfish','1960s',True),
    '70s':Style('1970s Old Aperture','BEE2_1970s','Carl Kenner, TeamSpen210','1970s',True),
    '80s':Style('1980s Old Aperture','BEE2_1980s','Carl Kenner, TeamSpen210','1980s',True),
    'twtm':Style('TWTM Style','TWTM_STYLE_PACK:TWTM','Stridemann, Catperson6, Super 82533, Darealxbox','Catperson6\'s TWTM',False),
    'none':Style('','','','None',True)
}

styleNames = []
for i in styles:
    if styles[i].ui_name == '':
        styleNames.append(styles[i].name)
    else:
        styleNames.append(styles[i].ui_name)

def label(window,column,row,text):
    tk.Label(window,text=text,foreground=light,background=dark).grid(column=column,row=row,padx=5)

def field(window,column,row,off=False):
    fld = tk.Entry(window,foreground=light,background=darkField,relief='flat',disabledbackground=inactive,disabledforeground=darkField,state= 'disabled' if off else 'normal')
    fld.grid(column=column,row=row,padx=5)
    return fld

def labelField(window,col,row,text,startInactive=False):
    """Constructs a labelled text field.\n
    \n
    window - a LabelFrame, Frame or Master object. The objects will be placed there.\n
    col - column in which both objects will be in.
    row - row of the Label. The Entry will be one row lower.\n
    text - the Label's content.\n
    startInactive - whether the Entry should start disabled.
    """
    label(window,col,row,text)
    fld = field(window,col,row+1,startInactive)
    return fld

win = tk.Tk()

darkmode = tk.BooleanVar(win,drk.isDark())

global dark, light, darkField, inactive, darkTip

darkTip = '#222244' if darkmode.get() else '#CCCCCC'
dark = '#111133' if darkmode.get() else None
light = '#FFFFFF' if darkmode.get() else None
darkField = '#333355' if darkmode.get() else '#FFFFFF'
inactive = '#202030' if darkmode.get() else '#DDDDDD'

def reloadTheme():

    print('[Theme refresh] Reload triggered! Intitiating theme reload functions...')

    global dark, light, darkField, inactive, darkTip

    darkTip = '#222244' if darkmode.get() else '#F5F5F5'
    dark = '#111133' if darkmode.get() else '#EEEEEE'
    light = '#FFFFFF' if darkmode.get() else '#000000'
    darkField = '#333355' if darkmode.get() else '#FFFFFF'
    inactive = '#000020' if darkmode.get() else '#DDDDDD'

    for i in main.winfo_children():
        for f in i.winfo_children():
            if type(f)!=ttk.Combobox:
                match type(f):
                    case tk.Entry:
                        f.configure(foreground=light,background=darkField,relief='flat',disabledbackground=inactive,disabledforeground=darkField)
                    case tk.Listbox:
                        f.config(yscrollcommand=scrollbar.set,relief='flat',background=darkField,foreground=light)
                    case tk.Checkbutton:
                        f.config(background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField)
                    case tk.Label:
                        f.config(background=dark,foreground=light)
                    case tk.Button:
                        f.config(background=darkField,foreground=light,activebackground=darkField,activeforeground=light,disabledforeground=inactive)
                    case tk.Spinbox:
                        f.config(foreground=light,background=darkField,buttonbackground=dark)
                print('[Theme refresh] Object ',i.winfo_children().index(f)+1,'/',len(i.winfo_children()),' refreshed!',sep='')
        if type(i)==tk.LabelFrame:
            i.configure(background=dark,foreground=light)
        print('[Theme refresh] Frame ',main.winfo_children().index(i)+1,'/',len(main.winfo_children()),' refreshed!',sep='')
    main.config(bg=dark)
    extra.config(bg=dark)

    #for i in tips:
    #    pass

    #for i in extra.winfo_children():
    #    for f in i.winfo_children():
    #        if type(f)!=type(ttk.Combobox()):
    #            print(f,type(f),sep=' | ')
    #            match type(f):
    #                case tk.Entry:
    #                    f.configure(foreground=light,background=darkField,relief='flat',disabledbackground=inactive,disabledforeground=darkField)
    #                case tk.Listbox:
    #                    f.config(yscrollcommand=scrollbar.set,relief='flat',background=darkField,foreground=light)
    #                case tk.Checkbutton:
    #                    f.config(background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField)
    #                case tk.Label:
    #                    f.config(background=dark,foreground=light)
    #                case tk.Button:
    #                    f.config(background=darkField,foreground=light)
    #                case tk.Spinbox:
    #                    f.config(foreground=light,background=darkField,buttonbackground=dark)
    #                case _:
    #                    pass
    #    if type(i)==tk.LabelFrame:
    #        i.configure(background=dark,foreground=light)

    print('[Theme refresh] Refreshing Extras tab...')

    for i in extra.winfo_children():
        i.config(background=dark,foreground=light)
        for g in i.winfo_children():
            match type(g):
                case tk.Checkbutton:
                    g.config(background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField)
                case tk.Button:
                    g.config(background=darkField,foreground=light,activebackground=darkField,activeforeground=light,disabledforeground=inactive)
                case tk.Label:
                    g.config(background=dark,foreground=light)
                case tk.Entry:
                    g.configure(foreground=light,background=darkField,relief='flat',disabledforeground=darkField,disabledbackground=inactive)
                case tk.LabelFrame:
                    g.config(background=dark,foreground=light)
                    for f in g.winfo_children():
                        match type(f):
                            case tk.Listbox:
                                f.config(relief='flat',background=darkField,foreground=light)
                            case tk.Scrollbar:
                                f.config()
                case _:
                    print(str(type(g))+' failed! [line 164]')
            print('[Theme refresh] Object ',i.winfo_children().index(g)+1,'/',len(i.winfo_children()),' refreshed!',sep='')
        print('[Theme refresh] Frame ',extra.winfo_children().index(i)+1,'/',len(extra.winfo_children()),' refresh completed!',sep='')

    win.config(background=dark)

    fileMenu.config(background=darkField,foreground=light)
    openMenu.config(background=darkField,foreground=light)
    menu.config(background=darkField,foreground=light)

    refreshTips()
    
    for i in menu.winfo_children():
        f.config(background=darkField,foreground=light)
    
    print('Theme setup done!')

tabs = ttk.Notebook(win)

startTime = tk.IntVar(win,int(time.time()))

# discord application ID of 'beeMMX R', which is used for rich presence
discord_APPID = '1132691764755578910'
with Presence(discord_APPID) as rpc:
    rpc.set(
        {
            'state':'Editing a package',
            'details':'File: none',
            'timestamps':{'start':startTime.get()},
            'assets':{
                'large-image':'beemmx_r',
                'large_text': 'beeMMX R is a tool which generates music packages for BEE2. Learn more by clicking the GitHub button.'
            },
            'buttons':[
                {
                    'url':'https://github.com/TPEcool/beeMMX-R',
                    'label': 'beeMMX R on GitHub'
                },
                {
                    'url':'https://discord.gg/gb7cp6asJF',
                    'label':'Discord server'
                }
            ]
        }
    )

def setPresence(filename:str | None):
    startTime.set(int(time.set()))
    with Presence(discord_APPID) as rpc:
        rpc.set(
            {
                'state':'Editing a package',
                'details':'File: '+('none' if filename is None else '\''+os.path.basename(filename)+'\''),
                'timestamps':{'start':startTime.get()},
                'assets':{
                    'large-image':'beemmx_r',
                    'large_text': 'beeMMX R is a tool which generates music packages for BEE2. Learn more by clicking the GitHub button.'
                },
                'buttons':[
                {
                    'url':'https://github.com/TPEcool/beeMMX-R',
                    'label': 'beeMMX R on GitHub'
                },
                {
                    'url':'https://discord.gg/gb7cp6asJF',
                    'label':'Discord server'
                }
            ]
            }
        )

main = tk.Frame(tabs,background=dark)
main.pack(side=tk.BOTTOM,fill=tk.BOTH)

win.iconbitmap(os.path.join(os.getcwd(),'media','icon.ico'))
win.resizable(False,False)
win.title('beeMMX R')

packdata = tk.LabelFrame(main,text='Package information',labelanchor='n',background = dark, foreground = light)
packdata.grid(row=0,column=0,padx=5,pady=5)

tk.Label(packdata,text='Package name',foreground=light,background=dark).grid(row=0,column=0,padx=5)
tk.Label(packdata,text='Package description',foreground=light,background=dark).grid(row=0,column=1,padx=5)
tk.Label(packdata,text='Package ID',foreground=light,background=dark).grid(row=2,column=0,padx=5)
tk.Label(packdata,text='Track ID prefix',foreground=light,background=dark).grid(row=2,column=1,padx=5)

main.config(background=dark)

packtitle = tk.Entry(packdata,foreground=light,background=darkField,relief='flat')
packtitle.grid(row=1,column=0,padx=5,pady=5)
packdesc = tk.Entry(packdata,foreground=light,background=darkField,relief='flat')
packdesc.grid(row=1,column=1,padx=5,pady=5)
packid = tk.Entry(packdata,foreground=light,background=darkField,relief='flat')
packid.grid(row=3,column=0,padx=5,pady=5)
prefix = tk.Entry(packdata,foreground=light,background=darkField,relief='flat')
prefix.grid(row=3,column=1,padx=5,pady=5)

trackdata = tk.LabelFrame(main,text='Track information',labelanchor='n',background=dark,foreground=light)
trackdata.grid(row=0,column=1,padx=5,pady=5)

desc = tk.Entry(trackdata,foreground=light,background=darkField,relief='flat')
desc.grid(row=1,column=0,padx=5,pady=5)
tk.Label(trackdata,text='Description',foreground=light,background=dark).grid(row=0,column=0,padx=5)

title = tk.Entry(trackdata,foreground=light,background=darkField,relief='flat')
title.grid(row=1,column=1,pady=5,padx=5)
label(trackdata,1,0,'Name')

shortName = tk.Entry(trackdata,foreground=light,background=darkField,relief='flat')
shortName.grid(row=1,column=2,padx=5,pady=5)
label(trackdata,2,0,'Short name')

loopvar = tk.BooleanVar(main,False)

def setLoop():
    tLen.config(state=('disabled' if loopvar.get() else 'normal'))

dontLoop = tk.Checkbutton(trackdata,text="Don't loop",variable = loopvar,command=setLoop,foreground=light,background=dark,relief='flat',activebackground=dark,activeforeground=light,selectcolor=darkField)
dontLoop.grid(row=1,column=3,padx=5,pady=5)

authors = field(trackdata,0,3)
label(trackdata,0,2,'Author(-s)')

tLen = labelField(trackdata,1,2,'Length')
tID = labelField(trackdata,2,2,'ID')
group = labelField(trackdata,3,2,'Group')

sortKey = tk.Spinbox(trackdata,from_=1,to=4294967296,foreground=dark,background=light,buttonbackground=dark,buttondownrelief=tk.FLAT,buttonuprelief=tk.FLAT)
tk.Label(trackdata,text='Sort key',foreground=light,background=dark).grid(row=4,column=0,padx=5,columnspan=2)
sortKey.grid(row=5,column=0,padx=5,pady=5,columnspan=2)

stylevar = tk.StringVar(main,'Clean')

tk.Label(trackdata,text='Suggested style',background=dark,foreground=light).grid(row=4,column=2,columnspan=2,padx=5,pady=5)
style = ttk.Combobox(trackdata,textvariable=stylevar,values=styleNames,state='readonly')
style.grid(row=5,column=2,padx=5,pady=5,columnspan=2,ipadx=25)

global beepath

if os.path.exists(os.getcwd()+'/bee2_path.txt'):
    with open(os.getcwd()+'/bee2_path.txt') as pathfile:
        beepath = tk.StringVar(main,pathfile.readlines()[0])
else:
    beepath = tk.StringVar(main,'')
    print('No pathfile found, initializing as empty path.')

#try:
global file_ico
file_ico = Image('media/file.png')
#except:
    #print('Image data failed to load, skipping...')
    #file_ico = None

trackmedia = tk.LabelFrame(main,text='Track media',labelanchor='n',background=dark,foreground=light)
trackmedia.grid(row=1,column=1,padx=5,pady=5)

prev = labelField(trackmedia,0,0,'Preview (1:1)')
photo  = labelField(trackmedia,2,0,'Image (4:3)')
samp = labelField(trackmedia,4,0,'Sample (10 secs)')
trac = labelField(trackmedia,6,0,'Track')

def sec(num:int) -> str:
    if len(str(num))==2:
        return str(num)
    elif len(str(num))==1:
        return '0'+str(num)
    else:
        raise Exception('Failed to format seconds: too long input number!')

def preview():
    shift = kb.is_pressed('shift')
    file = fs.askopenfile(defaultextension='.png',initialfile='image.png',title='Specify preview file',filetypes=[('PNG image','.png')])
    if not (file is None):
        size = img.open(file.name).size
        if size[0]==size[1] or shift:
            prev.delete(0,tk.END)
            prev.insert(tk.END,file.name)
        else:
            msg.showerror('Wrong aspect ratio','Entered image is not 1:1! If you have no other versions of this image (aspect ratio-wise), please cut it so it is 1:1, preferably with a resolution of 96x96. Hold SHIFT while clicking the button to dismiss this warning. This will make BEE2 stretch the image.')

def phot():
    shift = kb.is_pressed('shift')
    file = fs.askopenfile(defaultextension='.png',initialfile='image.png',title='Specify image file',filetypes=[('PNG image','.png')])
    if not (file is None):
        size = img.open(file.name).size
        if size[0]/4*3==size[1] or shift:
            photo.delete(0,tk.END)
            photo.insert(tk.END,file.name)
        else:
            msg.showerror('Wrong aspect ratio','Entered image is not 4:3! If you have no other versions of this image (aspect ratio-wise), please cut it so it is 4:3, preferably with a resolution of 256x192. Hold SHIFT while clicking the button to dismiss this warning. This will make BEE2 stretch the image.')

def sample():
    shift = kb.is_pressed('shift')
    file = fs.askopenfile(defaultextension='.ogg',initialfile='music.ogg',title='Specify sample file',filetypes=[('OGG Vorbis music','.ogg .vorbis'),('Microsoft WAVE music','.wav .wave')])
    if file is not None:
        if mg.File(file.name).info.length<=10 or shift:
            samp.delete(0,tk.END)
            samp.insert(tk.END,file.name)
        else:
            msg.showerror('Music file too long','The selected music file is too long! Music samples must be 10 seconds long or less! Hold SHIFT while clicking the button to dismiss this warning.')

def testWaveFile(filename:str = '') -> bool:

    '''
    Test a WAVE file for Portal 2 compatibility.\n
    Returns true if compatible, makes a dialogue box and returns False otherwise.\n\n
    filename - the name of the file to test.
    '''

    formats = {
        'float32':'32-bit floating-point',
        'int32':'32-bit or 24-bit integer PCM',
        'uint8':'8-bit integer PCM',
        'int16':'16-bit integer PCM'
    }
    global fileformat, fileformat

    fileformat = formats[str(wave.read(filename)[1].dtype)]

    if wave.read(filename)[0] == 44100:
        if str(wave.read(filename)[1].dtype) == 'int16':
            return True
        else:
            msg.showerror('Incorrect sample format',f'The file has an incorrect sample format! Expected 16-bit integer PCM, read {fileformat}. This file will crash Portal 2 and therefore was not imported.')
            return False
    else:
        msg.showerror('Incorrect sample rate','The file has an incorrect sample rate! Expected 44100 hertz, read {}. This file will crash Portal 2\'s sound engine and therefore was not imported.'.format(str(wave.read(filename)[1].dtype)))
        return False

def track():
    file = fs.askopenfilename(defaultextension='.wav',initialfile='music.wav',title='Specify track file',filetypes=[('Microsoft WAVE music','.wav .wave')])
    if file is not None and testWaveFile(file):
        trac.delete(0,tk.END)
        trac.insert(tk.END,file)
        tLen.delete(0,tk.END)
        tLen.insert(tk.END,str(int(mg.File(file).info.length//60))+':'+sec(math.ceil(mg.File(file).info.length%60)))

tk.Button(trackmedia,image=file_ico,command=preview,foreground=light,background=darkField,relief='flat').grid(row=1,column=1,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=phot,foreground=light,background=darkField,relief='flat').grid(row=1,column=3,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=sample,foreground=light,background=darkField,relief='flat').grid(row=1,column=5,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=track,foreground=light,background=darkField,relief='flat').grid(row=1,column=7,padx=5,pady=5)

def checklists():
    if shortName.get().strip()=='':
        return 'short name'
    elif title.get().strip()=='':
        return 'full name'
    elif desc.get().strip()=='':
        return 'description'
    elif authors.get().strip()=='':
        return 'authors'
    elif tLen.get().strip()=='' and loopvar.get()==False:
        return 'length'
    elif photo.get().strip()=='':
        return 'photo filename'
    elif prev.get().strip()=='':
        return 'preview filename'
    elif trac.get().strip()=='':
        return 'full track filename'
    elif samp.get().strip()=='':
        return 'sample filename'
    elif group.get().strip()=='':
        return 'group'
    else: return True
    
def resetFields():
    reset(tID,'')
    reset(shortName,'')
    reset(title,'')
    reset(desc,'')
    reset(authors,'')
    loopvar.set(False)
    tLen.config(state='normal')
    reset(tLen,'')
    reset(photo,'')
    reset(prev,'')
    reset(trac,'')
    reset(samp,'')
    reset(group,'')
    reset(sortKey,str(len(music)+1))
    reset(funnelFile,'')

def genGelData():
    result = {
        'blue':'',
        'orange':''
    }
    if len(blueGelBox.get(0,tk.END)) == 1:
        result['blue'] = blueGelBox.get(0,tk.END)[0]
    else:
        result['blue'] = tuple(blueGelBox.get(0,tk.END))
    
    if len(orangeGelBox.get(0,tk.END)) == 1:
        result['orange'] = orangeGelBox.get(0,tk.END)[0]
    else:
        result['orange'] = tuple(orangeGelBox.get(0,tk.END))

    return result
        
def addToList():
    if tID.get().strip()!='':
        if checklists()==True:
            if len(tLen.get().split(':'))==2 or loopvar.get():
                duplicate = False
                if len(music)!=0:
                    for i in music:
                        if i.id==tID.get():
                            duplicate = True
                            break
                if not duplicate:
                    if tID.get()!='Package':
                        try:
                            int(sortKey.get())
                        except:
                            msg.showerror('Not a number','Sort key must be a number! No operations have been performed.')
                        finally:
                            if tID.get().upper() == tID.get():
                                msg.showwarning('ID not uppercase','The ID of this track is not all-uppercase. This means it doesn\'t follow the style of the official packages. The track will still be added.')
                            if ('_' in tID.get() or '-'  in tID.get()) and not kb.is_pressed('shift'):
                                msg.showwarning('Underscore or hyphen in ID','The ID field has a hyphen or underscore. This means that you may have tried to add a prefix via the ID field. A prefix can be defined in the prefix field. The track will still be added.\nHold SHIFT when adding a song to dismiss this warning.')
                            music.append(Track(tID.get(),shortName.get(),title.get(),desc.get(),authors.get(),-1 if loopvar.get() else tLen.get(),photo.get(),prev.get(),trac.get(),samp.get(),group.get(),sortKey.get(),style=styles[tuple(styles.keys())[styleNames.index(stylevar.get())]], noLarge=skipImg.get(),gels=genGelData(),funnel=funnelData(funnelFile.get(),syncFunnel.get()) if enableFunnel.get() else None))
                            tracklist.insert(tk.END,tID.get())
                                             
                            resetFields()
                    else:
                        msg.showerror("Invalid ID','The ID you entered is invalid! Please do not name your song IDs 'Package', as this will break the saving/loading functions.")
                else:
                    msg.showerror('Duplicate IDs','The entered ID is a duplicate! Please change the ID and try again.')
            else:
                msg.showerror('Misformatted length field','The length field is misformatted! It must be formatted as mm:ss or m:ss.')
        else:
            msg.showerror('Empty field','The '+checklists()+' field is empty! Please enter something and try again.')
    else:
        msg.showerror('ID field is empty','The ID field is empty! Please fill this field in and try again.')

def reset(field,value):
    field.delete(0,tk.END)
    field.insert(tk.END,value)

def opn():
    if len(tracklist.curselection())!=0:
        cur = tracklist.curselection()[0]

        tID.delete(0,tk.END)
        tID.insert(tk.END,music[cur].id)

        if music[cur].length==-1:
            loopvar.set(True)
            tLen.config(state='disabled')
        else:
            loopvar.set(False)
            tLen.config(state='normal')
            tLen.delete(0,tk.END)
            tLen.insert(tk.END,music[cur].length)

        group.delete(0,tk.END)
        group.insert(tk.END,music[cur].group)

        sortKey.delete(0,tk.END)
        sortKey.insert(tk.END,music[cur].key)

        reset(shortName,music[cur].short_title)

        stylevar.set((music[cur].style.ui_name) if music[cur].style.ui_name!='' else music[cur].style.name)

        tr = music[cur]

        skipImg.set(tr.noLarge)

        reset(authors,music[cur].authors)
        reset(desc,tr.desc)
        reset(title,tr.title)

        reset(samp,tr.sample)
        reset(trac,tr.music)
        reset(prev,tr.preview)
        reset(photo,tr.image)

        if tr.funnel!=None:
            reset(funnelFile,tr.funnel.file)
            enableFunnel.set(funnel.used)
        else:
            enableFunnel.set(False)
        funnelChange()

actions = tk.LabelFrame(main,text='Actions',labelanchor='n',background=dark,foreground=light)
actions.grid(row=1,column=0,padx=5,pady=5)

add = tk.Button(actions,text='Add',command=addToList,background=darkField,foreground=light,relief='flat',activebackground=darkField,activeforeground=light)
add.grid(row=0,column=0,padx=10,pady=10,ipadx=25)

load = tk.Button(actions,text='Load selected',command=opn,background=darkField,foreground=light,relief='flat',activebackground=darkField,activeforeground=light)
load.grid(row=1,column=0,padx=10,pady=10,)

tracks = tk.LabelFrame(main,text='Your tracks',labelanchor='n',background=dark,foreground=light)
tracks.grid(row=0,column=2,padx=5,pady=5,rowspan=2,ipady=100)

scrollbar=ttk.Scrollbar(tracks)
scrollbar.pack(side='right',fill='y')

tracklist = tk.Listbox(tracks,yscrollcommand=scrollbar.set,relief='flat',background=darkField,foreground=light)
tracklist.pack(side='left',fill='both')

scrollbar.config(command = tracklist.yview)

def delList():
    if len(tracklist.curselection())==0:
        msg.showerror('No selection','Nothing is selected! Please select something and try again.')
    else:
        ask = msg.askyesno('Are you sure?','Are you sure you want to delete this track?')
        if ask == True:
            music.pop(tracklist.curselection()[0])
            tracklist.delete(tracklist.curselection()[0],tracklist.curselection()[0])

def ind(i):
    return '\t'*i

def BProperty(name,value):
    print('Property "'+name+'" generated with value "'+value+'"')
    return '"'+name+'" "'+value+'"\n'

def generate():
    if packdesc.get().strip()=='':
        msg.showerror('No package description','The package description field is empty! A package cannot be generated.')
    elif packid.get().strip()=='':
        msg.showerror('No package ID','The package ID field is empty! A package cannot be generated.')
    elif packtitle.get().strip()=='':
        msg.showerror('No package name','The package name field is empty! A package cannot be generated.')
    elif len(music)==0:
        msg.showerror('No music in list','There is no music in the package! A package cannot be generated.')
    else:
        if prefix.get().strip()=='':
            msg.showwarning('No prefix','The prefix field is empty! This means the ID could conflict with other UCPs. The compiler has not been interrupted.')

        zipfile = fs.asksaveasfilename(initialfile=str.lower(packid.get())+'.bee_pack',confirmoverwrite=True,filetypes=[('BEE2.4 package file','.bee_pack')],title='Compile package',initialdir=(None if beepath=='' else beepath))
        if zipfile!='':

            global customstyles,stylepacks
            customstyles = ''
            stylepacks = {
                'twtm':'Catperson6\'s TWTM style\n',
                'bts': 'BTS style package or old BEE2\n',
                'grass_clean':'joethegamer\'s Grass Clean style\n',
                'hybrid':'Axo\'s Hybrid style\n',
                'cave' or 'rocky' or 'dev' or 'gray' or 'gmod' or 'floor':'Drgregs Dumb Styles\n'
            }

            if not kb.is_pressed('shift'):
                for i in music:
                    if not i.style.vanilla and ('Drgregs Dumb Styles' if 'Drgregs' in i.style.authors else 'Catperson6\'s TWTM style') not in customstyles:
                        customstyles += i.style.ui_name if i.style.ui_name != '' else i.style.name
                if customstyles!='':
                    msg.showwarning('UCP styles',f'Your package uses custom styles. You will need the following packages for your package to work:\n{customstyles}\nYou can hold SHIFT when clicking Compile to skip this dialog box.')

            os.makedirs(os.getcwd()+'/temp',exist_ok=True)

            print(customstyles)

            with open(os.getcwd()+'/temp/info.txt','w') as inf:

                indent = 0

                inf.write('// Generated by beeMMX R')
                inf.write('// the BEE2 music package generator')

                inf.write('"ID" "'+packid.get()+'"\n')
                inf.write('"Name" "'+packtitle.get()+'"\n')
                inf.write('"Desc" "'+packdesc.get()+'"\n\n')

                global allNone, noneStyled
                noneStyled=0

                for i in music:
                    if i.style=='none':
                        noneStyled+=1

                if noneStyled==len(music):
                    allNone=True
                else:
                    allNone=False

                if not allNone:
                    inf.write('\n"Overrides"\n')
                    indent+=1
                    inf.write('\t'*indent+'{\n')


                for g in styles:

                    if g!='none':

                        matched = []
                        for i in music:
                            if i.style==styles[g]:
                                matched.append(i.id)

                        if len(matched)>0:

                            indent+=1
                            print(indent)

                            inf.write('\t'*indent+'"Style"\n'+ind(indent)+'{\n')
                            indent+=1

                            inf.write('\t'*indent+'"ID" "'+styles[g].id+'"\n')
                            inf.write('\t'*indent+'"Authors" "'+styles[g].authors+'"\n')
                            inf.write('\t'*indent+'"Name" "'+styles[g].name+'"\n')

                            inf.write('\t'*indent+'"Suggested"\n')

                            inf.write(ind(indent)+'{\n')
                            indent+=1

                            for i in matched:
                                inf.write('\t'*indent+'"Music" "'+prefix.get().replace('"','\\"')+'_'+i+'"\n')

                            for i in range(2):
                                indent-=1
                                inf.write(ind(indent)+'}\n')
                            indent-=1
                            inf.write(ind(indent)+'}\n\n')
                            indent-=1

                            indent+=1
                        
                for i in music:
                    print(indent)
                    inf.write('"Music"\n')
                    inf.write('{\n')
                    inf.write(ind(indent)+'"ID" "'+prefix.get().replace('"','\\"')+'_'+i.id+'"\n')
                    inf.write(ind(indent)+'"Name" "'+i.title.replace('"','\\"')+'"\n')
                    inf.write(ind(indent)+BProperty('ShortName',i.short_title.replace('"','\\"')))
                    inf.write(ind(indent)+BProperty('Group',i.group.replace('"','\\"')))
                    if i.noLarge!=False:
                        inf.write(ind(indent)+BProperty('Icon','small/'+os.path.basename(i.preview)))
                    inf.write(ind(indent)+BProperty('IconLarge','large/'+os.path.basename(i.image)))
                    inf.write(ind(indent)+BProperty('Authors',i.authors.replace('"','\\"')))
                    inf.write(ind(indent)+BProperty('Sort_key',i.key))
                    inf.write(ind(indent)+BProperty('Description',i.desc.replace('"','\\"')))
                    if i.length!=-1:
                        inf.write(ind(indent)+BProperty('Loop_len',i.length))
                    inf.write(ind(indent)+'"Sample"\n'+ind(indent)+'{\n')
                    indent+=1
                    inf.write(ind(indent)+BProperty('Base',os.path.basename(i.sample)))
                    indent-=1
                    inf.write(ind(indent)+'}\n')
                    inf.write(ind(indent)+'"Soundscript"\n'+ind(indent)+'{\n')
                    indent+=1
                    inf.write(ind(indent)+BProperty('Base',os.path.basename(i.music)))
                    indent-=1
                    inf.write(ind(indent)+'}\n')
                    indent-=1
                    inf.write(ind(indent)+'}\n\n')
                    print(indent)
                    indent=1
                inf.close()
            os.makedirs(os.getcwd()+'/temp/resources/BEE2/large',exist_ok=True)
            os.makedirs(os.getcwd()+'/temp/resources/BEE2/small',exist_ok=True)
            os.makedirs(os.getcwd()+'/temp/resources/music_samp',exist_ok=True)
            os.makedirs(os.getcwd()+'/temp/resources/sound',exist_ok=True)
            for i in music:
            
                shutil.copy2(i.music,os.getcwd()+'/temp/resources/sound')
                shutil.copy2(i.sample,os.getcwd()+'/temp/resources/music_samp')
                shutil.copy2(i.image,os.getcwd()+'/temp/resources/BEE2/large')
                shutil.copy2(i.preview,os.getcwd()+'/temp/resources/BEE2/small')

            if os.path.exists(zipfile):
                os.remove(zipfile)

            shutil.make_archive(os.path.splitext(zipfile)[0],'zip',os.getcwd()+'/temp/')
            os.rename(os.path.splitext(zipfile)[0]+'.zip',os.path.splitext(zipfile)[0]+'.bee_pack')
            shutil.rmtree(os.getcwd()+'/temp/')

        del(allNone,noneStyled)

prevFile = tk.StringVar(win,'')

def save(asFile:bool = False):

    if len(music)!=0:
        
        if prevFile.get() != '' or asFile:
            file = fs.asksaveasfilename(defaultextension='.bxs',filetypes=[('beeMMX R save file','.bxs .beemmx .bxsave')],initialfile=packid.get()+'.bxs',title='Save beeMMX R project file')
        else:
            file = prevFile.get()


        if file!=None:

            setPresence(file)

            prevFile.set(file)
            
            fileMenu.activate(5)

            savedata = {
                'Package':{
                    'ID':packid.get().replace('"','\\"'),
                    'Name':packtitle.get().replace('"','\\"'),
                    'Desc':packdesc.get().replace('"','\\"'),
                    'Prefix':prefix.get().replace('"','\\"')
                }
            }

            for i in music:
                savedata.update({i.id:{
                    'Name':i.title.replace('"','\\"'),
                    'ShortName':i.short_title.replace('"','\\"'),
                    'Desc':i.desc.replace('"','\\"'),
                    'Image':i.image,
                    'Preview':i.preview,
                    'Sample':i.sample,
                    'Music':i.music,
                    'Authors':i.authors.replace('"','\\"'),
                    'Group':i.group.replace('"','\\"'),
                    'Key':i.key,
                    'Loop_length':i.length,
                    'NoLoop':i.length==-1,
                    'NoSmall':i.preview==-1,
                    'Style':tuple(styles.keys())[styleNames.index(stylevar.get())],
                    'Funnel':i.funnel,
                    'Gels':i.gels
                }})

            #json.dump(savedata,file,indent=4)

            with open(file,'w') as fileIO:
                dumpSaveData(savedata,fileIO)

    else:
        msg.showerror('No music','There is no music in the package! The save operation has been cancelled.')    

def dumpSaveData(savedata:dict,file):
    parser = cfg.ConfigParser()

    for section in savedata.keys():
        parser.add_section(enc(section))

        fields = savedata[section].keys()
        for field in fields:
            val = savedata[section][field]
            parser.set(enc(section), enc(field), enc(str(val)))

    parser.write(file); file.close()

def enc(obj:str) -> str:
    '''
    Escape all unescaped Unicode characters in the string.
    '''
    return obj.encode('unicode-escape').decode()

def isLegacy(data: list[str]=['']):
    isLegacyFile = True
    for i in data:
        if '"Funnel"' in i or '"Gel"' in i:
            isLegacyFile = False
            break
    return isLegacyFile

def loadFile(fileIn=None):
    
    if fileIn==None:
        file = fs.askopenfile(defaultextension='.bxs',filetypes=[('beeMMX R save file','.bxs .beemmx .bxsave')],title='Load beeMMX R project file')
    else:
        file=fileIn

    if file != None:
        if fileIn==None:
            ask = msg.askyesno('Please confirm','Are you sure you want to overwrite all data for values from this project?')
        else:
            ask = True

        if ask:

            prevFile.set(file.name)

            fileMenu.activate(5)

            setPresence(file.name)
            
            legacy = isLegacy(file.readlines())

            if legacy:
                print('Legacy file detected! Skipping funnel and gel music...')

            savedata = json.load(file)
            trackDicts = tuple(savedata.keys())[1:]

            reset(packid,savedata['Package']['ID'])
            reset(packtitle,savedata['Package']['Name'])
            reset(packdesc,savedata['Package']['Desc'])
            reset(prefix,savedata['Package']['Prefix'])

            music.clear()
            tracklist.delete(0,tk.END)
            
            for i in trackDicts:
                tr = savedata[i]
                music.append(Track(i,tr['ShortName'].replace('\\"','"'),tr['Name'].replace('\\"','"'),tr['Desc'].replace('\\"','"'),tr['Authors'].replace('\\"','"'),tr['Loop_length'],tr['Image'],tr['Preview'],tr['Music'],tr['Sample'],tr['Group'].replace('\\"','"'),tr['Key'],styles[tr['Style']],tr['NoSmall'],gelData(check(tr,'Gels')),funnelData(check(tr,'Funnel'))))
                tracklist.insert(tk.END,i)

def discord():
    web.open('https://discord.gg/CGAvCwdJHM')

def check(container: tuple | list | dict, index):
    try:
        return container[index]
    except IndexError:
        return None

def askpath():
    pth = fs.askdirectory(mustexist=True,title='Select BEE2 packages folder')
    if pth!='':
        if os.path.basename(pth)=='packages':
            beepath.set(pth)
            with open(os.getcwd()+'/bee2_path.txt',mode='w') as path:
                path.write(beepath.get())
                path.close()
        else:
            msg.showerror('Not a packages folder','This is not a packages folder! Please specify another folder.')

def save_as():
    save(True)

def save_key():
    if prevFile.get() != '':
        save()

kb.add_hotkey('ctrl+shift+s',save_as)
kb.add_hotkey('ctrl+s',save_key)

def new():
    if msg.askyesno('Start a new project?','Are you sure you want to start a new project? You will lose any unsaved changes to the previous file.') == tk.YES:
        prevFile.set(''); fileMenu.entryconfig('New',state=tk.DISABLED); resetFields()
        setPresence(None)

menu = tk.Menu(win,foreground=light,background=darkField,relief='flat')
fileMenu = tk.Menu(menu,tearoff=False,foreground=light,background=darkField,relief='flat')
fileMenu.add_command(label='New',command = new)
fileMenu.add_command(label='Compile',command=generate,accelerator='Ctrl + G')
kb.add_hotkey('ctrl+g',generate)
fileMenu.add_command(label='Add song', command=addToList)
fileMenu.add_command(label='Set up BEE2 packages folder',command=askpath)
fileMenu.add_separator()
fileMenu.add_command(label='Save as...',command=save_as, accelerator = 'Ctrl + Shift + S')
fileMenu.add_command(label='Save',command=save,accelerator='Ctrl + S',state=tk.DISABLED)
fileMenu.add_command(label='Load',command=loadFile)
fileMenu.add_separator()

def clear():
    print('Deleting log files...')
    files = os.listdir(os.path.join(os.getcwd(),'logs'))
    for i in range(len(files)):
        os.remove(os.path.join(os.getcwd(),'logs',files[i]))
        print('File {}/{} deleted!'.format(i,len(files)))

fileMenu.add_command(label='Clear log folder',command=clear)
fileMenu.add_separator()

fileMenu.add_checkbutton(label='Dark theme',variable=darkmode,command=reloadTheme,selectcolor='#FFFFFF')

fileMenu.add_separator()

fileMenu.add_command(label='Quit',command=sys.exit)
menu.add_cascade(label='File',menu=fileMenu)

openMenu = tk.Menu(menu,tearoff=False,relief='flat',foreground=light,background=darkField)
openMenu.add_command(command=openDir,label='App directory')
openMenu.add_command(command=discord,label='Discord server')
menu.add_cascade(menu=openMenu,label='Open')

def changeSkip():
    prev.config(state=('disabled' if skipImg.get() else 'normal'))

skipImg = tk.BooleanVar(main,False)
largeImageSkip = tk.Checkbutton(trackdata,text="Use Image only",variable=skipImg,command=changeSkip,background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField)
largeImageSkip.grid(row=0,column=3,padx=5,pady=5)

win.config(menu=menu,relief='flat',background=dark)

delBtn = tk.Button(actions,text='Delete selected',command=delList,relief='flat',background=darkField,foreground=light,activebackground=darkField,activeforeground=light)
delBtn.grid(row=0,column=1,padx=5,pady=5)

compileBtn = tk.Button(actions,text='Compile',command=generate,relief='flat',background=darkField,foreground=light,activebackground=darkField,activeforeground=light)
compileBtn.grid(row=1,column=1,padx=5,pady=5,ipadx=16)

if len(sys.argv)==2:
    with open(sys.argv[1]) as svf:
        loadFile(svf)

extra = tk.Frame(tabs,padx=5,pady=5)

funnel = tk.LabelFrame(extra,text='Excursion funnel',labelanchor=tk.N)
funnel.grid(row=0,column=0,padx=5,pady=5)

def selFunnel():
    file = fs.askopenfilename(defaultextension='wav',filetypes=[('Microsoft wave file','.wav .wave')],title='Open funnel music')
    if file!=None:
        if testWaveFile(file):
            reset(funnelFile,file)

funnelFile = labelField(funnel,0,0,'Funnel music',True)

funnelButton = tk.Button(funnel,image=file_ico,relief=tk.FLAT,command=selFunnel,foreground=darkField,state='disabled',disabledforeground=inactive)
funnelButton.grid(row=1,column=1,padx=5,pady=5)

def funnelChange():
    syncCheckbox.config(state='normal' if enableFunnel.get() else 'disabled')
    funnelButton.config(state='normal' if enableFunnel.get() else 'disabled')
    funnelFile.config(state='normal' if enableFunnel.get() else 'disabled')

syncFunnel = tk.BooleanVar(main,False)
enableFunnel = tk.BooleanVar(main,False)
funnelCheckbox = tk.Checkbutton(funnel,text='Enable funnel music',variable=enableFunnel,background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField,command=funnelChange)
syncCheckbox = tk.Checkbutton(funnel,text='Sync funnel music',variable=syncFunnel,background=dark,foreground=light,activebackground=dark,activeforeground=light,selectcolor=darkField,state='disabled')

funnelCheckbox.grid(row=2,column=0,padx=5,pady=1,columnspan=2)
syncCheckbox.grid(row=3,column=0,padx=5,pady=1,columnspan=2)

gels = tk.LabelFrame(extra,text='Gels',labelanchor='n')
gels.grid(padx=5,pady=5,column=1,row=0)

bluegelframe = tk.LabelFrame(gels,labelanchor=tk.N,text='Repulsion gel',padx=5,pady=5)
bluegelframe.grid(row=0,column=0,padx=5,pady=5,columnspan=2,rowspan=5)

bluegelscroll = tk.Scrollbar(bluegelframe,orient=tk.VERTICAL)
bluegelscroll.pack(side=tk.RIGHT,expand=True,fill=tk.Y)

bluegelxscroll = tk.Scrollbar(bluegelframe,orient=tk.HORIZONTAL)
bluegelxscroll.pack(side=tk.BOTTOM,expand=True,fill=tk.X)

blueGelBox = tk.Listbox(bluegelframe,selectmode=tk.SINGLE,yscrollcommand=bluegelscroll.set,xscrollcommand=bluegelxscroll.set)
blueGelBox.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

bluegelscroll.config(command=blueGelBox.yview)
bluegelxscroll.config(command=blueGelBox.xview)

def addBlueGel():
    formats = {
        'float32':'32-bit floating-point',
        'int32':'32-bit or 24-bit integer PCM',
        'uint8':'8-bit integer PCM',
        'int16':'16-bit integer PCM'
    }
    global sampleformat
    if bluefile.get().strip() != '':
        if os.path.exists(bluefile.get()):
            sampleformat = formats[str(wave.read(bluefile.get())[1].dtype)]
            if wave.read(bluefile.get())[0] == 44100:
                if wave.read(bluefile.get())[1].dtype == 'int16':
                    blueGelBox.insert(tk.END,bluefile.get())
                    reset(bluefile,'')
                else:
                    msg.showerror('Invalid sample format',"Invalid sample format in specified file! Read {sampleformat} instead of 16-bit integer PCM. This file will crash Portal 2 and therefore was not imported.")
            else:
                msg.showerror('Invalid sample rate',"The specified file's sample rate is not 44100 hertz! This file will crash Portal 2's sound engine and therefore was not imported.")
        else:
            msg.showerror('Invalid filename','The entered filename does not exist! Please specify a valid file and try again.')
    else:
        msg.showerror('Empty filename','No filename specified in the field! Please enter a filename and try again.')
    del(formats)

def addOrangeGel():
    formats = {
        'float32':'32-bit floating-point',
        'int32':'32-bit or 24-bit integer PCM',
        'uint8':'8-bit integer PCM',
        'int16':'16-bit integer PCM'
    }
    global sampleformat
    if bluefile.get().strip() != '':
        if os.path.exists(bluefile.get()):
            sampleformat = formats[str(wave.read(bluefile.get())[1].dtype)]
            if wave.read(bluefile.get())[0] == 44100:
                if wave.read(bluefile.get())[1].dtype == 'int16':
                    orangeGelBox.insert(tk.END,bluefile.get())
                    reset(bluefile,'')
                else:
                    msg.showerror('Invalid sample format',"Invalid sample format in specified file! Read {sampleformat} instead of 16-bit integer PCM. This file will crash Portal 2 and therefore was not imported.")
            else:
                msg.showerror('Invalid sample rate',"The specified file's sample rate is not 44100 hertz! This file will crash Portal 2's sound engine and therefore was not imported.")
        else:
            msg.showerror('Invalid filename','The entered filename does not exist! Please specify a valid file and try again.')
    else:
        msg.showerror('Empty filename','No filename specified in the field! Please enter a filename and try again.')
    del(sampleformat)
    del(formats)


def selectGel():
    file = fs.askopenfilename(title='Add repulsion gel music',filetypes=[('Microsoft WAVE file','.wav .wave')])
    if file!=None:
        reset(bluefile,file)

bluefile = labelField(gels,0,5,'Filename')
tk.Button(gels,image=file_ico,relief=tk.FLAT,command=selectGel).grid(row=6,column=1,padx=5,pady=5)

tabs.add(main,text='Data')
tabs.add(extra,text='Extras')
tabs.pack(side=tk.TOP)

addIcons = {
    'blue': Image('media/blue.png'),
    'orange': Image('media/orange.png'),
    'remove': Image('media/remove.png'),
    'help': Image('media/help.png')
}

orangeFrame = tk.LabelFrame(gels,labelanchor=tk.N,text='Propulsion gel')

orangescroll = tk.Scrollbar(orangeFrame,orient=tk.VERTICAL)
orangescroll.pack(expand=True,fill=tk.Y,side=tk.RIGHT)

orangexscroll = tk.Scrollbar(orangeFrame,orient=tk.HORIZONTAL)
orangexscroll.pack(expand=True,fill=tk.X,side=tk.BOTTOM)

orangeGelBox = tk.Listbox(orangeFrame,selectmode=tk.SINGLE,yscrollcommand=orangescroll.set,xscrollcommand=orangexscroll.set)
orangeGelBox.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

orangescroll.config(command=orangeGelBox.yview)
orangexscroll.config(command=orangeGelBox.xview)

orangeFrame.grid(row=0,column=4,padx=5,pady=5)

def removeGelection():
    if len(orangeGelBox.curselection())>0:
        orangeGelBox.remove(orangeGelBox.curselection()[0])
    elif len(blueGelBox.curselection())>0:
        blueGelBox.remove(blueGelBox.curselection()[0])
    else:
        msg.showerror('No selection','There is no selection in either the repulsion or propulsion gel box. Please select something and try again.')

def gelHelp():
    web.open('https://github.com')

tk.Button(gels,image=addIcons['blue'],relief=tk.FLAT,command=addBlueGel).grid(row=6,column=2,padx=5,pady=5)
tk.Button(gels,image=addIcons['orange'],relief=tk.FLAT,command=addOrangeGel).grid(row=5,column=2,padx=5,pady=5)
tk.Button(gels,image=addIcons['remove'],relief=tk.FLAT,command=removeGelection).grid(row=5,column=1,padx=5,pady=5)
tk.Button(gels,image=addIcons['help'],relief=tk.FLAT,command=gelHelp).grid(row=6,column=3,padx=5,pady=5)

win.focus_set()

tips = {
    'key':tip.ToolTip(sortKey,'Position of this track in the Group.'),
    'group':tip.ToolTip(group,'Which part of the music picker window this song will be under. Will be created if it doesn\'t exist.'),
    'style':tip.ToolTip(style, 'If the current pallete\'s style is set to this value, suggest this track. If None, don\'t generate suggestions for this track.'),
    'packid':tip.ToolTip(packid,'The internal ID of the package, used by BEE2. Usually written as "PREFIX_NAME", where PREFIX is usually the author\'s name and NAME is a shortened name of the package, for example "VALVE_STILLALIVE_REMIXES" is a good ID for a package which adds several remixes of Still Alive, originally made by Valve.'),
    'trackfile':tip.ToolTip(trac,'Filename of the full track. Must be a 44100 hertz, 16-bit PCM WAV file.'),
    'sample':tip.ToolTip(samp,'The filename of a 10-second long OGG or WAV file (limitations of full files don\'t apply) to be used when clicking the play button.'),
    'preview':tip.ToolTip(prev,'The filename of a square PNG image used as the small icon when browsing for tracks. Usually a part of the full image.'),
    'packdesc':tip.ToolTip(packdesc,'The description of the package in BEE2\'s package manager.'),
    'prefix':tip.ToolTip(prefix,'The prefix for all track IDs. Used to prevent ID conflicts with official or other packages. Applied as "PREFIX_ID".'),
    'packname':tip.ToolTip(packtitle,'The name of this package in BEE2\'s package manager.'),
    'image':tip.ToolTip(photo,'A PNG 4:3 image displayed on the right of the music picker window after a track has been selected. Usually 256x192 pixels large.'),
    'tracklist':tip.ToolTip(tracklist,'See a readout of your tracks by their IDs here.'),
    'id':tip.ToolTip(tID,'BEE2\'s internal ID for this song.'),
    'title':tip.ToolTip(title,'The GUI name of this track.'),
    'imgskip':tip.ToolTip(largeImageSkip,'Don\'t use a small image for this track. BEE2 will automatically cut the image to turn the large image into a small one.'),
    'noloop':tip.ToolTip(dontLoop,'Disable looping this track by removing the \'Loop_len\' property from the info.txt file.'),
    'shortname':tip.ToolTip(shortName,'If the tracks\' name is longer than 20 characters, enter a shortened version of the regular name. Otherwise, enter the normal name. E.g. ""Welcome To The Future" -> "Welcome Future".'),
    'authors':tip.ToolTip(authors,'The author(-s) of this track. BEE2 will automatically change \'Author\' to \'Authors\' if it finds a comma.'),
    'desc':tip.ToolTip(desc,'GUI description of this track. The description usually includes information such as where this track plays.'),
    'len':tip.ToolTip(tLen,'The track\'s length, formatted as \'MM:SS\' or \'M:SS\' if the minute count is only one digit. Used for looping. Automatically determined when a song file is selected.'),
    'del':tip.ToolTip(delBtn,'Delete the currently selected track from the track list.'),
    'add':tip.ToolTip(add,'Generate a track object with the current parameters and add it to the track list.'),
    'loadbtn':tip.ToolTip(load,'Replace all current values with ones from the current selection in the track list.'),
    'compile':tip.ToolTip(compileBtn,'Generate a BEE2 package from this project.')
}

def refreshTips():
    print('Refreshing tooltips...')
    for i in tips:
        tip = tips[i]
        tip.__init__(tip.widget,tip.msg,tip.delay,tip.follow,tip.refresh,tip.x_offset,tip.y_offset,{},bg=darkTip,fg=light)
        print('[Refresh tooltips] tooltip ',tuple(tips.keys()).index(i)+1,'/',len(tips),' refreshed!',sep='')
    print('Tooltips refreshed!')

reloadTheme()

tk.mainloop()

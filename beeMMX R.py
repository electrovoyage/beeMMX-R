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

def openDir():
    web.open('file:///'+os.getcwd())

def Image(name):
    return it.PhotoImage(img.open(os.getcwd()+'/'+name))

music = []

class Track:
    def __init__(self,ID,short_title,title,description,authors,length,image,preview,music,sample,group,key,style,noLarge):
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

class Style:
    def __init__(self,name,id,authors,ui_name):
        self.name = name
        self.id = id
        self.authors = authors
        self.ui_name = ui_name

styles = {
    'bts':Style('Behind The Scenes','BEE2_BTS','TeamSpen210',''),
    'over':Style('Overgrown','BEE2_OVERGROWN','TeamSpen210',''),
    'clean':Style('Clean','BEE2_CLEAN','Valve, Carl Kenner, TeamSpen210',''),
    'original_clean':Style('Clean (Original Textures)','BEE2_CLEAN_ORIGINAL','Valve','Original Clean'),
    'grass_clean':Style('Grass Clean','BEE2_GRASS_CLEAN','joethegamer',"joethegamer's Grass Clean"),
    'hybrid':Style('Hybrid','AXO_HYBRID','Valve, Axo',"Axo's Hybrid"),
    'p1':Style('Portal 1 Style','BEE2_PORTAL_1','Carl Kenner, TeamSpen210, Valve','Portal 1'),
    'cave':Style('Deep Cave','DDS_CAVE_STYLE','Drgregs',"Drgregs' Deep Cave"),
    'rocky':Style('Rocky Cave','SUBSTYLE_CAVE_STYLE','Drgregs',"Drgregs' Rocky Cave"),
    'dev':Style('Developer Style','DDS_DEV_STYLE','Drgregs',"Drgregs' Developer"),
    'gray':Style('Solid Gray Dev','SUBSTYLE_DEV_STYLE','Drgregs',"Drgregs' Solid Gray Developer"),
    'gmod':Style("Garry's Mod Style",'DDS_GMOD_STYLE','Facepunch, Drgregs',"Drgregs' GMod"),
    'floor':Style('Unpolished Floor','SUBSTYLE_GMOD_STYLE','Facepunch, Drgregs',"Drgregs' Unpolished Floor"),
    '50s':Style('1950s Old Aperture','BEE2_1950s','Carl Kenner, TeamSpen210, Critfish','1950s'),
    '60s':Style('1960s Old Aperture','BEE2_1960s','Carl Kenner, TeamSpen210, Critfish','1960s'),
    '70s':Style('1970s Old Aperture','BEE2_1970s','Carl Kenner, TeamSpen210','1970s'),
    '80s':Style('1980s Old Aperture','BEE2_1980s','Carl Kenner, TeamSpen210','1980s'),
    'none':Style('','','','None')
}

styleNames = []
for i in styles:
    if styles[i].ui_name == '':
        styleNames.append(styles[i].name)
    else:
        styleNames.append(styles[i].ui_name)

def label(win,column,row,text):
    tk.Label(win,text=text).grid(column=column,row=row,padx=5)

def field(win,column,row):
    fld = tk.Entry(win)
    fld.grid(column=column,row=row,padx=5,pady=5)
    return fld

def labelField(win,col,row,text):
    tk.Label(win,text=text).grid(column=col,row=row,padx=5)
    fld = field(win,col,row+1)
    return fld

main = tk.Tk()
main.iconbitmap(os.getcwd()+'/media/icon.ico')
main.resizable(False,False)
main.title('beeMMX R')

packdata = tk.LabelFrame(main,text='Package information',labelanchor='n')
packdata.grid(row=0,column=0,padx=5,pady=5)

tk.Label(packdata,text='Package name').grid(row=0,column=0,padx=5)
tk.Label(packdata,text='Package description').grid(row=0,column=1,padx=5)
tk.Label(packdata,text='Package ID').grid(row=2,column=0,padx=5)
tk.Label(packdata,text='Track ID prefix').grid(row=2,column=1,padx=5)

packtitle = tk.Entry(packdata)
packtitle.grid(row=1,column=0,padx=5,pady=5)
packdesc = tk.Entry(packdata)
packdesc.grid(row=1,column=1,padx=5,pady=5)
packid = tk.Entry(packdata)
packid.grid(row=3,column=0,padx=5,pady=5)
prefix = tk.Entry(packdata)
prefix.grid(row=3,column=1,padx=5,pady=5)

trackdata = tk.LabelFrame(main,text='Track information',labelanchor='n')
trackdata.grid(row=0,column=1,padx=5,pady=5)

desc = tk.Entry(trackdata)
desc.grid(row=1,column=0,padx=5,pady=5)
tk.Label(trackdata,text='Description').grid(row=0,column=0,padx=5)

title = tk.Entry(trackdata)
title.grid(row=1,column=1,pady=5,padx=5)
label(trackdata,1,0,'Name')

shortName = tk.Entry(trackdata)
shortName.grid(row=1,column=2,padx=5,pady=5)
label(trackdata,2,0,'Short name')

loopvar = tk.BooleanVar(main,False)

def setLoop():
    tLen.config(state=('disabled' if loopvar.get() else 'normal'))

dontLoop = tk.Checkbutton(trackdata,text="Don't loop",variable = loopvar,command=setLoop)
dontLoop.grid(row=1,column=3,padx=5,pady=5)

authors = field(trackdata,0,3)
label(trackdata,0,2,'Author(-s)')

tLen = labelField(trackdata,1,2,'Length')
tID = labelField(trackdata,2,2,'ID')
group = labelField(trackdata,3,2,'Group')

sortKey = tk.Spinbox(trackdata,from_=1,to=4294967296)
tk.Label(trackdata,text='Sort key').grid(row=4,column=0,padx=5,columnspan=2)
sortKey.grid(row=5,column=0,padx=5,pady=5,columnspan=2)

stylevar = tk.StringVar(main,'Clean')

tk.Label(trackdata,text='Suggested style').grid(row=4,column=2,columnspan=2,padx=5,pady=5)
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

trackmedia = tk.LabelFrame(main,text='Track media',labelanchor='n')
trackmedia.grid(row=1,column=1,padx=5,pady=5)

prev = labelField(trackmedia,0,0,'Preview (1:1)')
photo  = labelField(trackmedia,2,0,'Image (4:3)')
samp = labelField(trackmedia,4,0,'Sample (10 secs)')
trac = labelField(trackmedia,6,0,'Track')

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

def track():
    file = fs.askopenfile(defaultextension='.wav',initialfile='music.wav',title='Specify track file',filetypes=[('Microsoft WAVE music','.wav .wave')])
    if file is not None:
        trac.delete(0,tk.END)
        trac.insert(tk.END,file.name)
        tLen.delete(0,tk.END)
        tLen.insert(tk.END,str(int(mg.File(file.name).info.length//60))+':'+str(int(mg.File(file.name).info.length%60)))

tk.Button(trackmedia,image=file_ico,command=preview).grid(row=1,column=1,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=phot).grid(row=1,column=3,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=sample).grid(row=1,column=5,padx=5,pady=5)
tk.Button(trackmedia,image=file_ico,command=track).grid(row=1,column=7,padx=5,pady=5)

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
                        music.append(Track(tID.get(),shortName.get(),title.get(),desc.get(),authors.get(),-1 if loopvar.get() else (tLen.get()),photo.get(),prev.get(),trac.get(),samp.get(),group.get(),sortKey.get(),style=styles[tuple(styles.keys())[styleNames.index(stylevar.get())]], noLarge=skipImg.get()))
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

actions = tk.LabelFrame(main,text='Actions',labelanchor='n')
actions.grid(row=1,column=0,padx=5,pady=5)

add = tk.Button(actions,text='Add',command=addToList)
add.grid(row=0,column=0,padx=10,pady=10)

load = tk.Button(actions,text='Load selected',command=opn)
load.grid(row=1,column=0,padx=10,pady=10)

tracks = tk.LabelFrame(main,text='Your tracks',labelanchor='n')
tracks.grid(row=0,column=2,padx=5,pady=5,rowspan=2,ipady=100)

scrollbar=tk.Scrollbar(tracks)
scrollbar.pack(side='right',fill='y')

tracklist = tk.Listbox(tracks,yscrollcommand=scrollbar.set)
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
            msg.showwarning('No prefix','The prefix field is empty! This means the ID could conflict with other UCPs! The compiler has not been interrupted.')

        zipfile = fs.asksaveasfilename(initialfile=str.lower(packid.get())+'.bee_pack',confirmoverwrite=True,filetypes=[('BEE2.4 package file','.bee_pack')],title='Compile package',initialdir=(None if beepath=='' else beepath))
        if zipfile!='':

            os.makedirs(os.getcwd()+'/temp',exist_ok=True)

            with open(os.getcwd()+'/temp/info.txt','w') as inf:

                indent = 0
                inf.write('"ID" "'+packid.get()+'"\n')
                inf.write('"Name" "'+packtitle.get()+'"\n')
                inf.write('"Desc" "'+packdesc.get()+'"\n\n')

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

def save():

    if len(music)!=0:

        file = fs.asksaveasfile(defaultextension='.bxs',filetypes=[('beeMMX R save file','.bxs .beemmx .bxsave')],initialfile=packid.get()+'.bxs',title='Save beeMMX R project file')

        if file!=None:

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
                    'NoSmall':i.prev==-1,
                    'Style':tuple(styles.keys())[styleNames.index(stylevar.get())]
                }})

            jsonData = json.dumps(savedata,indent=4)

            file.write(jsonData)

        else:
            msg.showerror('No music','There is no music in the package! The save operation has been cancelled.')    

def loadFile():
    
    file = fs.askopenfile(defaultextension='.bxs',filetypes=[('beeMMX R save file','.bxs .beemmx .bxsave')],title='Load beeMMX R project file')

    if file != None:
        ask = msg.askyesno('Please confirm','Are you sure you want to overwrite all data for values from this project?')

        if ask:

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
                music.append(Track(i,tr['ShortName'].replace('\\"','"'),tr['Name'].replace('\\"','"'),tr['Desc'].replace('\\"','"'),tr['Authors'].replace('\\"','"'),tr['Loop_length'],tr['Image'],tr['Preview'],tr['Music'],tr['Sample'],tr['Group'].replace('\\"','"'),tr['Key'],styles[tr['Style']],tr['NoSmall']))
                tracklist.insert(tk.END,i)

def discord():
    web.open('https://discord.gg/CGAvCwdJHM')

def askpath():
    pth = fs.askdirectory(mustexist=True,title='Select BEE2 packages folder')
    if pth!=None:
        if os.path.basename(pth)=='packages':
            beepath.set(pth)
            with open(os.getcwd()+'/bee2_path.txt',mode='w') as path:
                path.write(beepath.get())
                path.close()
        else:
            msg.showerror('Not a packages folder','This is not a packages folder! Please specify another folder and try again.')

menu = tk.Menu(main,tearoff=False)
fileMenu = tk.Menu(menu,tearoff=False)
fileMenu.add_command(label='Compile',command=generate)
fileMenu.add_command(label='Add song', command=addToList)
fileMenu.add_command(label='Set up BEE2 packages folder',command=askpath)
fileMenu.add_separator()
fileMenu.add_command(label='Save',command=save)
fileMenu.add_command(label='Load',command=loadFile)
fileMenu.add_separator()
fileMenu.add_command(label='Quit',command=sys.exit)
menu.add_cascade(label='File',menu=fileMenu)

openMenu = tk.Menu(menu,tearoff=False)
openMenu.add_command(command=openDir,label='App directory')
openMenu.add_command(command=discord,label='Discord server')
menu.add_cascade(menu=openMenu,label='Open')

def changeSkip():
    prev.config(state=('disabled' if skipImg.get() else 'normal'))

skipImg = tk.BooleanVar(main,False)
largeImageSkip = tk.Checkbutton(trackdata,text="Use Image only",variable=skipImg,command=changeSkip)
largeImageSkip.grid(row=0,column=3,padx=5,pady=5)

main.config(menu=menu)

tk.Button(actions,text='Delete selected',command=delList).grid(row=0,column=1,padx=5,pady=5)

tk.Button(actions,text='Compile',command=generate).grid(row=1,column=1,padx=5,pady=5)

tk.mainloop()

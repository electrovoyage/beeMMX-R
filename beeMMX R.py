ver = '0.2'
print('beeMMX R v.'+ver+' loaded')

import tkinter as tk
import tkinter.messagebox as msg
import datetime as dt

release = '0'
year = '2023'

windowMain = tk.Tk()
windowMain.title('beeMMX R v.'+ver)
windowMain.geometry('650x400')
windowMain.resizable(False,False)

class MusicObject: # made to simplify generation
    def __init__(self, title, shortTitle, ID, sort, imgSm, imgLg, auth, audFl, audSp, length, group, desc):
        self.title = title
        self.shortTitle = shortTitle
        self.ID = ID
        self.key = sort
        self.smallImage = imgSm
        self.largeImage = imgLg
        self.authors = auth
        self.fullAudioSamp = audFl
        self.AudioSamp = audSp
        self.length = length
        self.group = group
        self.desc = desc

windowSongs = tk.Tk()
windowSongs.title('beeMMX R - Songs')
windowSongs.geometry('350x200')
windowSongs.resizable(False,False)

musicScroll = tk.Scrollbar(windowSongs)
musicScroll.pack(side=tk.RIGHT, fill = tk.Y)

trackBox = tk.Listbox(windowSongs, width=100,selectmode=tk.SINGLE)

global track
track = 1

musicBox = tk.Listbox(windowSongs,width=55,height = 1, selectmode=tk.SINGLE)
titleTxt = tk.Label(windowMain, text='Title (>3 chars)')
titleFld = tk.Entry(windowMain)
titleSmTxt = tk.Label(windowMain,text='Short title (<20 chars)')
titleSmFld = tk.Entry(windowMain)
IDTxt = tk.Label(windowMain,text='ID (without prefix)')
IDFld = tk.Entry(windowMain)
SortTxt = tk.Label(windowMain,text='Sort key (controls music order)')
SortFld = tk.Spinbox(windowMain, from_ = 0, to = 4294967295)
SmallImgTxt = tk.Label(windowMain,text='Small image filename (1:1 square)')
SmallImgFld = tk.Entry(windowMain)
LargeImgTxt = tk.Label(windowMain,text='Large image filename (4:3 rectangle)')
LargeImgFld = tk.Entry(windowMain)
AuthorTxt = tk.Label(windowMain,text='Author (-s)')
AuthorFld = tk.Entry(windowMain)
FullAudTxt = tk.Label(windowMain,text='Full audio filename')
FullAudFld = tk.Entry(windowMain)
ShortAudTxt = tk.Label(windowMain,text='Short (10 sec) audio sample filename')
ShortAudFld = tk.Entry(windowMain)
LengthTxt = tk.Label(windowMain,text='Song length')
LengthFld = tk.Entry(windowMain)
DescTxt = tk.Label(windowMain,text='Description of this song')
DescFld = tk.Entry(windowMain)
GrpTxt = tk.Label(windowMain,text='Group this song should be in')
GrpFld = tk.Entry(windowMain)


trackBox.config(yscrollcommand=musicScroll.set)
trackBox.pack(side=tk.LEFT, fill=tk.BOTH)
musicScroll.config(command = trackBox.yview)


titleTxt.grid(row=0,column=0,pady=5,padx=15)
titleFld.grid(row=1,column=0,pady=5,padx=15)
titleSmTxt.grid(row=0,column=1,pady=15,padx=15)
titleSmFld.grid(row=1,column=1,pady=5,padx=15)
IDTxt.grid(row=0,column=2,pady=15,padx=15)
IDFld.grid(row=1,column=2,pady=5,padx=15)
SortTxt.grid(row=2,column=0,pady=15,padx=15)
SortFld.grid(row=3,column=0,pady=5,padx=15)
SmallImgTxt.grid(row=2,column=1,pady=15,padx=15)
SmallImgFld.grid(row=3,column=1,pady=5,padx=15)
LargeImgTxt.grid(row=2,column=2,pady=15,padx=15)
LargeImgFld.grid(row=3,column=2,pady=5,padx=15)
AuthorTxt.grid(row=4,column=0,pady=15,padx=15)
AuthorFld.grid(row=5,column=0,pady=5,padx=15)
FullAudTxt.grid(row=4,column=1,pady=15,padx=15)
FullAudFld.grid(row=5,column=1,pady=5,padx=15)
ShortAudTxt.grid(row=4,column=2,pady=15,padx=15)
ShortAudFld.grid(row=5,column=2,pady=5,padx=15)
LengthTxt.grid(row=6,column=0,pady=15,padx=15)
LengthFld.grid(row=7,column=0,pady=5,padx=15)
DescTxt.grid(row=6,column=1,pady=15,padx=15)
DescFld.grid(row=7,column=1,pady=5,padx=15)
GrpTxt.grid(row=6,column=2,pady=15,padx=15)
GrpFld.grid(row=7,column=2,pady=5,padx=15)

packData = tk.Tk()
packData.title('Package information')
packData.geometry('300x150')
packData.resizable(False,False)

prefTxt = tk.Label(packData,text='Prefix')
prefTxt.grid(column=0,row=0,pady=5,padx=5)
prefFld = tk.Entry(packData)
prefFld.grid(column=0,row=1,pady=5,padx=5)

packIDTxt = tk.Label(packData,text='Package ID')
packIDTxt.grid(column=1,row=0,pady=5,padx=5)
packIDFld = tk.Entry(packData)
packIDFld.grid(column=1,row=1,pady=5,padx=5)

packNameTxt = tk.Label(packData,text='Package GUI name')
packNameTxt.grid(column=0,row=2,pady=5,padx=5)
packNameFld = tk.Entry(packData)
packNameFld.grid(column=0,row=3,pady=5,padx=5)

packDescTxt = tk.Label(packData,text='Package GUI description')
packDescTxt.grid(column=1,row=2,pady=5,padx=5)
packDescFld = tk.Entry(packData)
packDescFld.grid(column=1,row=3,pady=5,padx=5)

music = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

img = tk.PhotoImage(file = 'BMMX.png')
windowMain.iconphoto(True,img)
def addBridge():
    global track
    track = add(track)
    if track==65:
        msg.showerror('Too many tracks', 'Too many tracks in package!')
        quit
def add(tr):
    track=tr+1
    trackBox.insert(tr,titleFld.get())
    musicBox.insert(tr,MusicObject(titleFld.get(), titleSmFld.get(), IDFld.get(), SortFld.get(), SmallImgFld.get(), LargeImgFld.get(), AuthorFld.get(), FullAudFld.get(), ShortAudFld.get(), LengthFld.get(), GrpFld.get(), DescFld.get()))
    return track
def about():
    msg.showinfo('About beeMMX R '+release,'beeMMX R version '+ver+'.\r\n'+'Made in '+year+' by electrovoyage.')
def generate():
    with open('info.txt', 'w') as inf:
        inf.write('"ID" "'+packIDFld.get()+'"\r\n')
        inf.write('"Name" "'+packNameFld.get()+'"\r\n')
        inf.write('"Desc" "'+packDescFld.get()+'"\r\n')
        for i in music:
            if i==track:
                break
            inf.write('// Generated by beeMMX R v.'+ver+'\r\n')
            inf.write('"Music"\r\n {')
            inf.write('"ID" "beeMMX_R_'+(prefFld.get()+'_')+i.ID+'"'+'\r\n')
            inf.write('"Name" "'+i.title+'"\r\n')
            inf.write('"ShortName" "'+i.shortTitle+'"\r\n')
            inf.write('"Group" "'+i.group+'"\r\n')
            inf.write('"Icon" "'+i.smallImage+'"\r\n')
            inf.write('"IconLarge" "'+i.largeImage+'"\r\n')
            inf.write('"Authors" "'+i.authors+'"\r\n')
            inf.write('"Sort_key" "'+i.key+'"\r\n')
            inf.write('"Description" "'+i.desc+'"\r\n')
            inf.write('"loop_len" "'+i.length+'"\r\n')
            inf.write('"Sample"\r\n')
            print('Music module: main info done, linking sounds...')
            inf.write('{\r\n')
            inf.write('"Base" "'+i.AudioSamp+'"\r\n')
            inf.write('}\r\n')
            inf.write('"SoundScript"\r\n')
            inf.write('"Base" "'+i.fullAudioSample+'"\r\n')
            inf.write('}')
            inf.write('}')
            print('Package "'+'beeMMX_R_'+(prefFld.get()+'_')+i.ID)+'"'+' done generating!')
            
def save():
    with open((prefFld.get()+'_')+IDFld.get()+'.beemmx','w') as save:
        for i in range(track):
            save.write(music[i])

def load():
    print('save function goes here')

date = dt.date.today()
datef = date.strftime('%d_%m_%Y')

ui_menu = tk.Menu(windowMain)
windowMain.config(menu=ui_menu)
fileMenu = tk.Menu(ui_menu)

ui_menu.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='Generate package...', command = generate)
fileMenu.add_command(label='Save current track and create new...', command = addBridge)
fileMenu.add_separator()
fileMenu.add_command(label='About beeMMX R '+release, command = about)
fileMenu.add_command(label='Quit', command = quit)

savesMenu = tk.Menu(ui_menu)
ui_menu.add_cascade(label='Saves', menu=savesMenu)
savesMenu.add_command(label='Save to "bMMX_'+datef+'.beemmx"...', command = save)
savesMenu.add_command(label='Load from "bMMX_'+datef+'.beemmx"...', command = load)

tk.mainloop()

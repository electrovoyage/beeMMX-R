# beeMMX R
beeMMX R is a repythonized version of BMMX.
## What is beeMMX R?
beeMMX R is an application that generates full BEE2.4 music packages. Made in Python, it is designed to simplify adding more music to BEE2.4.
### Building the app
To build the app, you will need the following libraries:
* `tkinter` - UI
* `PIL` (`pillow`) - loading images
* `os` - getting path of `sys.executable`, `os.chdir` if 'Open with' is used
* `mutagen` - length of audio
* `keyboard` - "Hold down SHIFT to dismiss this message."
* `sys` - proper path detection, quitting
* `json` - saving/loading functions
* `shutil` - zipping the end package
* `webbrowser` - for opening Discord and the app folder
* `PyInstaller` - for building an executable
Then, to build the executable, go to the directory with the `beemmx.py` file and open the command line.
At the command line, type:
```
py -m PyInstaller --onefile --icon media/icon.ico --noconsole beemmx.py
```
After it's done, copy the `media/` folder to `dist/` under the same name.

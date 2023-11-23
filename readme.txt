Note: Below instructions are for a Windows 11 PC. Mac might be slightly different.
It has been tested to work on Mac as well

Open terminal at the folder location
Check what vrsion of tkinter is installed by running: 
    python3 -m tkinter. 
Need 8.6 or above
To install tkinter, type: 
    pip3 install tkinter
Type: 
    pip3 install -r requirements.txt 
to install the other packages
Type:
    python3 ./tkslidespeaker.py
to run the application
For presentation name, enter: woc-full

Packaging

python -m pip pyinstaller
pyinstaller ./tkslidespeaker.py
Edit the tkslidespeaker.spec file
To ensure that you don't get error from pptx module when doing ppt2convert
Add the following under datas inside Analysis(...)
    datas=[
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\default.pptx', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\notesMaster.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\theme.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\notes.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\docx-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\generic-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\pptx-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\xlsx-icon.emf', '.\\pptx\\templates\\')
    ]

To ensure that console window does not show up, set console=False inside EXE(...)

Rerun the pyinstaller by pointing to the spec file
pyinstaller -spec ./tkslidespeaker.spec

Go to the dist folder
Type .\tkslidespeaker.exe







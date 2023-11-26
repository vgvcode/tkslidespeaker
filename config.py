canvasWidth = 650
canvasHeight = 400
canvasPadX = 15
notesFontSize = 10
pageNumFontSize = 10
notesHeight = 12
notesWidth = 74
notesWrapLength = 500
notesPadX = 65
fillerFontSize = 3
modalHeight = 150
modalWidth = 500
modalFontSize = 10
copyrightText = "(C) ConnectedWorld Technology Solutions    |    http://connectedworldtech.com"
copyrightFgColor = "blue"
copyrightPadY = 5
outerButtonBgColor = "#004d00"
innerButtonBgColor = "green"
errorButtonBgColor = "red"
textHightlightColor = "OliveDrab1"
disabledForegroundColor = "gainsboro"
autoAdvanceDelay = 3    #3 second delay before advancing to next page
isPlaying = False
speakerComboBoxWidth = 50 

home = None
appName = "tkslidespeaker"
friendlyAppName = "SlideSpeaker"
appFolder = None
stagingFolder = None
tmpFolder = None
outputFolder = None
txtPresoName = None
pageNum = 0
presentation = {"pages" : []}
autoAdvance = 0
speakerList = [
    ("US English, Female, Joanna", "Joanna", ""), 
    ("British English, Female, Amy", "Amy", ""), 
    ("Indian English, Female, Kajal", "Kajal", ""), 
    ("US English, Male, Stephen", "Stephen", ""), 
    ("British English, Male, Brian", "Brian", ""), 
    ("Tamil, Male, Kumar", "Kumar", ""), 
    ("Tamil, Female, Malar", "Malar", ""),
    ("Hindi, Female, Kajal", "Kajal", "hi-IN")
    ]
threadReturnValue = None
maxSlides = 300
apiKey = 'maistrosoft.connectedworldtech'
intervalTimer = None

#widgets
rootWin = None
can = None
can_image_container = None
txtNotes = None
lblPageNum = None
goToPageCombo = None
uploadButton = None
downloadButton = None
playButton = None
firstButton = None
lastButton = None
nextButton = None
previousButton = None
replayButton = None
stopButton = None
autoAdvanceCheckBox = None
progressBar = None

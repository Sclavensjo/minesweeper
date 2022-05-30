from cmu_graphics import *
import time

app.title = "Minesweeper 1.0"
app.start=False
app.steps = 30
app.bwidth = 10
app.bheight = 10
app.bombs = 20
app.bombsplaced = False
app.bombcolor = "red"
app.bordcolor = rgb(100,100,100)
app.bordercolor = rgb(159,85,2)
app.covercolor = rgb(126,240,148)
app.flagcolor = rgb (115,90,230)
app.textcolor = rgb(0,0,0)
app.uncovering = True
app.flags = app.bombs
app.haveuncoverdzeros = False
app.started = False
app.paintedbord = False
app.starttimer = 0
app.lost = False
app.didhewin = 0


infoscreen = Group( 
    Rect(0,0,400,400,fill=rgb(38,68,110),opacity = 30,border=rgb(111,230,6)),
    Label("MINESWEEPER",200,50,fill=app.textcolor,size = 40),
    Label("Discover bombs with your mouse, the number on ",200,95,size = 18),
    Label("the square is the amount of bombs around it",200,115,size = 18),
    Label("Press space to change to flag mode, while in",200,145,size = 18),
    Label("flag mode uncoverd squres will turn orange",200,165,size = 18),
    Label("When you feel you have discoverd every tile",200,195,size = 18),
    Label("without pressing a bomb",200,215,size = 18),
    Label("press d to check for the win",200,235,size = 18),
    Label("press s to change size of the bord",200,265,size = 18),
    Label("Press r to restart",200,295,size = 18),
)
closeboxbox = Rect(100,325,200,50,fill=app.bordcolor)
startlabel = Label("START",200,350,size=20,fill=app.textcolor)
closebox = Group(
    closeboxbox,
    startlabel
)
losescreen = Group(
    Rect(100,100,200,200,fill=rgb(38,68,110),border=rgb(111,230,6),opacity=70),
    Label("You Lose",200,200,fill=app.textcolor,size = 40)
)
losescreen.visible=False

winscreen = Group(
    Rect(100,100,200,200,fill=rgb(38,68,110),border=rgb(111,230,6),opacity=70),
    Label("You win with a time of",200,160,fill=app.textcolor,size = 20),
    Label("seconds",200,240,fill=app.textcolor,size = 20),
)
app.wintimer = Label(0,200,200,fill=app.textcolor,size = 40)
winscreen.add(app.wintimer)
winscreen.visible= False

def choosesize():
    size = app.getTextInput("type in a size (less then 25)")
    bombs = app.getTextInput("Type in amounts of bombs")
    if size.isdigit() or size != 0 or size <= 25:
        app.bwidth = int(size)
        app.bheight = int(size)
    if bombs.isdigit():
        app.bombs = int(bombs)

def paintbord():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            app.bord[row][col] = Rect(0 + 400/app.bwidth * row, 0 + 400/app.bheight * col,400/app.bwidth,400/app.bheight,fill=app.bordcolor,border=app.bordercolor,borderWidth = 1)
            app.coverbord[row][col] = Rect(0 + 400/app.bwidth * row, 0 + 400/app.bheight * col,400/app.bwidth,400/app.bheight,fill=app.covercolor,border=app.bordercolor,borderWidth = 1)
            pass

def placebomb():
    for bomb in range(app.bombs):
        bo = choice(app.bord)
        bom = choice(bo)
        while(bom.fill == app.bombcolor):
            bo = choice(app.bord)
            bom = choice(bo)
        bom.fill=app.bombcolor

    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.bord[row][col]
            bombs = 0
            here.bombss = 0
            if col < app.bwidth-1:
                if app.bord[row][col+1].fill==app.bombcolor:
                    bombs += 1
            if col < app.bwidth-1 and row > 0:
                if app.bord[row-1][col+1].fill==app.bombcolor:
                    bombs += 1
            if col < app.bwidth-1 and row < app.bwidth-1:
                if app.bord[row+1][col+1].fill==app.bombcolor:
                    bombs += 1
            if col > 0:
                if app.bord[row][col-1].fill==app.bombcolor:
                    bombs += 1
            if col > 0 and row < app.bwidth-1:
                if app.bord[row+1][col-1].fill==app.bombcolor:
                    bombs +=1
            if col > 0 and row > 0:
                if app.bord[row-1][col-1].fill==app.bombcolor:
                    bombs +=1
            if row > 0:
                if app.bord[row-1][col].fill==app.bombcolor:
                    bombs +=1
            if row < app.bwidth-1:
                if app.bord[row+1][col].fill==app.bombcolor:
                    bombs += 1
            
            here.bombss = bombs
            if here.fill != app.bombcolor:
                Label(bombs,here.centerX,here.centerY,fill=app.textcolor)
            app.coverbord[row][col].toFront()
def uncoverzeros(x,y):
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.coverbord[row][col]
            underhere = app.bord[row][col]
            if here.hits(x,y) and underhere.bombss == 0:
                if col < app.bheight-1:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row][col+1].opacity = 0
                if col < app.bheight-1 and row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col+1].opacity = 0
                if col < app.bheight-1 and row < app.bheight-1:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col+1].opacity = 0
                if col > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row][col-1].opacity = 0
                if col > 0 and row < app.bheight-1:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col-1].opacity = 0
                if col > 0 and row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col-1].opacity = 0
                if row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col].opacity = 0
                if row < app.bheight-1:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col].opacity = 0
def zerouncoverings():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.bord[row][col]
            overhere = app.coverbord[row][col]
            if here.bombss == 0 and here.fill!=app.bombcolor:
                if col < app.bheight-1:
                    if app.coverbord[row][col+1].opacity == 0:
                        overhere.opacity = 0
                if col < app.bheight-1 and row > 0:
                    if app.coverbord[row-1][col+1].opacity == 0:
                        overhere.opacity = 0
                if col < app.bheight-1 and row < app.bheight-1:
                    if app.coverbord[row+1][col+1].opacity == 0:
                        overhere.opacity = 0
                if col > 0:
                    if app.coverbord[row][col-1].opacity == 0:
                        overhere.opacity = 0                     
                if col > 0 and row < app.bheight-1:
                    if app.coverbord[row+1][col-1].opacity == 0:
                        overhere.opacity = 0
                if col > 0 and row > 0:
                    if app.coverbord[row-1][col-1].opacity == 0:
                        overhere.opacity = 0  
                if row > 0:
                    if app.coverbord[row-1][col].opacity == 0:
                        overhere.opacity = 0
                if row < app.bheight-1:
                    if app.coverbord[row+1][col].opacity == 0:
                        overhere.opacity = 0
                if overhere.opacity == 0 and col < app.bheight-1 and col > 0 and row < app.bheight-1 and row > 0:
                        app.coverbord[row][col+1].opacity = 0
                        app.coverbord[row-1][col+1].opacity = 0
                        app.coverbord[row+1][col+1].opacity = 0
                        app.coverbord[row][col-1].opacity = 0
                        app.coverbord[row+1][col-1].opacity = 0
                        app.coverbord[row-1][col-1].opacity = 0
                        app.coverbord[row-1][col].opacity = 0
                        app.coverbord[row+1][col].opacity = 0
                        
def lose(x,y):
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.coverbord[row][col]
            underhere = app.bord[row][col]
            if here.hits(x,y) and underhere.fill == app.bombcolor and here.fill != app.flagcolor and app.uncovering == True:
                losescreen.visible=True
                losescreen.toFront()
                app.lost= True
                app.start = False
                pass
def losed(cheat):
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.coverbord[row][col]
            underhere = app.bord[row][col]
            if cheat == "no":
                here.visible = False
            elif cheat == "yes" and underhere.fill != app.bombcolor:
                here.opacity = 0
def win():
    uncoverd = 0
    for row in range(app.bwidth):
        for col in range(app.bheight):
            now = app.coverbord[row][col]
            if now.opacity == 0:
                uncoverd += 1 
    return uncoverd

def falgplacing(x,y):
    for row in range(app.bwidth):
            for col in range(app.bheight):
                rec = app.coverbord[row][col]
                if rec.hits(x,y):
                    if app.uncovering==True and rec.fill != app.flagcolor:
                        rec.opacity = 0
                    elif app.uncovering == False and rec.fill==app.flagcolor:
                        rec.fill=app.covercolor
                        app.flags += 1
                    elif app.flags > 0 and app.uncovering == False:
                        rec.fill=app.flagcolor
                        app.flags -= 1
def restart():
    for col in range(app.bwidth):
        for row in range(app.bheight):
            here = app.bord[row][col]
            overhere = app.coverbord[row][col]
            here = None
            overhere = None
            app.group.clear()
def coverbordtofront():
    for col in range(app.bwidth):
        for row in range(app.bwidth):
            here = app.coverbord[row][col]
            here.toFront()
def flagmode(mode):
    for col in range(app.bwidth):
        for row in range(app.bheight):
            here = app.bord[row][col]
            if mode == "flag" and here.fill != app.bombcolor:
                here.fill= rgb(179, 143, 61)
            elif mode != "flag" and here.fill!=app.bombcolor:
                here.fill= app.bordcolor


def onKeyPress(key):
    if app.start == True:
        if key == "space":
            if app.uncovering == True:
                app.uncovering = False
                flagmode("flag")
            else:
                app.uncovering = True
                flagmode("no")
        if key == "d":
            app.didhewin = win()
            if app.didhewin >= (app.bwidth*app.bheight)-app.bombs:
                timde = rounded(time.time()-app.starttimer)
                winscreen.visible = True
                winscreen.toFront()
                app.start = False
                app.wintimer.value = timde
        if key == "o":
            losed("yes")
    if key == "r":
        losescreen.visible = False
        winscreen.visible = False
        app.start = True
        app.lost = False
        restart()
        paintbord()
        coverbordtofront()
        app.starttimer=time.time()
        placebomb()
    if app.start == False:
        if key == "s":
            choosesize()
def onStep():
    if app.start==True:
        if app.bombsplaced == True:
            zerouncoverings()
    if app.lost== True:
        losed("no")

def onMouseMove(mouseX,mouseY):
    if closebox.contains(mouseX,mouseY):
        closeboxbox.fill=rgb(126,240,148)

    else:
        closeboxbox.fill=app.bordcolor
def onMousePress(mouseX,mouseY):
    if closebox.hits(mouseX,mouseY) and app.paintedbord == False:
        app.coverbord = makeList(app.bwidth, app.bheight)
        app.bord = makeList(app.bwidth, app.bheight)
        infoscreen.visible= False
        closebox.visible=False
        paintbord()
        app.paintedbord = True
        app.start=True
        app.starttimer = time.time()
    if app.start == True:
        if app.bombsplaced == False and infoscreen.visible==False:
            placebomb()
            app.bombsplaced = True
            return
        if app.bombsplaced == True:
            uncoverzeros(mouseX,mouseY)
        if infoscreen.visible == False:
            falgplacing(mouseX,mouseY)
            lose(mouseX,mouseY)



cmu_graphics.run()
from __future__ import with_statement
from multiprocessing.sharedctypes import Value
from tkinter import FALSE
from turtle import color
from cmu_graphics import *
app.start=False
app.steps = 60
app.bwidth = 20
app.bheight = 20
app.bombs = 60
app.coverbord = makeList(app.bwidth, app.bheight)
app.bord = makeList(app.bwidth, app.bheight)
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
app.mode = Rect(0,0,400,400,fill=rgb(252, 3, 3),opacity = 30,visible = False)
app.hiddentimer = Label(0,0,0,fill=app.textcolor,visible = False)
app.timer = Label(0,200,50,fill=app.textcolor,size = 20,visible = False)
app.alluncoverd = 0 
app.lost = False
infoscreen = Group( 
    Rect(0,0,400,400,fill=rgb(38,68,110),opacity = 30,border=rgb(111,230,6)),
    Label("MINESWEEPER",200,50,fill=app.textcolor,size = 40),
    Label("Discover bombs with you mouse, the number on ",200,110,size = 18),
    Label("the square is the amount of bombs around it",200,130,size = 18),
    Label("Press space to change to flag mode, while in",200,160,size = 18),
    Label("flag mode uncoverd squres will turn orange",200,180,size = 18),
    

)
closebox = Group(
    Rect(100,300,200,50,fill=app.covercolor),
    Label("START",200,325,size=20,fill=app.textcolor),
)
losescreen = Group(
    Rect(100,100,200,200,fill=rgb(38,68,110),border=rgb(111,230,6),opacity=70),
    Label("You Lose",200,200,fill=app.textcolor,size = 40)
)
losescreen.visible=False

winscreen = Group(
    Rect(100,100,200,200,fill=rgb(38,68,110),border=rgb(111,230,6),opacity=70),
    Label("You win with a time of",200,200,fill=app.textcolor,size = 40),
    Label(app.timer.value,200,220,fill=app.textcolor,size = 40)
)
winscreen.visible= False
def paintbord():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            squ = Rect(0 + 400/app.bwidth * row, 0 + 400/app.bheight * col,400/app.bwidth,400/app.bheight,fill=app.bordcolor,border=app.bordercolor,borderWidth = 1)
            squ.bombss = 0
            app.bord[row][col] = squ
            csqu = Rect(0 + 400/app.bwidth * row, 0 + 400/app.bheight * col,400/app.bwidth,400/app.bheight,fill=app.covercolor,border=app.bordercolor,borderWidth = 1)
            app.coverbord[row][col] = csqu
            pass
def placebomb():
    for bomb in range(app.bombs):
        bo = choice(app.bord)
        bom = choice(bo)
        bom.fill=app.bombcolor

    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.bord[row][col]
            bombs = 0
            if col < app.bwidth-1:
                if app.bord[row][col+1].fill=="red":
                    bombs += 1
            if col < app.bwidth-1 and row > 0:
                if app.bord[row-1][col+1].fill=="red":
                    bombs += 1
            if col < app.bwidth-1 and row < app.bwidth-1:
                if app.bord[row+1][col+1].fill=="red":
                    bombs += 1
            if col > 0:
                if app.bord[row][col-1].fill=="red":
                    bombs += 1
            if col > 0 and row < app.bwidth-1:
                if app.bord[row+1][col-1].fill=="red":
                    bombs +=1
            if col > 0 and row > 0:
                if app.bord[row-1][col-1].fill=="red":
                    bombs +=1
            if row > 0:
                if app.bord[row-1][col].fill=="red":
                    bombs +=1
            if row < app.bwidth-1:
                if app.bord[row+1][col].fill=="red":
                    bombs += 1
            
            here.bombss = bombs
            if here.fill != "red":
                Label(bombs,here.centerX,here.centerY,fill=app.textcolor)
            app.coverbord[row][col].toFront()
def uncoverzeros(x,y):
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.coverbord[row][col]
            underhere = app.bord[row][col]
            if here.hits(x,y) and underhere.bombss == 0:
                if col < 19:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row][col+1].opacity = 0
                if col < 19 and row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col+1].opacity = 0
                if col < 19 and row < 19:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col+1].opacity = 0
                if col > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row][col-1].opacity = 0
                if col > 0 and row < 19:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col-1].opacity = 0
                if col > 0 and row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col-1].opacity = 0
                if row > 0:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row-1][col].opacity = 0
                if row < 19:
                    if underhere.bombss==0 and underhere.fill != app.bombcolor:
                        app.coverbord[row+1][col].opacity = 0
def zerouncoverings():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.bord[row][col]
            overhere = app.coverbord[row][col]
            if here.bombss == 0 and here.fill!=app.bombcolor:
                if col < 19:
                    if app.coverbord[row][col+1].opacity == 0:
                        overhere.opacity = 0
                if col < 19 and row > 0:
                    if app.coverbord[row-1][col+1].opacity == 0:
                        overhere.opacity = 0
                if col < 19 and row < 19:
                    if app.coverbord[row+1][col+1].opacity == 0:
                        overhere.opacity = 0
                if col > 0:
                    if app.coverbord[row][col-1].opacity == 0:
                        overhere.opacity = 0                     
                if col > 0 and row < 19:
                    if app.coverbord[row+1][col-1].opacity == 0:
                        overhere.opacity = 0
                if col > 0 and row > 0:
                    if app.coverbord[row-1][col-1].opacity == 0:
                        overhere.opacity = 0  
                if row > 0:
                    if app.coverbord[row-1][col].opacity == 0:
                        overhere.opacity = 0
                if row < 19:
                    if app.coverbord[row+1][col].opacity == 0:
                        overhere.opacity = 0
                if overhere.opacity == 0 and col < 19 and col > 0 and row < 19 and row > 0:
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
def losed():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            here = app.coverbord[row][col]
            here.visible = False
def win():
    for row in range(app.bwidth):
        for col in range(app.bheight):
            now = app.coverbord[row][col]
            if now.visible == False:
                app.alluncoverd += 1 
    pass

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
def onKeyPress(key):
    if app.start == True:
        if key == "space":
            if app.uncovering == True:
                app.uncovering = False
                app.mode.fill = rgb(252, 165, 3)
            else:
                app.uncovering = True
                app.mode.fill = rgb(252, 3, 3)
def onStep():
    if app.start==True:
        if app.bombsplaced == True:
            zerouncoverings()
    if app.start==True:
        app.hiddentimer.value += 1
    app.timer.value = app.hiddentimer.value // 6
    if app.lost== True:
        losed() 
def onMousePress(mouseX,mouseY):
    if closebox.hits(mouseX,mouseY) and app.paintedbord == False:
        infoscreen.visible= False
        closebox.visible=False
        paintbord()
        app.paintedbord = True
        app.start=True
        app.mode.visible =True
        app.mode.toFront()
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
            win()
    if app.alluncoverd == (app.bwidth*app.bheight)-app.bombs:
        winscreen.visible = True
        winscreen.toFront()
        app.start = False


cmu_graphics.run()
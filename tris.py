
import pygame as pg
import random
import time
pg.init()

def draw_board_back():

    for i in range(1,3):
        pg.draw.line(display,line_color,(i*tilesize,0),(i*tilesize,displaysize[1]-3*fontsize),line_thickness)
    for i in range(1,4):
        pg.draw.line(display,line_color,(0,i*tilesize),(displaysize[0],i*tilesize),line_thickness)
    score_text = font.render(" Crosses: "+str(xscore)+"                 Circles: "+str(oscore),True,line_color)
    display.blit(score_text,(0,3*tilesize+fontsize))
    


def draw_cursor():
    for rectangle in board_rects:
        rectangle = rectangle[0]
        if rectangle.collidepoint(mousepos):
            if xturn:
                pg.draw.circle(display,x_color,mousepos,5)
            else:
                pg.draw.circle(display,o_color,mousepos,5)
        
def detect_click():
    global board_rects
    global xturn
    if process_mouse:
        if mousepressed[0]:
            for rect in board_rects:
                rect1 = rect[0]
                if rect1.collidepoint(mousepos):
                    if xturn and rect[1] == "Empty":
                        board_rects[board_rects.index(rect)][1] = "Cross"
                        xturn = False
                    elif not xturn and rect[1] == "Empty":
                        board_rects[board_rects.index(rect)][1] = "Circle"
                        xturn = True
                    if debug:
                        print(board_rects.index(rect),rect[1])


def draw_cross(x,y,x_color):
    pg.draw.line(display,x_color,(x+tilesize*0.1,y+tilesize*0.1),(x+tilesize*0.9,y+tilesize*0.9),round(tilesize/10))
    pg.draw.line(display,x_color,(x+tilesize*0.9,y+tilesize*0.1),(x+tilesize*0.1,y+tilesize*0.9),round(tilesize/10))
    
def draw_circle(x,y,o_color):
    pg.draw.circle(display,o_color,(round(x+tilesize/2),round(y+tilesize/2)),round(0.45*tilesize),round(tilesize/10))

def draw_symbols():
    for rect in board_rects:
        if rect[1] == "Cross":
            draw_cross(rect[0].left,rect[0].top,x_color)
        elif rect[1] == "Circle":
            draw_circle(rect[0].left,rect[0].top,o_color)


def detect_state():
    global end_state
    crosses = []
    circles = []
    for rect in board_rects:
        if rect[1] == "Cross":
            crosses.append(board_rects.index(rect))
        elif rect[1] == "Circle":
            circles.append(board_rects.index(rect))
    crosses.sort()
    circles.sort()

    if debug:
        print(circles,crosses)
    if len(circles)+len(crosses) == 9:
        end_state = "Tie"
    for possible in winning_combs:
        if all(x in circles for x in possible):
            end_state = "Circles"
        elif all(x in crosses for x in possible):
            end_state = "Crosses"
    
def draw_onhover():
    for rect in board_rects:
        rect2 = rect
        rect = rect[0]
        if rect.collidepoint(mousepos) and rect2[1] == "Empty":
            pg.draw.rect(display,onhover_color,rect)
            if xturn:
                draw_cross(rect.left,rect.top,xghost_color)
            else:
                draw_circle(rect.left,rect.top,oghost_color)



def KOMPACT():
        display.fill(background_color)
        draw_onhover()
        draw_board_back()
        detect_click()
        draw_symbols()
        detect_state()
        draw_cursor()
        pg.display.update()
        clock.tick(1000)


#settings
debug = False
downtime = 1
color_style = 1



#colors

black = (0,0,0)
white = (255,255,255)
cream = (255,255,230)
red = (255,0,0)
light_red = (255,100,100)
lime = (0,255,0)
light_lime = (100,255,100)
blue = (0,0,255)
dark_cream = (240,240,210)
dark_gray = (50,50,50)
light_gray = (100,100,100)

if color_style == 1:                        #1:dark mode
    background_color = (dark_gray)
    line_color = (cream)
    x_color = (red)
    xghost_color = (light_red)
    o_color = (lime)
    oghost_color = (light_lime)
    onhover_color = (light_gray)
    
elif color_style == 2:                      #2:light mode
    background_color = (cream)
    line_color = (black)
    x_color = (red)
    xghost_color = (light_red)
    o_color = (lime)
    oghost_color = (light_lime)
    onhover_color = (dark_cream)



#display
tilesize = 200
fontsize = 50
displaysize = [tilesize*3,tilesize*3]
line_thickness = round(tilesize/50)
font = pg.font.SysFont("Calibri",fontsize)
pg.mouse.set_visible(False)
displaysize[1] += 3*fontsize



#pre initialization
xscore = 0
oscore = 0
start_turn = random.choice([True,False])
winning_combs = [[0,1,2],[0,3,6],[3,4,5],[1,4,7],[6,7,8],[2,5,8],[0,4,8],[2,4,6]]
display = pg.display.set_mode(displaysize)
pg.display.set_caption("Trys")
clock = pg.time.Clock()
#main loop
quitted = False
while not quitted:
    #initialization

    board_rects = []
    for i in range(3):
        for y in range(3):
            board_rects.append([pg.Rect(i*tilesize,y*tilesize,tilesize,tilesize),"Empty"])
 
    process_mouse = False

    xturn = start_turn
    start_turn = not start_turn
    end_state = 0    
    dead = False
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
                quitted = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True
                    quitted = True
                if event.key == pg.K_r:
                    dead = True



            if event.type == pg.MOUSEBUTTONDOWN and process_mouse == False:
                process_mouse = True
                
        mousepos = pg.mouse.get_pos()
        mousepressed = pg.mouse.get_pressed(3)



        KOMPACT()
        
        process_mouse = False
        if end_state != 0:
            print("Game over!  ",end = "")
            if end_state == "Circles":
                print("circles won!")
                dead = True
                oscore += 1
            elif end_state == "Crosses":
                print("crosses won!")
                dead = True
                xscore += 1
            else:
                print("It's a tie!")
                dead = True
            time.sleep(downtime)
                

pg.quit()
quit()

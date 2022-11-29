from xml.etree import ElementTree as ET
from typing import Optional
from random import randrange

caveMap = '''
 1
 
 11111111111111
 1     11     1
 1            1
 1    1C 1    1
 1            1
 1            1
  111112 11111
'''

mainMap = '''      1111
     11  1
   1     1
  1      1
11       1111111
1               3
11              
 1            11
 1            1
  111111111111'''

room3 = '''1111111111111111
1111111111111111
11  11    1
1       1 1
1 S I G   1
        1 1
          1
1       1  11N11
11  11          4
1111111111111111
'''

finalRoom = '''1
1111111111111111
 1          1 1 
1           1  1
1           1  1
1           1Z 1
1111111111111  1
1              1
              11
1111111111111115              
'''

#################### BEGIN EDITABLE CONSTANTS ####################
# you shouldn't edit these, they were just tweakable while I was making the game
BACKGROUND_IMAGE_SOURCE = "https://i.imgur.com/mEqB7qg.png"

SCREEN_WIDTH = 256 * 2
SCREEN_HEIGHT = 168 * 2
CONTROLLER_AREA_HEIGHT = 214

HERO_WIDTH = 16 * 2
HERO_HEIGHT = 16 * 2

TILE_WIDTH = 16 * 2
TILE_HEIGHT = 16 * 2

# HERO_START_ coordinates should be given in tiles, relative to top left (0, 0)
# since everything is pretty much hard coded anyway, changing this will probably break everything
HERO_START_X = 10
HERO_START_Y = 8

# relative to the top left of the controller area
BUTTONS_START_X = 90
BUTTONS_START_Y = 90

BUTTON_WIDTH = 24
BUTTON_HEIGHT = 24

MESSAGE_MARGIN = 12

# debug constants
BLOCKER_COLOR = "rgb(58, 59, 59)"
BLOCKER_OPACITY = 0.5
SHOW_OVERFLOW = True
##################### END EDITABLE CONSTANTS #####################

# precomputed constants
NUM_FORCED_OPEN_TILES = 0 # this is to deal with the annoying fact that the cave entrance isn't at the edge of the screen
MEMORY_HEIGHT = SCREEN_HEIGHT + CONTROLLER_AREA_HEIGHT - NUM_FORCED_OPEN_TILES
OVERFLOW_STRING = ";overflow:hidden" if not SHOW_OVERFLOW else ""
# where the buttons begin relative to the specific controller image im using
# make sure these are at least as large as BUTTONS_START_X and BUTTONS_START_Y
CONTROLLER_MARGIN_X = 32
CONTROLLER_MARGIN_Y = 66

# where the a button is relative to the top left of the buttons
CONTROLLER_A_X = 280
CONTROLLER_A_Y = 40

CONTROLLER_IMG_WIDTH = 389
CONTROLLER_IMG_HEIGHT = 171

def append(parent: ET.Element, childTag: str, style: Optional[str] = None, innerText: Optional[str] = None) -> ET.Element:
    attribs = {"style": style} if style else {}
    child = ET.SubElement(parent, childTag, attrib=attribs)
    child.text = innerText if innerText else None
    return child

def computeLeftAndTopStyle(memoryInfluence: tuple[int, int], referenceMemory: tuple[int, int], referencePosition: tuple[int, int]) -> str:
   return f"left:calc({referencePosition[0]}px + {memoryInfluence[0]} * calc(100% - {SCREEN_WIDTH + referenceMemory[0]}px));top:calc({referencePosition[1]}px + {memoryInfluence[1]} * calc(100% - {MEMORY_HEIGHT + referenceMemory[1]}px))"

def makeButton(memoryInfluence: tuple[int, int], referenceMemory: tuple[int, int], referencePosition: tuple[int, int], width: Optional[int] = BUTTON_WIDTH, height: Optional[int] = BUTTON_HEIGHT, xMemory: Optional[int] = None, yMemory: Optional[int] = None) -> ET.Element:
    details = ET.Element("details")
    append(details, "summary", f"position:absolute;{computeLeftAndTopStyle(memoryInfluence, referenceMemory, referencePosition)};width:{width}px;height:{height}px;list-style:none;cursor:pointer")
    memoryDivStyle = ""
    memoryDivStyle += f"width:{xMemory}px;" if xMemory is not None else ""
    memoryDivStyle += f"height:{yMemory}px;" if yMemory is not None else ""
    append(details, "div", memoryDivStyle)
    return details

def makeSignButton(memoryInfluence: tuple[int, int], referenceMemory: tuple[int, int], referencePosition: tuple[int, int], message: str):
    details = ET.Element("details")
    append(details, "summary", f"position:absolute;{computeLeftAndTopStyle(memoryInfluence, referenceMemory, referencePosition)};width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;list-style:none;cursor:pointer")
    messageDiv = append(details, "div", f"position:absolute;left:{MESSAGE_MARGIN}px;top:{MESSAGE_MARGIN}px;width:{SCREEN_WIDTH - 2 * MESSAGE_MARGIN - 10 - 2}px;padding:5px;background:#c84c0c;color:white;border:2px solid white;font-size:18px;font-weight:700;line-height:1.2;font-family:sans-serif;text-align:center;user-select:none", message)
    controlBlocker = append(details, "div", f"position:absolute;left:{BUTTONS_START_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{3 * BUTTON_WIDTH}px;height:{3 * BUTTON_HEIGHT}px;background:green")
    return details

def makeMovementButtons(memory: ET.Element) -> None:
    setupI = []
    
    for i in range(20):
        button = makeButton((0, -2 * BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH, SCREEN_HEIGHT + BUTTONS_START_Y + 2 * BUTTON_HEIGHT + 2 * BUTTON_HEIGHT * i), yMemory=1)
        memory[0].append(button)
        if 0 < i < HERO_START_Y or 11 <= i <= 15: # the second condition on i here is because exiting the cave does not place you at the edge of the map!
            button.set("open", "")
    for j in range(80):
        if j == 17: # don't let them walk without a raft!
            continue
        button = makeButton((-2 * BUTTON_WIDTH, 0), (0, 0), (BUTTONS_START_X + 2 * BUTTON_WIDTH + 2 * BUTTON_WIDTH * j, SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_HEIGHT), xMemory=1)
        memory.append(button)
        if j < HERO_START_X:
            button.set("open", "")

def makeMapColliders(memory: ET.Element, mapString: str, warpPoints: dict[str, tuple[int, int, str]], deferredMemoryChildren: list, startCoordinates: Optional[tuple[int, int]] = (0, 0), heroHelper: Optional[tuple[int, int]] = (0, 0), customTeleporterWidth: Optional[int] = 2 * BUTTON_WIDTH) -> None:
    i = startCoordinates[1]
    j = startCoordinates[0]
    for char in mapString:
        if char == "\n":
            i, j = i + 1, startCoordinates[0]
        else:
            if char == "1":
                append(memory, "div", f"position:absolute;{computeLeftAndTopStyle((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH * (j + 1), SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_HEIGHT * (i + 1)))};width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{'purple' if SHOW_OVERFLOW else 'transparent'};opacity:{BLOCKER_OPACITY}")
            elif char == "C": # the candle is pretty unique so handle it independently
                raftButton = makeButton((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH * (j + 1), SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_WIDTH * (i + 1)), width=2*BUTTON_WIDTH)
                memory[0].append(raftButton)
                J = 17
                append(raftButton, "div", f"position:absolute;left:{7 * TILE_WIDTH}px;top:{6 * TILE_HEIGHT}px;width:{2 * TILE_WIDTH}px;height:{TILE_HEIGHT}px;background:url('https://i.imgur.com/0BDU2rt.png')")
                button = makeButton((-2 * BUTTON_WIDTH, 0), (0, 0), (BUTTONS_START_X + 2 * BUTTON_WIDTH + 2 * BUTTON_WIDTH * J, SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_HEIGHT), xMemory=1)
                closeBlocker = append(raftButton, "div", f"position:absolute;{computeLeftAndTopStyle((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH * (j + 1), SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_WIDTH * (i + 1)))};width:{2 * BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:green")
                raftButton.append(button)
            elif char in ["S", "I", "G", "N", "Z"]: # characters reserved for signs lol
                signMessages = {
                    "S": "Welcome to my post! Pretty neat, huh? Press A again to close signs!",
                    "I": "This thing is so ridiculously hacked together! I'm surprised it's functional at all!",
                    "G": "Everything in this post is raw HTML with inline css!",
                    "N": "That means I can put anything I want in here! On this last screen I'm going to put the Eraserhead baby and turn you into eggbug!",
                    "Z": "That's it! Thanks for playing my game :D",
                }
                append(memory, "div", f"position:absolute;{computeLeftAndTopStyle((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH * (j + 1), SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_HEIGHT * (i + 1)))};width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{'purple' if SHOW_OVERFLOW else 'transparent'};opacity:{BLOCKER_OPACITY}")
                signButton = makeSignButton((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + CONTROLLER_A_X + BUTTON_WIDTH * (j), SCREEN_HEIGHT + BUTTONS_START_Y + CONTROLLER_A_Y + BUTTON_HEIGHT * (i + 1)), signMessages[char])
                deferredMemoryChildren.append(signButton)
                #memory.append(signButton)
            elif char != " ":
                warpButton = makeButton((-BUTTON_WIDTH, -BUTTON_HEIGHT), (0, 0), (BUTTONS_START_X + BUTTON_WIDTH * (j + 1), SCREEN_HEIGHT + BUTTONS_START_Y + BUTTON_WIDTH * (i + 1)), width=customTeleporterWidth, height=3*BUTTON_HEIGHT, xMemory=warpPoints[char][0], yMemory=warpPoints[char][1])
                append(warpButton, "div", f"position:absolute;left:0;top:0;width:{SCREEN_WIDTH}px;height:{SCREEN_HEIGHT}px;background:no-repeat url('{warpPoints[char][2]}');opacity:{BLOCKER_OPACITY}")
                print("making a hero for " + str(heroHelper))
                heroUrl = "https://i.imgur.com/kvUg4yb.png" if char == "5" else "https://i.imgur.com/Y44LaK6.png"
                append(memory, "div", f"position:absolute;left:calc({TILE_WIDTH} * calc(100% - {SCREEN_WIDTH + heroHelper[0]}px));top:calc({TILE_HEIGHT} * calc(100% - {SCREEN_HEIGHT + CONTROLLER_AREA_HEIGHT + heroHelper[1]}px));width:{HERO_WIDTH}px;height:{HERO_HEIGHT}px;background:url('{heroUrl}');background-size: 100% 100%")
                
                if char == "4":
                    babyShadow = append(warpButton, "div", f"position:absolute;left:60px;top:160px;width:300px;height:30px;filter:blur(4px);border-radius:50%;background:rgba(0, 0, 0, 0.3);box-shadow: 0 0 40px 40px rgba(0, 0, 0, 0.3);")
                    baby = append(warpButton, "div", f"position:absolute;left:40px;top:70px;width:350px;height:300px;background:no-repeat url('https://i.imgur.com/lBPlLPy.png');background-size:100%;filter: drop-shadow(2px 4px 6x black);animation: 2s ease-in-out infinite alternate-reverse none running spin;transform:translateY(-7%)")

                if char == "2":
                    warpButton.set("open", "")
                    memory[0].append(warpButton)
                #deferredMemoryChildren.append(warpButton)
                else:
                    memory.append(warpButton)
            j += 1

# main containers and objects
# STYLE ORDER: display [display-formatting], position, left, top, width, height, actual-styling
mainContainer = ET.Element("div", attrib={"style": "line-height:1.3;display:flex;flex-direction:column;width:100%;justify-content:center;align-items:center;font-family:sans-serif"})
mainHeading = append(mainContainer, "div")

screen = append(mainContainer, "div", f"width:{SCREEN_WIDTH}px;height:{MEMORY_HEIGHT}px;background:black" + OVERFLOW_STRING)
memory = append(screen, "div", f"display:inline-flex;position:relative;left:0;top:0;padding-right:{SCREEN_WIDTH}px;padding-top:{MEMORY_HEIGHT}px;background:no-repeat url('{BACKGROUND_IMAGE_SOURCE}')")
# y memory needs to be handled separately because memory can only have one flex-direction
memoryYDiv = append(memory, "div", f"display:inline-flex;flex-direction:column")

deferredMemoryChildren = []
makeMovementButtons(memory)
makeMapColliders(memory, caveMap, {"2": (0, 4, "https://i.imgur.com/3CoCBCW.png")}, deferredMemoryChildren)
makeMapColliders(memory, mainMap, {"3": (3, 0, "https://i.imgur.com/ABeuDUn.png")}, deferredMemoryChildren, startCoordinates=(3, 10), heroHelper=(3, 10))
makeMapColliders(memory, room3, {"4": (23, 0, "https://i.imgur.com/iUAbQJN.png")}, deferredMemoryChildren, startCoordinates=(21, 10), heroHelper=(21, 10), customTeleporterWidth=(22 * BUTTON_WIDTH))
makeMapColliders(memory, finalRoom, {"5": (3, 0, "https://i.imgur.com/iUAbQJN.png")}, deferredMemoryChildren, startCoordinates=(59, 10), heroHelper=(59, 10))

aButtonUnderlay = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + CONTROLLER_A_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y + CONTROLLER_A_Y}px;width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:orange")
for child in deferredMemoryChildren:
    memory.append(child)

# controller blockers: cover most of the control area in divs so the player can't click buttons when they're not supposed to
# i dont remember if any of these are placed in a way that would break if you change around the constants. the answer is: probably!
controllerBlocker1 = append(memory, "div", f"position:absolute;left:0;top:{SCREEN_HEIGHT}px;width:{SCREEN_WIDTH}px;height:{BUTTONS_START_Y}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
# controllerBlocker2 is gone ever since I added the a button
controllerBlocker3 = append(memory, "div", f"position:absolute;left:0;top:{SCREEN_HEIGHT + BUTTONS_START_Y + 3 * BUTTON_HEIGHT}px;width:{SCREEN_WIDTH}px;height:{CONTROLLER_AREA_HEIGHT - BUTTONS_START_Y - 3 * BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
controllerBlocker4 = append(memory, "div", f"position:absolute;left:0;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{BUTTONS_START_X}px;height:{3 * BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
controllerBlocker5 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + 3 * BUTTON_WIDTH}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{CONTROLLER_A_X - 3 * BUTTON_WIDTH}px;height:{3 * BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
controllerBlocker6 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + CONTROLLER_A_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{SCREEN_WIDTH - BUTTONS_START_X - CONTROLLER_A_X}px;height:{CONTROLLER_A_Y}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
controllerBlocker7 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + CONTROLLER_A_X + BUTTON_WIDTH}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y + CONTROLLER_A_Y}px;width:{SCREEN_WIDTH - BUTTONS_START_X - CONTROLLER_A_X - BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
controllerBlocker8 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + CONTROLLER_A_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y + CONTROLLER_A_Y + BUTTON_HEIGHT}px;width:{SCREEN_WIDTH - BUTTONS_START_X - CONTROLLER_A_X}px;height:{2 * BUTTON_HEIGHT - CONTROLLER_A_Y}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")

cbCorner1 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
cbCorner2 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + 2 * BUTTON_WIDTH}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y}px;width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
cbCorner3 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y + 2 * BUTTON_HEIGHT}px;width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")
cbCorner4 = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X + 2 * BUTTON_WIDTH}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y + 2 * BUTTON_HEIGHT}px;width:{BUTTON_WIDTH}px;height:{BUTTON_HEIGHT}px;background:{BLOCKER_COLOR};opacity:{BLOCKER_OPACITY}")

screenBlocker = append(memory, "div", f"position:absolute;left:0;top:0;width:{SCREEN_WIDTH}px;height:{SCREEN_HEIGHT}px;background:transparent")
controller = append(memory, "div", f"position:absolute;left:{BUTTONS_START_X - CONTROLLER_MARGIN_X}px;top:{SCREEN_HEIGHT + BUTTONS_START_Y - CONTROLLER_MARGIN_Y}px;width:{CONTROLLER_IMG_WIDTH}px;height:{CONTROLLER_IMG_HEIGHT}px;background:no-repeat url('https://i.imgur.com/ukWSvMK.png');filter:drop-shadow(0px 0px 10px black);pointer-events:none;opacity:{BLOCKER_OPACITY}")

# cheater style tag, only used for debug! need to comment to post to cohost
if SHOW_OVERFLOW:
    append(mainContainer, "style", "position:absolute;", "details > summary { background: red } details[open] > summary { background: blue }")

ET.ElementTree(mainContainer).write("./zelda.html", encoding="unicode", method="html")
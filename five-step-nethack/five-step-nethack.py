from xml.etree import ElementTree as ET

FORCED_SHIFT = 0.25

# size of room containing player
GRID_WIDTH = 14
GRID_HEIGHT = 3

# top left tile of room
ROOM_START_X = 36
ROOM_START_Y = 15

# player start relative to top left corner of room (nonfunctional)
PLAYER_START_X = 0
PLAYER_START_Y = 0

MAX_DEPTH = 5

wrapper = ET.Element("div", attrib={"style": "display:flex;width:100%;flex-direction:column;align-items:center"})
stupidIntermediateContainer = ET.Element("div", attrib={"style": "overflow:hidden;position:relative;font-family:monospace;background:black;color:white;line-height:100%;min-width:59ch;min-height:22em"})
mainContainer = ET.Element("div", attrib={"style": "overflow:hidden;white-space:pre-wrap;position:absolute;inset:0"})

wrapper.append(stupidIntermediateContainer)
stupidIntermediateContainer.append(mainContainer)

mainContainer.text = '''Wizard needs food, badly!
 
  --------
  |.......#      ------    -----------
  |......|#      |....-####..........|
  |..<...|#      |....|   #|......>..|
  --------#      |....|    |.........|
          #      ----.-    ..........|
          ##         #     |.........|
          ##0        #     -|---------
          # #        ##     ########
          # #         #            ###########
        ### #         #                ######
        #---|---------.--            0##    #
        #|...............          ---------.------
        #-..............|          | .....%.......|
         |..............|          |..............|
         |...............          |..............|
         ----------------          ----------------
 
Eggbug the Evoker       St:11 Dx:12 Co:15 In:16 Wi:11 Ch:9
Dlvl:1  $:21 HP:11(11) Pw:7(7) AC:9 Exp:1 T:2046'''

mainContainer.text = mainContainer.text.replace(" ", " ")
#                                                ^    ^
#                                                |    |
#                                   ordinary space    no-break space

starvingText = ET.Element("div", attrib={"style": "position:absolute;background:red;color:white;font-weight:700;left:50ch;top:21em"})
starvingText.text = "Starving"
mainContainer.append(starvingText)

roomContainer = ET.Element("div", attrib={"style": f"transform-style:preserve-3d;position:absolute;width:{GRID_WIDTH}ch;height:{GRID_HEIGHT}em;left:{ROOM_START_X}ch;top:{ROOM_START_Y}em"})
mainContainer.append(roomContainer)

detailsBaseAttribs = {"style": "transform-style:preserve-3d;position:absolute"}
blockerDivBaseAttribs = {"style": "cursor:default;transform-style:preserve-3d;position:absolute;inset:-3em"}
summaryBaseAttribs = {"style": "cursor:pointer;transform-style:preserve-3d;position:absolute;list-style:none;background:black"}
spanBaseAttribs = {"style": "position:absolute;background:black"}

def makeAndAppendDetails(element, direction, zindex):
    detailsAttribs = detailsBaseAttribs.copy()
    detailsAttribs["style"] += f";left:{direction[0]}ch;top:{direction[1]}em;transform:translateZ({zindex}px)"
    details = ET.Element("details", attrib=detailsAttribs)
    element.append(details)
    return details

def makeAndAppendBlockerDiv(element, zindex):
    blockerDivAttribs = blockerDivBaseAttribs.copy()
    blockerDivAttribs["style"] += f";transform:translateZ({zindex}px)"
    blockerDiv = ET.Element("div", attrib=blockerDivAttribs)
    element.append(blockerDiv)

def makeAndAppendSummary(element, zindex):
    summaryAttribs = summaryBaseAttribs.copy()
    summaryAttribs["style"] += f";transform:translateZ({zindex}px)"
    summary = ET.Element("summary", attrib=summaryAttribs)
    summary.text = "."
    element.append(summary)

def makeAndAppendSpan(element, zindex, position=None):
    spanAttribs = spanBaseAttribs.copy()
    spanAttribs["style"] += f";color:black;background:white;transform:translateZ({zindex}px)"
    if position is not None:
        spanAttribs["style"] += f";left:{position[0]}ch;top:{position[1]}em"
    span = ET.Element("span", attrib=spanAttribs)
    span.text = "@"
    element.append(span)

def makeAndAppendBacktrackSpan(element, direction, zindex):
    backtrackSpanAttribs = spanBaseAttribs.copy()
    backtrackSpanAttribs["style"] += f";left:{-1 * direction[0]}ch;top:{-1 * direction[1]}em;transform:translateZ({zindex}px)"
    backtrackSpan = ET.Element("span", attrib=backtrackSpanAttribs)
    backtrackSpan.text = "."
    element.append(backtrackSpan)

def makeAndAppendDeathMessage(element, elmx, elmy):
    deathMsgAttribs = spanBaseAttribs.copy()
    deathMsgAttribs["style"] += f";left:{-elmx - ROOM_START_X}ch;top:{-elmy - ROOM_START_Y}em;white-space:pre"
    deathMsgSpan = ET.Element("span", attrib=deathMsgAttribs)
    deathMsgSpan.text = '''You die from starvation.--More--
                        '''
    element.append(deathMsgSpan)

def makeEndingScreen(element, elmx, elmy, depth, prevDirection):
    makeAndAppendBlockerDiv(element, 2 * depth + 2)
    makeAndAppendBacktrackSpan(element, prevDirection, 2 * depth + 1)
    makeAndAppendDeathMessage(element, elmx, elmy)

def makeAndAppendDirections(element, elmx, elmy, depth, prevDirection):
    if depth == 0:
        makeAndAppendSpan(element, 1, (0, 0))

    if depth >= MAX_DEPTH:
        makeEndingScreen(element, elmx, elmy, depth, prevDirection)
        return
    
    directions = []
    if elmx > 0:
        directions.append((-1, 0))
    if elmy > 0:
        directions.append((0, -1))
    if elmx < GRID_WIDTH - 1:
        directions.append((1, 0))
    if elmy < GRID_HEIGHT - 1:
        directions.append((0, 1))

    for direction in directions:
        nextDetails = makeAndAppendDetails(element, direction, depth + 2)
        makeAndAppendBlockerDiv(nextDetails, 2 * depth + 2)
        makeAndAppendSummary(nextDetails, 2 * depth + 1)
        makeAndAppendSpan(nextDetails, 2 * depth + 1)

        makeAndAppendDirections(nextDetails, elmx + direction[0], elmy + direction[1], depth + 1, direction)

makeAndAppendDirections(roomContainer, PLAYER_START_X, PLAYER_START_Y, 0, None)
ET.ElementTree(wrapper).write("test3.html", encoding="unicode", method="html")

# STRINGS USED FOR DEBUG:
'''mainContainer.text = 1izard needs food, badly!
2
3 --------
4 |.......#      ------    -----------
5 |......|#      |....-####..........|
6 |..?...|#      |....|   #|......?..|
7 --------#      |....|    |.........|
8         #      ----.-    ..........|
9         ##         #     |.........|
10        ##0        #     -|---------
11        # #        ##     ########
12        # #         #            ###########
13      ### #         #                ######
14      #---|---------.--            0##    #
15      #|...............          ---------.------
16      #-..............|          |@.............|
17       |..............|          |..............|
18       |...............          |..............|
19       ----------------          ----------------
20
21gbug the Evoker       St:11 Dx:12 Co:15 In:16 Wi:11 Ch:9
22vl:1  $:21 HP:11(11) Pw:7(7) AC:9 Exp:1 T:2046'''

'''mainContainer.text = 1234567890123456789012345678901234567890123456789012345678
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22'''
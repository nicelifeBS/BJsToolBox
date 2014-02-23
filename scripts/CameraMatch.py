#python

##---------------------------------------------------------##
#
#   Script to match a camera to a still image.
#   It uses two vanishing points to orient the camera.
#   
#   User has to define two x and two y axis in the image.
#   Each y axis has to be perpendicular to the x axis.
#
#   Bjoern Siegert
#   2014-02-18
##---------------------------------------------------------##

#from math import sqrt
import math

layerService = lx.Service("layerservice")
sceneService = lx.Service("sceneservice")
layerService.select("layer", "main")

arg = lx.arg()

def vertList():
    """
    Creates a dictionary with two vertex pairs.
    {0:[(0.2,0.1,0.0),(-2.0,0.2,0.0)]}
    """
    layerService.select("edges","all")
    numEdge = layerService.query("edge.N")
    verts_list = {}
    key = 0
    for edge in xrange(numEdge):
        layerService.select("edge.name", str(edge))
        if layerService.query("edge.selected"):
            verts = layerService.query("edge.vertList")
            edgeIndex = layerService.query("edge.index")
            lx.out("verts: ", verts)
            
            layerService.select("vert.index", str(verts[0]))
            A = layerService.query("vert.pos")
            
            layerService.select("vert.index", str(verts[1]))
            B = layerService.query("vert.pos")
            
            verts_list[key] = [A,B]
            verts_list["edge_%s" %key] = edgeIndex
            
            key = key + 1
    
    lx.out(verts_list.keys())

    return verts_list

def lowestEdge(vertList):
    """
    return the lowest edge. "0" for edge0 "1" for edge1
    """
    edge1 = vertList["edge_0"]
    edge2 = vertList["edge_1"]
    
    layerService.select("edge", str(edge1))
    edge1Pos = layerService.query("edge.pos")
    
    layerService.select("edge", str(edge2))
    edge2Pos = layerService.query("edge.pos")
    
    # Compare the y coordinate of the two edges
    if edge1Pos[1] < edge2Pos[1]:
        return 0
    else:
        return 1
    
# Allgemeine Geradenschnitt funktion machen! -> lineA, lineB als input.
def vanPoint(line1,line2):
    """
    Returns a vanish point of two not parallel lines. A dictionary with four points must be given.
    Basic formular:
        line1   =   line2
          |           |
    Am * x + An = Bm * x + An
    """
    # Points of line A
    Ax1 = float(line1[0][0])
    Ay1 = float(line1[0][1])
    Ax2 = float(line1[1][0])
    Ay2 = float(line1[1][1])
        
    # Points of line B
    Bx1 = float(line2[0][0])
    By1 = float(line2[0][1])
    Bx2 = float(line2[1][0])
    By2 = float(line2[1][1])
    
    # slope and y-intercept of line A
    An = Ay1 - Ax1 * (Ay2 - Ay1) / (Ax2 - Ax1)
    Am = (Ay2 - Ay1) / (Ax2 - Ax1)
    
    # slope and y-intercept of line B
    Bn = By1 - Bx1 * (By2 - By1) / (Bx2 - Bx1)
    Bm = (By2 - By1) / (Bx2 - Bx1)
    
    # Intersection point of line A and B
    x = (An - Bn) / (Bm - Am)
    y = Am * x + An
    
    return x,y

def backdropSize(backdropID):    
    # select backdrop item
    sceneService.select("item", str(backdropID))
    lx.eval("select.subItem %s set mesh" %backdropID) # select item in scene to use "backdrop.edit ?"

    # Here we look up the clip of the backdrop item and find its pixel dimensions
    # We iterate though the clips and if we find the the matching ID the width and height is saved
    clipID = lx.eval("backdrop.edit ?")
    sceneService.select("clip", str(clipID))
    clipNum = layerService.query("clip.N")
    for clip in xrange(clipNum):
        layerService.select("clip",str(clip))
        if layerService.query("clip.id") == clipID:
            clipInfo = layerService.query("clip.info").split(" ") # clipInfo = ['RGB', 'w:3456', 'h:5184', 'bpp:32', 'pa: 1']
            
            # Width and height of image
            pixelWidth = int(clipInfo[1][2:])
            pixelHeight = int(clipInfo[2][2:])
            break
        else:
            lx.out("No clip found for backdrop: %s" %backdropID)
    
    # Get the pixel size value of the backdrop
    pixelSize = lx.eval("channel.value ? channel:{%s:pixelSize}" %backdropID)
    
    ## Actual width and height of the backdrop
    backdropWidth = pixelSize * pixelWidth
    backdropHeight = pixelSize * pixelHeight
    
    return backdropWidth, backdropHeight

def createDummy(FD, backdropSize, xm, M):
    """
    Creates the vanish points as vertecies. Only for Debugging
    """
    lx.eval("item.create mesh DEBUG")
    
    VP_01 = lx.eval("user.value xAxisVP ?").split(";")
    VP_02 = lx.eval("user.value yAxisVP ?").split(";")
    
    # Create vanish point 01
    lx.eval("tool.set prim.makeVertex on 0")
    lx.eval("tool.attr prim.makeVertex cenX %s" %VP_01[0])
    lx.eval("tool.attr prim.makeVertex cenY %s" %VP_01[1])
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Create vanish point 02
    lx.eval("tool.attr prim.makeVertex cenX %s" %VP_02[0])
    lx.eval("tool.attr prim.makeVertex cenY %s" %VP_02[1])
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Create distance between VPs
    lx.eval("tool.attr prim.makeVertex cenX %s" %VP_01[0])
    lx.eval("tool.attr prim.makeVertex cenY 0")
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    lx.eval("tool.attr prim.makeVertex cenX %s" %VP_02[0])
    lx.eval("tool.attr prim.makeVertex cenY 0")
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Create Focal Distance point
    lx.eval("tool.attr prim.makeVertex cenX 0")
    lx.eval("tool.attr prim.makeVertex cenY %s" %FD)
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Create Focal Distance point
    lx.eval("tool.attr prim.makeVertex cenX %s" %xm)
    lx.eval("tool.attr prim.makeVertex cenY 0")
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Create Mid Point of FD
    lx.eval("tool.attr prim.makeVertex cenX %s" %M[0])
    lx.eval("tool.attr prim.makeVertex cenY %s" %M[1])
    lx.eval("tool.attr prim.makeVertex cenZ 0")
    lx.eval("tool.doApply")
    
    # Drop the tool
    lx.eval("tool.set prim.makeVertex flush 0")
    
    # Create backdrop dimensions
    lx.eval("tool.set prim.cube on")
    lx.eval("tool.reset prim.cube")
    lx.eval("tool.setAttr prim.cube segmentsX 2")
    lx.eval("tool.setAttr prim.cube segmentsY 2")
    lx.eval("tool.attr prim.cube sizeX %s" %backdropSize[0])
    lx.eval("tool.attr prim.cube sizeY %s" %backdropSize[1])
    lx.eval("tool.attr prim.cube sizeZ 0")
    lx.eval("tool.apply")
    lx.eval("tool.set prim.cube off 0")


def tanAlpha(a,b):
    """
    Return the angle alpha of a right triangle in degrees. Legs a and b must be given
    """
    return math.degrees(math.atan(a / b))


def focalLength(a,d):
    """
    Returns the focal length
    a = angle of view
    d = film width
    """
    return 1/2 * d * (1 / math.tan(a/2))

def userValueTemp(userValueName, value):
    """
    Create a temporary uservalue with the "userValueName" and the "value"
    Check if user value already exists.
    """
    if lx.eval("query scriptsysservice userValue.isDefined ? %s" %userValueName):
        lx.eval("user.value %s {%s}" %(userValueName, value))
    else:
        lx.eval("user.defNew %s string temporary" %userValueName)
        lx.eval("user.value %s {%s}" %(userValueName, value))
        
def convert2list(string):
    """Converts strings like that '(1,2,3)' to proper lists ['1','2','3']"""
    new_list = ""
    
    for i in string:
        
        # Check if no '(' or ')' is in string
        if i not in '()':
            new_list += i
    
    return new_list.split(',')

def scalar(vector01,vector02):
    """
    Return the scalar product of two vectors(vector01, vector02)
    """
    x = vector01[1]*vector02[2] - vector01[2]*vector02[1]
    y = vector01[2]*vector02[0] - vector01[0]*vector02[2]
    z = vector01[0]*vector02[1] - vector01[1]*vector02[0]
    
    return x,y,z

    
if arg == "createBackdrop":
    lx.eval("view3d.projection fnt")
    lx.eval("item.create backdrop")
    
    # Save the backdrop id as a user value
    sceneService.select("selection", "backdrop")
    backdropID = sceneService.query("selection")
    if lx.eval("query scriptsysservice userValue.isDefined ? backdropID"):
        lx.eval("user.value backdropID {%s}" %backdropID)
    else:
        lx.eval("user.defNew backdropID string temporary")
        lx.eval("user.value backdropID {%s}" %backdropID)
    lx.out("user value saved")
    
    # Load an image
    lx.eval("clip.load")
    sceneService.select("selection", "videoStill") # Select the created clip
    clipName = sceneService.query("selection")
    lx.eval("backdrop.edit {%s}" %clipName) # Load imported image into backdrop
    
    # Create mesh layer
    lx.eval("item.create mesh CameraMatch_AXIS")

if arg == "xAxis":
    # Save vanish point of X Axis
    # Values are stored in a temporary user value x and y are separated by ";"
    xy_coordinates = vanPoint(vertList()[0],vertList()[1])
    if lx.eval("query scriptsysservice userValue.isDefined ? xAxisVP"):
        lx.eval("user.value xAxisVP {%s;%s}" %(xy_coordinates[0],xy_coordinates[1]))
    else:
        lx.eval("user.defNew xAxisVP string temporary")
        lx.eval("user.value xAxisVP {%s;%s}" %(xy_coordinates[0],xy_coordinates[1]))
        
    # Save points of lowest edge for the ground plane
    if lowestEdge(vertList()) == 0:
        userValueTemp("ground_xAxis", str(vertList()[0][0]) + ";" + str(vertList()[0][1]))
    else:
        userValueTemp("ground_xAxis", str(vertList()[1][0]) + ";" + str(vertList()[1][1]))


if arg == "yAxis":
    # Save vanish point of Y Axis
    # Values are stored in a temporary user value x and y are separated by ";"
    xy_coordinates = vanPoint(vertList()[0],vertList()[1])
    if lx.eval("query scriptsysservice userValue.isDefined ? yAxisVP"):
        lx.eval("user.value yAxisVP {%s;%s}" %(xy_coordinates[0],xy_coordinates[1]))
    else:
        lx.eval("user.defNew yAxisVP string temporary")
        lx.eval("user.value yAxisVP {%s;%s}" %(xy_coordinates[0],xy_coordinates[1]))

    # Save points of lowest edge for the ground plane
    if lowestEdge(vertList()) == 0:
        userValueTemp("ground_yAxis", str(vertList()[0][0]) + ";" + str(vertList()[0][1]))
    else:
        userValueTemp("ground_yAxis", str(vertList()[1][0]) + ";" + str(vertList()[1][1]))


if arg == "calcCam":
    ## Backdrop
    backdropWith = backdropSize(lx.eval("user.value backdropID ?"))[0]
    backdropHeight = backdropSize(lx.eval("user.value backdropID ?"))[1]
    
    ## Vanish Points X-Axis
    VPx1 = float(lx.eval("user.value xAxisVP ?").split(";")[0])
    VPy1 = float(lx.eval("user.value xAxisVP ?").split(";")[1])
    
    ## Vanish Points Y-Axis
    VPx2 = float(lx.eval("user.value yAxisVP ?").split(";")[0])
    VPy2 = float(lx.eval("user.value yAxisVP ?").split(";")[1])


    # Define left and right vanish point
    # VPL and VPR
    VP1 = float(lx.eval("user.value xAxisVP ?").split(";")[0]), float(lx.eval("user.value xAxisVP ?").split(";")[1])
    VP2 = float(lx.eval("user.value yAxisVP ?").split(";")[0]), float(lx.eval("user.value yAxisVP ?").split(";")[1])

    if VP1 < VP2:
        VPL = VP1
        VPR = VP2
        lx.out("VP1 < VP2")
    else:
        VPL = VP2
        VPR = VP1
        lx.out("VP1 > VP2")
    
    lx.out("VPR: ", VPR)
    lx.out("VPL: ", VPL)
    
    ## Distance between the two vanish points
    VPD = abs(VPR[0] - VPL[0])
    
    ## Evaluate midpoint x coordinate of VPD
    #xm = VPL[0] + VPD/2
    xm = (VPL[0] + VPR[0])/2
    
    M = ((VPR[0] - VPL[0])/2) + VPL[0], ((VPR[1] - VPL[1])/2) + VPL[1]

    # c = sqrt(a^2 + b^2)
    M_length = math.sqrt((M[1]-VPL[1])**2 + (M[0]-VPL[0])**2)
    
    ## Focal distance FD
    # Intersection point on Y axis
    # y = 1/2 sqrt(VPD^2 - 4*(VPD/2)^2)
    FD = math.sqrt((VPD/2)**2-xm**2)
    
    ## Angle of View horizontally
    AoV_hor = 2*tanAlpha(backdropWith/2, FD)
    
    ## Angle of View vertically
    AoV_ver = 2*tanAlpha(backdropHeight/2, FD)
    
    ## camera roll angle value
    camRoll = tanAlpha(VPy2-VPy1,VPD)
    
    ## camera tilt value
    horizonHeight = VPy1 - VPx1 * ((VPy2-VPy1)/(VPx2-VPx1))
    camTilt =  - tanAlpha(horizonHeight,FD)
    
    ## camera pan
    edge1 = []
    edge2 = []
    
    for i in lx.eval("user.value ground_xAxis ?").split(";"):
        edge1.append(convert2list(i))
        
    for i in lx.eval("user.value ground_yAxis ?").split(";"):
        edge2.append(convert2list(i))        
    # edge = [(x1,y1),(x2,y2)]
    
    lx.out("edge1: ", edge1)
    lx.out("edge2: ", edge2)
    
    
    """NOPE"""
    # n = y1 - [(y2-y1)/(x2-x1)]*x1
    origin = (0,float(edge1[0][1])-((float(edge1[1][1])-float(edge1[0][1]))/(float(edge1[1][0])-float(edge1[0][0])))*float(edge1[0][0]))
    camHMid = (0,VPL[1] - ((VPR[1]-VPL[1])/(VPR[0]-VPL[0]))*VPL[0])
    
    
    b_length = math.sqrt((camHMid[0] - VPL[0])**2 + (camHMid[1] - VPL[1])**2)
    c_length = math.sqrt((origin[0] - VPL[0])**2 + (origin[1] - VPL[1])**2)
    
    camPan = 90 - math.degrees(math.acos(b_length/c_length))
    """NOPE END"""
    ###### Debugging ######
    lx.out("VPD: ", VPD)
    lx.out("xm: ", xm)
    lx.out("FD: ", FD)
    lx.out("AoV_hor: ",AoV_hor)
    lx.out("AoV_ver: ",AoV_ver)
    lx.out("M: ",M)
    lx.out("origin: ", origin)
    lx.out("camHmid: ", camHMid)
    lx.out("M_length: ", M_length)
    lx.out("b: ", b_length)
    lx.out("c: ", c_length)
    lx.out("a = ", M[1]-VPL[1])
    lx.out("b = ", M[0]-VPL[0])
    
    
    
    lx.out("camPan: ", camPan)
    #lx.out("roll value: ", camRoll)
    #lx.out("camTilt: ", camTilt)
    #######################
    
    ## Debugging ##
    # Create dummy geometry for debugging
    """
    ## Create camera
    lx.eval("item.create camera")
    lx.eval("item.name CamMatch camera")
    lx.eval("transform.channel rot.X %s" %camTilt)
    lx.eval("transform.channel rot.Y %s" %camPan)
    lx.eval("transform.channel rot.Z %s" %camRoll)
    
    filmBack_X = lx.eval("item.channel apertureX ?")
    filmBack_Y = lx.eval("item.channel apertureY ?")
    
    if AoV_ver < AoV_hor:
        lx.eval("camera.hfov %s" %AoV_hor)
    else:
        # switching filmback values
        lx.eval("item.channel apertureX %s" %filmBack_Y)
        lx.eval("item.channel apertureY %s" %filmBack_X)
        lx.eval("camera.hfov %s" %AoV_ver)
    """
    ## Create camera END
    
    
    
    createDummy(FD, backdropSize(lx.eval("user.value backdropID ?")), xm, M)



"""    
if arg == "backdrop":
    # save the backdrop id as a user value
    sceneService.select("selection", "backdrop")
    backdropID = sceneService.query("selection")
    
    if not backdropID:
        lx.out("Please select a backdrop item")
    else:    
        if lx.eval("query scriptsysservice userValue.isDefined ? backdropID"):
            lx.eval("user.value backdropID {%s}" %backdropID)
        else:
            lx.eval("user.defNew backdropID string temporary")
            lx.eval("user.value backdropID {%s}" %backdropID)
        lx.out("user value saved")
    
"""
"""
list = sceneService.query("item")
for i in list:
    try:
        lx.out(i," : ",sceneService.query(str(i)))
    except:
        pass
"""    

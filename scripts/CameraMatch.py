#python

##------------------------------------------------------##
#         Camera Match
#   Matching a camera of an image using
#   two vanish points.
#   User has to draw two edge bundles which
#   resemble the x and the y axis.
#   The image must not be cropped. Otherwise
#   it is not possible to derive the focal length
#
#   Author: Bjoern Siegert 2014-03-16
#
##------------------------------------------------------##


import math

class vector(object):
    """vector([x,y,z]) -> create a vector object in 3D space."""
    def __init__(self, data):
        self.data = data
        if len(self.data) != 3:
           raise ValueError("Expecting a 3D vector -> [x,y,z]")
    
    def __repr__(self):
        return repr(self.data)
    
    def __getitem__(self, index):
        """vector[i] -> return the value of the given index i"""
        return self.data[index]
    
    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        data = []
        for i in range(len(self.data)):
            data.append(self.data[i] + other.data[i])
        return vector(data)

    def __sub__(self, other):
        data = []
        for i in range(len(self.data)):
            data.append(self.data[i] - other.data[i])
        return vector(data)
    
    def __mul__(self, other):
        data = []
        try:
            for i in range(len(self.data)):
                data.append(self.data[i] * other.data[i])
        
        except AttributeError:
            for i in range(len(self.data)):
                data.append(self.data[i] * other)
                
        return vector(data)
    
    def __div__(self, other):
        data = []
        try:
            for i in range(len(self.data)):
                data.append(self.data[i] / other.data[i])
        except AttributeError:
            for i in range(len(self.data)):
                data.append(self.data[i] / other)
        
        return vector(data)
    
    def __floordiv__(self, other):
        data = []
        try:
            for i in range(len(self.data)):
                data.append(self.data[i] // other.data[i])
        except AttributeError:
            for i in range(len(self.data)):
                data.append(self.data[i] // other)
        
        return vector(data)
        
    def __pow__(self, power):
        data = []
        for i in range(len(self.data)):
            data.append(self.data[i]**power)
        return vector(data)

### Functions ###   
def cross(vector01, vector02):
    """Cross product of two vectors"""
    data = []
    try:                
        if len(vector01) == len(vector02) and len(vector01) == 3:
            x = vector01[1]*vector02[2] - vector01[2]*vector02[1]
            y = vector01[2]*vector02[0] - vector01[0]*vector02[2]
            z = vector01[0]*vector02[1] - vector01[1]*vector02[0]
            return vector([x,y,z])
        else:
            pass
    
    except AttributeError:
        for i in range(len(vector01)):
            data.append(vector01[i] * other)
        return vector(data)

def dot(vector01, vector02):
    """vector01.dot(vector02) -> return the dot product of two vectors"""
    data = []
    for i in range(len(vector01)):
        data.append(vector01[i] * vector02[i])
    return sum(data)

def normalize(vector01):
    """normalized vector/ unit vector"""
    return vector01/length(vector01)

def length(vector01):
    """return the length of a vector"""
    return math.sqrt(vector01.data[0]**2 + vector01.data[1]**2 + vector01.data[2]**2)

def angle(vector01, vector02):
    """Angle between two vectors in degrees"""
    return math.degrees(math.acos(dot(vector01, vector02) / (length(vector01) * length(vector02))))

def sqrt(vector01):
    data = []
    for i in range(len(vector01)):
        data.append(math.sqrt(vector01[i]))
    return vector(data)


#------- LINE MATH --------#
# Line intersection in 2D space
def lineIntersect(line1,line2):
    """
    Returns the line-line intersection point of two not parallel lines in 2D space (X,Y).
    Expects two lines with following format: line = [[1,2,3],[1,2,3]]
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
    
    return [x,y]

def lineNM(point01, point02):
    """return y-intercept 'n' and slope 'm'"""
    x1 = float(point01[0])
    y1 = float(point01[1])
    x2 = float(point02[0])
    y2 = float(point02[1])

    n = y1 - ((y2 - y1) / (x2 - x1)) * x1
    m = (y2 - y1) / (x2 - x1)
    
    return [n,m]
     
def angleAlpha(a,b,c):
    """Return the angle alpha of a right triangle. Two side lengths must be given the third must be defined as None -> angleAlpha(3.4,None,5.3)"""
    if a == None:
        return math.degrees(math.acos(b / c))
    
    elif b == None:
        return math.degrees(math.asin(a / c))
        
    elif c == None:
        return math.degrees(math.atan(a / b))
    
def midPoint(point01, point02):
    """Mid point between two points"""
    return [(point01[0]+point02[0])/2,(point01[1]+point02[1])/2]
    
#--- Photogrammetry Stuff ---#
def focalDistance(VPL,VPR):
    """Calculate the focal distance of the camera. Two vanish point as input."""
    Fu = VPR
    Fv = VPL
    Puv = vector([0,lineNM(VPL,VPR)[0],0])
    
    PPuv = Puv
    FvPuv = Puv - Fv
    PuvFu = Fu - Puv
    
    OPuv = sqrt(FvPuv*PuvFu)
    
    OP = sqrt(OPuv**2 + PPuv**2)
    
    return [0,length(OP)]
    
###-------- modo stuff -----------###

## modo methods START ##

def warning_msg(name):
    """A modal warning dialog. Message text can be set through name var."""
    try:
        lx.eval("dialog.setup warning")
        lx.eval("dialog.title {Error}")
        lx.eval("dialog.msg {%s}" %name)
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
    except RuntimeError:
        pass

def vertList():
    """
    Creates a dictionary for each edge with two vertex pairs.
    {0:[[0.2,0.1,0.0],[-2.0,0.2,0.0]]}
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
            
            layerService.select("vert.index", str(verts[0]))
            A = list(layerService.query("vert.pos"))
            
            layerService.select("vert.index", str(verts[1]))
            B = list(layerService.query("vert.pos"))
            
            verts_list[key] = [A,B]
            verts_list["edge_%s" %key] = edgeIndex
            
            key = key + 1
    
    lx.out(verts_list["edge_0"])
    lx.out(verts_list["edge_1"])

    return verts_list

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

def backdropSize(backdropID):
    """Extract the actual image size based on the pixel ration of a backdrop item.
    backdropSize[backdropWidth, backdropHeight, aspectRatio, pixelWidth, pixelHeight]"""
    # select backdrop item
    sceneService.select("item", str(backdropID))
    lx.eval("select.subItem %s set mesh" %backdropID) # select item in scene to use "backdrop.edit ?"

    # Here we look up the clip of the backdrop item and find its pixel dimensions
    # We iterate though the clips and if we find the the matching ID the width and height is saved
    clipID = lx.eval("backdrop.edit ?")
    sceneService.select("clip", str(clipID))
    clipNum = layerService.query("clip.N")
    for clip in xrange(clipNum):
        layerService.select("clip.id", str(clip))
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
    aspectRatio = float(pixelWidth) / float(pixelHeight)
    return backdropWidth, backdropHeight, aspectRatio, pixelWidth, pixelHeight

def create3Dpoint(value):
    """Creates a 3D point list [x,y,z]
    Splits value with ';' and adds z with 0 if len is 2 """
    data = []
    for i in value:
        data.append(float(i))
    if len(data) == 2:
        data.append(0)
    else:
        pass
    
    return data

def convert2list(string):
    """Converts strings like that '(1,2,3)' to proper lists ['1','2','3']"""
    new_list = ""
    
    for i in string:
        
        # Check if no '(' or ')' is in string
        if i not in '()' and i not in '[]':
            new_list += i
            
    return new_list.split(',')

## modo methods END ##

## modo Services ##
layerService = lx.Service("layerservice")
sceneService = lx.Service("sceneservice")
arg = lx.arg()

# Select activ mesh layer
layerService.select("layer", "main")

## Arguments ##
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
    lx.out("user value saved: ", backdropID)
    
    # Load an image
    lx.eval("clip.load")
    sceneService.select("selection", "videoStill") # Select the created clip
    clipName = sceneService.query("selection")
    lx.eval("backdrop.edit {%s}" %clipName) # Load imported image into backdrop
    
    # Create mesh layer
    lx.eval("item.create mesh CameraMatch_AXIS")

elif arg == "xAxis":
    # Save vanish point of X Axis
    # Values are stored in a temporary user value x and y are separated by ";"
    try:
        pointList = vertList()
    except:
        warning_msg("Please select two edges to calculate the vanish point.")
    else:
        xy_coordinates = lineIntersect(pointList[0],pointList[1])
        userValueTemp("xAxisVP", str(xy_coordinates[0]) + ";" + str(xy_coordinates[1])) # Save vanish point in a user variable
        
elif arg == "yAxis":
    # Save vanish point of Y Axis
    # Values are stored in a temporary user value x and y are separated by ";"
    try:
        pointList = vertList()
    except:
        warning_msg("Please select two edges to calculate the vanish point.")
    else:
        xy_coordinates = lineIntersect(pointList[0],pointList[1])
        userValueTemp("yAxisVP", str(xy_coordinates[0]) + ";" + str(xy_coordinates[1])) # Save vanish point in a user variable

elif arg == "createCamera":
    # Check if all necessary variables are there
    if not lx.eval("query scriptsysservice userValue.isDefined ? backdropID"):
        warning_msg("Please load an image first.")
        
    elif not lx.eval("query scriptsysservice userValue.isDefined ? xAxisVP"):
        warning_msg("Please set the first vanish point.")
    
    elif not lx.eval("query scriptsysservice userValue.isDefined ? yAxisVP"):
        warning_msg("Please set the second vanish point.")
    
    else:
        backdropWidth = backdropSize(lx.eval("user.value backdropID ?"))[0]
        backdropHeight = backdropSize(lx.eval("user.value backdropID ?"))[1]
        backdropPixelWidth = backdropSize(lx.eval("user.value backdropID ?"))[3]
        backdropPixelHeight = backdropSize(lx.eval("user.value backdropID ?"))[4]
        
        # Vanish points
        VP1 = create3Dpoint(lx.eval("user.value xAxisVP ?").split(";"))
        VP2 = create3Dpoint(lx.eval("user.value yAxisVP ?").split(";"))
    
        # Check the order of the two vanish points
        # and assign them to left vanish point: VPL or right vanis point: VPR
        # Points are also converted to a vector with vector()
        if VP1 < VP2:
            VPL = vector(VP1)
            VPR = vector(VP2)
            #lx.out("VP1 < VP2")
        else:
            VPL = vector(VP2)
            VPR = vector(VP1)
            #lx.out("VP1 > VP2")
        
        ## FocalDistance ##
        FD = focalDistance(VPL, VPR)
        lx.out("focal distance: ", FD)
        
        ## Angle of View ##
        AoV_hor = 2*angleAlpha(backdropWidth / 2, FD[1], None)
        AoV_ver = 2*angleAlpha(backdropHeight / 2, FD[1], None)
        
        ## Camera Orientation ##
        O = vector([0,0,FD[1]])
        Fu = VPR
        Fv = VPL
        
        OFu = Fu - O
        OFv = Fv - O
        
        s1 = length(OFu)
        s2 = length(OFv)
        
        upRc = normalize(OFu)
        vpRc = normalize(OFv)
        wpRc = cross(upRc,vpRc)
        
        ## Create camera orientation as verticies ##
        lx.eval("item.create mesh camMatchOrientation")
        
        # Get the ID of the created mesh
        sceneService.select("selection", "mesh")
        camMatchMesh = sceneService.query("selection")
        
        lx.eval("tool.set prim.makeVertex on 0")
        
        # Create upRc
        lx.eval("tool.attr prim.makeVertex cenX %s" %upRc[0])
        lx.eval("tool.attr prim.makeVertex cenY %s" %upRc[1])
        lx.eval("tool.attr prim.makeVertex cenZ %s" %upRc[2])
        lx.eval("tool.doApply")
        
        # Create Origin
        lx.eval("tool.attr prim.makeVertex cenX 0")
        lx.eval("tool.attr prim.makeVertex cenY 0")
        lx.eval("tool.attr prim.makeVertex cenZ 0")
        lx.eval("tool.doApply")
        
        # Create vpRc
        lx.eval("tool.attr prim.makeVertex cenX %s" %vpRc[0])
        lx.eval("tool.attr prim.makeVertex cenY %s" %vpRc[1])
        lx.eval("tool.attr prim.makeVertex cenZ %s" %vpRc[2])
        lx.eval("tool.doApply")
        
        # Switch off make verticies
        lx.eval("tool.set prim.makeVertex off 0")
        
        
        ##-------------------- ORIENT THE WORKPLANE ------------------------##
        ## The workplane is oriented to the three "bottom" vertex points.   ##
        ## The middle vertex is the "origin" of the workplane               ##
        ##------------------------------------------------------------------##
        
        layerService.select("layer", "main")
        layer = layerService.query("layer.index")
        layerService.select("verts", "all")
        numVerts = layerService.query("vert.N")
        lx.eval("select.typeFrom vertex;edge;polygon;item;pivot;center;ptag true")
        lx.eval("select.drop vertex")
        
        for i in range(numVerts):
            lx.eval("select.element %s vertex add %s" %(layer, i))
        lx.eval("workPlane.fitSelect")
        
        ## Extract rotation values from the workplane ##
        rotX = math.degrees(lx.eval("workPlane.edit rotX:?"))
        rotY = math.degrees(lx.eval("workPlane.edit rotY:?"))
        rotZ = math.degrees(lx.eval("workPlane.edit rotZ:?"))
        lx.eval("workPlane.reset")
        
        ## Fix UP orientation of the rotZ values ##
        if rotZ > 90:
            rotZ = 180 - rotZ
        elif rotZ < -90:
            rotZ = -(rotZ + 180)
        else:
            pass
        
        ##------------------------------##
        ##         CREATE CAMERA        ##
        ##------------------------------##
        
        lx.eval("select.drop item {}")

        lx.eval("item.create camera")
        lx.eval("item.name CamMatch camera")
        lx.eval("transform.channel rot.X %s" %rotX)
        lx.eval("transform.channel rot.Y %s" %rotY)
        lx.eval("transform.channel rot.Z %s" %rotZ)
        lx.eval("transform.channel pos.Y 2.0") # default height of 2 meters
        
        # Set the film back of the camera to the aspect ratio of the backdrop image.
        filmBack_X = lx.eval("item.channel apertureX ?") * backdropSize(lx.eval("user.value backdropID ?"))[2]
        filmBack_Y = lx.eval("item.channel apertureY ?") * backdropSize(lx.eval("user.value backdropID ?"))[2]
        
        ## Check if the image is horizontally or vertically
        ## If it is vertically the filmBack values must be switched
        if AoV_ver < AoV_hor:
            lx.eval("item.channel apertureX %s" %filmBack_X)
            lx.eval("item.channel apertureY %s" %filmBack_Y)
        else:
            # switching filmback values
            lx.eval("item.channel apertureX %s" %filmBack_Y)
            lx.eval("item.channel apertureY %s" %filmBack_X)
        
        ## Apply the angle of view to the camera ##
        ## IMPORTANT: Must happen after the filmback is set!
        lx.eval("camera.hfov %s" %AoV_hor)
        
        
        ##------------------------------------##
        ## Lock Rotation values of the camera ##
        ##------------------------------------##
        
        if lx.eval("user.value BJsToolbox_cameraLock ?") == True:
            cameraName = lx.eval("item.name ? camera")
            sceneService.select("selection", "camera")
            cameraID = sceneService.select("item.id", sceneService.query("selection"))
            #lx.eval("select.subItem %s set mesh" %cameraID)
            camRotChannelName = sceneService.query("item.xfrmRot")
            
            # Select Rotation Channels
            lx.eval("select.channel {%s:rot.X} set" %camRotChannelName)
            lx.eval("select.channel {%s:rot.Y} add" %camRotChannelName)
            lx.eval("select.channel {%s:rot.Z} add" %camRotChannelName)
            
            # Create group with selected channels and lock it
            lx.eval("group.create %s_GRP mode:selChans" %cameraName)
            lx.eval("item.channel group$lock on")
            
            lx.out("Camera Locked")
        else:
            pass
        
        
        ##------------------------------##
        ##          SCENE SETUP         ##
        ##------------------------------##
        
        # Change viewer to camera
        lx.eval("view3d.projection cam")
        
        # Change backdrop mode to camera
        lx.eval("select.subItem %s set mesh" %lx.eval("user.value backdropID ?"))
        lx.eval("item.channel backdrop$projection camera")
        
        # Change render resolution to backdrop image
        sceneService.select("item.N", "all")
        numItems = sceneService.query("item.N")
        
        for i in range(numItems):
            sceneService.select("item.type", str(i))
            if sceneService.query("item.type") == "polyRender":
                lx.out("Render Item: ", sceneService.query("item.id"))
                lx.eval("select.subItem %s set" %sceneService.query("item.id"))
                break
        
        lx.eval("render.res 0 %s" %backdropPixelWidth)
        lx.eval("render.res 1 %s"%backdropPixelHeight)
        
        
        ##------------------------------##
        ##          SCENE CLEANUP       ##
        ##------------------------------##
    
        lx.eval("select.item %s" %camMatchMesh)
        lx.eval("item.delete")
        
        ###---- LOGGING ----##
        #lx.out("AoV horizontal: ", AoV_hor)
        #lx.out("AoV vertical: ", AoV_ver)
        #lx.out("Left Vanish Point: ", VPL)
        #lx.out("Right Vanish Point: ", VPR)
        #lx.out("backdrop info: ", backdropSize(lx.eval("user.value backdropID ?")))
        #lx.out("Camera Rotation X: ", rotX)
        #lx.out("Camera Rotation Y: ", rotY)
        #lx.out("Camera Rotation Z: ", rotZ)
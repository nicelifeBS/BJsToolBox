#python

"""
Create Threads v1.1

Script creates an inner or an outer thread. The thread profile is hard coded in the function profileInner() and profileOuter().
Script has 

Script was inspired by the modelling techniques of Peter Stammbach

Bjoern Siegert aka nicelife

Last edit:
29.11.2013
"""


import math

class vector_class(object):
    """ Let's you do math with vectors in a list"""
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return repr(self.data)
    
    def __add__(self, other):
        data = [] #start with an empty list
        for i in range(len(self.data)):
            data.append(self.data[i] + other.data[i])
        return vector_class(data)
    
    def __sub__(self, other):
        data = [] #start with an empty list
        for i in range(len(self.data)):
            data.append(self.data[i] - other.data[i])
        return vector_class(data)
    
    def __mul__(self, other):
        data = [] #start with an empty list
        for i in range(len(self.data)):
            data.append(self.data[i] * other.data[i])
        return vector_class(data)
    
    def __div__(self, other):
        data = [] #start with an empty list
        for i in range(len(self.data)):
            data.append(self.data[i] / other.data[i])
        return vector_class(data)
    
    def __getitem__(self, key):
        return self.data[key]

    
### FUNCTIONS ####
def checkExistence(itemList, name):
    if name in itemList:
        return True
    else:
        return False

def createMesh(itemList, name):
    """Create a mesh layer with a name. If mesh already exists all polys will be deleted."""
    if checkExistence(itemList, name) == False:
        lx.eval("item.create mesh {%s}" %name)
    elif checkExistence(itemList, name) == True:
        lx.eval("select.item {%s} set mesh" %name)
        lx.eval("select.typeFrom polygon true")
        lx.eval("delete")  
    else:
        pass

def profileInner():
    """Creates a profile poly for an inner side of a thread"""
    layer_index = lx.eval("query layerservice layer.index ? selected")
    # create a cube 
    lx.eval("tool.set prim.cube on")
    lx.eval("tool.reset prim.cube")
    lx.eval("tool.attr prim.cube cenX 0.0")
    lx.eval("tool.attr prim.cube cenY 0.0")
    lx.eval("tool.attr prim.cube cenZ 0.0")
    lx.eval("tool.attr prim.cube sizeX 0.001")
    lx.eval("tool.attr prim.cube sizeY 0.005")
    lx.eval("tool.attr prim.cube sizeZ 0.0")
    lx.eval("tool.apply")
    lx.eval("tool.set prim.cube off 0")
    
    # modify the cube to a thread profile
    lx.eval("select.typeFrom edge true")
    
    lx.eval("select.element %s edge set 2 3" %layer_index)
    lx.eval("tool.set edge.extend on")
    lx.eval("tool.reset edge.extend")
    lx.eval("tool.setAttr edge.extend offX 0.005")
    lx.eval("tool.setAttr edge.extend offY 0.0")
    lx.eval("tool.setAttr edge.extend offZ 0.0")
    lx.eval("tool.doApply")
    lx.eval("tool.set edge.extend off 0")
    
    lx.eval("select.element %s edge set 4 5" %layer_index)
    lx.eval("tool.set TransformScale on")
    lx.eval("tool.reset xfrm.transform")
    lx.eval("tool.set actr.origin on")
    lx.eval("tool.setattr xfrm.transform SY 0.7")
    lx.eval("tool.apply")
    lx.eval("tool.set actr.origin off 0")
    lx.eval("tool.set TransformScale off 0")
    
    lx.eval("select.element %s edge set 2 1" %layer_index)
    lx.eval("tool.set edge.extend on")
    lx.eval("tool.reset edge.extend")
    lx.eval("tool.attr edge.extend offY 0.004")
    lx.eval("tool.apply")
    lx.eval("tool.set edge.extend off 0")
    lx.eval("select.drop edge")
    
    # center profile 
    lx.eval("vert.center all")
    
def profileOuter():
    """Creates a profile poly for an outer side of a thread. It uses the profileInner() function and then mirrors the geometry."""
    profileInner()
    lx.eval("tool.set TransformScale on")
    lx.eval("tool.reset xfrm.transform")
    lx.eval("tool.setattr xfrm.transform SX -1.0")
    lx.eval("tool.apply")
    lx.eval("tool.set TransformScale off 0")
    lx.eval("vert.center all")

def profileLength(bounding_box):
    """Get the length/height of the created profile by using the two points of the bounding box"""
    POS_A = bounding_box[0:3]
    POS_C = [bounding_box[0],bounding_box[4],bounding_box[2]]
    vector_C = vector_class(POS_C) - vector_class(POS_A)
    length = math.sqrt(vector_C[0]**2 + vector_C[1]**2 + vector_C[2]**2)
    return length

def radial_sweep(diameter, sides, num_threads):
    """Create a radial sweep with the profile. Diameter, sides and the number of threads(height) must be given."""
    # get the bounds of the profile
    bounding_box = list(lx.eval("query layerservice layer.bounds ? selected")) #[X_A,Y_A,Z_A,X_B,Y_B,Z_B])
    
    #select the mesh layer with the thread
    layer_index = lx.eval("query layerservice layer.index ? selected")
    
    #select all polys of the thread for later use
    lx.eval("select.typeFrom polygon true") # set selection mode
    lx.eval("select.all")
    
    # move the profile to the specified diameter
    lx.eval("tool.set TransformMove on")
    lx.eval("tool.reset xfrm.transform")
    lx.eval("tool.attr xfrm.transform TX %s" %( - (diameter / 2)))
    lx.eval("tool.apply")
    lx.eval("tool.set TransformMove off 0")
    
    # select edges for radial sweep
    lx.eval("select.typeFrom edge true") # set selection mode
    lx.eval("select.drop edge") # clear selection
    lx.eval("select.element %s edge add 2 6" %layer_index)
    lx.eval("select.element %s edge add 2 5" %layer_index)
    lx.eval("select.element %s edge add 4 5" %layer_index)
    lx.eval("select.element %s edge add 3 4" %layer_index)
    
    # radial sweep with origin as center 
    lx.eval("tool.set {Radial Sweep} on")
    lx.eval("tool.reset gen.helix")
    lx.eval("tool.set actr.origin on")
    lx.eval("tool.attr gen.helix axis 1")
    lx.eval("tool.attr gen.helix sides %s" %(sides * num_threads))
    lx.eval("tool.attr gen.helix end %s" %(360 * num_threads))
    lx.eval("tool.attr gen.helix offset %s" %(profileLength(bounding_box) * num_threads))
    lx.eval("tool.apply")
    lx.eval("tool.set actr.origin off")
    
    lx.eval("tool.set {Radial Sweep} on") #otherwise tool is not cleared correctly
    lx.eval("tool.set {Radial Sweep} off")
    
    # get rid of the profile poyls
    lx.eval("select.typeFrom polygon true") # set selection mode
    lx.eval("delete")
    
    # zoom all
    lx.eval("viewport.fit")

### DIALOGS ###
def overwrite_msg():
    """Warning message if mesh item is already in scene"""
    try:
        lx.eval("dialog.setup yesNo")
        lx.eval("dialog.title {Confirm Operation}")
        lx.eval("dialog.msg {There is already a thread. Do you want to overwrite it?}")
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
        lx.eval("dialog.result ?")
        return True
    
    except RuntimeError:
        return False

def warning(): # Depricated!
    """Warning message if no profile mesh is in scene"""
    try:
        lx.eval("dialog.setup warning")
        lx.eval("dialog.title {Warning}")
        lx.eval("dialog.msg {Please create a profile first}")
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
    except RuntimeError:
        pass


### VARIABLES ###
args = lx.args()

layer_list = lx.evalN("query layerservice layer.name ? all") #get all mesh items in scene
bounding_box = list(lx.eval("query layerservice layer.bounds ? selected")) #[X_A,Y_A,Z_A,X_B,Y_B,Z_B])
mesh_name_thread = "BJ_Tools_thread"

### USER VALUES ###
diameter = lx.eval("user.value thread_diameter ?")
sides = lx.eval("user.value num_segments ?")
num_threads = lx.eval("user.value num_threads ?")

# Check if mesh_name_thread already in scene and ask user
if checkExistence(layer_list, mesh_name_thread) == True:
    userinput = overwrite_msg()

else:
    userinput = True

# creates actual thread with the radial sweep tool

if args[0] == "innerThread" and userinput == True:
    createMesh(layer_list, mesh_name_thread)
    profileInner()
    radial_sweep(diameter, sides, num_threads)
    
elif args[0] == "outerThread" and userinput == True:    
    createMesh(layer_list, mesh_name_thread)
    profileOuter()
    radial_sweep(diameter, sides, num_threads)
    lx.eval("poly.flip")
    
elif args[0] == "createThread" and mesh_name_thread not in layer_list:
    warning()

elif args[0] == "debug":
    profileInner()
    
else:
    lx.out("42")    

    

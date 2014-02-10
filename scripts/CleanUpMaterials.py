#python

"""
Adaption of script by funk: funk_Mat2MatGroups.py
# Converts materials to correct material groups. Used to fix some OBJ imports
# where materials are shown in the mesh statistics, but no materials groups
# are imported into the shader tree

Now parses the whole scene

Bjoern Siegert Nov 2013
v 2.0

"""

#### FUNCTIONS ####

# create dropdown UI with two options: all or selected mesh items
def userValueList():
    try:
        lx.eval("user.defNew listUI integer momentary")
        lx.eval("user.def listUI dialogname {Clean Up Materials Options}")
        lx.eval("user.def listUI username {Select option}")
        lx.eval("user.def listUI list all;selected")
        lx.eval('user.def listUI listnames {all selected meshes;selected mesh}')
        lx.eval("user.value listUI")
        
        result = lx.eval("user.value listUI ?")
        if result == "all":
            return True
        elif result == "selected":
            return False
        else:
            pass 
    except RuntimeError:
        pass

# create the material for a layer
# input is the number of material set for that layer
def createMaterial(num_mats):
    for mat in range(num_mats):
        mat_name = lx.eval("query layerservice material.name ? %s" %mat) # get the material name
        lx.eval("select.drop polygon")
        lx.eval("select.polygon add material face {%s}" %mat_name) 
        lx.eval("poly.setMaterial {%s}" %mat_name)
        lx.eval("select.drop polygon")

#### VARIABLES ####
mesh_names = lx.evalN("query layerservice layer.name ? all") # get number of mesh layers in scene
current_layer = lx.evalN("query layerservice layer.index ? current")

### START ###
user_input = userValueList() # ask the user for input

if user_input == True:
    lx.eval("select.drop item") # clear the selection
    
    # walktrough all meshes and get the number of materials per mesh
    for i in range(len(mesh_names)):
        lx.eval("select.item %s" %mesh_names[i]) # select mesh item
        lx.eval("query layerservice layer.index ? %s" %mesh_names[i]) # select mesh layer
        num_mats = lx.eval("query layerservice material.N ?") # get the number of materials of the layer
        createMaterial(num_mats) # create materials
    lx.eval("select.drop item")
    
elif user_input == False:
    lx.eval("query layerservice layer.index ? %s" %current_layer)
    num_mats = lx.eval("query layerservice material.N ?") # get the number of materials of the layer
    createMaterial(num_mats)
else:
    pass
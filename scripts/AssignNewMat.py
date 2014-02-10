#python

"""
Assign different materials

Script assigns each selected item a new individual material in the shader tree.
User is able to set a pre-fix to the material so it is easier to find.

Bjoern Siegert aka nicelife Oct 2013
v1.0

"""

# user dialog. Ask user for a prefix

def preFixUI():
    try:
        lx.eval("user.defNew Material.Name string momentary")
        lx.eval("user.def Material.Name username {Pre-fix}")
        lx.eval("user.def Material.Name transient true")
        lx.eval("user.value Material.Name")
        return lx.eval("user.value Material.Name ?")
        
    except RuntimeError:
        pass
    
def selectionMsg():
    try:
        lx.eval("dialog.setup warning")
        lx.eval("dialog.title {No Selection}")
        lx.eval("dialog.msg {Please select one or more mesh items.}")
        lx.eval("dialog.open")
    
    except RuntimeError:
        pass

### VARIABLES ###
meshList = lx.evalN("query sceneservice selection ? mesh") # get selected mesh items from scene

### START ###
if meshList:
    userInput = preFixUI() # get the prefix name from the user
    
    lx.eval("select.drop item")
    for mesh in range(len(meshList)):
        lx.out("material group name: ", (userInput + meshList[mesh]))
        lx.eval("select.item %s" %meshList[mesh])
        lx.eval("poly.setMaterial {%s} {1.0 1.0 1.0} 0.8 0.2 true false false" %(userInput + meshList[mesh]))
        lx.eval("item.name {%s} advancedMaterial" %(userInput + meshList[mesh] + "_Material"))
        
else:
    selectionMsg()
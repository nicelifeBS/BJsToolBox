#python

"""
MARI TOOLs v1.2
Bjoern Siegert aka nicelife

Last edited 2013-12-06

Arguments:
loadFiles, gammaCorrect, setUVoffset, sortSelection, createPolySets

Import textures from MARI and some tools to manage these:
For import the user can choose:
- a delimiter so that the script can find the UDIM number
- to ignore the 8x8 pixel textures from import
- if the textures should be gamma corrected

Tools:
- Sets the UV offset automatically from the file name
- Gamma correction of imported texutres if needed
- Sort the images in scene tree in alphabetic order
- Create polygon sets for each UDIM


Version History:
v1.2
New Feature:
- Create selection sets for the different UDIMs

v1.1
Bugfixes:
- Creating the image maps didn't work reliable because of a selection in the shader tree. Clears selection (only select the Mesh) before creating the image maps now
- Sorting fixed
- Added some logging
"""


### FUNCTIONS ####

def locator_ID(imageMap_ID):
    """
    Find ID of the texture locator of an image map. The ID of the image map in the shadertree is needed as argument.
    """
    texture_num = lx.eval("query layerservice texture.N ? all")
    # Parse through all textures until texture ID of layer matches the selected one.
    for i in range(texture_num):
        
        texture_ID = lx.eval("query layerservice texture.id ? %s" %i)
        lx.out("(%s) texture ID: %s" %(i, texture_ID))
        
        if texture_ID == imageMap_ID:
            return lx.eval("query layerservice texture.locator ? %s" %i) #retruns the texture locator ID
            break
        else:
            lx.out("no match")

def create_imageMap(clipPath):
    """
    Create material in shader tree. Change it to an image map and set up UV projection type and tiling
    """
    lx.out("Create Image: texture.N ", lx.eval("query layerservice texture.N ?"))
    
    lx.eval("clip.addStill %s" %clipPath)
    lx.eval("shader.create constant")
    lx.eval("item.setType imageMap textureLayer")
    lx.eval("texture.setIMap {%s}" %get_filename(clipPath))
    lx.eval("item.channel imageMap$aa false")
    lx.eval("item.channel txtrLocator$projType uv")
    lx.eval("item.channel txtrLocator$tileU reset")
    lx.eval("item.channel txtrLocator$tileV reset")
    layer_index = lx.eval("query layerservice layer.index ? main")
    
def load_files():
    """
    Load in files and save complete paths in a list
    """
    try:
        lx.eval("dialog.setup fileOpenMulti")
        lx.eval("dialog.title {Import MARI textures}")
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
        return lx.evalN("dialog.result ?")
    
    except RuntimeError:
        return False

def get_file_extension(filename):
    """returns the file extension, e.g. ".tif". Searches from end until it finds "." """
    file_extension = ""
    
    for i in filename[::-1]: # reverse the filename and walkthrough all chars and add each one to variable until finding the first period
        if i !=".":
            file_extension += i
        else:
            break
        
    return "." + file_extension[::-1] # return the saved extension by reversing it back and adding the period

def get_filename(filePath):
    """returns the file name without the extension -> clip name"""
    filename = filePath.split("/")[-1]
    return filename.replace(get_file_extension(filename), "")

def get_clipPath(selection):
    """Returns a dictionary. The key is the actual file path of the image map. Per key the current
    position number and the texture ID are saved."""
    list = {}
    for imap in selection:
        for number in range(lx.eval("query layerservice texture.N ?")):
            if lx.eval("query layerservice texture.id ? %s" %number) == imap:
                list [lx.eval("query layerservice texture.clipFile ? %s" %number)] = [number,imap]
    return list

def get_UDIM(file_name, delimiter):
    """Extract the UDIM value from file name. A file name and a delimiter must be given. Returns False if it is not a MARI texture."""
    for item in file_name.split(delimiter): # try if string is a number and if the length is 4 chars long it is identified as UDIM
        try:
            int(item)
            if len(item) == 4:
                U_offset = -(int(item[3]) - 1)
                V_offset = -(int(item[1:3]))
                return U_offset, V_offset
            
        except ValueError:
            pass
    
def check_clip_size(clip_name):
    """Checks the size of a clip and return True if it is 8x8 pixels"""
    
    clip_size = "w:8"
    for i in range(lx.eval("query layerservice clip.N ?")):
        if lx.eval("query layerservice clip.id ? %s" %i) == clip_name:
            clip_info = lx.eval("query layerservice clip.info ? %s" %i)
            clip_info = clip_info.split(" ")
            
            if clip_size in clip_info[1]: 
                lx.out("%s deleted" %clip_name)
                return True
            else:
                lx.out("%s correct size" %clip_name)
                return False

def set_gamma(value):
    """Set gamma with given value for selected images."""
    if not lx.eval("query sceneservice selection ? imageMap"):
        lx.out("nothing selected")
    else:
        lx.eval("item.channel imageMap$gamma %s" %value)

def get_texture_parent(item_ID):
    """Returns the parent of an image map"""
    return lx.eval("query sceneservice textureLayer.parent ? %s" %item_ID)

def vmap_selected(vmap_num, layer_index):
    """See if a UV map of the current layer is selected and returns the name.
    Also returns false if no vmaps are in scene"""
    
    if vmap_num == 0:
        return False
    
    else:
        for i in range(vmap_num):
            vmap_layer = lx.eval("query layerservice vmap.layer ? %s" %i) + 1 # Layer index starts at 1 and not at 0 -> +1 to shift index
            vmap_type = lx.eval("query layerservice vmap.type ? %s" %i) 
    
            if vmap_type == "texture" and vmap_layer == layer_index:         
                if lx.eval("query layerservice vmap.selected ? %s" %i) == True:
                    
                    #lx.out("layer_index: ", layer_index)
                    #lx.out("vmap_layer: ", vmap_layer)
                    #lx.out("vmap_type: ", vmap_type)
                    
                    vmap_name = lx.eval("query layerservice vmap.name ? %s" %i)
                    return vmap_name
                    break
            
            else:
                pass

def test(test):
    lx.out(test)
    
###############################################################

### DIALOGS & MESSAGES ###
def warning_msg(name):
    """A modal warning dialog. Message text can be set through name var."""
    try:
        lx.eval("dialog.setup warning")
        lx.eval("dialog.title {Error}")
        lx.eval("dialog.msg {Ooopsy. %s.}" %name)
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
    except RuntimeError:
        pass

def dialog_brake():
    try:
        lx.eval("dialog.setup yesNo")
        lx.eval("dialog.title {Coffee Brake?}")
        lx.eval("dialog.msg {This could take a while. Do you want to grab a cup of coffee?}")
        lx.eval("dialog.result ok")
        lx.eval("dialog.open")
        
        lx.eval("dialog.result ?")
        return True
    
    except RuntimeError:
        return False

###############################################################


### FUNCTIONS END ###


### VARIABLES ###
args = lx.args()[0] # Arguments. Only the first argument is passed.

layer_index = lx.eval("query layerservice layer.index ? main") #select the current mesh layer
layer_id = lx.eval("query layerservice layer.id ? main")
scene_index = lx.eval("query sceneservice scene.index ? current")
imap_selection = lx.evalN("query sceneservice selection ? imageMap") # get the name of the selected images
vmap_num = lx.eval("query layerservice vmap.N ?") # Number of vertex maps of selected mesh

## USER VALUES ##
gamma_correction = lx.eval("user.value MARI_TOOLS_gamma ?") # Gamma correction on/off
gamma_value = lx.eval("user.value MARI_TOOLS_gammavalue ?") # Gamma value from UI
delimiter =  lx.eval("user.value MARI_TOOLS_delimiter ?") # Delimiter form UI
filter_clips = lx.eval("user.value MARI_TOOLS_filter_clips ?") # Delete 8x8 clips on/off


## Delimiter Interpreter ##
if delimiter == "option1":
    delimiter = "."
elif delimiter == "option2":
    delimiter = "_"


### ARGS parsing ###

# Import Files including name check
if args == "loadFiles":
    
    # Check if a UV set is selected
    lx.out(vmap_selected(vmap_num, layer_index))
    
    if vmap_selected(vmap_num, layer_index) == False or not vmap_selected(vmap_num, layer_index):
        warning_msg("Please select a UV map.")
    
    else:
        UVmap_name = vmap_selected(vmap_num, layer_index)
        
        # Create folder
        lx.eval("shader.create shaderFolder") # Create Folder for imported Textures
        lx.eval("texture.parent Render 0") # Move created folder to bottom of shader tree
        folder_ID = lx.eval("query sceneservice selection ? shaderFolder")
        #lx.out("folder_ID: ", folder_ID
        
        fileList = load_files() # Open dialog to load image files
        
        # Create the image maps in shader tree
        for filePath in fileList:
            lx.eval("select.item %s set" %layer_id) # Select only the Mesh for a fresh start
            
            file_name = get_filename(filePath)
            
            # Debuging
            lx.out("File Path: ", filePath)
            lx.out("File Name: ", file_name)
            lx.out("UDIM: ", get_UDIM(file_name, delimiter))
            
            if get_UDIM(file_name, delimiter):
                
                # Create image maps in shadertree
                create_imageMap(filePath)
                lx.out("Selection: ", lx.eval("query sceneservice selection ? all"))
                
                # Check the image size and ignore it if it's 8x8 pixels
                clip_name = lx.eval("query sceneservice selection ? mediaClip")
                if check_clip_size(clip_name) == True and filter_clips == True:
                    lx.eval("clip.delete")
                    lx.eval("texture.delete")
                    break
                else:
                    pass
                  
                # Gamma correction
                if gamma_correction == True:
                    set_gamma(gamma_value)
                
                #Set UV map
                lx.eval("texture.setUV %s" %UVmap_name)
                
                # Set the UV offset values
                imap_ID = lx.eval("query sceneservice selection ? imageMap")
                lx.eval("select.subItem %s set txtrLocator" %locator_ID(imap_ID))
                lx.eval("item.channel txtrLocator$m02 %s" %get_UDIM(file_name, delimiter)[0])
                lx.eval("item.channel txtrLocator$m12 %s" %get_UDIM(file_name, delimiter)[1])
                lx.eval("texture.parent %s 0" %folder_ID) # Move texture to the bottom of the created folder
                
            else:
                lx.eval("item.delete shaderFolder") # Delete created folder to clean up scene
                warning_msg("Please select file(s) with an UDIM or change delimiter")


## Gamma Correction: Correct Gamma of textures 1.0/2.2 = 0.4546 ##
elif args == "gammaCorrect":
    
    set_gamma(gamma_value)

## set the UVoffset according to image file name ##
elif args == "setUVoffset":
    for imap in imap_selection:
        for i in range(lx.eval("query layerservice texture.N ?")):
            if lx.eval("query layerservice texture.id ? %s" %i) == imap:
                lx.out("setting UV offset for ", imap)
                file_name = get_filename(lx.eval("query layerservice texture.clipFile ? %s" %i))
                lx.eval("select.subItem %s set txtrLocator" %lx.eval("query layerservice texture.locator ? %s" %i))
                lx.eval("item.channel txtrLocator$m02 %s" %get_UDIM(file_name, delimiter)[0])
                lx.eval("item.channel txtrLocator$m12 %s" %get_UDIM(file_name, delimiter)[1])                
                lx.eval("item.channel txtrLocator$tileU reset")
                lx.eval("item.channel txtrLocator$tileV reset")

## Sort selected images top to bottom ##
elif args == "sortSelection":
    clip_list = get_clipPath(imap_selection)
    sorted_list= sorted(clip_list) # Sort keys of dict in alphabetic order
    
    for i in sorted_list:
        lx.out("clip path: ", i)
        
        # If selection is directly parented under Render -> not in a sub group
        if "Render" in get_texture_parent(clip_list[i][1]):
            lx.eval("select.item %s set textureLayer" %clip_list[i][1])
            lx.eval("texture.parent %s 1" %get_texture_parent(clip_list[i][1]))
        
        # If selection is parented in a group
        else:
            lx.eval("select.item %s set textureLayer" %clip_list[i][1])
            lx.eval("texture.parent %s 0" %get_texture_parent(clip_list[i][1]))

## Create poly selection set for each UDIM            
elif args == "createPolySets":
    
    # Check if a UV map is selected
    if vmap_selected(vmap_num, layer_index) == False or not vmap_selected(vmap_num, layer_index):
        warning_msg("Please select a UV map.")
    
    # Proceed with MARI_Tools_createPolySets.py script
    elif dialog_brake() == True:
        lx.eval("@MARI_Tools_createPolySets.py")


elif args == "test":
    lx.out("TESTING")
    
else:
    lx.out("Please choose one argument: loadFiles, gammaCorrect, setUVoffset, sortSelection, createPolySets")

    
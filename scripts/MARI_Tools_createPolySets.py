#python

"""
UVselset v1.2

Author: Bjoern Siegert aka nicelife

Last edit: 2014-01-18

Creates poly selection sets based on the UV offset values. Each sector containing polys will get a selection set.
The name follows the UDIM scheme of MARI. E.g.: If u and v are between 0-1 the space 0-1 gets a selection set with the name UDIM_1001,
1-2: UDIM_1002. If v = 1-2 -> UDIM_1011, UDIM_1012,...

Problems:
- Slow with big models
"""

import time

### LX SERVICE ###
layer_svc = lx.Service("layerservice")
progressbar = lx.Monitor()

### LAYER SELECTION and index ###
layer_svc.select("layers", "main")
layer_index = layer_svc.query("layer.index")

### VARIABLES ###
uv_dict = {}
layer_svc.select("polys", "all")
poly_list = layer_svc.query("polys")

# Get the name of selected uv map
selected_uv_map = lx.eval("vertMap.list type:txuv ?")

# Get the index of the selected uv map
if selected_uv_map != "_____n_o_n_e_____":
    # Select the vmap
    layer_svc.select("vmaps", "all")
    vmap_list = layer_svc.query("vmap.name")
    
    for vmap in xrange(len(vmap_list)):
        layer_svc.select("vmap.index", str(vmap))
        
        # Compare vmap name with the selected uv map. If it matches we have the index we need.
        if layer_svc.query("vmap.name") == selected_uv_map:
            vmap_index = vmap
            break

else:
    lx.out("Hey mate, you didn't select a proper UV map. So all I did was printing this stupid message.")
    # Warning dialog!

############################################################
#
# Here we fill the uv_dict with the poly indices
# We only need the first uv values of the polygon. This is 
# enough to identify uv sector
#
############################################################
for poly in poly_list:
    layer_svc.select("poly.index", str(poly))
    vmap_value = layer_svc.query("poly.vmapValue")
    
    # First we convert to integer to identify the uv sector
    vmap_value = map(int, vmap_value)
    
    # Get the first uv values in the list
    u = vmap_value[0]
    v = vmap_value[1]
    
    # Here we write in the poly index to the UDIM key. If the key is not found it is created via the exception
    try:
        uv_dict[1001 + (v * 10) + u ].append(poly)
        
    except KeyError:
        uv_dict[1001 + (v * 10) + u ] = [poly]    


# Initialize the progress bar
progressbar.init(len(uv_dict))


#############################################################
#
# Check if there are already some UDIM selection sets.
# If yes then delete those
#
#############################################################

lx.eval("select.type polygon")
layer_svc.select("polsets")
poly_set_num = layer_svc.query("polsets")
if poly_set_num:
    delete_sets = []
    
    for i in poly_set_num:
        # Select the poly set
        layer_svc.select("polset.index", str(i))
        poly_set_name = layer_svc.query("polset.name")
        
        # Find a UDIM selection set and delete it
        if "UDIM_" in poly_set_name:
            delete_sets.append(poly_set_name)
            
        else:
            pass
        
    lx.out("Delete Sets: ", delete_sets)
    
    # Delete Sets
    layer_svc.select("layer.index", str(layer_index))
    for sets in delete_sets:
        lx.eval("select.deleteSet %s" %sets)
        lx.out("Deleted Selection Set: ", sets)

#############################
### Debugging: Start Time ###
t1 = time.time()
#############################


##########################################
#
# Now lets create something!
# Here we select the polys which were stored in the uv_dict
# and assign them to their UDIM selection set
#
# iteritems() is faster and gives access to key and value at the same time.
#
##########################################

for key, index in uv_dict.iteritems():
    # Clear selection
    lx.eval("select.drop polygon")
    
    # Select polys
    for i in index:
        lx.eval("select.element %s polygon add %s" %(layer_index, i))
        
    # Create a new selection set with the UDIM as name: UDIM_1011
    lx.eval("select.editSet UDIM_%s add" %key)
    
    # Logging
    lx.out("New selection set created: UDIM_", key)
    
    # Clear selection
    lx.eval("select.drop polygon")
    
    # Progressbar step
    progressbar.step(1)

#############################
### Debugging: Stop Time  ###
t2 = time.time()
sets_creation = t2 - t1
#############################

# Debugging Speed
lx.out("Selection Sets Creation: %s sec" %sets_creation)

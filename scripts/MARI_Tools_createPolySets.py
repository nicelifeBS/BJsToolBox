#python

"""
UVselset v1.0

Author: Bjoern Siegert aka nicelife

Last edit: 2013-12-06

Creates poly selection sets based on the UV offset values. Each sector sector containing polys will
get a selection set. The name follows the UDIM scheme of MARI. E.g.: If v = 0-1 the space 0-1 gets a selection set with the name UDIM_1001,
1-2: UDIM_1002. If v = 1-2 -> UDIM_1011, UDIM_1012,...

Problems:
- Slow with big models

"""

import time

### METHODS ###


### LX SERVICE ###
layer_svc = lx.Service("layerservice")
progressbar = lx.Monitor()

### LAYER SELECTION and index ###
layer_svc.select("layers", "main")
layer_index = layer_svc.query("layer.index")

### VARIABLES ###
uv_dict = {}

#############################
### Debugging: Start Time ###
t1 = time.time()
#############################

# Select the UVs
layer_svc.select("uvs", "all")
uv_indices = layer_svc.query("uvs")

# Assign UV the UDIMs to the different UVs. Save result in dictionary.
for index in uv_indices:
    layer_svc.select("uv.index", str(index))
    uv_pos = layer_svc.query("uv.pos")
    vert_index = layer_svc.query("uv.vert")
    
    # Convert to integers to identify the UV offset sector    
    u = int(uv_pos[0])
    v = int(uv_pos[1])
    
    try:
        uv_dict[1001 + (v * 10) + u ].append(vert_index)
    
    except KeyError:
        uv_dict[1001 + (v * 10) + u ] = [vert_index]

############################
### Debugging: Stop Time ###
t2 = time.time()
dict_setup = t2 - t1
############################

# Check if selection set already exists. If yes it is deleted.
lx.eval("select.type polygon")
layer_svc.select("polsets")
poly_set_num = layer_svc.query("polsets")
if poly_set_num:
    delete_sets = []
    
    for i in poly_set_num:
        
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

# Selection type
lx.eval("select.type vertex")


# Create selection sets

################################
#   Code to change:
# Use following to get key and value at the same time.
# for key, value in uv_dict.iteritems():
#
################################

# Progress bar steps
#progressbar.init(len(uv_dict))

#lx.out("dict length: ", len(uv_dict))

for key, index in uv_dict.iteritems():
    # Clear selection
    lx.eval("select.drop polygon")
    lx.eval("select.drop vertex")
    
    # Progress bar
    progressbar.init(len(index))
    lx.out("index length:" ,len(index))
    
    # Select verts
    for i in index:
        lx.eval("select.element %s vertex add %s" %(layer_index, i))
        # Progressbar step
        progressbar.step(1)
    
    # Convert selection to polys and create a new selection set with UDIM
    lx.eval("select.convert polygon")
    lx.eval("select.editSet UDIM_%s add" %key)
    
    # Logging
    lx.out("New selection set created: UDIM_", key)

#############################
### Debugging: Stop Time  ###
t2 = time.time()
sets_creation = t2 - t1
#############################

# Debugging Speed
lx.out("Dictionary Setup: %s sec" %dict_setup)
lx.out("Selection Sets: %s sec" %sets_creation)




#python

#####################################################################
#   Each element in a mesh item gets a new material
#   with a random color applied.
#   
#
#   Written by Bjoern Siegert aka nicelife Nov 2013
#
#               v0.1
#####################################################################


### MODULES ###
import random

### VARIABLES ####
layer_index = lx.eval("query layerservice layer.index ? selected")
layer_name = lx.eval("query layerservice layer.name ? selected")
num_poly = lx.eval("query layerservice poly.N ? all")


### START ####

if num_poly != 0:
    
    #   create temp layer
    lx.eval("item.create mesh %s" %("tempMat___" + layer_name))
    temp_layer_index = lx.eval("query layerservice layer.index ? selected") # get index of temp layer
    
    #   select previous layer again
    lx.eval("select.item %s set mesh" %layer_name)

    for i in range(num_poly):
        if num_poly != 0:
            lx.out(num_poly)
            
            # Create random RGB color values
            color_R = round(random.random(),3)
            color_G = round(random.random(),3)
            color_B = round(random.random(),3)
            
            #   select previous layer
            lx.eval("query layerservice layer.name ? %s" %layer_index)
        
            #   select first poly and connect selection
            poly_index = lx.eval("query layerservice poly.index ? first") # index of the first poly in mesh
            lx.eval("select.element %s polygon set %s" %(layer_index, poly_index))
            lx.out("select.element %s polygon set %s" %(layer_index, poly_index))
            lx.eval("select.polygonConnect m3d")
    
            #   assign new material to selection
            lx.eval("poly.setMaterial %s {%s %s %s}" %("material_" + str(i), color_R, color_G, color_B))
            
            #   cut out the polys and place them in the temp layer
            lx.eval("cut")
            lx.eval("select.item %s set mesh" %("tempMat___" + layer_name))
            lx.eval("paste")
            
            #   go back to previous layer and repeat setps
            lx.eval("select.item %s set mesh" %layer_name)
            
            num_poly = lx.eval("query layerservice poly.N ?")
            
        else:
            lx.out("no polys anymore")
            
            # copy polys back to original mesh and delete the temp layer
            lx.eval("select.item %s set mesh" %("tempMat___" + layer_name))
            lx.eval("select.typeFrom polygon true")
            lx.eval("select.all")
            lx.eval("cut")
            lx.eval("item.delete mesh")
            lx.eval("select.item %s set mesh" %layer_name)
            lx.eval("paste")
            break
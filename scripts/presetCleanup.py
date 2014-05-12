#python

##----------------------------##
#
# Clean up material presets
# in the shader tree
#
#
#
##----------------------------##

# Services
sceneservice = lx.Service('sceneservice')
layerservice = lx.Service('layerservice')

# Arguments
arg = lx.arg()

sceneservice.select('render.id', '0')
renderID = sceneservice.query('render.id')
renderChildren = list(sceneservice.queryN('render.children'))

sceneservice.select('mask.N', 'all')
mask_num = sceneservice.query('mask.N')

PTag_filter = ['(all)','(none)']

# Find the preset masks in shader tree
# unlock them and save id in list
masks_move = []
masks_delete = []
masks_locked = []
for num in xrange(mask_num):
    sceneservice.select('mask.id', str(num))
    maskID = sceneservice.query('mask.id')
    maskName = sceneservice.query('mask.name')
    maskChildren = sceneservice.queryN('mask.children')
    maskParent = sceneservice.query('mask.parent')
    
    # Go through all material presets ".lxp"
    # If the mask is not in the root ptags and types are checked of all masks above it
    # if one of these masks has an assignment the current maskID is ignored
    # it is also ignored if the ptag is "none" or "all"
    if '.lxp' in maskName and len(maskChildren) != 0:
        masks_move.append(maskID)
        lx.out(maskID,':', maskChildren)
        while maskParent != renderID:
            lx.eval('select.subItem {0} set textureLayer'.format(maskParent))
            item_mask = lx.eval('mask.setMesh ?')
            ptag_type = lx.eval('mask.setPTagType ?')
            
            if item_mask not in PTag_filter or ptag_type != 'Material':
                masks_move.remove(maskID)
                break
            
            else:
                sceneservice.select('item.id', maskParent)
                maskParent = sceneservice.query('item.parent')
        else:
            if maskID in masks_move:
                lx.eval('select.subItem {0} set textureLayer'.format(maskID))
                pTag = lx.eval('mask.setPTag ?')
                
                if pTag in PTag_filter:
                    masks_move.remove(maskID)

lx.out(masks_move)

# Clean up duplicates and not used materials
ptag_list = []
for i in masks_move:
    lx.eval('select.subItem {0} set textureLayer'.format(i))
    pTag = lx.eval('mask.setPTag ?')
    
    if pTag not in ptag_list:
        sceneservice.select('item.id', i)
        maskName = sceneservice.query('item.name')
        maskName = maskName[:maskName.index('.lxp')] # mask name without .lxp
        
        lx.eval('texture.parent %s 1' %renderID)
        lx.eval('material.reassign {%s} {%s}' %(pTag, maskName))
        lx.eval('item.name {} mask')
        lx.eval('item.editorColor blue')
        
        # maskName is the new ptag and added to the list
        ptag_list.append(maskName)
        
    else:
        lx.eval('item.editorColor red')
        lx.eval('texture.delete')

lx.eval('material.purge')
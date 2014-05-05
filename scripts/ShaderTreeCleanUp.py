#python

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
masks_delete = []
for num in xrange(mask_num):
    sceneservice.select('mask.id', str(num))
    maskID = sceneservice.query('mask.id')
    maskName = sceneservice.query('mask.name')
    maskTags = sceneservice.queryN('mask.tags')
    maskchildren = sceneservice.queryN('mask.children')
    
    # Find the preset mask group and unlock it
    # If the ptag is all or none move it to the delete list
    if ('.lxl' or '.lxp') in maskName:
        lx.out('maskID: ',maskID)
        lx.eval('select.subItem {0} set textureLayer'.format(maskID))

        if 'folded' in maskTags:
            lx.eval('shader.unlock')
        
        # Check if preset has a nested lxl group
        sceneservice.select('item.id', maskchildren[0])
        childID = sceneservice.query('item.id')
        if ('.lxl' or '.lxp') in sceneservice.query('item.name') and sceneservice.query('item.type') == 'mask':
            masks_delete.append(maskID)
            masks_delete.append(childID)

        else:
            masks_delete.append(maskID)
     
             
# Check if any child is not a mask group
# If so delete the parent from delete list, break and hop to the next mask in the list
# Else move the group directly under the root
masks_moved = {}
for mask in masks_delete:
    sceneservice.select('item.id', mask)
    mask_children = sceneservice.queryN('mask.children')
    
    mask_children = sceneservice.queryN('mask.children')
    for child in mask_children:
        sceneservice.select('item.type', child)
        lx.eval('select.subItem {0} set textureLayer'.format(child))
        childPTag = lx.eval('mask.setPTag ?')
        
        if sceneservice.query('item.type') != 'mask' or childPTag in PTag_filter:
            masks_delete.remove(maskID)
            break
    
        else:
            lx.eval('texture.parent {0} {1}'.format(renderID, '1'))
            masks_moved[child] = childPTag
    
# Find duplicated in the mask groups
pTags = list(set(masks_moved.values())) # unique list
for key, value in masks_moved.iteritems():
    #3lx.eval('select.subItem {0} set textureLayer'.format(key))
    if value in pTags:
        pTags.remove(value)
    else:
        masks_delete.append(key)
        

# Clean Up Shader Tree
lx.eval('select.drop item textureLayer')
for item in masks_delete:
    lx.eval('select.subItem {0} add textureLayer'.format(item))

try:
    lx.eval('!texture.delete')
except:
    lx.out('Nothing was selected')
    
lx.out('deleted masks: ',masks_delete)
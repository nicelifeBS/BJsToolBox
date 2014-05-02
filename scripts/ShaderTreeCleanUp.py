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
masks_delete = []
for num in xrange(mask_num):
    sceneservice.select('mask.id', str(num))
    maskID = sceneservice.query('mask.id')
    maskName = sceneservice.query('mask.name')
    maskTags = sceneservice.queryN('mask.tags')
    
    if arg == 'locked':
        # Find the preset mask group and unlock it
        if 'folded' in maskTags and '.lxl' in maskName:
            lx.out('maskID: ',maskID)
            lx.eval('select.subItem {0} set textureLayer'.format(maskID))
            lx.eval('shader.unlock')
            if maskID not in masks_delete:
                masks_delete.append(maskID)
        else:
            continue
                
    elif arg == 'unlocked':
        if '.lxl' in maskName:
            lx.out('maskID: ',maskID)
            if maskID not in masks_delete:
                masks_delete.append(maskID)
        else:
            continue        
    else:
        break
    
    # Go thourgh the mask children
    # Move them to the root
    maskChild = sceneservice.queryN('mask.children')
    lx.out('mask children: ',maskChild)
    for child in maskChild:
        # Position of mask in shader tree
        # If not in root then the index is 1
        if child in renderChildren:
            mask_ST_index = child
        else:
            mask_ST_index = 1
        
        # Select the mask inside the mask group
        # and move those to the root
        sceneservice.select('item.id', child)
        if sceneservice.query('item.type') == 'mask':            
            lx.eval('select.subItem {0} set textureLayer'.format(child))
            lx.eval('texture.parent {0} {1}'.format(renderID, mask_ST_index))
            lx.out('Moved {0} to shadertree root. {1}: {2}'.format(child, renderID, mask_ST_index))

lx.out('masks to delete: ',masks_delete)

# Clean Up Shader Tree
lx.eval('select.drop item textureLayer')
for item in masks_delete:
    lx.eval('select.subItem {0} add textureLayer'.format(item))
try:
    lx.eval('!texture.delete')
except:
    lx.out('Nothing was selected')
    
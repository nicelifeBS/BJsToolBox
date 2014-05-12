#python

# Requirement
'''
-Find duplicates of .lxl or .lxp mask groups in the shader tree
-Keep only one instance of the groups
-And move those directly in the root of the shader tree
-
'''

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
    maskTags = sceneservice.queryN('mask.tags')
    maskChildren = sceneservice.queryN('mask.children')
    maskParent = sceneservice.query('mask.parent')
    
    # Find the preset mask group and unlock it
    # If the ptag is all or none move it to the delete list
    if '.lxp' in maskName:
        lx.eval('select.subItem {0} set textureLayer'.format(maskID))
        pTag = lx.eval('mask.setPTag ?')
        
        if pTag not in PTag_filter:
            masks_move.append(maskID)
            
            # Find nested lxp mask group and move its content to the current maskID group
            if len(maskChildren) == 1:
                sceneservice.select('item.id', maskChildren[0])
                childName = sceneservice.query('item.name')
                maskType = sceneservice.query('item.type')
                
                if maskName[:maskName.index('.lx')] in childName and maskType == 'mask':
                    lx.eval('select.drop item')
                    for i in sceneservice.query('item.children'):
                        lx.eval('select.subItem {0} add textureLayer'.format(i))
                    
                    lx.eval('texture.parent %s -1' %maskID)
                    lx.eval('select.drop item')
                    
            # Now we check if maskID is underneath a mask group
            # If there is an item mask applied it is copied to the maskID group            
            while 'polyRender' not in maskParent:
                lx.eval('select.subItem {0} set textureLayer'.format(maskParent))
                parent_item = lx.eval('mask.setMesh ?')
                lx.out('mask Parent:', maskParent)                
                
                if parent_item not in PTag_filter:
                    lx.eval('select.subItem {0} set textureLayer'.format(maskID))
                    lx.eval('mask.setMesh {%s}' %parent_item)
                    lx.eval('texture.parent %s 1' %renderID)
                    masks_move.remove(maskID)
                    break

                else:
                    sceneservice.select('item.id', maskParent)
                    maskParent = sceneservice.query('item.parent')
        else:
            masks_delete.append(maskID)
            
    elif '.lxl' in maskName and 'folded' in maskTags:
        lx.eval('select.subItem {0} set textureLayer'.format(maskID))
        lx.eval('shader.unlock')
        lx.eval('select.drop item')
        for child in maskChildren:
            lx.eval('select.subItem {0} add textureLayer'.format(child))
        lx.eval('texture.parent %s 1' %renderID)
           
             
lx.out(masks_locked)
lx.out(masks_move)
lx.out(masks_delete)

# Clean up the shader tree
# Found ptags are stored in a list and compared against the mask groups
# If a mask with the same ptag is found it is deleted
ptag_list = []
lx.eval('select.drop item')
for i in masks_move:
    lx.eval('select.subItem {0} set textureLayer'.format(i))
    ptag = lx.eval('mask.setPTag ?')
    sceneservice.select('item.id', i)
    maskChildren = sceneservice.query('item.children')

    if ptag not in ptag_list and maskChildren != '(none)':        
        ptag_list.append(ptag)
        lx.eval('item.editorColor blue')
        lx.eval('texture.parent %s 1' %renderID)
    else:
        if i not in masks_delete:
            masks_delete.append(i)
        
for i in masks_delete:
    lx.eval('select.subItem {0} set textureLayer'.format(i))
    lx.eval('item.editorColor red')
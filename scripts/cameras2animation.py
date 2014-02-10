#python

##---------------------------------------------------------##
#
#   Cameras to camera animation
#
#   Combines different cameras as one camera as keys in the
#   animation timeline.
#
#   Useful if you have various camera position from a
#   scanned object. And you want to combine all
#   into one camera as keys in the timeline.
#
#   Usage:
#   Select all cameras. Selection order defines the position
#   in the timeline. The last selected camera is the one
#   which is animated. Fire the script
#
#   Bjoern Siegert 2014-02-11
#
##---------------------------------------------------------##


sceneService = lx.Service("sceneservice")
layerService = lx.Service("layerservice")

# Camera selection
# Last selected camera is the target camera
sceneService.select("selection", "camera")
cameraList = list(sceneService.query("selection"))

targetCam = cameraList.pop()


lx.out(cameraList)
lx.out(targetCam)

## Reset to timeline to key 0
lx.eval("select.time 0.0 0 0")

for camera in cameraList:
    # Clear selection
    lx.eval("select.item %s set camera" %camera)
    
    focalLength = lx.eval("item.channel name:camera$focalLen ? item:%s" %camera)
    filmWidth = lx.eval("item.channel name:apertureX ? item:%s" %camera)
    filmHeight = lx.eval("item.channel name:apertureY ? item:%s" %camera)
    
    lx.out(camera)
    lx.out(focalLength)
    lx.out(filmWidth)
    lx.out(filmHeight)
    
    # select target camera and current camera from list
    lx.eval("select.item %s set" %targetCam)
    lx.eval("item.channel name:camera$focalLen value:%s mode:set item:%s" %(focalLength, targetCam))
    lx.eval("item.channel name:apertureX value:%s mode:set item:%s" %(filmWidth, targetCam))
    lx.eval("item.channel name:apertureY value:%s mode:set item:%s" %(filmHeight, targetCam))
    
    
    lx.eval("select.item %s add camera" %camera)
    lx.eval("item.match item pos")
    lx.eval("item.match item rot")
    
    lx.eval("item.key mode:all item:%s" %targetCam)
    lx.eval("time.step frame next")
    
    lx.eval("select.drop item")

lx.eval("select.time 0.0 0 0")
lx.eval("select.item %s set" %targetCam)

    
    
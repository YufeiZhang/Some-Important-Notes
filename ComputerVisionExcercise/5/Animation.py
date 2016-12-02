#----------------------------------------------------------
# File:   Animation.py
# Author: Yufei Zhang
# CCID:   1373240
#----------------------------------------------------------
import bpy
from math import pi, sin, cos # sin(pi/2) = 1.0


def addCopyLocationConstraint(ob, name, target):
    cpyloc = ob.constraints.new('COPY_LOCATION')
    cpyloc.name = name
    cpyloc.use_x = False
    cpyloc.use_y = False
    cpyloc.target = target
    cpyloc.subtarget = 'Head'
    return
    

def addDistanceConstraint(ob, name, target):
    dis = ob.constraints.new('LIMIT_DISTANCE')
    dis.name = name
    dis.target = target
    dis.subtarget = 'Head'
    dis.distance = 5
    dis.limit_mode = "LIMITDIST_ONSURFACE"
    return


def addTrackToConstraint(ob, name, target):
    cns = ob.constraints.new('TRACK_TO')
    cns.name = name
    cns.target = target
    cns.subtarget = 'Head'
    cns.track_axis = 'TRACK_NEGATIVE_Z'
    cns.up_axis = 'UP_Y'
    cns.owner_space = 'WORLD'
    cns.target_space = 'WORLD'
    return


def addKeyFrame(camera, target, currentFrame):
    head = target.pose.bones['Head']
    rad = (((currentFrame-1) / 1147) * 360) / 180 * pi
    camera.location[0] = head.location[0] + 10 * cos(rad)
    camera.location[1] = head.location[1] + 10 * sin(rad)
    bpy.ops.anim.keyframe_insert(type='Location', confirm_success=True)
    return

  
def run(origin):
    # set the start and end frame
    scn = bpy.context.scene
    scn.frame_start = 1
    scn.frame_end = 1147
    
    # get the skel_obj
    skel_obj = bpy.data.objects['131_09_60fps']
    skel_obj.select = False
    
    # delete all objects excapt armature
    for ob in scn.objects:
        if ob.name != '131_09_60fps':
            bpy.data.objects[ob.name].select = True
            bpy.ops.object.delete()
            
    # crate a camera
    bpy.ops.object.add(type='CAMERA')        
    rot_cam = bpy.context.object
    rot_cam.name = 'rot_cam'
    rot_cam.lock_location[2] = True
    rot_cam.rotation_mode = 'XYZ'   
    rot_cam.select = True
    
    # add a copy location constarin to camera
    addCopyLocationConstraint(rot_cam, 'location', skel_obj)
    
    # add a distance constraint to camera
    addDistanceConstraint(rot_cam, 'distance', skel_obj)
                
    # add a track constraint to camera
    addTrackToConstraint(rot_cam, 'tracking', skel_obj)
    
    # add keyframe to each frame and rotate the camera 1 degree per frame:
    i = 1
    while i < 1147: 
        scn.frame_current = i
        addKeyFrame(rot_cam, skel_obj, i)
        i += 1
          
    return
 
 
if __name__ == "__main__":
    run((0,0,0))
    bpy.ops.screen.animation_play(reverse=False, sync=False)

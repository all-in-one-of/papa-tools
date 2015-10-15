import maya.cmds as cmds
from functools import partial

prefix = ''
browMacro = []
browMinor = []
upperFaceMacro = []
upperFaceMinor = []
lowerFaceMacro = []
lowerFaceMinor = []
mouthMacro = []
mouthMinor = []
minorCtrl = []
microCtrl = []


def nameThings(prefix):
       
    browMacroTemp = [prefix + 'gui_master_brow_UD_ctrl', prefix + 'gui_rt_brow_inn_UD_ctrl', prefix + 'gui_rt_brow_mid_UD_ctrl', prefix + 'gui_rt_brow_out_UD_ctrl', prefix + 'gui_lf_brow_inn_UD_ctrl', prefix + 'gui_lf_brow_mid_UD_ctrl', prefix + 'gui_lf_brow_out_UD_ctrl', prefix + 'gui_rt_brow_scrunch_ctrl', prefix + 'gui_lf_brow_scrunch_ctrl']
    browMacro.extend(browMacroTemp)
    browMinorTemp = [prefix + 'gui_rt_brow_inn_TW_ctrl', prefix + 'gui_rt_brow_mid_TW_ctrl', prefix + 'gui_rt_brow_out_TW_ctrl', prefix + 'gui_lf_brow_inn_TW_ctrl', prefix + 'gui_lf_brow_mid_TW_ctrl', prefix + 'gui_lf_brow_out_TW_ctrl', prefix + 'gui_rt_brow_out_LR_ctrl', prefix + 'gui_rt_brow_mid_LR_ctrl', prefix + 'gui_rt_brow_inn_LR_ctrl', prefix + 'gui_lf_brow_inn_LR_ctrl', prefix + 'gui_lf_brow_mid_LR_ctrl', prefix + 'gui_lf_brow_out_LR_ctrl', prefix + 'gui_rt_brow_inn_FB_ctrl', prefix + 'gui_rt_brow_mid_FB_ctrl', prefix + 'gui_rt_brow_out_FB_ctrl', prefix + 'gui_lf_brow_inn_FB_ctrl', prefix + 'gui_lf_brow_mid_FB_ctrl', prefix + 'gui_lf_brow_out_FB_ctrl']
    browMinor.extend(browMinorTemp)
    
    upperFaceMacroTemp = [prefix +'gui_lf_eyelidUp_ctrl', prefix + 'gui_lf_eyelidLo_ctrl', prefix +'gui_rt_eyelidLo_ctrl', prefix +'gui_rt_eyelidUp_ctrl', prefix + 'gui_rt_eyelidUp_inn_UD_ctrl', prefix + 'gui_rt_eyelidUp_mid_UD_ctrl', prefix + 'gui_rt_eyelidUp_out_UD_ctrl', prefix + 'gui_lf_eyelidUp_inn_UD_ctrl', prefix + 'gui_lf_eyelidUp_mid_UD_ctrl', prefix + 'gui_lf_eyelidUp_out_UD_ctrl', prefix + 'gui_rt_eyePop_ctrl', prefix + 'gui_rt_iris_ctrl', prefix + 'gui_rt_pupil_ctrl', prefix + 'gui_lf_eyePop_ctrl', prefix + 'gui_lf_iris_ctrl', prefix + 'gui_lf_pupil_ctrl', prefix + 'gui_rt_eye_height_ctrl', prefix + 'gui_lf_eye_height_ctrl', prefix + 'gui_rt_eyelidLo_inn_UD_ctrl', prefix + 'gui_rt_eyelidLo_mid_UD_ctrl', prefix + 'gui_rt_eyelidLo_out_UD_ctrl', prefix + 'gui_rt_squint_ctrl', prefix + 'gui_lf_eyelidLo_inn_UD_ctrl', prefix + 'gui_lf_eyelidLo_mid_UD_ctrl', prefix + 'gui_lf_eyelidLo_out_UD_ctrl', prefix + 'gui_lf_squint_ctrl']
    upperFaceMacro.extend(upperFaceMacroTemp)	
    upperFaceMinorTemp = [prefix + 'gui_rt_eyelidUp_out_LR_ctrl', prefix + 'gui_rt_eyelidUp_mid_LR_ctrl', prefix + 'gui_rt_eyelidUp_inn_LR_ctrl', prefix + 'gui_lf_eyelidUp_inn_LR_ctrl', prefix + 'gui_lf_eyelidUp_mid_LR_ctrl', prefix + 'gui_lf_eyelidUp_out_LR_ctrl', prefix + 'gui_rt_eye_ctrl', prefix + 'gui_lf_eye_ctrl', prefix + 'gui_rt_eyelidLo_out_LR_ctrl', prefix + 'gui_rt_eyelidLo_mid_LR_ctrl', prefix + 'gui_rt_eyelidLo_inn_LR_ctrl', prefix + 'gui_lf_eyelidLo_inn_LR_ctrl', prefix + 'gui_lf_eyelidLo_mid_LR_ctrl', prefix + 'gui_lf_eyelidLo_out_LR_ctrl', prefix + 'gui_rt_squint_LR_ctrl', prefix + 'gui_lf_squint_LR_ctrl', prefix + 'gui_rt_squint_inn_ctrl', prefix + 'gui_rt_squint_mid_ctrl', prefix + 'gui_rt_squint_out_ctrl', prefix + 'gui_lf_squint_inn_ctrl', prefix + 'gui_lf_squint_mid_ctrl', prefix + 'gui_lf_squint_out_ctrl', prefix + 'gui_rt_squint_LR_ctrl', prefix + 'gui_lf_squint_LR_ctrl', prefix + 'gui_rt_squint_inn_LR_ctrl', prefix + 'gui_rt_squint_mid_LR_ctrl', prefix + 'gui_rt_squint_out_LR_ctrl', prefix + 'gui_lf_squint_inn_LR_ctrl', prefix + 'gui_lf_squint_mid_LR_ctrl', prefix + 'gui_lf_squint_out_LR_ctrl']
    upperFaceMinor.extend(upperFaceMinorTemp)
    
    lowerFaceMacroTemp = [prefix + 'gui_jaw_box_ctrl', prefix + 'gui_rt_sneer_ctrl', prefix + 'gui_lf_sneer_ctrl', prefix + 'gui_rt_flare_ctrl', prefix + 'gui_lf_flare_ctrl', prefix + 'gui_rt_lipCorner_ctrl', prefix + 'gui_jaw_ctrl', prefix + 'gui_lf_lipCorner_ctrl', prefix + 'gui_jaw_drop_ctrl', prefix + 'gui_stickyLips_ctrl']
    lowerFaceMacro.extend(lowerFaceMacroTemp)	
    lowerFaceMinorTemp = [prefix + 'gui_rt_nose_micro_ctrl', prefix + 'gui_rt_nose_TW_ctrl', prefix + 'gui_rt_nose_FB_ctrl', prefix + 'gui_rt_lipCorner_UD_ctrl', prefix + 'gui_rt_jaw_micro_ctrl', prefix + 'gui_rt_jaw_TW_ctrl', prefix + 'gui_rt_jaw_FB_ctrl', prefix + 'gui_lf_lipCorner_UD_ctrl']
    lowerFaceMinor.extend(lowerFaceMinorTemp)	
    
    mouthMacroTemp = [prefix + 'gui_lowerLip_UD_ctrl',prefix + 'gui_upperLip_rt_CURL_ctrl', prefix + 'gui_upperLip_mid_CURL_ctrl', prefix + 'gui_upperLip_lf_CURL_ctrl', prefix + 'gui_upperLip_CURL_ctrl', prefix + 'gui_lowerLip_rt_CURL_ctrl', prefix +'gui_lowerLip_mid_CURL_ctrl', prefix + 'gui_lowerLip_lf_CURL_ctrl', prefix + 'gui_lowerLip_CURL_ctrl', prefix +'gui_upperLip_UD_ctrl', prefix + 'gui_upperLip_rt_UD_ctrl', prefix + 'gui_upperLip_mid_UD_ctrl', prefix + 'gui_upperLip_lf_UD_ctrl', prefix + 'gui_lowerLip_rt_UD_ctrl', prefix + 'gui_lowerLip_mid_UD_ctrl', prefix + 'gui_lowerLip_lf_UD_ctrl']
    mouthMacro.extend(mouthMacroTemp)
    mouthMinorTemp = [prefix + 'gui_rt_mouth_TW_ctrl', prefix + 'gui_rt_mouth_FB_ctrl', prefix + 'gui_mouth_micro_ctrl', prefix + 'gui_upperLip_rt_LR_ctrl', prefix + 'gui_upperLip_mid_LR_ctrl', prefix + 'gui_upperLip_lf_LR_ctrl', prefix + 'gui_lowerLip_rt_LR_ctrl', prefix + 'gui_lowerLip_mid_LR_ctrl', prefix + 'gui_lowerLip_lf_LR_ctrl', prefix + 'gui_upperLip_rt_FB_ctrl', prefix + 'gui_upperLip_mid_FB_ctrl', prefix + 'gui_upperLip_lf_FB_ctrl', prefix + 'gui_lowerLip_rt_FB_ctrl', prefix + 'gui_lowerLip_mid_FB_ctrl', prefix + 'gui_lowerLip_lf_FB_ctrl']
    mouthMinor.extend(mouthMinorTemp)
    minorCtrlTemp = [prefix + 'grp_gui_lf_brow_out_FB', prefix + 'lf_nose_FB_label', prefix + 'grp_gui_lf_eyelidLo_out_LR_ctrl', prefix + 'grp_gui_rt_brow_out_FB', prefix + 'grp_gui_lf_lipCorner_UD', prefix + 'grp_gui_upperLip_mid_LR_ctrl', prefix + 'grp_gui_rt_brow_out_LR_ctrl' ,prefix + 'grp_gui_upperLip_lf_FB' , prefix + 'grp_gui_mouth_micro' , prefix + 'grp_gui_lf_brow_inn_FB', prefix + 'rt_brow_twist_label' , prefix + 'grp_gui_lf_squint_out' , prefix + 'grp_gui_lf_squint_inn',prefix + 'lf_jaw_FB_label' ,prefix + 'mouth_FB_label' , prefix + 'grp_gui_rt_eye', prefix + 'mouth_TW_label' , prefix + 'grp_gui_rt_nose_micro', prefix + 'grp_gui_lf_squint_mid' ,prefix + 'lf_brow_twist_label' , prefix + 'grp_gui_rt_squint_out' , prefix + 'grp_gui_rt_eyelidUp_out_LR_ctrl' , prefix + 'grp_gui_lf_eyelidLo_mid_LR_ctrl' , prefix + 'grp_gui_rt_jaw_micro' , prefix + 'grp_gui_lf_brow_inn_TW' , prefix + 'grp_gui_lowerLip_rt_FB' , prefix + 'grp_gui_upperLip_rt_FB',prefix + 'rt_brow_forward_back_label' , prefix + 'grp_gui_upperLip_lf_LR_ctrl',prefix + 'rt_nose_TW_label' , prefix + 'grp_gui_lowerLip_mid_LR_ctrl' , prefix + 'grp_gui_rt_brow_mid_LR_ctrl' , prefix + 'grp_gui_rt_nose_FB', prefix + 'lf_brow_forward_back_label' , prefix + 'grp_gui_lowerLip_mid_FB' , prefix + 'grp_gui_rt_brow_inn_TW' , prefix + 'grp_gui_lf_eyelidLo_inn_LR_ctrl' , prefix + 'grp_gui_lf_brow_out_TW' , prefix + 'grp_gui_rt_squint_mid' , prefix + 'grp_gui_rt_eyelidUp_mid_LR_ctrl' ,prefix + 'lf_lipCorner_label' , prefix + 'grp_gui_rt_jaw_FB' , prefix + 'grp_gui_lowerLip_rt_LR_ctrl' , prefix + 'grp_gui_rt_brow_inn_LR_ctrl' , prefix + 'grp_gui_lf_brow_mid_LR_ctrl', prefix + 'rt_jaw_TW_label' , prefix + 'grp_gui_rt_eyelidLo_mid_LR_ctrl' , prefix + 'grp_gui_rt_squint_LR_ctrl' , prefix + 'grp_gui_rt_mouth_FB' , prefix + 'grp_gui_lowerLip_lf_LR_ctrl' , prefix + 'grp_gui_rt_eyelidUp_inn_LR_ctrl' ,prefix + 'rt_lipCorner_label' , prefix + 'grp_gui_rt_brow_inn_FB' ,prefix + 'lip_FB_label' , prefix + 'grp_gui_lowerLip_lf_FB' , prefix + 'grp_gui_lf_brow_mid_TW' , prefix + 'grp_gui_rt_brow_mid_FB' , prefix + 'grp_gui_rt_brow_out_TW' , prefix + 'grp_gui_lf_brow_mid_FB' , prefix + 'grp_gui_lf_eyelidUp_inn_LR_ctrl' , prefix + 'grp_gui_lf_eyelidUp_out_LR_ctrl' , prefix + 'grp_gui_rt_nose_TW' , prefix + 'grp_gui_lf_squint_LR_ctrl' , prefix + 'grp_gui_rt_jaw_TW' , prefix + 'grp_gui_rt_lipCorner_UD' , prefix + 'grp_gui_rt_squint_inn', prefix + 'nose_label', prefix + 'mouth_label' , prefix + 'grp_gui_lf_brow_inn_LR_ctrl' , prefix + 'grp_gui_rt_eyelidLo_inn_LR_ctrl' , prefix + 'grp_gui_rt_eyelidLo_out_LR_ctrl' , prefix + 'grp_gui_lf_brow_out_LR_ctrl' , prefix + 'grp_gui_upperLip_mid_FB' , prefix + 'grp_gui_rt_brow_mid_TW' , prefix + 'grp_gui_rt_mouth_TW' , prefix + 'grp_gui_upperLip_rt_LR_ctrl' , prefix + 'grp_gui_lf_eyelidUp_mid_LR_ctrl' , prefix + 'grp_gui_lf_eye']
    minorCtrl.extend(minorCtrlTemp)
    microCtrlTemp = [prefix + 'papa_rt_EyeLid_ctrl', prefix + 'papa_rt_EyeLidUp_ctrl', prefix + 'papa_rt_EyeLidUpInn_ctrl', prefix + 'papa_rt_EyeLidUpMid_ctrl', prefix + 'papa_rt_EyeLidUpOut_ctrl', prefix + 'papa_rt_EyeLidLo_ctrl', prefix + 'papa_rt_EyeLidLoInn_ctrl', prefix + 'papa_rt_EyeLidLoMid_ctrl', prefix + 'papa_rt_EyeLidLoOut_ctrl', prefix + 'papa_lf_EyeLid_ctrl', prefix + 'papa_lf_EyeLidUp_ctrl', prefix + 'papa_lf_EyeLidUpInn_ctrl', prefix + 'papa_lf_EyeLidUpMid_ctrl', prefix + 'papa_lf_EyeLidUpOut_ctrl', prefix + 'papa_lf_EyeLidLo_ctrl', prefix + 'papa_lf_EyeLidLoInn_ctrl', prefix + 'papa_lf_EyeLidLoMid_ctrl', prefix + 'papa_lf_EyeLidLoOut_ctrl', prefix + 'papa_lf_brow_ctrl', prefix + 'papa_lf_inn_brow_ctrl', prefix + 'papa_lf_mid_brow_ctrl', prefix + 'papa_lf_out_brow_ctrl', prefix + 'papa_rt_brow_ctrl', prefix + 'papa_rt_inn_brow_ctrl', prefix + 'papa_rt_mid_brow_ctrl', prefix + 'papa_rt_out_brow_ctrl', prefix + 'papa_mouth_ctrl', prefix + 'papa_lipUp_ctrl', prefix + 'papa_lf_lipUp_ctrl', prefix + 'papa_mid_lipUp_ctrl', prefix + 'papa_rt_lipUp_ctrl', prefix + 'papa_lipLo_ctrl', prefix + 'papa_lf_lipLo_ctrl', prefix + 'papa_mid_lipLo_ctrl', prefix + 'papa_lipLo_ctrl', prefix + 'papa_rt_lipLo_ctrl', prefix + 'papa_rt_lipLo_ctrl', prefix + 'papa_jaw_ctrl', prefix + 'papa_jaw_xtra_ctrl', prefix + 'papa_lf_corner_ctrl', prefix + 'papa_rt_corner_ctrl', prefix + 'papa_nose_ctrl', prefix + 'papa_lf_nose_ctrl', prefix + 'papa_rt_nose_ctrl', prefix + 'papa_lf_cheek_ctrl', prefix + 'papa_lf_inn_cheek_ctrl', prefix + 'papa_lf_mid_cheek_ctrl', prefix + 'papa_lf_out_cheek_ctrl', prefix + 'papa_rt_cheek_ctrl', prefix + 'papa_rt_inn_cheek_ctrl', prefix + 'papa_rt_mid_cheek_ctrl', prefix + 'papa_rt_out_cheek_ctrl']
    microCtrl.extend(microCtrlTemp)
    
def microVisibility(prefix, *args):
    if(cmds.getAttr(prefix + 'grp_papa_facial_ctrl.v')==False):
        cmds.setAttr(prefix + 'grp_papa_facial_ctrl.v', 1)
        return
    elif(cmds.getAttr(prefix + 'grp_papa_facial_ctrl.v')==True):
        cmds.setAttr(prefix + 'grp_papa_facial_ctrl.v', 0)
        return

def minorVisibility(prefix, *args):
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==False):
        cmds.setAttr(prefix + 'gui_micro_vis_ctrl.v', 1)
        for s in minorCtrl:
            cmds.setAttr(s + '.v', 1)
        return
    elif(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        cmds.setAttr(prefix + 'gui_micro_vis_ctrl.v', 0)
        for s in minorCtrl:
            cmds.setAttr(s + '.v', 0)
        return      
             
        
def keyMinor(*args):
    for i in browMinor:
        cmds.setKeyframe(i)
    for i in upperFaceMinor:
        cmds.setKeyframe(i)
    for i in lowerFaceMinor:
        cmds.setKeyframe(i)
    for i in mouthMinor:
        cmds.setKeyframe(i)
        
def clearAll(*args):
    for i in browMacro:
        cmds.cutKey(i, s=True)
    for i in browMinor:
        cmds.cutKey(i, s=True)
    for i in upperFaceMacro:
        cmds.cutKey(i, s=True)
    for i in upperFaceMinor:
        cmds.cutKey(i, s=True)        
    for i in lowerFaceMacro:
        cmds.cutKey(i, s=True)
    for i in lowerFaceMinor:
        cmds.cutKey(i, s=True)
    for i in mouthMacro:
        cmds.cutKey(i, s=True)
    for i in mouthMinor:
        cmds.cutKey(i, s=True)
        
def resetMicro(*args):
    for i in microCtrl:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)
        cmds.setAttr(i + '.translateZ', 0)
        cmds.setAttr(i + '.rotateX', 0)
        cmds.setAttr(i + '.rotateY', 0)
        cmds.setAttr(i + '.rotateZ', 0)
        cmds.setAttr(i + '.scaleX', 1)
        cmds.setAttr(i + '.scaleY', 1)
        cmds.setAttr(i + '.scaleZ', 1)        

        
def keyAll(prefix, *args):
    print prefix
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        for i in browMacro:
            cmds.setKeyframe(i)
        for i in browMinor:
            cmds.setKeyframe(i)
        for i in upperFaceMacro:
            cmds.setKeyframe(i)
        for i in upperFaceMinor:
            cmds.setKeyframe(i)       
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)
        for i in lowerFaceMinor:
            cmds.setKeyframe(i)
        for i in mouthMacro:
            cmds.setKeyframe(i)
        for i in mouthMinor:
            cmds.setKeyframe(i)
    else:
        for i in browMacro:
            cmds.setKeyframe(i)
        for i in upperFaceMacro:
            cmds.setKeyframe(i)      
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)
        for i in mouthMacro:
            cmds.setKeyframe(i)     
               
def resetAll(*args):
    for i in browMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)        
       
    for i in browMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)  
        cmds.setAttr(i + '.rotateZ', 0)     
       
    for i in upperFaceMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)
        cmds.setAttr('gui_rt_eyelidUp_ctrl.translateY', -1)
        cmds.setAttr('gui_rt_eyelidLo_ctrl.translateY', -1)
        cmds.setAttr('gui_lf_eyelidUp_ctrl.translateY', -1)
        cmds.setAttr('gui_lf_eyelidLo_ctrl.translateY', -1)     
      
    for i in upperFaceMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)   
    
    for i in lowerFaceMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
              
    for i in lowerFaceMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0) 
        cmds.setAttr(i + '.rotateZ', 0)      
     
    for i in mouthMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)  

    for i in mouthMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)   
        cmds.setAttr(i + '.rotateZ', 0)    
             
                
def keyBrows(prefix, *args):
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        for i in browMacro:
            cmds.setKeyframe(i)
        for i in browMinor:
            cmds.setKeyframe(i)
    else:
        for i in browMacro:
            cmds.setKeyframe(i)
     
def keyUpperFace(prefix, *args):
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        for i in upperFaceMacro:
            cmds.setKeyframe(i)
        for i in upperFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in upperFaceMacro:
            cmds.setKeyframe(i)  

def keyLowerFace(prefix, *args):
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)
        for i in lowerFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)  

def keyMouth(prefix, *args):
    if(cmds.getAttr(prefix + 'gui_micro_vis_ctrl.v')==True):
        for i in mouthMacro:
            cmds.setKeyframe(i)
        for i in mouthMinor:
            cmds.setKeyframe(i)            
    else:
        for i in mouthMacro:
            cmds.setKeyframe(i)  

def theyPushedIt(*args):
    confirm = cmds.confirmDialog( title='Confirm', message='Are you sure?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    print confirm
    if(confirm == 'Yes'):
        confirm2 = cmds.confirmDialog( title='Please Click No', message='Are you REALLY sure?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if(confirm2 == 'Yes'):
            confirm3 = cmds.confirmDialog( title='WHY!', message='Dont you understand the meaning of the word DONT?!? Continue Anyways?', button=['Im really set on this','No, Im good now'], defaultButton='Im really set on this', cancelButton='No, Im good now', dismissString='No')
            if(confirm3 == 'Im really set on this'):
                confirm4 = cmds.confirmDialog( title='NOOOOOOOOOOOOO', message='THIS IS YOUR LAST CHANCE TO TURN BACK!', button=['DO IT!','Hmmm, maybe I shouldnt'], defaultButton='DO IT!', cancelButton='Hmmm, maybe I shouldnt', dismissString='No')
                if(confirm4 == 'DO IT!'):
                    DOIT()
                else:
                    cmds.confirmDialog(title='...', message = 'I need an aspirin.', button='...')
            else:
                cmds.confirmDialog(title='That was close.', message = 'Too close.', button='You possibly saved the film.')              
        else:
            cmds.confirmDialog(title='Oh good', message = 'Glad you thought it through', button='Happy Animating!')            
    else:
        cmds.confirmDialog(title='Whoosh.', message = 'That could have been catastrophic', button='Thanks for understanding')
    

def DOIT(*args):
    cameralist = cmds.listCameras()
    imageFile = '/groups2/papa/Rigging'
    for i in cameralist:
        imagePlaneName = cmds.imagePlane(c=i)
        print imagePlaneName
        cmds.setAttr(imagePlaneName[0] + '.imageName', '/groups2/papa/Rigging/theInspiration.JPG', type='string')
        
    
    cmds.warning('Welp, you asked for it.')
    
########CREATE WINDOW#########    

def go():

	if cmds.objExists('papa_papa_rig_stable:cam_GUI_papa_01') == True:
		prefix = 'papa_papa_rig_stable:'
		
	elif cmds.objExists('cam_GUI_papa_01') == True: 
		prefix = ''
		
	else:
		confirm = cmds.confirmDialog(title='Error', message='Make sure Papa is in your scene.', button='Ok', defaultButton='Ok')
		return
    
	if cmds.windowPref('window',exists=True): cmds.windowPref('window',remove=True)
	if cmds.window('window',exists=True): cmds.deleteUI('window',wnd=True)
	
	nameThings(prefix)
	
	newWindow = cmds.window('window', title = 'Papa Facial GUI', s=True, w=560)
	form = cmds.formLayout(w=560)
	papaEditor = cmds.modelEditor()
	papaAll = cmds.button(label = 'Key All', w=50, command = partial(keyAll, prefix))
	papaRowTop = cmds.rowLayout(w=560,parent = form, nc=3)
	papaClearAll = cmds.button(label = 'Clear All', w= 182, command = clearAll)
	papaResetMicro = cmds.button(label = 'Reset Micro Ctrl', w=182, command = resetMicro)
	papaResetAll = cmds.button(label = 'Reset All GUI Ctrl', w= 182, command = resetAll)
	
	cmds.setParent( '..' )
	papaColumn = cmds.columnLayout(w=560)
	cmds.button(label = 'K', height=173, command = partial(keyBrows, prefix))
	cmds.button(label = 'K', height=185, command = partial(keyUpperFace, prefix))
	cmds.button(label = 'K', height=330, command = partial(keyLowerFace, prefix))
	cmds.button(label = 'K', height=185, command = partial(keyMouth, prefix))
	papaRow = cmds.rowLayout(parent = form, nc=3)
	cmds.button(label = 'Toggle GUI Minor Controls', w=182, command = partial(minorVisibility, prefix))
	cmds.button(label = 'Toggle Micro Controls', w=182, command = partial(microVisibility, prefix))
	cmds.button(label = 'DONT CLICK THIS BUTTON', w=182, command = theyPushedIt)
	cmds.formLayout( form, edit=True, attachForm=[(papaEditor, 'top', 5), (papaEditor, 'left', 5), (papaAll, 'left', 5), (papaAll, 'right', 5), (papaRowTop, 'left', 5), (papaRowTop, 'right', 5), (papaRow, 'left', 5), (papaRow, 'bottom', 5), (papaRow, 'right', 5), (papaColumn, 'top', 5), (papaColumn, 'right', 5) ], attachControl=[(papaEditor, 'bottom', 5, papaAll), (papaColumn, 'bottom', 5, papaAll), (papaAll, 'bottom', 5, papaRowTop),(papaRowTop, 'bottom', 5, papaRow)], attachPosition=[(papaEditor, 'right', 0, 96), (papaColumn, 'left', 0, 96)], attachNone=(papaAll, 'top') )
	
	cmds.modelEditor( papaEditor, edit=True, camera= prefix + 'cam_GUI_papa_01', wos=False, hud=False, gr=False, da = "smoothShaded", handles=False)
	
	cmds.showWindow(newWindow)

	
go()
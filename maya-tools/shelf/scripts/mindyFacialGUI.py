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


def nameThings(prefix):
	    
	browMacroTemp = [prefix + 'cc_rEyeBrowOut_01', prefix + 'cc_rEyeBrowMid_01', prefix + 'cc_rEyeBrowInn_01', prefix + 'cc_rEyeBrowScrunch_01', prefix + 'cc_EyeBrows_01', prefix + 'cc_lEyeBrowScrunch_01', prefix + 'cc_lEyeBrowInn_01', prefix + 'cc_lEyeBrowMid_01', prefix + 'cc_lEyeBrowOut_01']
	browMacro.extend(browMacroTemp)
	browMinorTemp = [prefix + 'cc_lBrowTWMid_01', prefix + 'cc_rBrowTWMid_01', prefix + 'cc_lBrowTWOut_01', prefix + 'cc_rBrowTWOut_01', prefix + 'cc_rBrowTWInn_01', prefix + 'cc_rBrowFBOut_01', prefix + 'cc_rBrowFBMid_01', prefix + 'cc_rBrowFBInn_01', prefix + 'cc_lBrowFBInn_01', prefix + 'cc_lBrowFBMid_01', prefix + 'cc_lBrowFBOut_01', prefix + 'cc_lBrowTWInn_01', prefix + 'cc_minor_rEyeBrowOutLR_01', prefix + 'cc_minor_rEyeBrowMidLR_01', prefix + 'cc_minor_rEyeBrowInnLR_01', prefix + 'cc_minor_lEyeBrowInnLR_01', prefix + 'cc_minor_lEyeBrowMidLR_01', prefix + 'cc_minor_lEyeBrowOutLR_01']
	browMinor.extend(browMinorTemp)
	
	upperFaceMacroTemp = [prefix + 'cc_nose_01', prefix + 'cc_noseTW_01', prefix + 'cc_rEyeScale_01', prefix + 'cc_rSquint_01', prefix + 'cc_rIris_01', prefix + 'cc_rPupil_01', prefix + 'cc_rEye_01', prefix + 'cc_rEyeLidDwn_01', prefix + 'cc_rEyeLidAngle_01', prefix + 'cc_lEyeLidAngle_01', prefix + 'cc_rEyeLidUpp_01', prefix + 'cc_lEyeLidDwn_01', prefix + 'cc_lEyeLidUpp_01', prefix + 'cc_lEye_01', prefix + 'cc_lIris_01', prefix + 'cc_lPupil_01', prefix + 'cc_lEyeScale_01', prefix + 'cc_lSquint_01']
	upperFaceMacro.extend(upperFaceMacroTemp)	
	upperFaceMinorTemp = [prefix + 'cc_lUppEyeLidUDInn_01', prefix + 'cc_lUppEyeLidLRInn_01', prefix + 'cc_lUppEyeLidLRMid_01', prefix + 'cc_minor_rEyeBrowMid_01', prefix + 'cc_lUppEyeLidUDOut_01', prefix + 'cc_lUppEyeLidLROut_01', prefix + 'cc_lDwnEyeLidUDInn_01', prefix + 'cc_lDwnEyeLidLRInn_01', prefix + 'cc_lDwnEyeLidUDMid_01', prefix + 'cc_lDwnEyeLidLRMid_01', prefix + 'cc_lDwnEyeLidUDOut_01', prefix + 'cc_lDwnEyeLidLROut_01', prefix + 'cc_minor_lSquintLROut_01', prefix + 'cc_rSquintOut_01', prefix + 'cc_minor_rSquintLROut_01', prefix + 'cc_rSquintMid_01', prefix + 'cc_minor_rSquintLRMid_01', prefix + 'cc_rSquintInn_01', prefix + 'cc_minor_rSquintLRInn_01', prefix + 'cc_rUppEyeLidUDOut_01', prefix + 'cc_rUppEyeLidLROut_01', prefix + 'cc_rUppEyeLidUDMid_01', prefix + 'cc_rUppEyeLidLRMid_01', prefix + 'cc_rUppEyeLidUDInn_01', prefix + 'cc_rUppEyeLidLRInn_01', prefix + 'cc_rDwnEyeLidUDOut_01', prefix + 'cc_rDwnEyeLidLROut_01', prefix + 'cc_rDwnEyeLidUDMid_01', prefix + 'cc_rDwnEyeLidLRMid_01', prefix + 'cc_rDwnEyeLidUDInn_01', prefix + 'cc_rDwnEyeLidLRInn_01', prefix + 'cc_lSquintInn_01', prefix + 'cc_minor_lSquintLRInn_01', prefix + 'cc_lSquintMid_01', prefix + 'cc_minor_lSquintLRMid_01', prefix + 'cc_lSquintOut_01', prefix + 'cc_rUppEyeLidLROut_01', prefix + 'cc_rUppEyeLidLRMid_01', prefix + 'cc_rUppEyeLidLRInn_01', prefix + 'cc_minor_rSquintLR_01', prefix + 'cc_rDwnEyeLidLROut_01', prefix + 'cc_rDwnEyeLidLRMid_01', prefix + 'cc_rDwnEyeLidLRInn_01', prefix + 'cc_lDwnEyeLidLRInn_01', prefix + 'cc_lDwnEyeLidLRMid_01', prefix + 'cc_lDwnEyeLidLROut_01', prefix + 'cc_minor_lSquintLR_01', prefix + 'cc_lUppEyeLidLRInn_01', prefix + 'cc_lUppEyeLidLRMid_01', prefix + 'cc_lUppEyeLidLROut_01']
	upperFaceMinor.extend(upperFaceMinorTemp)
	
	lowerFaceMacroTemp = [prefix + 'cc_uppLipUDRgt_01', prefix + 'cc_uppLidUDMid_01', prefix + 'cc_uppLipUDLft_01', prefix + 'cc_dwnLipUDRgt_01', prefix + 'cc_dwnLidUDMid_01', prefix + 'cc_dwnLipUDLft_01', prefix + 'cc_rSneer_01', prefix + 'cc_lSneer_01', prefix + 'cc_lMouthCorner_01', prefix + 'cc_rMouthCorner_01', prefix + 'cc_jaw_01', prefix + 'cc_jawUp_01', prefix + 'cc_stickyLips_01']
	lowerFaceMacro.extend(lowerFaceMacroTemp)	
	lowerFaceMinorTemp = [prefix + 'cc_jawTW_01', prefix + 'cc_uppLipLRRgt_01', prefix + 'cc_uppLipLRMid_01', prefix + 'cc_uppLipLRLft_01', prefix + 'cc_minor_rSneerLR_01', prefix + 'cc_minor_lSneerLR_01', prefix + 'cc_uppLipFBLft_01', prefix + 'cc_uppLipFBRgt_01', prefix + 'cc_uppLipFBMid_01', prefix + 'cc_dwnLipLRRgt_01', prefix + 'cc_dwnLipLRMid_01', prefix + 'cc_dwnLipLRLft_01', prefix + 'cc_dwnLipFBLft_01', prefix + 'cc_dwnLipFBMid_01', prefix + 'cc_dwnLipFBRgt_01', prefix + 'cc_jawJutt_01', prefix + 'cc_jawUD_01', prefix + 'cc_jawLR_01', prefix + 'cc_uppLipCRRgt_01', prefix + 'cc_uppLipCRMid_01', prefix + 'cc_uppLipCRLft_01', prefix + 'cc_dwnLipCRRgt_01', prefix + 'cc_dwnLipCRMid_01', prefix + 'cc_dwnLipCRLft_01', prefix + 'cc_uppLipSCALELft_01', prefix + 'cc_uppLipSCALEMid_01', prefix + 'cc_uppLipSCALERgt_01', prefix + 'cc_dwnLipSCALELft_01', prefix + 'cc_dwnLipSCALEMid_01', prefix + 'cc_dwnLipSCALERgt_01', prefix + 'cc_minor_lMouthCorner_01', prefix + 'cc_minor_rMouthCorner_01']
	lowerFaceMinor.extend(lowerFaceMinorTemp)	
	
	mouthMacroTemp = [prefix + 'cc_mouth_01', prefix + 'cc_uppLipCurl_01', prefix + 'cc_dwnLipCurl_01']
	mouthMacro.extend(mouthMacroTemp)
	mouthMinorTemp = [prefix + 'cc_mouthTW_01', prefix + 'cc_mouthFB_01']
	mouthMinor.extend(mouthMinorTemp)
    
def microVisibility(prefix, *args):
    if(cmds.getAttr(prefix + 'grp_micro_face_controls_01.v')==False):
        cmds.setAttr(prefix + 'grp_micro_face_controls_01.v', 1)
        return
    elif(cmds.getAttr(prefix + 'grp_micro_face_controls_01.v')==True):
        cmds.setAttr(prefix + 'grp_micro_face_controls_01.v', 0)
        return

def minorVisibility(prefix, *args):
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==False):
        cmds.setAttr(prefix + 'cc_minorHelper_01.v', 1)
        return
    elif(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
        cmds.setAttr(prefix + 'cc_minorHelper_01.v', 0)
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


def keyAll(prefix, *args):
    print prefix
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
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
        cmds.setAttr(i + '.translateZ', 0)          
    for i in browMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)          
    for i in upperFaceMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)          
    for i in upperFaceMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)          
    for i in lowerFaceMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)                  
    for i in lowerFaceMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)          
    for i in mouthMacro:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)
    for i in mouthMinor:
        cmds.setAttr(i + '.translateX', 0)
        cmds.setAttr(i + '.translateY', 0)      
        cmds.setAttr(i + '.translateZ', 0)                 
                
def keyBrows(prefix, *args):
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
        for i in browMacro:
            cmds.setKeyframe(i)
        for i in browMinor:
            cmds.setKeyframe(i)
    else:
        for i in browMacro:
            cmds.setKeyframe(i)
     
def keyUpperFace(prefix, *args):
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
        for i in upperFaceMacro:
            cmds.setKeyframe(i)
        for i in upperFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in upperFaceMacro:
            cmds.setKeyframe(i)  

def keyLowerFace(prefix, *args):
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)
        for i in lowerFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)  

def keyMouth(prefix, *args):
    if(cmds.getAttr(prefix + 'cc_minorHelper_01.v')==True):
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

def go():

	if cmds.objExists('papa_mindy_rig_stable:cam_GUIMINDY_01') == True:
		prefix = 'papa_mindy_rig_stable:'
		
	elif cmds.objExists('cam_GUIMINDY_01') == True: 
		prefix = ''
		
	else:
		confirm = cmds.confirmDialog(title='Error', message='Make sure Mindy is in your scene.', button='Ok', defaultButton='Ok')
		return
    
	if cmds.windowPref('window',exists=True): cmds.windowPref('window',remove=True)
	if cmds.window('window',exists=True): cmds.deleteUI('window',wnd=True)
	
	nameThings(prefix)
	
	newWindow = cmds.window('window', title = 'Mindy Facial GUI', s=False, w=605)
	form = cmds.formLayout(w=605)
	mindyEditor = cmds.modelEditor()
	mindyAll = cmds.button(label = 'Key All', w=50, command = partial(keyAll, prefix))
	mindyRowTop = cmds.rowLayout(parent = form, nc=2)
	mindyClearAll = cmds.button(label = 'Clear All', w= 296, command = clearAll)
	mindyResetAll = cmds.button(label = 'Reset All', w= 296, command = resetAll)
	cmds.setParent( '..' )
	mindyColumn = cmds.columnLayout(w=605)
	cmds.button(label = 'K', height=158, command = partial(keyBrows, prefix))
	cmds.button(label = 'K', height=198, command = partial(keyUpperFace, prefix))
	cmds.button(label = 'K', height=295, command = partial(keyLowerFace, prefix))
	cmds.button(label = 'K', height=160, command = partial(keyMouth, prefix))
	mindyRow = cmds.rowLayout(parent = form, nc=3)
	cmds.button(label = 'Toggle Minor Controls', w=195, command = partial(minorVisibility, prefix))
	cmds.button(label = 'Toggle Micro Controls', w=200, command = partial(microVisibility, prefix))
	cmds.button(label = 'DONT CLICK THIS BUTTON', w=195, command = theyPushedIt)
	
	cmds.formLayout( form, edit=True, attachForm=[(mindyEditor, 'top', 5), (mindyEditor, 'left', 5), (mindyAll, 'left', 5), (mindyAll, 'right', 5), (mindyRowTop, 'left', 5), (mindyRowTop, 'right', 5), (mindyRow, 'left', 5), (mindyRow, 'bottom', 5), (mindyRow, 'right', 5), (mindyColumn, 'top', 5), (mindyColumn, 'right', 5) ], attachControl=[(mindyEditor, 'bottom', 5, mindyAll), (mindyColumn, 'bottom', 5, mindyAll), (mindyAll, 'bottom', 5, mindyRowTop),(mindyRowTop, 'bottom', 5, mindyRow)], attachPosition=[(mindyEditor, 'right', 0, 96), (mindyColumn, 'left', 0, 96)], attachNone=(mindyAll, 'top') )
	
	cmds.modelEditor( mindyEditor, edit=True, camera= prefix + 'cam_GUIMINDY_01', wos=False, hud=False, gr=False, da = "smoothShaded", handles=False)
	
	cmds.showWindow(newWindow)

	
go()

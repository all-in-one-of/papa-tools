import maya.cmds as cmds

browMacro = ['cc_rEyeBrowOut_01', 'cc_rEyeBrowMid_01', 'cc_rEyeBrowInn_01', 'cc_rEyeBrowScrunch_01', 'cc_EyeBrows_01', 'cc_lEyeBrowScrunch_01', 'cc_lEyeBrowInn_01', 'cc_lEyeBrowMid_01', 'cc_lEyeBrowOut_01']
browMinor = ['cc_lBrowTWMid_01', 'cc_rBrowTWMid_01', 'cc_lBrowTWOut_01', 'cc_rBrowTWOut_01', 'cc_rBrowTWInn_01', 'cc_rBrowFBOut_01', 'cc_rBrowFBMid_01', 'cc_rBrowFBInn_01', 'cc_lBrowFBInn_01', 'cc_lBrowFBMid_01', 'cc_lBrowFBOut_01', 'cc_lBrowTWInn_01', 'cc_minor_rEyeBrowOutLR_01', 'cc_minor_rEyeBrowMidLR_01', 'cc_minor_rEyeBrowInnLR_01', 'cc_minor_lEyeBrowInnLR_01', 'cc_minor_lEyeBrowMidLR_01', 'cc_minor_lEyeBrowOutLR_01']
upperFaceMacro = ['cc_nose_01', 'cc_noseTW_01', 'cc_rEyeScale_01', 'cc_rSquint_01', 'cc_rIris_01', 'cc_rPupil_01', 'cc_rEye_01', 'cc_rEyeLidDwn_01', 'cc_rEyeLidAngle_01', 'cc_lEyeLidAngle_01', 'cc_rEyeLidUpp_01', 'cc_lEyeLidDwn_01', 'cc_lEyeLidUpp_01', 'cc_lEye_01', 'cc_lIris_01', 'cc_lPupil_01', 'cc_lEyeScale_01', 'cc_lSquint_01']
upperFaceMinor = ['cc_rUppEyeLidLROut_01', 'cc_rUppEyeLidLRMid_01', 'cc_rUppEyeLidLRInn_01', 'cc_minor_rSquintLR_01', 'cc_rDwnEyeLidLROut_01', 'cc_rDwnEyeLidLRMid_01', 'cc_rDwnEyeLidLRInn_01', 'cc_lDwnEyeLidLRInn_01', 'cc_lDwnEyeLidLRMid_01', 'cc_lDwnEyeLidLROut_01', 'cc_minor_lSquintLR_01', 'cc_lUppEyeLidLRInn_01', 'cc_lUppEyeLidLRMid_01', 'cc_lUppEyeLidLROut_01']
lowerFaceMacro = ['cc_rSneer_01', 'cc_lSneer_01', 'cc_lMouthCorner_01', 'cc_rMouthCorner_01', 'cc_jaw_01', 'cc_jawUp_01', 'cc_stickyLips_01']
lowerFaceMinor = ['cc_uppLipLRRgt_01', 'cc_uppLipLRMid_01', 'cc_uppLipLRLft_01', 'cc_minor_rSneerLR_01', 'cc_minor_lSneerLR_01', 'cc_uppLipFBLft_01', 'cc_uppLipFBRgt_01', 'cc_uppLipFBMid_01', 'cc_dwnLipLRRgt_01', 'cc_dwnLipLRMid_01', 'cc_dwnLipLRLft_01', 'cc_dwnLipFBLft_01', 'cc_dwnLipFBMid_01', 'cc_dwnLipFBRgt_01', 'cc_jawJutt_01', 'cc_jawUD_01', 'cc_jawLR_01', 'cc_uppLipCRRgt_01', 'cc_uppLipCRMid_01', 'cc_uppLipCRLft_01', 'cc_dwnLipCRRgt_01', 'cc_dwnLipCRMid_01', 'cc_dwnLipCRLft_01', 'cc_uppLipSCALELft_01', 'cc_uppLipSCALEMid_01', 'cc_uppLipSCALERgt_01', 'cc_dwnLipSCALELft_01', 'cc_dwnLipSCALEMid_01', 'cc_dwnLipSCALERgt_01', 'cc_minor_lMouthCorner_01', 'cc_minor_rMouthCorner_01']
mouthMacro = ['cc_uppLipCurl_01', 'cc_dwnLipCurl_01']

    
def microVisibility(*args):
    if(cmds.getAttr('grp_micro_face_controls_01.v')==False):
        cmds.setAttr('grp_micro_face_controls_01.v', 1)
        return
    elif(cmds.getAttr('grp_micro_face_controls_01.v')==True):
        cmds.setAttr('grp_micro_face_controls_01.v', 0)
        return

def minorVisibility(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==False):
        cmds.setAttr('cc_minorHelper_01.v', 1)
        return
    elif(cmds.getAttr('cc_minorHelper_01.v')==True):
        cmds.setAttr('cc_minorHelper_01.v', 0)
        return
        
def keyMinor(*args):
    for i in browMinor:
        cmds.setKeyframe(i)
    for i in upperFaceMinor:
        cmds.setKeyframe(i)
    for i in lowerFaceMinor:
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

def keyAll(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==True):
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
                
def keyBrows(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==True):
        for i in browMacro:
            cmds.setKeyframe(i)
        for i in browMinor:
            cmds.setKeyframe(i)
    else:
        for i in browMacro:
            cmds.setKeyframe(i)
     
def keyUpperFace(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==True):
        for i in upperFaceMacro:
            cmds.setKeyframe(i)
        for i in upperFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in upperFaceMacro:
            cmds.setKeyframe(i)  

def keyLowerFace(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==True):
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)
        for i in lowerFaceMinor:
            cmds.setKeyframe(i)
    else:
        for i in lowerFaceMacro:
            cmds.setKeyframe(i)  

def keyMouth(*args):
    if(cmds.getAttr('cc_minorHelper_01.v')==True):
        for i in mouthMacro:
            cmds.setKeyframe(i)
    else:
        for i in lowerFaceMacro:
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
			
		if cmds.windowPref('window',exists=True): cmds.windowPref('window',remove=True)
		if cmds.window('window',exists=True): cmds.deleteUI('window',wnd=True)

		newWindow = cmds.window('window', title = 'Mindy Facial GUI', s=False, w=605)
		form = cmds.formLayout(w=605)
		mindyEditor = cmds.modelEditor()
		mindyAll = cmds.button(label = 'Key All', w=50, command = keyAll)
		mindyRowTop = cmds.rowLayout(parent = form, nc=2)
		mindyClearAll = cmds.button(label = 'Clear All', w= 296, command = clearAll)
		mindyResetAll = cmds.button(label = 'Reset All', w= 296, command = resetAll)
		cmds.setParent( '..' )
		mindyColumn = cmds.columnLayout(w=605)
		cmds.button(label = 'K', height=158, command = keyBrows)
		cmds.button(label = 'K', height=198, command = keyUpperFace)
		cmds.button(label = 'K', height=295, command = keyLowerFace)
		cmds.button(label = 'K', height=160, command = keyMouth)
		mindyRow = cmds.rowLayout(parent = form, nc=3)
		cmds.button(label = 'Toggle Minor Controls', w=195, command = minorVisibility)
		cmds.button(label = 'Toggle Micro Controls', w=200, command = microVisibility)
		cmds.button(label = 'DONT CLICK THIS BUTTON', w=195, command = theyPushedIt)
		
		cmds.formLayout( form, edit=True, attachForm=[(mindyEditor, 'top', 5), (mindyEditor, 'left', 5), (mindyAll, 'left', 5), (mindyAll, 'right', 5), (mindyRowTop, 'left', 5), (mindyRowTop, 'right', 5), (mindyRow, 'left', 5), (mindyRow, 'bottom', 5), (mindyRow, 'right', 5), (mindyColumn, 'top', 5), (mindyColumn, 'right', 5) ], attachControl=[(mindyEditor, 'bottom', 5, mindyAll), (mindyColumn, 'bottom', 5, mindyAll), (mindyAll, 'bottom', 5, mindyRowTop),(mindyRowTop, 'bottom', 5, mindyRow)], attachPosition=[(mindyEditor, 'right', 0, 96), (mindyColumn, 'left', 0, 96)], attachNone=(mindyAll, 'top') )
		
		cmds.modelEditor( mindyEditor, edit=True, camera= 'papa_mindy_rig_stable:cam_GUIMINDY_01', wos=False, hud=False, gr=False, da = "smoothShaded", handles=False)
		
		cmds.showWindow(newWindow)
	else:
		confirm = cmds.confirmDialog(title='Error', message='Make sure Mindy is in your scene.', button='Ok', defaultButton='Ok', dismissString='Ok' )

	
go()

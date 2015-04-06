import maya.cmds as cmds
# import utilities as amu #asset manager utilities
import maya_geo_export as geo
import os
import Facade.facade as facade

def saveFile():
    if not cmds.file(q=True, sceneName=True) == '':
        cmds.file(save=True, force=True) #save file

def checkAssetType(givenType):
    # unpack decoded entries and check if the asset type matches what was passed in.
    """ precondition: givenType is either 'model', 'rig', or 'animation' """
    assetName, assetType, version = geo.decodeFileName()
    return assetType == givenType

def saveGeo():
    print 'saving geo to .obj, .bjson'
    # this is not a model asset, don't save objs!
    if not checkAssetType('model'):
        return True
    #print 'we have a model'
    # if we can export the objs, export the objs to the asset folder
    if geo.generateGeometry():
        print 'geo was exported to files.'
        geo.installGeometry()
            
        return True # copy was successful
    else:
        print 'geo was NOT exported to files.'
        return False

def showFailDialog(): 
    return cmds.confirmDialog( title         = 'Checkin Failed'
                             , message       = 'Checkin was unsuccessful'
                             , button        = ['Ok']
                             , defaultButton = 'Ok'
                             , cancelButton  = 'Ok'
                             , dismissString = 'Ok')

def checkin():
    print 'checkin NEW'
    saveFile() # save the file before doing anything
    print 'File saved'

    fileName = cmds.file(q=True, sceneName=True)
    toInstall = checkAssetType('model')
    if not toInstall:
        toInstall = checkAssetType('rig')

    if facade.canCheckin(fileName) and saveGeo(): # objs must be saved before checkin
        print "Can check in."
        comment = 'Comment'
        commentPrompt = cmds.promptDialog(
                  title='Comment',
                  message='What changes did you make?',
                  # button=['OK','Cancel'],
                  # defaultButton='OK',
                  button=['CheckIn',
                  #'ReadyForShaders',
                  'Cancel'],
                  defaultButton='CheckIn',
                  dismissString='Cancel',
              sf = True)
        if commentPrompt == 'CheckIn':
            comment = cmds.promptDialog(query=True, text=True);
            print "Comment is: " + comment
            saveFile() # One more save
            cmds.file(force=True, new=True) # Open a new file.
            checkinDest = facade.checkin(fileName, comment, toInstall) # checkin, install to stable directories.
        # elif commentPrompt == 'ReadyForShaders':
        #     comment = cmds.promptDialog(query=True, text=True); #setFlag to true so it will always go to check in
        #     print "Comment is: " + comment
        #     saveFile() # One more save
        #     cmds.file(force=True, new=True) # Open a new file.
        #     checkinDest = facade.checkin(fileName, comment, toInstall) # checkin, install to stable directories.
        #     tagGeometry()
        else:
            return
        # saveFile() # One more save
        # cmds.file(force=True, new=True) # Open a new file.
        # checkinDest = facade.checkin(fileName, comment, toInstall) # checkin, install to stable directories.
    else:
        showFailDialog()


def go():
    try:
        checkin()
    except Exception as ex:
        msg = "RuntimeException:" + str(ex)
        print msg
        cmds.confirmDialog( title         = 'Uh Oh!'
                          , message       = 'An exception just occured!\r\nHere is the message: ' + msg
                          , button        = ['Dismiss']
                          , defaultButton = 'Dismiss'
                          , cancelButton  = 'Dismiss'
                          , dismissString = 'Dismiss')

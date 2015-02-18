import maya.cmds as cmds
import os
import utilities as amu
import maya_checkout # This isn't used... probably because the checkout module needs context, and this doesn't have it.
import maya_checkin
import Facade.facade as facade

def go():
    filePath = cmds.file(q=True, sceneName=True)
    # Need to grab the asset name and asset type so we can check it out later on.
    assetType = facade.getAssetType(filePath)
    assetName = facade.getAssetName(filePath)
    # print "assetType: ", assetType
    # print "assetName: ", assetName
    maya_checkin.checkin()

    try:
        destpath = facade.checkout(assetName, True, assetType)
    except Exception as e:
        print str(e)
        if not facade.checkedOutByMe(assetName, assetType):
            cmd.confirmDialog(  title          = 'Can Not Checkout'
                               , message       = str(e)
                               , button        = ['Ok']
                               , defaultButton = 'Ok'
                               , cancelButton  = 'Ok'
                               , dismissString = 'Ok')
            return
        else:
            destpath = facade.getCheckoutDest(assetName, assetType)

    filename = facade.getFilepath(destpath, assetName, assetType)
    filename = filename + ".mb"
    toOpen = os.path.join(destpath, filename)
    # open the file
    if os.path.exists(toOpen):
        cmds.file(toOpen, force=True, open=True)#, loadReferenceDepth="none")
    else:
        # create new file
        cmds.file(force=True, new=True)
        cmds.file(rename=toOpen)
        cmds.viewClipPlane('perspShape', ncp=0.01)
        cmds.file(save=True, force=True)
import asset_manager.DAOs.getItemsDAO as getItems
import asset_manager.DAOs.newAnimationDAO as animation
import asset_manager.DAOs.checkinDAO as checkinDAO
from _xmlplus.dom.javadom import Text

def getAssetPath(self, assetName, location):
    path = getItems.getAssetPath(self, assetName, location)
    print path
    return path

def newAnimation(self, name, inputText):
    # create a new animation
    if(name == 'Previs'):
        animation.createNewPrevisFolders(inputText)
    else:
        animation.createNewShotFolders(name)
    animation.copyTemplateAnimation(self, inputText)
    return

def getShots(self):
    # creates a QTreeWidget with the items to return
    tree = getItems.getShots(self)
    return tree

def getPrevis(self):
    # creates a QTreeWidget with the items to return
    tree = getItems.getPrevis(self)
    return tree

def getAssets(self):
    # creates a QTreeWidget with the items to checkout
    tree = getItems.getAssets(self)
    return tree

def checkoutShot(self, shot, user):
# check out the indicated shot for the given user
    return

def checkoutAsset(self, asset, user):
# check out the indicated asset for the given user
    return

def addAsset(self, asset):
# add an asset
    return

def createNewPrevisFolder(self):
    return

def createNewShotFolder(self):
    return

def isLocked(self):
# check if scene is LOCKED
    return

def unlock(self):
# unlock an asset
    return

def checkout(self):
# checkout a shot
    return

def checkedOutByMe(self):
# is this checked out by me?
    return

def getCheckoutDest(self):
# get checkout destination
    return

def getVersionedFolderInfo(self):
    return
    
def canCheckin(filePath):
    print "In facade canCheckin ", filePath
    # This will check if a user can check in a particular file.
    
    return checkinDAO.canCheckin(filePath)

def checkin(asset, comment, toInstall):
    # This will checkin the asset and free it for others to checkout.
    checkinDest = checkinDAO.checkin(asset, comment)

    # Then in here we'll update the install files, as well.
    checkinDAO.installFiles(toInstall, checkinDest)

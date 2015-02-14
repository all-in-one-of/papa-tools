import asset_manager.DAOs.getItemsDAO as getItems
import asset_manager.DAOs.newItemDAO as newItem
import asset_manager.DAOs.checkoutDAO as checkoutDAO
import asset_manager.DAOs.checkinDAO as checkinDAO
import asset_manager.DAOs.rollbackDAO as rollbackDAO
import asset_manager.DAOs.alembicDAO as alembicDAO
import asset_manager.DAOs.editShotDAO as editShotDAO
from _xmlplus.dom.javadom import Text

def getAssetPath(self, assetName, location):
    path = getItems.getAssetPath(self, assetName, location)
    print path
    return path

def newAnimation(self, name, inputText):
    # create a new getItem
    if(name == 'Previs'):
        newItem.createNewPrevisFolders(name, inputText)
    else:
        newItem.createNewShotFolders(name, inputText)
    newItem.copyTemplateAnimation(self, inputText)
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

def getVersions(self, origFileName):
    """
    Returns the versions of an asset.
    """
    return rollbackDAO.getVersions(self, origFileName)

# # The checkout method works for both shots and assets currently, at least in Maya... do we need checkoutShot and checkoutAsset here?
# def checkoutShot(self, shot, user):
# # check out the indicated shot for the given user
#     return

# def checkoutAsset(self, asset, user):
# # check out the indicated asset for the given user
#     return

# def addAsset(self, asset):
# # add an asset
#     return

# def createNewPrevisFolder(self):
#     return

# def createNewShotFolder(self):
#     return

def isLocked(self, toUnlock):
# check if scene is LOCKED
    return checkoutDAO.isLocked(toUnlock)

def unlock(self, toUnlock):
# unlock an asset
    return checkoutDAO.unlock(toUnlock)

def checkout(self, toCheckout, lock, location):
    # Checkout an asset or shot. 
    # Need to first grab the path in here. Not the best place, but I guess it makes sense.
    coPath = getAssetPath(self, toCheckout, location)

    # The checkout command will return the destination of the item that is checked out.
    filePath = checkoutDAO.checkout(coPath, lock)
    
    print "facade filePath ", filePath
    return filePath
    # return checkoutDAO.checkout(coPath, lock)

def checkedOutByMe(self, itemToCheckout, location):
    # Checks if this item is checked out by the user.
    coPath = getAssetPath(self, itemToCheckout, location)
    return checkoutDAO.checkedOutByMe(coPath)

def getCheckoutDest(self, itemToCheckout, location):
    # get checkout destination
    coPath = getAssetPath(self, itemToCheckout, location)
    return checkoutDAO.getCheckoutDest(coPath)

def getFilename(self, filePath, itemToCheckout, location):
    # Gets the filename of the item. Needs to combine some stuff. I guess we could call this in the checkoutDAO...?
    coPath = getAssetPath(self, itemToCheckout, location)
    return checkoutDAO.getFilename(filePath, coPath)

def getCheckinDest(filePath):
# for rollback 
    return

def tempSetVersion(toCheckout, version):
 # for rollback
    return
def getVersionComment(checkInDest,asset_version):
# for rollback
    return
def discard():
# for rollback 
    return
def tempSetVersion(toCheckout, latestVersion):
#for rollback
    return
def getVersionedFolderInfo(self):
    return
    
def canCheckin(filePath):
    print "In facade canCheckin ", filePath
    # This will check if a user can check in a particular file.
    # TODO: How is this different from checkoutOutByMe??
    return checkinDAO.canCheckin(filePath)

def checkin(asset, comment, toInstall):

    # This will checkin the asset and free it for others to checkout.
    checkinDest = checkinDAO.checkin(asset, comment)

    # Then in here we'll update the install files, as well.
    checkinDAO.installFiles(toInstall, checkinDest)


def removeFolder(currentlySelected, context):
    # Removes the folder of the shot. (For deleting shots.)
    editShotDAO.removeFolder(currentlySelected, context)

def isShotCheckedOut(currentlySelected, currentIndex):
    # Checks to see if a shot can be renamed.
    return editShotDAO.isShotCheckedOut(currentlySelected, currentIndex)

def isNameTaken(currentIndex, newName):
    # Checks to see if a name is already taken.
    return editShotDAO.isNameTaken(currentIndex, newName)

def renameShot(currentIndex, currentlySelected, newName):
    editShotDAO.renameShot(currentIndex, currentlySelected, newName)

def previsToAnim(name):
    return editShotDAO.previsToAnim(name)

def checkCloneShots(src_name, dst_name, currentIndex):
    return editShotDAO.checkCloneShots(src_name, dst_name, currentIndex)

def cloneShot(src_name, dst_name, currentIndex):
    return editShotDAO.cloneShot(src_name, dst_name, currentIndex)


# ----------------------------------------------  ALEMBIC METHODS  ----------------------------------------------

def build_alembic_filepath(self, refPath, filePath):
    # This will build the Alembic command that Maya will call to export Alembic.
    return alembicDAO.build_alembic_filepath(self, refPath, filePath)


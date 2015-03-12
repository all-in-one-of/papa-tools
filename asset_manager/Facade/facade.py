import asset_manager.DAOs.getItemsDAO as getItems
import asset_manager.DAOs.newItemDAO as newItem
import asset_manager.DAOs.checkoutDAO as checkoutDAO
import asset_manager.DAOs.checkinDAO as checkinDAO
import asset_manager.DAOs.rollbackDAO as rollbackDAO
import asset_manager.DAOs.alembicDAO as alembicDAO
import asset_manager.DAOs.editShotDAO as editShotDAO
import asset_manager.DAOs.discardDAO as discardDAO
from _xmlplus.dom.javadom import Text

def newAsset(name):
    if name.strip() != '':
		filename = name.replace(' ', '_')
		newItem.createAssetDirectory(filename)
		return

def getAssetPath(assetName, location):
    path = getItems.getAssetPath(assetName, location)
    print path
    return path

def newAnimation(name, inputText):
    # create a new getItem
    if(name == 'Previs'):
        newItem.createNewPrevisFolders(name, inputText)
    else:
        newItem.createNewShotFolders(name, inputText)
    newItem.copyTemplateAnimation(inputText)
    return

def getShots():
    # creates a QTreeWidget with the items to return
    tree = getItems.getShots()
    return tree

def getPrevis():
    # creates a QTreeWidget with the items to return
    tree = getItems.getPrevis()
    return tree

def getAssets():
    # creates a QTreeWidget with the items to checkout
    tree = getItems.getAssets()
    return tree

def getVersions(origFileName):
    """
    Returns the versions of an asset.
    """
    return rollbackDAO.getVersions(origFileName)

def isLocked(toUnlock):
# check if scene is LOCKED
    return checkoutDAO.isLocked(toUnlock)

def unlock(toUnlock):
# unlock an asset
    return checkoutDAO.unlock(toUnlock)

def checkout(toCheckout, lock, location):
    # Checkout an asset or shot. 
    # Need to first grab the path in here. Not the best place, but I guess it makes sense.
    coPath = getAssetPath(toCheckout, location)

    # The checkout command will return the destination of the item that is checked out.
    filePath = checkoutDAO.checkout(coPath, lock)
    return filePath

def checkedOutByMe(itemToCheckout, location):
    # Checks if this item is checked out by the user.
    coPath = getAssetPath(itemToCheckout, location)
    return checkoutDAO.checkedOutByMe(coPath)

def getCheckoutDest(itemToCheckout, location):
    # get checkout destination
    coPath = getAssetPath(itemToCheckout, location)
    return checkoutDAO.getCheckoutDest(coPath)

def getCheckinDest(originalFileName):
    
    return rollbackDAO.getCheckinDest(originalFileName)

def getFilepath(filePath, itemToCheckout, location):
    # Gets the filename of the item. Needs to combine some stuff. I guess we could call this in the checkoutDAO...?
    coPath = getAssetPath(itemToCheckout, location)
    return checkoutDAO.getFilepath(filePath, coPath)

def getAssetVersions(originalFileName):
    return rollbackDAO.getAssetVersions(originalFileName)

def tempSetVersion(originalFileName, version):
 # for rollback
    return rollbackDAO.tempSetVersion(originalFileName, version)

def getAssetType(originalFileName):
    # Gets the asset's type back. This is necessary for buttons that don't have menus representing the different assets.
    return rollbackDAO.getAssetType(originalFileName)

def getAssetName(filePath):
    # Gets the name of the asset/shot to work with.
    return rollbackDAO.getAssetName(filePath)

def getVersionComment(assetVersion, originalFileName):
    # Returns the comment associated with that version.
    return rollbackDAO.getVersionComment(assetVersion, originalFileName)

def rollback(originalFileName, assetName, assetType, destPath):
    # Rollbacks the asset/shot to the desired place.
    # Returns the location of the file to open up.

    # I'd rather not have these in here, but this will have to do for now.
    correctCheckoutDir = getCheckoutDest(assetName, assetType) # Problem: this calls it twice, but the path will change beause it checks out after this.

    return rollbackDAO.rollback(originalFileName, destPath, correctCheckoutDir)


def isCheckedOutByMe(filePath): # Aaargh. This is almost the same thing as checkedOutByMe (this one checks the .checkout file). TODO: Fix this.
    return discardDAO.isCheckedOutByMe(filePath)

def discard(filePath):
    print "discard filePath: ", filePath

    return discardDAO.discard(filePath)

def getVersionedFolderInfo(self):
    return
    
def canCheckin(filePath):
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


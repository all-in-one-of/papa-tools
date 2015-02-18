import os, glob
import asset_manager.DAOs.utilities_new as amu
import asset_manager.DAOs.getItemsDAO as getItemsDAO


def getCheckinDest(originalFileName):
    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    print "tempSetVersion filePath: ", filePath
    return amu.getCheckinDest(filePath)

def tempSetVersion(originalFileName, version):
    """
    Temporarily sets the 'latest version' as the specified version without deleting later versions
    Returns the version number that we override
    @precondition 'original_file_name' is a valid file name
    """
    # I wanted this to be the originalFileName instead of the path to it, but we need a place to get the pathname.
    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    print "tempSetVersion filePath: ", filePath
    toCheckout = amu.getCheckinDest(filePath)

    return amu.tempSetVersion(toCheckout, version)

def getVersions(self, origFileName):
	# Gets the version numbers available to rollback. 
    filePath = os.path.join(getItemsDAO.getUserCheckoutDir(self), os.path.basename(os.path.dirname(origFileName)))
    checkInDest = amu.getCheckinDest(filePath)
    versionFolders = os.path.join(checkInDest, "src")
    selection = glob.glob(os.path.join(versionFolders, '*'))
    for s in range(0, len(selection)):
    	selection[s] = os.path.basename(selection[s]) # Strip off the path for the moment.

    return selection

def getAssetType(originalFileName):
    # This gets back the file's asset type. Necessary for buttons that don't have a context(menus) to help us know, like rollback.

    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    toCheckin = amu.getCheckinDest(filePath)
    print "toCheckout: ", toCheckin

    # Need to distinguish between previs and animation. These are actually located on the third directory up, not the most recent one.

    assetType = os.path.basename(toCheckin).capitalize() # Prepping this for checking out.

    if assetType == 'Model' or assetType == 'Rig':
        return assetType
    else:
        # Otherwise check if it is Previs.
        assetType = os.path.basename(os.path.dirname(os.path.dirname(toCheckin))).capitalize()
        if assetType == 'Previs':
            return assetType
        else:
            return 'Animation'


def getVersionComment(assetVersion, originalFileName):
    # Gets the comment of that version from the .nodeInfo file.

    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    checkInDest = amu.getCheckinDest(filePath)

    return amu.getVersionComment(checkInDest, assetVersion)

def getAssetVersions(originalFileName):

    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    checkInDest = amu.getCheckinDest(filePath)
    versionFolders = os.path.join(checkInDest, "src")
    selections = glob.glob(os.path.join(versionFolders, '*'))
    for i in range(0, len(selections)):
        selections[i] = os.path.basename(selections[i]) # Strip the path so its just the version number.
    return selections

def getAssetName(originalFileName):
    # Precondition: filePath is a valid path to a asset currently checked out.
    # Returns the name of the asset split from the path.
    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    checkinDest = amu.getCheckinDest(filePath)
    return os.path.basename(os.path.dirname(checkinDest))


def rollback(originalFileName, destpath, correctCheckoutDir):
    # Move to the correct checkout directory.
    if not destpath==correctCheckoutDir:
        if os.path.exists(correctCheckoutDir):
            shutil.rmtree(correctCheckoutDir)
        os.rename(destpath, correctCheckoutDir)

    # Return the path to the file name.
    filePath = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(originalFileName)))
    checkinDest = amu.getCheckinDest(filePath)

    return os.path.join(correctCheckoutDir, amu.get_filename(checkinDest))

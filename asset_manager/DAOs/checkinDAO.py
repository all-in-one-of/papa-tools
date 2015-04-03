import os, time, shutil
from ConfigParser import ConfigParser
import asset_manager.DAOs.utilities_new as amu

"""DAO for implementing the checkin action. """

def getUsername():
    return os.environ['USER']
def getUserCheckoutDir():
    return os.path.join(os.environ['USER_DIR'], 'checkout')

def canCheckin(filePath):
    """
    @returns: True if destination is not locked by another user
        AND this checkin will not overwrite a newer version
    """
    toCheckin = os.path.join(getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
    chkoutInfo = ConfigParser()
    chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
    chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
    version = chkoutInfo.getint("Checkout", "version")
    lockedbyme = chkoutInfo.getboolean("Checkout", "lockedbyme") # currently we call it "lockedbyme"... but it's true for everyone, no matter what. Not a particuarly good name.
    
    nodeInfo = ConfigParser()
    nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
    locked = nodeInfo.getboolean("Versioning", "locked") # This actually checks if it is locked.
    latestVersion = nodeInfo.getint("Versioning", "latestversion")
    
    result = True
    if lockedbyme == False:
        if locked == True:
            result = False
        if version < latestVersion:
            result = False
    
    return result

def setComment(toCheckin, comment):
    chkoutInfo = ConfigParser()
    chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
    chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")

    nodeInfo = ConfigParser()
    nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
    newVersion = nodeInfo.getint("Versioning", "latestversion") + 1
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    commentLine = getUsername() + ': ' + timestamp + ': ' + '"' + comment + '"' 
    nodeInfo.set("Comments", 'v' + "%03d" % (newVersion,), commentLine) 
    amu._writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)

def checkin(asset, comment):
    """
    Checks a folder back in as the newest version
    @precondition: toCheckin is a valid path
    @precondition: canCheckin() == True OR all conflicts have been resolved
    """
    print "Checking in asset ", asset

    # First, we'll have to set the comment in here.
    assetToCheckIn = os.path.join(getUserCheckoutDir(), os.path.basename(os.path.dirname(asset)))
    setComment(assetToCheckIn, comment)

    # Then we configure everything that is in here.

    # print toCheckin
    chkoutInfo = ConfigParser()
    chkoutInfo.read(os.path.join(assetToCheckIn, ".checkoutInfo"))
    chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
    lockedbyme = chkoutInfo.getboolean("Checkout", "lockedbyme")
    
    nodeInfo = ConfigParser()
    nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))
    locked = nodeInfo.getboolean("Versioning", "locked")
    toKeep = nodeInfo.getint("Versioning", "Versionstokeep")
    newVersion = nodeInfo.getint("Versioning", "latestversion") + 1
    newVersionPath = os.path.join(chkInDest, "src", "v"+("%03d" % newVersion))
    
    if not canCheckin(asset):
        print "Can not overwrite locked folder."
        raise Exception("Can not overwrite locked folder.")
    
    # Checkin
    shutil.copytree(assetToCheckIn, newVersionPath)

    # And fix permissions for the new version asset so that everyone can access it.
    os.system('chmod 774 -R '+ newVersionPath)
    
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    nodeInfo.set("Versioning", "lastcheckintime", timestamp)
    nodeInfo.set("Versioning", "lastcheckinuser", getUsername())
    nodeInfo.set("Versioning", "latestversion", str(newVersion))
    nodeInfo.set("Versioning", "locked", "False")
    amu._writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)
    
    #print glob.glob(os.path.join(chkInDest, "src", "*"))
    if toKeep > 0:
        amu.purge(os.path.join(chkInDest, "src"), nodeInfo, newVersion - toKeep)
        amu._writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)

    # Clean up
    shutil.rmtree(assetToCheckIn)
    os.remove(os.path.join(newVersionPath, ".checkoutInfo"))

    return chkInDest


def installFiles(toInstall, dest):
    """
    Installs files, removes dependencies.
    """
    specialInstallFiles = [os.path.join(os.environ['SHOTS_DIR'], 'static/animation')]
    toInstall |= (dest in specialInstallFiles) # Not sure what this or above is.

    srcFile = amu.getAvailableInstallFiles(dest)[0] # Gets a list of all files in the latest version of this directory.
    if toInstall: # If it is a rig, then this updates the stable with the latest version.
        amu.install(dest, srcFile)
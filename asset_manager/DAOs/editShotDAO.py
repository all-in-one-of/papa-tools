import os, shutil, glob, time
import asset_manager.DAOs.newItemDAO as newItemDAO
import asset_manager.DAOs.utilities_new as amu
from ConfigParser import ConfigParser

# Functions for editing, deleting shots.

def canRemove(dirPath):
    return canRename(dirPath)

def removeFolder(currentlySelected, context):

    # First build path.
    if context == 1:
        dirPath = str(amu.getProductionDir() + '/previs/' + currentlySelected)
    else:
        dirPath = str(amu.getProductionDir() + '/shots/' + currentlySelected)

    if not canRemove(dirPath):
        raise Exception ("Cannot remove directory: " + str(dirPath))
    shutil.rmtree(dirPath)

def canRename(assetDirPath, newName='__null_asset_path'):
    head, tail = os.path.split(assetDirPath)
    dest = os.path.join(head, newName)
    modelDir = os.path.join(assetDirPath, 'model')
    rigDir = os.path.join(assetDirPath, 'rig')
    if not amu.isCheckedOut(modelDir) and not amu.isCheckedOut(rigDir) and not os.path.exists(dest):
        return True
    return False



# -------------- Renaming Shot Methods (Don't confuse with above) -----------------

def buildDirPath(currentIndex):
    dirPath = ''
    if currentIndex == 1:
        dirPath = amu.getProductionDir() + '/previs/' 
    else:
        dirPath = amu.getProductionDir() + '/shots/'

    return dirPath


def isShotCheckedOut(currentlySelected, currentIndex):
    # Checks to see if a shot can be renamed.
    
    dirPath = buildDirPath(currentIndex)

    coPath = dirPath + currentlySelected + '/animation';
    coPath = str(coPath);
    if not amu.isVersionedFolder(coPath):
        raise Exception("Not a versioned folder.");

    if amu.isCheckedOut(coPath): # If it isn't checkout out, it's free to rename.
        return False
    else:
        return True


def isNameTaken(currentIndex, newName):
    dirPath = buildDirPath(currentIndex)
    print "dirPath: ", dirPath

    newNameTaken = False
    shots = os.listdir(dirPath)
    for s in shots:
        print 'shot: ' + s
        if (s == newName):
            newNameTaken = True
            print 'Name <' + s + '> is already taken'

    return newNameTaken


def renameShot(currentIndex, currentlySelected, newName):
    # Renames a shot: all files and folders. 
    dirPath = buildDirPath(currentIndex)
    dirPath = dirPath + currentlySelected;
                        
    #check /animation folder
    animDirPath = str(dirPath + '/animation');
    if canRename(animDirPath):
        print 'anim rename';
        ''' The renameVersionedFiles() method only searches for *.mb files.
        If other types of files need to be changed, just copy the code from
        the renameVersionedFiles() method in asset_manager/utilities.py and
        change the file extension from *.mb to whatever files type you need.'''
        renameFiles(animDirPath, currentlySelected, newName);

    #check /compositing folder
    compDirPath = str(dirPath + '/compositing');
    if canRename(compDirPath):
        print 'comp rename';
        renameFiles(compDirPath, currentlySelected, newName);

    #check /lighting folder
    lightDirPath = str(dirPath + '/lighting');
    if canRename(lightDirPath):
        print 'lighting rename' ;
        renameFiles(lightDirPath, currentlySelected, newName);
    renameFolder(str(dirPath), newName);


def renameFiles(vDirPath, oldName, newName):
    # This renames all of the files, replacing the oldName with the newName.
    src = glob.glob(os.path.join(vDirPath, 'src', '*', '*.*'))
    stable = glob.glob(os.path.join(vDirPath, 'stable', '*', '*.*'))
    stable = stable+glob.glob(os.path.join(vDirPath, 'stable', '*.*'))
    for s in src+stable:
        head, tail = os.path.split(s)
        dest = os.path.join(head, newName+tail.split(oldName)[1])
        os.renames(s, dest)

def renameFolder(oldDir, newName):

    head, tail = os.path.split(oldDir)
    dest = os.path.join(head, newName)
    if os.path.exists(dest):
        raise Exception ("Folder already exists")
    os.renames(oldDir, dest)


# -------------- Copying Previs to Animation Methods -----------------


def previsToAnim(name):
    # This creates a new animation with the name of the previs and clones the shot over.
    # previs_path = os.path.join(os.environ['PREVIS_DIR'], name, 'animation')
    anim_path = os.path.join(os.environ['SHOTS_DIR'], name, 'animation')
    # print previs_path
    # print anim_path
    #no such animation file exists!
    if not os.path.exists(anim_path):
        newItemDAO.createNewShotFolders('Animation', name)

    return cloneShot(name, name, 2) # This will be using both previs and shot.

def checkCloneShots(src_name, dst_name, currentIndex):
    paths = prepCloneShot(src_name, dst_name, currentIndex)
    src = paths[0]
    dst = paths[1]

    valid_paths = os.path.exists(src) and os.path.exists(dst)
    if not valid_paths:
        return False

    return True


def prepCloneShot(src_name, dst_name, currentIndex):
    # First prep the paths of the src and dest.
    if not src_name:
        return
    if currentIndex == 1:
        src = os.path.join(os.environ['PREVIS_DIR'], src_name, 'animation')
    elif currentIndex == 2: # Not super robust, but it should work.
        src = os.path.join(os.environ['PREVIS_DIR'], src_name, 'animation')
    else:
        src = os.path.join(os.environ['SHOTS_DIR'], src_name, 'animation')

    if not dst_name:
        return
    if currentIndex == 1:
        dst = os.path.join(os.environ['PREVIS_DIR'], dst_name, 'animation')
    elif currentIndex == 2: # Not super robust, but it should work.
        dst = os.path.join(os.environ['SHOTS_DIR'], dst_name, 'animation')
    else:
        dst = os.path.join(os.environ['SHOTS_DIR'], dst_name, 'animation')


    return src, dst


"""
src and dst must be valid filepaths to a previs or animation shot folder
src_name and dst_name are the shot names that correspond to the filepaths
"""
def cloneShot(src_name, dst_name, currentIndex):

    paths = prepCloneShot(src_name, dst_name, currentIndex)
    src = paths[0]
    dst = paths[1]

    # First, check if the shot isn't checked out.
    if (amu.isCheckedOut(dst)):
        return False

    # I wish we could clean up the ConfigParser code in all of the buttons so that we write to utilities... But it might have to wait.
    src_cfg = ConfigParser()
    dst_cfg = ConfigParser()
    src_cfg.read(os.path.join(src, ".nodeInfo"))
    dst_cfg.read(os.path.join(dst, ".nodeInfo"))
    src_version = amu.getLatestVersion(src)
    dst_version = amu.getLatestVersion(dst)

    src_path = os.path.join(src, "src", 'v'+"%03d" % src_version)
    src_filepath = os.path.join(src_path, src_name+'_animation.mb')
    print dst_version
    dst_path = os.path.join(dst, "src", 'v'+"%03d" % (dst_version+1))
    os.mkdir(dst_path)
    dst_filepath = os.path.join(dst_path, dst_name+'_animation.mb')
    print 'copying '+src_filepath+' to '+dst_filepath
    shutil.copyfile(src_filepath, dst_filepath)

    #write out new animation info
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    user = amu.getUsername()
    comment = 'copied from '+src_name
    dst_cfg.set("Versioning", "lastcheckintime", timestamp)
    dst_cfg.set("Versioning", "lastcheckinuser", user)
    dst_cfg.set("Versioning", "latestversion", str(dst_version+1))
    commentLine = user + ': ' + timestamp + ': ' + '"' + comment + '"' 
    dst_cfg.set("Comments", 'v' + "%03d" % (dst_version+1,), commentLine)   
    amu._writeConfigFile(os.path.join(dst, ".nodeInfo"), dst_cfg)
    return True
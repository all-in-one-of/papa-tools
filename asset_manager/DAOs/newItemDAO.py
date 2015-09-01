import os, glob, time
import shutil
import asset_manager.DAOs.utilities_new as amu
from ConfigParser import ConfigParser
# import hou

# This DAO creates new assets, previs and animation shots.

def createNodeInfoFile(dirPath, toKeep):
    """
    Creates the .nodeInfo file in the directory specified by dirPath.
    The Node:Type must be set by concrete nodes
    @precondition: dirPath is a valid directory
    @postcondition: All sections/tags are created and set except "Type".
        "Type" must be set by concrete nodes.
    """
    print "in createNodeInfoFile"
    username = amu.getUsername()
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    
    nodeInfo = ConfigParser()
    nodeInfo.add_section('Node')
    nodeInfo.set('Node', 'Type', '')
    
    nodeInfo.add_section('Versioning')
    nodeInfo.set('Versioning', 'LatestVersion', '0')
    nodeInfo.set('Versioning', 'VersionsToKeep', str(toKeep))
    nodeInfo.set('Versioning', 'Locked', 'False')
    nodeInfo.set('Versioning', 'LastCheckoutTime', timestamp)
    nodeInfo.set('Versioning', 'LastCheckoutUser', username)
    nodeInfo.set('Versioning', 'LastCheckinTime', timestamp)
    nodeInfo.set('Versioning', 'LastCheckinUser', username)
    nodeInfo.add_section('Comments')
    nodeInfo.set('Comments', 'v000', 'New')

    amu._writeConfigFile(os.path.join(dirPath, ".nodeInfo"), nodeInfo)

def addProjectFolder(parent, name):
    newPath = os.path.join(parent, name)
    os.makedirs(newPath)
    os.system('chmod 774 -R '+ newPath)
    return newPath

def addVersionedFolder(parent, name, toKeep):
    new_dir = os.path.join(parent, name)
    os.makedirs(os.path.join(new_dir, "src", "v000"))
    os.makedirs(os.path.join(new_dir, "stable"))
    os.makedirs(os.path.join(new_dir, 'stable', 'backups'))
    os.system('chmod 774 -R '+ new_dir)

    #os.symlink(os.path.join(new_dir, 'stable', getNullReference()), os.path.join(new_dir, 'stable','stable'))
    #TODO change for stable selection
    #os.symlink(getNullReference(), os.path.join(new_dir, 'stable','stable'))
    createNodeInfoFile(new_dir, toKeep)
    nodeInfoLocation = new_dir + "/.nodeInfo"
    print nodeInfoLocation
    os.system('chmod 660 -R '+ nodeInfoLocation)
    return new_dir
    
def copyTemplateAnimation(shotName):
    template = os.path.join(os.environ['SHOTS_DIR'], 'static/animation/stable/static_animation_stable.mb')
    if(os.path.exists(template)):
        dest = os.path.join(shotName, 'animation/src/v000/'+shotName+'_animation.mb')
        shutil.copyfile(template, dest)
        print 'copied '+template+' to '+dest
    return

def createNewShotFolders(parent, name):
    if(parent == 'Animation'):
        parent = os.environ['SHOTS_DIR']
        
    if parent != os.environ['SHOTS_DIR']:
        raise Exception("Shot folders must be created in "+os.environ['SHOTS_DIR'])
    
    new_dir = os.path.join(parent, name)
    print 'creating :'+new_dir
    addProjectFolder(parent, name)
    addVersionedFolder(new_dir, 'animation', -1)
    addVersionedFolder(new_dir, 'lighting', 5)
    addVersionedFolder(new_dir, 'compositing', 5)
    addProjectFolder(new_dir, 'animation_cache')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'abc')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'geo_sequences')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'point_cache')
    addProjectFolder(new_dir, 'playblasts')
    addProjectFolder(new_dir, 'renders')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'lighting')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'compositing')

    # Papa-specific directories. For Papa convenience only. These will need to be renamed per film.
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'papa')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'papa'), 'stable')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'mindy')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'mindy'), 'stable')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'steve')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'steve'), 'stable')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'set')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'set'), 'stable')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'misc')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'misc'), 'stable')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting'), 'lights')
    addProjectFolder(os.path.join(new_dir, 'renders', 'lighting', 'lights'), 'stable')


def createNewPrevisFolders(parent, name):
    parent = os.environ['PREVIS_DIR']
    # This is basically the same as "createNewShotFolders" method
    # doesn't include a lighting folder; may need to add/remove additional folders for production
    if parent != os.environ['PREVIS_DIR']:
        raise Exception("Shot folders must be created in "+os.environ['PREVIS_DIR'])
    
    new_dir = os.path.join(parent, name)
    print 'creating :'+new_dir
    addProjectFolder(parent, name)
    addVersionedFolder(new_dir, 'animation', -1)
    addVersionedFolder(new_dir, 'compositing', 5)
    addProjectFolder(new_dir, 'animation_cache')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'abc')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'geo_sequences')
    addProjectFolder(new_dir, 'playblasts')
    addProjectFolder(new_dir, 'renders')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'lighting')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'compositing')


def createNewAssetFolders(parent, name):
    new_dir = os.path.join(parent, name)
    addProjectFolder(parent, name)
    addVersionedFolder(new_dir, 'model', 5)
    addVersionedFolder(new_dir, 'rig', -1)
    addVersionedFolder(new_dir, 'otl', -1)
    os.makedirs(os.path.join(new_dir, "geo"))
    os.makedirs(os.path.join(new_dir, "images"))
    os.makedirs(os.path.join(new_dir, "reference"))
    return new_dir
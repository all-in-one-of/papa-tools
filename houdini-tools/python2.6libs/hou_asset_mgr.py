# Digital Asset management
# Provides New, Add, Checkin, Checkout, Revert, and other functionality for .otl files
# Author: Brian Kingery
import shutil
import sqlite3 as lite
import os, glob, sys
import hou
import subprocess
from ui_tools import ui, messageSeverity, fileMode
from miscutil import fileutil

import utilities as amu #asset manager utilites

JOB=os.environ['JOB']
USERNAME=os.environ['USER']
OTLDIR=os.environ['OTLS_DIR']
ASSETSDIR=os.environ['ASSETS_DIR']
USERDIR=os.path.join(os.environ['USER_DIR'], 'otls')

database=os.path.join(OTLDIR, '.otl.db')
otlTableDef="otl_table(id INTEGER PRIMARY KEY, filename TEXT, locked INT, lockedby TEXT, UNIQUE(filename))"
insert_ignore_sql="INSERT OR IGNORE INTO otl_table (filename, locked, lockedby) VALUES (?, ?, ?)"

def createUsrDir():
    if not os.path.exists(USERDIR):
        os.makedirs(USERDIR)

def updateDB():
    """Update the database with what is in OTLDIR"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS "+otlTableDef+";")
        files = glob.glob(os.path.join(OTLDIR, '*.otl'))
        # Add any new files to the Database
        for file in files:
            cur.execute(insert_ignore_sql, (os.path.basename(file), 0, ""))
        con.commit()
        # Delete any files that are no longer with us
        cur.execute("SELECT filename FROM otl_table")
        rows = cur.fetchall()
        toDelete = []
        for row in rows:
            toDelete.append(row[0].encode('utf-8'))
        for file in files:
            f = os.path.basename(file)
            if f in toDelete:
                toDelete.remove(f)
        for d in toDelete:
            cur.execute("DELETE FROM otl_table WHERE filename='"+d+"'")
        con.commit()
    con.close()

def getSelectedNode():
    """Returns the current node if EXACTLY ONE is selected
        Otherwise returns None"""
    node = None
    nodes = hou.selectedNodes()
    if len(nodes) == 1:
        node = nodes[0]
    return node

def isDigitalAsset(node):
    """Returns True if node is a digital asset, False if not"""
    if node.type().definition() is None:
        return False
    else:
        return True

def saveOTL():
    """Calls saveOTL with the selected node"""
    node = getSelectedNode()
    if node != None:
        saveOTL(node)

def saveOTL(node):
    """If node is a digital asset,
        Saves node's operator type and marks node as the current defintion"""
    if isDigitalAsset(node):
        # try/except statement is needed for assets that generate code, like shaders.
        try:
            node.type().definition().updateFromNode(node)
        except:
            pass
        node.matchCurrentDefinition()

def switchOPLibraries(oldfilepath, newfilepath):
    hou.hda.uninstallFile(oldfilepath, change_oplibraries_file=False)
    hou.hda.installFile(newfilepath, change_oplibraries_file=True)
    hou.hda.uninstallFile("Embedded")

def copyToOtlDir(node, filename, newName, newDef):
    """Moves the .otl file out of the USERDIR into the OTLDIR and removes it from USERDIR.
        Changes the oplibrary to the one in OTLDIR."""
    newfilepath = os.path.join(OTLDIR, filename)
    oldfilepath = os.path.join(USERDIR, filename)
    node.type().definition().copyToHDAFile(newfilepath, new_name=newName, new_menu_name=newDef)
    #fileutil.clobberPermissions(newfilepath)
    switchOPLibraries(oldfilepath, newfilepath)

def moveToOtlDir(node, filename):
    """Calls copyToOtlDir and then removes the otl from USERDIR."""
    oldfilepath = os.path.join(USERDIR, filename)
    copyToOtlDir(node, filename, None, None)
    os.remove(oldfilepath)

def copyToUsrDir(node, filename, destpath):
    """Copies the .otl file from OTLDIR to USERDIR
        Changes the oplibrary to the one in USERDIR"""
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    newfilepath = os.path.join(destpath, filename)
    oldfilepath = os.path.join(OTLDIR, filename)
    node.type().definition().copyToHDAFile(newfilepath)
    #fileutil.clobberPermissions(newfilepath)
    switchOPLibraries(oldfilepath, newfilepath)

def lockOTL(filename):
    """Updates the database entry specified by filename to locked=1 and lockedby=USERNAME"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE otl_table SET locked=1, lockedby='"+USERNAME+"' WHERE filename='"+filename+"'")
        con.commit()
    con.close()

def unlockOTLbyNode(node = None):
    """Calls unlockOTL with the selected node"""
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            warningMsg = 'WARNING! You are unlocking this node! \n If you didn\'t mean to do this, please click \n CANCEL!'
            reply = hou.ui.displayMessage(warningMsg, title='Warning!', buttons=('Ok', 'Cancel'), default_choice=1)
            if reply == 0:
                libraryPath = node.type().definition().libraryFilePath()
                filename = os.path.basename(libraryPath)
                #TODO save this somewhere
                unlockOTL(filename)
            else:
                hou.ui.displayMessage('Thank you for being safe. \n If you have a question please talk to someone in charge.')                

def unlockOTL(filename):
	asset_name, ext = os.path.splitext(filename)
	toUnlock = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'otl')
	print toUnlock
	if amu.isLocked(toUnlock):
		reply = hou.ui.displayMessage('Are you REALLY sure you want to unlock this node?', buttons=('Ok', 'Cancel'))
		if reply == 0:	
			amu.unlock(toUnlock)
			hou.ui.displayMessage('Node unlocked')
	else:
		hou.ui.displayMessage('Node already unlocked')
		return
	

def addOTL(filename):
    """Updates the database with a new table entry for filename"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute(insert_ignore_sql, (filename, 0, ""))
        con.commit()
    con.close()

def getFileInfo(filename):
    """Returns all of the table information for filename"""
    info = None
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM otl_table WHERE filename='"+filename+"'")
        info = cur.fetchone()
    con.close()
    return info

def isContainer(node):
    if not isDigitalAsset(node):
        return False

    ndef = node.type().definition()
    nsec = ndef.sections()['Tools.shelf']
    contents = str(nsec.contents())
    if contents.find('Container Assets') != -1:
        return True
    else:
        return False

def isEditableAsset(node):
    if not isDigitalAsset(node):
        return False

    ndef = node.type().definition()
    nsec = ndef.sections()['Tools.shelf']
    contents = str(nsec.contents())
    if contents.find('Editable Assets') != -1:
        return True
    else:
        return False

def _lockAssetOriginal(node, lockit):
     if isContainer(node):
         ndef = node.type().definition()
         opts = ndef.options()
         opts.setLockContents(lockit)
         ndef.setOptions(opts)
 
def _lockAssetNew(node, lockit):
    if isDigitalAsset(node):
        ndef = node.type().definition()
        opts = ndef.options()
        val = '' if lockit else '*'
        if isContainer(node): 
            ndef.addSection('EditableNodes', '')
            opts.setLockContents(True)
            ndef.setOptions(opts)
        elif isEditableAsset(node):
            ndef.addSection('EditableNodes', val)
            opts.setLockContents(True)
            ndef.setOptions(opts)
        else: # On everything else, for now do nothing. 
            pass

lockAsset = _lockAssetNew

def get_filename(parentdir):
    return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

def checkoutLightingFile():
    print("checkoutLightingFile")
    shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
    selections = []
    for sp in shotPaths:
        selections.append(os.path.basename(sp))
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Select shot file to checkout:', exclusive=True)
    if answer:
        answer = answer[0]
        toCheckout = os.path.join(os.environ['SHOTS_DIR'], selections[answer], 'lighting')

        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            if not amu.checkedOutByMe(toCheckout):
                hou.ui.displayMessage('Can Not Checkout: '+str(e))
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)

        toOpen = os.path.join(destpath, get_filename(toCheckout)+'.hipnc')

        if os.path.exists(toOpen):
            hou.hipFile.load(toOpen)
        else:
            hou.hipFile.clear()
            hou.hipFile.save(toOpen) 

def unlockLightingFile():
    print("unlockLightingFile")
    shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
    selections = []
    for sp in shotPaths:
        selections.append(os.path.basename(sp))
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Select shot file to unlock:', exclusive=True)
    if answer:
        answer = answer[0]
        toUnlock = os.path.join(os.environ['SHOTS_DIR'], selections[answer], 'lighting')
    if amu.isLocked(toUnlock):
        reply = hou.ui.displayMessage('Are you sure you want to unlock this file?', buttons=('Ok', 'Cancel'))
        if reply == 0:
            hou.hipFile.save()
            hou.hipFile.clear()		
            amu.unlock(toUnlock)
            hou.ui.displayMessage('Lighting file unlocked')

    else:
        hou.ui.displayMessage('Lighting file already unlocked')
        return

def checkinLightingFile():
    print('checkin lighting file')
    filepath = hou.hipFile.path()
    toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filepath)))
    backups = os.path.join(toCheckin, 'backup')
    print 'backup = ' + backups
    if os.path.isdir(backups):
        os.system('rm -rf '+backups)
    if amu.canCheckin(toCheckin):
        response = hou.ui.readInput("What did you change?", buttons=('OK', 'Cancel',), title='Comment')
        if(response[0] != 0):
            return
        comment = response[1]
        hou.hipFile.save()
        hou.hipFile.clear()
        amu.setComment(toCheckin, comment)
        dest = amu.checkin(toCheckin)
        srcFile = amu.getAvailableInstallFiles(dest)[0]
        amu.install(dest, srcFile)
    else:
        hou.ui.displayMessage('Checkin Failed')

def discardLightingFile():
    filepath = hou.hipFile.path()
    #TODO
    print(filepath)
    if hou.ui.displayMessage('YOU ARE ABOUT TO IRREVOKABLY DISCARD ALL CHANGES YOU HAVE MADE. '
                        'Please think this through very carefully.\n '
                        'Are you sure you want to discard '
                        'your changes?'
                        , buttons=('Yes','No',)
                        , default_choice=1
                        , title='Discard Confirmation') == 0:
        toDiscard = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filepath)))
        if amu.isCheckedOutCopyFolder(toDiscard):
            hou.hipFile.clear()
            amu.discard(toDiscard)
        else:
            hou.ui.displayMessage('This is not a checked out file.  There is nothing to discard', title='Invalid Command')
    else:
        hou.ui.displayMessage('Thank you for being responsible.', title='Discard Cancelled')

def checkout(node):
    """Checks out the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist."""
    if not isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        if node.type().name() == "geometryTemplate":
            hou.ui.displayMessage("Cannot checkout geometry template node.")
            return False
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)

        asset_name, ext = os.path.splitext(filename)
        toCheckout = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'otl')
        myCheckout = False
        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            print str(e)
            myCheckout = amu.checkedOutByMe(toCheckout)
            if not myCheckout:
                hou.ui.displayMessage('Can Not Checkout.')
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)

        if myCheckout:
            switchOPLibraries(os.path.join(OTLDIR, filename), os.path.join(destpath, filename))
        else:
            copyToUsrDir(node, filename, destpath)
        lockAsset(node, True)
        saveOTL(node)
        node.allowEditingOfContents()
        hou.ui.displayMessage("Checkout Successful!", title='Success!')

def isCameraAsset(node):
    return 'cameras' in node.name()

def isSetAsset(node):
    sets = ('owned_abby_family_room', 'owned_jeffs_apartment')
    return getAssetName(node) in sets

def writeToAlembic(outDir, filename, rootObject, objects='*', trange='off', startFrame=1, endFrame=240, stepSize=1):
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    abcFilePath = os.path.join(outDir, filename)

    # Create alembic ROP
    abcROP = hou.node('/out').createNode('alembic')

    # Set parameters
    parms = {}
    parms['trange'] = trange
    parms['f1'] = startFrame
    parms['f2'] = endFrame
    parms['f3'] = stepSize
    parms['filename'] = abcFilePath
    parms['root'] = rootObject.path()
    parms['objects'] = objects
    abcROP.setParms(parms)

    # Render ROP
    abcROP.render()
    abcROP.destroy()

    return abcFilePath
    
def writeCamerasToAlembic(node):
    sequence = node.name().split('_')[2][0]
    children = node.children()
    for c in children:
        name = c.name()
        if 'shot' in name:
            shot = name.split('_')[1]
            camDir = os.path.join(os.environ['SHOTS_DIR'], sequence+shot, 'camera')
            abcName = sequence+shot+'_camera'+'.abc'
            sFrame, eFrame = hou.playbar.playbackRange()
            sSize = hou.playbar.frameIncrement()
            abcFilePath = writeToAlembic(camDir, abcName, node
                                        , objects=os.path.join(c.path(), 'cam1')
                                        , trange='normal'
                                        # , startFrame=sFrame
                                        # , endFrame=eFrame
                                        , stepSize=sSize)
            mayaFilePath = os.path.join(camDir, sequence+shot+'_camera'+'.mb')
            if os.path.exists(mayaFilePath):
                os.remove(mayaFilePath)
            amu.mayaImportAlembicFile(mayaFilePath, abcFilePath)
            print hou.node(os.path.join(c.path(),'cam1')).evalParm('focal')
            amu.setFocalLengthMaya(mayaFilePath, hou.node(os.path.join(c.path(),'cam1')).evalParm('focal'))
            

def writeSetToAlembic(node):
    exclude_objects = ('owned_jeff_couch', 'owned_jeffs_controller', 'owned_abby_controller', 'owned_cyclopes_toy')
    assetName = getAssetName(node)
    print(assetName)
    abcName = assetName+'.abc'
    setDir = os.path.join(os.environ['PRODUCTION_DIR'], 'set_cache', assetName)
    include_objects = ''
    for c in node.children():
        name = getAssetName(c)
        if name != None and name not in exclude_objects and 'wall' not in name and 'layout' not in name:
            include_objects += ' '+c.path()
    abcFilePath = writeToAlembic(setDir, abcName, node, objects=include_objects)
    mayaFilePath = os.path.join(setDir, assetName+'.mb')
    if os.path.exists(mayaFilePath):
        os.remove(mayaFilePath)
    amu.mayaImportAlembicFile(mayaFilePath, abcFilePath)


def checkin(node = None):
    """Checks in the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist, and USERNAME must have the lock."""
    if not isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        libraryPath = node.type().definition().libraryFilePath() #user checkout folder
        filename = os.path.basename(libraryPath) # otl filename
        toCheckin = os.path.dirname(libraryPath)

        if os.path.exists(os.path.join(toCheckin, ".checkoutInfo")) and amu.canCheckin(toCheckin):
            response = hou.ui.readInput("What did you change?", buttons=('OK', 'Cancel',), title='Comment')
            if(response[0] != 0):
                return
            comment = response[1]
            lockAsset(node, False)
            saveOTL(node)
            node.type().definition().save(libraryPath)
            hou.hda.uninstallFile(libraryPath, change_oplibraries_file=False)
            amu.setComment(toCheckin, comment)
            assetdir = amu.checkin(toCheckin)
            assetpath = amu.getAvailableInstallFiles(assetdir)[0]
            amu.install(assetdir, assetpath)
            hou.hda.installFile(os.path.join(OTLDIR, filename), change_oplibraries_file=True)
            hou.hda.uninstallFile("Embedded")
            if isCameraAsset(node) and hou.ui.displayMessage('Export Alembic?'
                                                        , buttons=('Yes','No',)
                                                        , default_choice=0
                                                        , title='Export Alembic') == 0:
                writeCamerasToAlembic(node)
            if isSetAsset(node) and hou.ui.displayMessage('Export Alembic?'
                                                        , buttons=('Yes','No',)
                                                        , default_choice=0
                                                        , title='Export Alembic') == 0:
                writeSetToAlembic(node)
            hou.ui.displayMessage("Checkin Successful!")

        else:
            hou.ui.displayMessage('Can Not Checkin.')

def discard(node = None):
    if not isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)
        toDiscard = os.path.dirname(libraryPath)
        if amu.isCheckedOutCopyFolder(toDiscard):
            switchOPLibraries(libraryPath, os.path.join(OTLDIR, filename))
            node.matchCurrentDefinition()
            amu.discard(toDiscard)
            hou.ui.displayMessage("Revert Successful!")

def formatName(name):
    name = name.strip()
    name = name.replace('_', ' ')
    if name.split()[0].lower() != os.environ['PROJECT_NAME']:
        name = str(os.environ['PROJECT_NAME']) + ' ' + name
    return name.lower()

def listContainers():
    dirlist = list()
    for root,dirs,files in os.walk(ASSETSDIR):
        if root != ASSETSDIR:
            break
        else:
            for dir in dirs:
                dirlist.append(str(dir))
    dirlist.sort()
    return dirlist

def newContainer(hpath):
    templateNode = hou.node(hpath).createNode("containerTemplate")
    templateNode.hide(True)
    # resp = ui.inputWindow("Enter the New Operator Label", wtitle="OTL Label")
    response = hou.ui.readInput("Enter the New Operator Label", buttons=('Ok', 'Cancel'), title="OTL Label")
    if response[0]==0:
        name = response[1]
    else:
        name = None
    if name != None and name.strip() != '':
        name = formatName(name)
        filename = name.replace(' ', '_')
        newfilepath = os.path.join(OTLDIR, filename+'.otl')
        
        if not os.path.exists(newfilepath):
            # create file heirarchy if container asset            
            amu.createNewAssetFolders(ASSETSDIR, filename)

            newversiondir = os.path.join(ASSETSDIR, filename+'/otl')
            print "dir " + newversiondir
            newversionpath = os.path.join(newversiondir, 'src/v000/'+filename+'.otl')
            print "path " + newversionpath
            templateNode.type().definition().copyToHDAFile(newversionpath, new_name=filename, new_menu_name=name)
            stablepath = amu.install(newversiondir, newversionpath)
            os.symlink(stablepath, newfilepath)
            hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            fileutil.clobberPermissions(newfilepath)
            newnode = hou.node(hpath).createNode(filename)
            
            # templateNode.type().definition().copyToHDAFile(newfilepath, new_name=filename, new_menu_name=name)
            # hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            # fileutil.clobberPermissions(newfilepath)
            # newnode = hou.node(hpath).createNode(filename)
        else:
            hou.ui.displayMessage("Asset by that name already exists. Cannot create asset.", title='Asset Name', severity=hou.severityType.Error)
        
    # clean up
    templateNode.destroy()

def printList(pList, ws=4):
    indent = ' '*ws
    result = ''
    for l in pList:
        result += indent + str(l) + '\n'
    return result

def getAssetDependents(assetName):
    dependents = []
    otls = glob.glob(os.path.join(OTLDIR, 'owned*.otl'))
    for o in otls:
        ndef = hou.hda.definitionsInFile(o)[0]
        contents = ndef.sections()['CreateScript'].contents().splitlines()
        for c in contents:
            if 'opadd -e -n' in c:
                c = c.split(' ')
                d = os.path.basename(o).split('.')[0]
                if c[3] == assetName and d not in dependents:
                    dependents.append(d)
    return dependents

def rename(node = None):
    """Renames the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist.
    """
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)

                dependents = getAssetDependents(oldAssetName)

                if dependents:
                    hou.ui.displayMessage('The following assets are depenent on this asset: \n\n'+printList(dependents)+'\nModify these assets first before attempting to rename again!!', title='Can NOT rename!', severity=hou.severityType.Error)
                    return
                nodeDir = os.path.join(os.environ['ASSETS_DIR'], oldAssetName, 'otl')
                info = amu.getVersionedFolderInfo(nodeDir);
                if info[0] == "":
                    if passwordWindow('r3n@m3p@ssw0rd', 'Enter the rename password...'):
                        resp = hou.ui.readInput("Enter the New Operator Label", title="Rename OTL")
                        print resp
                        if resp != None and resp[1].strip() != '':
                            name = formatName(resp[1])
                            newfilename = name.replace(' ', '_')
                            newfilepath = os.path.join(OTLDIR, newfilename+'.otl')
                            if os.path.exists(newfilepath):
                                hou.ui.displayMessage("Asset by that name already exists. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                            elif not amu.canRename(assetDirPath, newfilename):
                                hou.ui.displayMessage("Asset checked out in Maya. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                            else:
                                node.type().definition().copyToHDAFile(newfilepath, new_name=newfilename, new_menu_name=name)
                                hou.hda.installFile(newfilepath, change_oplibraries_file=True)
                                newnode = hou.node(determineHPATH()).createNode(newfilename)
                                node.destroy()
                                hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                                subprocess.check_call( ['rm','-f',oldlibraryPath] )
                                amu.renameAsset(assetDirPath, newfilename)
                else:
                    logname, realname = amu.lockedBy(info[0].encode('utf-8'))
                    whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
                    errstr = 'Cannot checkout asset. Locked by: \n\n' + whoLocked
                    hou.ui.displayMessage(errstr, title='Asset Locked', severity=hou.severityType.Error)
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")

def deleteAsset(node = None):
    """Deletes the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist. It may not be already checked out in Houdini or in Maya.
    """
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.", title='Non-Asset Node', severity=hou.severityType.Error)
            return
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)
                dependents = getAssetDependents(oldAssetName)

                if dependents:
                    hou.ui.displayMessage('The following assets are depenent on this asset: \n\n'+printList(dependents)+'\nModify these assets first before attempting to delete again!!', title='Can NOT delete!', severity=hou.severityType.Error)
                    return
                nodeDir = os.path.join(os.environ['ASSETS_DIR'], oldAssetName, 'otl')
                info = amu.getVersionedFolderInfo(nodeDir);
                print info[0]
                if not info[0] == "":
                    logname, realname = amu.lockedBy(info[0].encode('utf-8'))
                    whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
                    errstr = 'Cannot delete asset. Locked by: \n\n' + whoLocked
                    hou.ui.displayMessage(errstr, title='Asset Locked', severity=hou.severityType.Error)
                    return

                if not amu.canRemove(assetDirPath):
                    hou.ui.displayMessage("Asset currently checked out in Maya. Cannot delete asset.", title='Maya Lock', severity=hou.severityType.Error)
                    return

                message = "The following paths and files will be deleted:\n" + assetDirPath + "\n" + oldlibraryPath
                hou.ui.displayMessage(message, title='Asset Deleted', severity=hou.severityType.Error)
                if passwordWindow('d3l3t3p@ssw0rd', wmessage='Enter the deletion password ...'):
                    node.destroy()
                    hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                    try:
                        amu.removeFolder(assetDirPath)
                        os.remove(oldlibraryPath)
                    except Exception as ex:
                        hou.ui.displayMessage("The following exception occured:\n" + str(ex), title='Exception Occured', severity=hou.severityType.Error)
                        return
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")
        return

def newGeo(hpath):
    templateNode = hou.node(hpath).createNode("geometryTemplate")
    alist = listContainers()
    response = hou.ui.readInput("Enter the New Operator Label", title="OTL Label", buttons=('OK', 'Cancel'))
    filename = str()
    if response[0]==0:
        name = response[1]
    else:
        name = None
    if name != None and name.strip() != '':
        name = formatName(name)
        filename = name.replace(' ', '_')
        templateNode.setName(filename, unique_name=True)
    answer = hou.ui.selectFromList(alist, message='Select Container Asset this belongs to:', exclusive=True)
    if not answer:
        hou.ui.displayMessage("Geometry must be associated with a container asset! Geometry asset not created.", severity=hou.severityType.Error)
        templateNode.destroy()
        return
    answer = answer[0]
    sdir = '$JOB/production/assets/'
    gfile = hou.ui.selectFile(start_directory=os.path.join(sdir, alist[answer]+'/geo'), title='Choose Geometry', chooser_mode=hou.fileChooserMode.Read, pattern='*.bjson, *.obj')
    if len(gfile) > 4 and gfile[:4] != '$JOB':
        hou.ui.displayMessage("Path must start with '$JOB'. Default geometry used instead.", title='Path Name', severity=hou.severityType.Error)
        templateNode.destroy()
    elif gfile != '':
        hou.parm(templateNode.path() + '/read_file/file').set(gfile)

def determineHPATH():
    hpane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    hpath = hpane.pwd().path()
    if not isinstance(hpane.pwd(), hou.ObjNode):
        hpath = "/obj"
    return hpath

def new():
    otb = ('Container', 'Geometry', 'Cancel')
    # optype = ui.infoWindow("Choose operator type.", wbuttons=otb, wtitle='Asset Type')
    optype = hou.ui.displayMessage("Choose operator type.", buttons=otb, title='Asset Type')
    hpath = determineHPATH()
    if optype == 0:
        newContainer(hpath)
    elif optype == 1:
        newGeo(hpath)

def getAssetName(node):
    if isDigitalAsset(node):
        lpath = node.type().definition().libraryFilePath()
        filename = os.path.basename(lpath)
        return str(filename.split('.')[0].replace("'", "_"))
    else:
        return None

def refresh(node = None):
    """Only updates transforms of internal nodes of "Editable Assets"

    Everything else is probably either light linking data, or something else 
    that should always have a local override."""
    hou.hscript("otrefresh -r") # Refresh all definitions first
    
    if node == None or hasattr(node, "__len__"):
        hou.ui.displayMessage("Select EXACTLY one node.")
    elif not isEditableAsset(node):
        hou.ui.displayMessage('Not an "Editable Asset".')
    else:
        npath = os.path.dirname(node.path())
        dopple = hou.node(npath).createNode(node.type().name())
        for c in node.children():
            for dc in dopple.children():
                if c.name() == dc.name() and isinstance(c, hou.ObjNode):
                    c.setParmTransform(dc.parmTransform())
        dopple.destroy()
        hou.ui.displayMessage('Refresh successful.')

# TODO: This function probably needs to be removed.
def add(node = None):
    """Adds the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node CAN NOT already exist."""
    updateDB()
    if node != None:
        if node.type().definition() is None:
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            libraryPath = node.type().definition().libraryFilePath()
            filename = os.path.basename(libraryPath)
            info = getFileInfo(filename)
            if info == None:
                saveOTL(node)
                moveToOtlDir(node, filename)
                addOTL(filename)
                hou.ui.displayMessage("Add Successful!")
            else:
                hou.ui.displayMessage("Already Added")
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")


def convert_texture(userTextureMap, assetImageDir, folder_name=''):
    print userTextureMap

    if os.path.isdir(userTextureMap):
        return

    extensions = ['.jpg','.jpeg','.tiff','.tif','.png','.exr']
    userFileName, userExt = os.path.splitext(os.path.basename(userTextureMap))
    if userExt not in extensions:
        return

    # Set Variables for texture paths
    convertedTexture = os.path.join('/tmp','intermediate'+userFileName+'.exr')
    print "convertedTexture:: "+convertedTexture
    finalTexture = os.path.join('/tmp','finished'+userFileName+'.rat')
    print "finalTexture:: "+finalTexture

    # Gamma correct for linear workflow
    if 'DIFF' in userTextureMap or 'diffuse' in userTextureMap:
        args = ['icomposite',convertedTexture,'=','gamma',str(1/2.2),userTextureMap]
        
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            hou.ui.displayMessage('Failed to convert texture. The following error occured:\n' + str(e))        
            return
        didgamma = '\nIt has been gamma corrected.'
    else:
        convertedTexture = userTextureMap
        didgamma = ''
    '''    
    # Convert to .exr with optimized settings. Also, setting compatible with RenderMan (in case we need to render there)
    args = ['txmake','-mode','periodic','-compression','zip']
    args += ['-format','openexr','-half',convertedTexture,finalTexture]
    '''
    # Uncomment the following and comment out the previous call if PRMan is not present

    args = ['iconvert', convertedTexture, finalTexture] 
    
    #subprocess.check_call( args.split() )


    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as e:
        hou.ui.displayMessage('Failed to convert texture. The following error occured:\n' + str(e))
    else:
        # Rename texture and move into production pipeline 
        newTextureName = userFileName + '.rat'

        newfilepath = os.path.join(assetImageDir, folder_name, newTextureName)
        print "new file path:: "+newfilepath

        try:
            shutil.move(finalTexture, newfilepath)  
        except Exception as e:
            os.remove(finalTexture)
            hou.ui.displayMessage('Failed to move texture. The following error occured:\n' + str(e), severity=hou.severityType.Error)
        finally:
            if convertedTexture != userTextureMap:
                os.remove(convertedTexture)

def newTexture():
    # Get a list of assets 
    assetList = glob.glob(os.path.join(os.environ['ASSETS_DIR'], '*'))
    selections = []
    for aL in assetList:
        # basename takes last folder in path.
        selections.append(os.path.basename(aL)) 
        # sort alphabetically
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Choose an asset to add/update textures for', exclusive=True)
    if answer:
        answer = answer[0]
        assetName = selections[answer]
        assetImageDir = os.path.join(os.environ['ASSETS_DIR'], assetName, 'images')

        # Allow user to choose texture map in user local directory   
        userDirectory = os.environ['USER_DIR']
        userSelection = hou.ui.selectFile(start_directory=userDirectory, title='Select texture map, or folder of texture maps', image_chooser=True, pattern='*.jpg,*.jpeg,*.tiff,*.tif,*.png,*.exr') 
        
        #Allow user to search for texture in any directory
        userSelection = os.path.expandvars(userSelection)

        if os.path.isdir(userSelection):
            folder_name = os.path.basename(os.path.dirname(userSelection))
            texture_paths = glob.glob(os.path.join(userSelection, '*'))

            newFileDir = os.path.join(assetImageDir, folder_name)
            os.system('rm -rf '+newFileDir)
            print 'newFileDir:: '+newFileDir
            os.makedirs(newFileDir)
            
            for t in texture_paths:
                convert_texture(t, assetImageDir, folder_name=folder_name)
        else:
            convert_texture(userSelection, assetImageDir)

        ui.infoWindow('Done.')

def getInfo(node):
    if node == None:
        # code for getting info from the checked out scene file goes here
        sys.stderr.write('Code for shot info does not yet exist for Houdini!')
        pass
    elif isDigitalAsset(node):
        # code for getting info selected node
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)
        assetname, ext = os.path.splitext(filename)
        nodeDir = os.path.join(os.environ['ASSETS_DIR'], assetname, 'otl')
        nodeInfo = amu.getVersionedFolderInfo(nodeDir)
        message = ''
        if nodeInfo[0]:
            logname, realname = amu.lockedBy(nodeInfo[0].encode('utf-8'))
            message = 'Checked out by '+realname+' ('+logname+').\n'
        else:
            message = 'Not Checked out.\n'
        message = message+'Last checked in by '+nodeInfo[3]
        hou.ui.displayMessage(message, title='Node Info')


def passwordWindow(password, wtitle='Enter Password', wmessage='Enter Password', wlabel='Password'):
    '''Pop up a window with a text window to enter a password into

Returns true when the password entered matches the password given as a 
parameter and false otherwise.'''
    resp = ''
    ok = 0
    first = True
    label = (wlabel + ':',)
    while ok == 0 and resp != password:
        if not first:
            hou.ui.displayMessage('Incorrect!\nTry Again.', buttons=('Ok',), title='Error', severity=hou.severityType.Message)
        ok, resp = hou.ui.readMultiInput(message=wmessage, input_labels=label, password_input_indices=(0,), buttons=('OK', 'Cancel'), title=wtitle)
        resp = resp[0]
        first = False
    return ok == 0


# make getNodeInfo an alias of getInfo
getNodeInfo = getInfo


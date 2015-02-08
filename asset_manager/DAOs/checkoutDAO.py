# DAO object for the checkout button.
import os, time, shutil
import asset_manager.DAOs.utilities_new as amu
from ConfigParser import ConfigParser


def isLocked(ulPath):
	print "Inside checkoutDAO isLocked"
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(ulPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "False":
		return False;
	
	return True;

def unlock(ulPath):
	print "Inside checkoutDAO unlock"
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(ulPath, ".nodeInfo"))
	nodeInfo.set("Versioning", "locked", "False")

	toCopy = getCheckoutDest(ulPath)
	dirname = os.path.basename(toCopy) 
	parentPath = os.path.join(os.path.dirname(toCopy), ".unlocked")
	if not (os.path.exists(parentPath)):
		os.mkdir(parentPath)

	os.system('mv -f '+toCopy+' '+parentPath+'/')
	amu._writeConfigFile(os.path.join(ulPath, ".nodeInfo"), nodeInfo)
	return 0;


def checkedOutByMe(dirPath): # I feel like this should be checking both if it is locked and if it is checked out by the current user...
	nodeInfo = os.path.join(dirPath, ".nodeInfo")
	if not os.path.exists(nodeInfo):
		return False
	cp = ConfigParser()
	cp.read(nodeInfo)
	return cp.get("Versioning", "lastcheckoutuser") == amu.getUsername()


def getCheckoutDest(coPath):
	# Returns the checkout destination path - inside the user's directory.

	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	version = nodeInfo.get("Versioning", "latestversion")
	return os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(coPath))+"_"+os.path.basename(coPath)+"_"+("%03d" % int(version)))


def checkout(coPath, lock):
	"""
	Copies the 'latest version' from the src folder into the local directory
	@precondition: coAsset is the name of an actual asset
	@precondition: lock is a boolean value
	
	@postcondition: A copy of the 'latest version' will be placed in the local directory
		with the name of the versioned folder
	@postcondition: If lock == True coPath will be locked until it is released by checkin
	"""

	print "in checkoutDAO, running checkout"
	print "coPath ", coPath
	# First need to grab the path file first.
	#if not os.path.exists(os.path.join(coPath, ".nodeInfo")):
	if not amu.isVersionedFolder(coPath):
		raise Exception("Not a versioned folder.")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "False": # Isn't this the point of the isCheckedOut method??
		version = nodeInfo.getint("Versioning", "latestversion")
		toCopy = os.path.join(coPath, "src", "v"+("%03d" % version))
		dest = getCheckoutDest(coPath)

		if(os.path.exists(toCopy)):
			try:
				shutil.copytree(toCopy, dest) # Make the copy. Note that dest (user's checkout directory) MUST NOT exist for this to work.
			except Exception:
				print "checkoutDAO, checkout: Could not copy files."
				raise Exception("Could not copy files.")
			timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
			nodeInfo.set("Versioning", "lastcheckoutuser", amu.getUsername())
			nodeInfo.set("Versioning", "lastcheckouttime", timestamp)
			nodeInfo.set("Versioning", "locked", str(lock))
			
			amu._writeConfigFile(os.path.join(coPath, ".nodeInfo"), nodeInfo)
			amu._createCheckoutInfoFile(dest, coPath, version, timestamp, lock)
		else:
			raise Exception("Version doesn't exist "+toCopy)
	else:
		whoLocked = nodeInfo.get("Versioning", "lastcheckoutuser")
		whenLocked = nodeInfo.get("Versioning", "lastcheckouttime")
		logname, realname = amu.lockedBy(whoLocked)
		whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
		raise Exception("Can not checkout. Folder is locked by:\n\n"+ whoLocked+"\nat "+ whenLocked)
	return dest


def getFilename(userFilePath, prodFilePath):
	# print "userFilePath: ", userFilePath
	# print "prodFilePath: ", prodFilePath
	# Builds the file path name.
	toOpen = os.path.join(userFilePath, os.path.basename(os.path.dirname(prodFilePath))+'_'+os.path.basename(prodFilePath))
	return toOpen
import os, shutil
import asset_manager.DAOs.utilities_new as amu
from ConfigParser import ConfigParser

# DAO for implementing the discard function.


def isCheckedOutByMe(filePath):
	toDiscard = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))

	return amu.isCheckedOutCopyFolder(toDiscard)


def discard(filePath):
	"""
	Discards a local checked out folder without creating a new version.
	"""

	toDiscard = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
	print "toDiscard: ", toDiscard
	chkoutInfo = ConfigParser()
	chkoutInfo.read(os.path.join(toDiscard, ".checkoutInfo"))
	chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")

	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(chkInDest, ".nodeInfo"))

	nodeInfo.set("Versioning", "locked", "False")
	amu._writeConfigFile(os.path.join(chkInDest, ".nodeInfo"), nodeInfo)

	shutil.rmtree(toDiscard)
	if(os.path.exists(toDiscard)):
		os.rmdir(toDiscard)
import os
import asset_manager.DAOs.utilities_new as amu

# Location for Alembic Commands and Functions.
	
def build_alembic_filepath(self, refPath, filePath):
	# This builds the location where the alembic file will be stored. This definitely needs to be moved.
	#Get Shot Directory
	# filePath = cmds.file(q=True, sceneName=True)
	toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
	dest = amu.getCheckinDest(toCheckin)
	
	#Get Asset Name
	# refPath = cmds.referenceQuery(unicode(ref), filename=True)
	assetName = os.path.basename(refPath).split('.')[0]
	
	return os.path.join(os.path.dirname(dest), 'animation_cache', 'abc', assetName+'.abc')


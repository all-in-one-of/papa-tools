import os, shutil, glob
import utilities as amu
import nuke
from ConfigParser import ConfigParser


def get_file_path():
	return nuke.callbacks.filenameFilter( nuke.root().name() )

def get_checkin_path():
	filePath = get_file_path()
	return os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))

def show_dialog(text):
	nuke.message(text)

def is_shot_checked_out():
	file_path = get_file_path()
	if file_path:
		toDiscard = get_checkin_path()
		if amu.isCheckedOutCopyFolder(toDiscard):
			# If it's checked out by the user, then we're good.
			return True
		else:
			return False
	else:
		return False

def getUserCheckoutDir():
    return os.path.join(os.environ['USER_DIR'], 'checkout')

def copyToStable(render_path):
	test_dir = os.listdir(render_path) # listdir lists the entries given by the path. Sweet!
	source_versions = []
	for dir in test_dir:
		if dir != 'stable':
			version_num = int(dir.split('v')[1])
			source_versions.append(version_num)

	if len(source_versions) > 0:
		latest_version = max(source_versions)

		# Then we connect the highest number with the directory.
		filled_latest_version = str(latest_version).zfill(3)
		for version in test_dir:
			if filled_latest_version in version:
				# show_dialog("The latest version is: " + version)

				version_path = os.path.join(render_path, version)
				renders = os.listdir(version_path)

				# We  remove everything that was in the stable folder.
				stable_dir = os.path.join(render_path, "stable")
				old_stable_files = glob.glob(stable_dir + '/*')
				for old_file in old_stable_files:
					os.remove(old_file)

				# Then copy the new renders to the stable folder.
				for image in renders:
					shutil.copy(os.path.join(version_path, image), stable_dir)
	# else:
	# 	# Is this necessary? Not every shot is going to have these...
	# 	show_dialog(os.path.basename(render_path) + " does not have any renders yet!")



# NOTE: In order for this to work, each of the subdirectories for renders must be set up, 
# as well as the stable files in those subdirectories.
def updateStableRenders():
	if is_shot_checked_out():
		toCheckin = os.path.join(getUserCheckoutDir(), os.path.basename(os.path.dirname(get_file_path())))
		chkoutInfo = ConfigParser()
		chkoutInfo.read(os.path.join(toCheckin, ".checkoutInfo"))
		chkInDest = chkoutInfo.get("Checkout", "checkedoutfrom")
		shotName = os.path.basename(os.path.dirname(chkInDest))
		# show_dialog("Shot name: " + shotName)

		# /production/shots/[shot_name]/renders/lighting/[folder names]
		renders_directory = os.path.join(os.environ['SHOTS_DIR'], shotName, "renders", "lighting")
		show_dialog("render_directory: " + renders_directory)

		# Then a list of renders that we want to do.
		render_group = ['mindy', 'misc', 'papa', 'set', 'steve']

		for group in render_group:
			copyToStable(os.path.join(renders_directory, group))
	else:
		show_dialog('ERROR: Not checked out.')

# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import re
import mari
import random
import subprocess
import PythonQt.QtGui as gui
from ConfigParser import ConfigParser

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
#JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"

# ------------------------------------------------------------------------------
def changeExportPath():
	# Make sure that there is an open project
	if mari.projects.current() is None:
		mari.utils.message('Please open a project first.')
		return

	# Find the currently selected object
	geo = mari.geo.current()
	if geo is None:
		mari.utils.message('Please select an object.')

	# Find the currently selected channel
	channel = geo.currentChannel()
	if channel is None:
		mari.utils.message('Please select a channel.')

	cp = ConfigParser()
	projPath = mari.current.project().info().projectPath()[:-11]
	projInfoFile = open(os.path.join(projPath, ".projectInfo"), "wb")

	exportPath = mari.utils.getExistingDirectory(None, 'Select Map Export Path')
	cp.read(os.path.join(projPath, ".projectInfo"))
	cp.add_section("FilePaths")
	cp.set("FilePaths", "Export", exportPath)

	cp.write(projInfoFile)

def convertToRat(geo, filePathNoUDIM):
	print "Converting to .rat: ", filePathNoUDIM
	print "PATH: ", os.environ.get('PATH')
	for patch in geo.patchList():
		# Get Patch UDIM numbers
		udim = 1001 + patch.u() + (10 * patch.v())

		# The current working directory... Is this not right for some reason?
		print "current working directory"
		print os.getcwd()

		# It's almost like we need to make sure this is relative. I haven't got it working with absolute paths.
		# I wonder if we can get away with it on the basename?
		print "Does the path exist from here?"
		print os.path.exists(filePathNoUDIM + "_" + str(udim) + '.png')

		# So we set the export path in the project. Can we get a hold of that and do it from there?

		# So the python version in the terminal is 2.7.5, using GCC 4.8.3.
		# Mari is using python 2.6.5, with GCC 4.1.2. It also uses Unicode Character Set 4.
		# I don't know if that has anything to do with these problems, but
		# The fact that I can do this in the terminal just fine - but I can't do this in Mari
		# is suspicious.
		# Okay, I tried running it in Mari with relative paths (os.path.relpath),
		# and it does get the correct relative path. But it still says it can't open the input file.

		print "path of file being converted: ", filePathNoUDIM + '_' + str(udim) + '.png'
		# Changing the permissions of the .png file, just in case that is a problem.
		os.system('chmod 777 ' + filePathNoUDIM + '_' + str(udim) + '.png')
		# Convert with Houdini iconvert
		args = ['iconvert', '-g', 'off', filePathNoUDIM + '_' + str(udim) + '.png', filePathNoUDIM + '_' + str(udim) + '.rat', 'makemips', 'compression="none"']
		# Consider the changing the working directory for the files?
		print "dirname of filePath"
		print os.path.dirname(filePathNoUDIM)
		try:
			# Mari runs on Python 2.6... Are Houdini 14 stuff in 2.7??
			subprocess.check_call(args)
		except subprocess.CalledProcessError as e:
			mari.utils.message("Error: " + str(e))

		# Delete the PNG file
		os.remove(filePathNoUDIM + '_' + str(udim) + '.png')

def exportChannel(geo, channel):
	# NOTE: As we are saving these images as pngs, the color depth MUST be 8-bit!
	# Set the template for the file name
	fileName = '$ENTITY_$CHANNEL_$UDIM'
	fileExt = '.png'

	# Check for the project info file 
	cp = ConfigParser()
	projPath = mari.current.project().info().projectPath()[:-11]
	cp.read(os.path.join(projPath, ".projectInfo")) 
	exportPath = ""

	try:
		# Try and pull the last export path
		exportPath = cp.get("FilePaths", "Export")
	except:
		# If there was none, Prompt user for destination directory
		exportPath = mari.utils.getExistingDirectory(None, 'Select Map Export Path for \"' + channel.name() + '\"')
		if(len(exportPath) == 0):
			return
		else:
			# Save it to a project info file
			projInfo = ConfigParser()
			projInfo.add_section("FilePaths")
			projInfo.set("FilePaths", "Export", exportPath)
			projInfoFile = open(os.path.join(projPath, ".projectInfo"), "wb")
			projInfo.write(projInfoFile)

	# Save all images as PNG
	fullFilePath = exportPath + '/' + fileName + fileExt
	print fullFilePath
	channel.exportImagesFlattened(fullFilePath, mari.Image.DISABLE_SMALL_UNIFORMS)

	# Convert to RAT
	convertToRat(geo, exportPath + '/' + geo.name() + '_' + channel.name())


def exportSelectedMaps():
	print "Export Selected"

	# Make sure that there is an open project
	if mari.projects.current() is None:
		mari.utils.message('Please open a project first')
		return

	# Find the currently selected object
	geo = mari.geo.current()
	if geo is None:
		mari.utils.message('Please select an object to export a channels from.')

	# Find the currently selected channel
	channel = geo.currentChannel()
	if channel is None:
		mari.utils.message('Please select a channel to export.')

	# Export all images in channel
	exportChannel(geo, channel)

	mari.utils.message('Maps for \"' + channel.name() + '\" successfully exported.')

def exportAllMaps():
	print "Exporting All Maps"

	# Make sure that there is an open project
	if mari.projects.current() is None:
		mari.utils.message('Please open a project first')
		return

	# Find the currently selected object
	geo = mari.geo.current()
	if geo is None:
		mari.utils.message('Please select an object to export a channels from.')

	# Get a list of all the channels attached to the current object
	channels = geo.channelList()
	print geo.name()
	print geo

	# Export all images in each channel
	for chan in channels:
		print chan.name()
		print chan
		exportChannel(geo, chan)

	mari.utils.message('All maps successfully exported.')
	
# ------------------------------------------------------------------------------


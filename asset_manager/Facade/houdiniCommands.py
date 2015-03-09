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
        name = hou_asset_mgr.formatName(name)
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
            fileutil.clobberPermissions(stablepath)
            os.symlink(stablepath, newfilepath)
            hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            newnode = hou.node(hpath).createNode(filename)
            
            # templateNode.type().definition().copyToHDAFile(newfilepath, new_name=filename, new_menu_name=name)
            # hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            # fileutil.clobberPermissions(newfilepath)
            # newnode = hou.node(hpath).createNode(filename)
        else:
            hou.ui.displayMessage("Asset by that name already exists. Cannot create asset.", title='Asset Name', severity=hou.severityType.Error)
        
    # clean up
    templateNode.destroy()

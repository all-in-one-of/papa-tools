import checkin_Nuke as ci
import checkout_Nuke as co
import rollback_Nuke as rb

def checkout():
    # nuke.message('check out')
    co.go()

def checkin():
    # nuke.message('check in')
    ci.go()

def discard():
    nuke.message('discard')

def unlock():
	nuke.message('unlock')

def rollback():
    nuke.message('rollback')

nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/check out', 'checkout()')
nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/check in', 'checkin()')
nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/discard', 'discard()')
nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/unlock', 'unlock()')
nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/rollback', 'rollback()')


#! /usr/bin/python

#TODO add the ability to read configs from a file and then run the rsync
#TODO add a GUI and script up the options that can be applied to rsync
#TODO add the ability to store passwords using a hash to hide the password??
#TODO add logging and maybe email notifications

# Stolen from https://ryanveach.com/233/calling-rsync-with-pythons-subprocess-module/


import subprocess
import os
import re
import yaml

def do_rsync(rh, ru, rd, rf, ld, sw):
    # rh == remote host name or ip address
    # ru == remote user name
    # rd == remote diretcory full path should be used
    # rf == remote file if you want to move only one file
    # ld == local directory, full path should be used


    # The full file path is the directory plus file.
    # But if we dont wnat a file but the whole directory then we need to use a "/" int he config file and then ignore it
    if not rf == "/":
        remote = os.path.join(rd, rf)
    else:
        remote = rd
    print remote
    # escape all characters in the full file path
    remote = re.escape(remote)
    print remote

    # format the remote location as 'username@hostname:'location'
    remote = "%s@%s:'%s'" % (ru, rh, remote)
    print remote

    # define the desired full path of the new file
    # Again caught out by the behaviour of the "/" in os.path.join
    if not rf == "/":
        local = os.path.join(ld, rf)
    else:
        local = ld

    # This statement will provide the contaioning directory of the file
    # this is usefull in case the file passed as rf contains a directory
    localdir = os.path.split(local)[0]

    # os.path.split always returns a diretcory without the trailing /
    # Add it back
    localdir = "%s/" % localdir

    # escape all characters in the local filename / directory
    local = re.escape(local)
    localdir = re.escape(localdir)

    # rsync options switch by defualt use -avz 'Archive (archive mode; same as -rlptgoD (no -H)), verbose, compression'
    if sw == "":
        switch = "avz"
    else:
        switch = sw


    # before issuing the rsync command, I've been running a mkdir command
    # Without this, if the directory did not exist, rsync would fail.
    # If the directory exists, then the mkdir command does nothing.
    # If you are copying the file to the remote directory, the mkdir command can be passed by ssh
    #mkdir_cmd = '/bin/mkdir -p %s' % localdir

    # create the rsync command
    rsync_cmd = '/usr/bin/rsync -%s %s %s' % (switch, remote, local)

    # now we run the commands
    # shell=True is used as the escaped characters would cause failures
    #p1 = subprocess.Popen(mkdir_cmd, shell=True).wait()
    p2 = subprocess.Popen(rsync_cmd, shell =True).wait()

    # for testing only
    print rsync_cmd
    print""
    return 0






with open("docs/config.txt", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

#for section in cfg:
#    print(section)
#print(cfg['remote'])
#print(cfg['local'])
#print(cfg['options'])

#for key in cfg['remote']: print (key)
rh = cfg ['remote']['host']
ru = cfg ['remote']['user']
rd = cfg ['remote']['directory']
rf = cfg ['remote']['file']
ld = cfg ['local']['directory']
sw = cfg ['options']['switch']



#print ("remote dir = %s" )%(rd)

#do_rsync(rh, ru, rd, rf, ld, sw)

# Test details for moving files from shed_bot to Minty....
#rh = "10.100.1.223"
#ru = "benc"
#rd = "/Volumes/DATA/iTunes Media/Music/X/"
#rf = "Live At The Stagedoor Tavern"
#ld = "/Data/Music/X/"


print "Here we do a simple test with test.dat"
do_rsync(rh, ru, rd, rf, ld, sw)

#rf = "this is a filename - with (stuff) in it.dat"




exit()


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


def show_header():
    print('##########################')
    print('#   Backup Media Store   #')
    print('##########################')


def do_rsync(rh, ru, rd, ld, sw, rf=None):

    # The full file path is the directory plus file.
    # But if we don't want a file but the whole directory then we need to use a "/"
    # in the config file and then ignore it
    if rf is not None:
        if not rf == "/":
            remote = os.path.join(rd, rf)
        else:
            remote = rd
    # print remote
    # escape all characters in the full file path
    remote = re.escape(remote)
    # print remote

    # format the remote location as 'username@hostname:'location'
    remote = "%s@%s:'%s'" % (ru, rh, remote)
    print("Source directory is {}".format(remote))

    # define the desired full path of the new file
    # Again caught out by the behaviour of the "/" in os.path.join
    if rf is not None:
        if not rf == "/":
            local = os.path.join(ld, rf)
        else:
            local = ld

    # This statement will provide the containing directory of the file
    # this is useful in case the file passed as rf contains a directory
    localdir = os.path.split(local)[0]

    # os.path.split always returns a directory without the trailing /
    # Add it back
    localdir = "%s/" % localdir

    # escape all characters in the local filename / directory
    local = re.escape(local)
    localdir = re.escape(localdir)
    assert isinstance(local, object)
    print("Destination directory is {}".format(str(local)))

    # rsync options switch by default use -avz 'Archive (archive mode; same as -rlptgoD (no -H)), verbose, compression'
    if sw == "":
        switch = "av"
    else:
        switch = sw

    # before issuing the rsync command, I've been running a mkdir command
    # Without this, if the directory did not exist, rsync would fail.
    # If the directory exists, then the mkdir command does nothing.
    # If you are copying the file to the remote directory, the mkdir command can be passed by ssh
    mkdir_cmd = '/bin/mkdir -p %s' % localdir

    # create the rsync command
    rsync_cmd = '/usr/bin/rsync -%s %s %s' % (switch, remote, local)
    print("The command to be run is {}".format(rsync_cmd))
    # now we run the commands
    # shell=True is used as the escaped characters would cause failures
    # p1 = subprocess.Popen(mkdir_cmd, shell=True).wait()
    try:
        subprocess.Popen(rsync_cmd, shell =True).wait()
    except ValueError:
        print('Opps! something is wrong at the remote end')


def get_options():
    with open("docs/config.txt", 'r') as ymlfile:
        # rh == remote host name or ip address
        # ru == remote user name
        # rd == remote directory full path should be used
        # rf == remote file if you want to move only one file
        # ld == local directory, full path should be used
        # md == The media files to copy i.e. the directory to copy the files from.
        cfg = yaml.load(ymlfile)
        rh = cfg['remote']['host']
        ru = cfg['remote']['user']
        rd = cfg['remote']['directory']
        rf = cfg['remote']['file']
        ld = cfg['local']['directory']
        sw = cfg['options']['switch']
        md = cfg['remote']['Media']

        return{'optrh':rh, 'optru':ru, 'optrd':rd, 'optrf':rf, 'optld':ld,'optsw':sw, 'optmd':md}


if __name__ == '__main__':
    show_header()
    options= get_options()
    # Dirs to rsync
    dirs = (options['optmd'])
    for rrd in dirs:
        do_rsync(options['optrh'], options['optru'], options['optrd'] + rrd, options['optrf'], options['optld'], options['optsw'])
        #do_rsync(options['optrh'], options['optru'], options['optrd'] + rrd, options['optld'],
        #         options['optsw'])
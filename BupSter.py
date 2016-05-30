#! /usr/bin/python

import subprocess
import os
import re


def do_rsync(rh, ru, rd, rf, ld):
    # The full file path is the directory plus file.
    remote = os.path.join(rd, rf)

    # escape all characters in the full file path
    remote = re.escape(remote)

    # format the remote location as 'username@hostname:'location'
    remote = "%s@%s:'%s'" % (ru, rh, remote)

    # define the desired full path of the new file
    local = os.path.join(ld, rf)

    # This statement will provide the contaioning directory of the file
    # this is usefull in case the file passed as rf contains a directory
    localdir = os.path.split(local)[0]

    # os.path.split always returns a diretcory without the trailing /
    # Add it back
    localdir = "%s/" % localdir

    # escape all characters in the local filename / directory
    local = re.escape(local)
    localdir = re.escape(localdir)

    # before issuing the rsync command, I've been running a mkdir command
    # Without this, if the directory did not exist, rsync would fail.
    # If the directory exists, then the mkdir command does nothing.
    # If you are copying the file to the remote directoy, the mkdir command can be passed by ssh
    mkdir_cmd = '/bin/mkdir -p %s' % localdir


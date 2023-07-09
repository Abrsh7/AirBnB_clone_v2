#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive (gzip compression) from the
 contents of the web_static
"""
from datetime import datetime
from fabric.api import local, runs_once
from os.path import isdir


@runs_once
def do_pack():
    """Packs web_static to versions/web_static_{date}.tgz"""
    try:
        if isdir("versions") is False:
            local("mkdir versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        print("Packing web_static to {}".format(file_name))
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None

#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive (gzip compression) from the
 contents of the web_static and deploys it to the servers
"""
from datetime import datetime
from fabric.api import env, run, local, put, runs_once
from fabric.decorators import hosts
from os.path import isdir, exists

env.hosts = ['100.26.221.249', '54.86.77.179']


@hosts("<local-only>")
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


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    extract_loc = archive_path.split(".tgz")[0]
    extract_loc = extract_loc.split("versions/")[1]
    extract_loc = "/data/web_static/releases/{}".format(extract_loc)
    remote_archive = archive_path.split("versions/")[1]
    remote_archive = "/tmp/{}".format(remote_archive)
    if archive_path and exists(archive_path):
        put(archive_path, remote_archive)
        run("mkdir -p {}/".format(extract_loc))
        run("tar -zxf {} -C {}/".format(remote_archive, extract_loc))
        run("rm -r {}".format(remote_archive))
        run("mv {}/web_static/* {}/".format(extract_loc, extract_loc))
        run("rm -rf {}/web_static".format(extract_loc))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(extract_loc))
        print("New version deployed!")
        return True
    else:
        return False


def deploy():
    """Compresses and distributes the web_static content to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


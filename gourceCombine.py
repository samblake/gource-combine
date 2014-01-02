import re
import subprocess
import os
import sys
from xml.dom.minidom import parse, getDOMImplementation


def launch(cmd, split_lines=True):
    stdout = ""
    stderr = ""
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=False, stderr=subprocess.PIPE)
        stdoutAndErr = p.communicate()
        stdout = stdoutAndErr[0]
        stderr = stdoutAndErr[1]
    except OSError, inst:
        raise LaunchError(1, cmd, stdout + " " + stderr + ": " + str(inst))
    
    printLines(stdout)
    if p.returncode == 0:
        return stdout.splitlines(False)
    else:
        for line in stderr.splitlines(False):
            print line
        raise LaunchError(p.returncode, cmd)

class LaunchError(Exception):
    "Command could not be run"


log = "log.xml"
workspace = "C:/Users/sam.adams/trunk"
projects = ["edge-core", "edge-common", "edge-engines", "eeg-common"]

dirs = [workspace + "/" + project for project in projects]


combined = getDOMImplementation().createDocument(None, "log", None)

for project in projects:
    dir = workspace + "/" + project
    os.chdir(dir)
    launch("svn log -r {2013-01-01}:HEAD --xml --verbose --quiet > " + log)

    dom = parse(log)
    for node in dom.documentElement.childNodes:
        combined.documentElement.appendChild(node)

nodes = combined.getElementsByTagName('logentry')
nodes.sort(key=lambda e: int(e.attributes['revision'].value))

with codecs.open("log.xml", "w", "utf-8") as out:
    combined.writexml(out)

#file_handle = open("filename.xml","wb")
#Your_Root_Node.writexml(file_handle)
#file_handle.close()

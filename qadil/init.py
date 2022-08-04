import sys
import re
import os
import shutil
import glob

chapterdir = sys.argv[1]
scriptdir = sys.path[0]

def copy_directory_if_dest_does_not_exist(sourceDir, destinationDir):
    if os.path.isdir(destinationDir):
        return

    os.mkdir(destinationDir)

    for fullName in glob.glob(sourceDir + '/*'):
        m = re.search('(\w+\.\w+)$', fullName)
        fileName = m.group(0)
        shutil.copyfile(fullName, destinationDir + '/' + fileName)

copy_directory_if_dest_does_not_exist(scriptdir + '/js', chapterdir + '/js')
copy_directory_if_dest_does_not_exist(scriptdir + '/css', chapterdir + '/css')

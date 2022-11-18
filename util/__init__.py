import os
import fnmatch
import gzip
import tarfile
import zipfile
import shutil
from datetime import datetime, timedelta
import time


def del_from_dict(row, start, stop=0):
    """ Delete item from ordered dict (1-based array) """

    if start > 0:
        start = start - 1
    if stop == 0:
        stop = start
    else:
        stop = stop - 1

    keys = list(row.keys())

    if start == -1:
        del row[keys[-1]]
    else:
        for index in range(start, stop + 1):
            del row[keys[index]]

    return row


def dict_to_list(row):

    ret = []
    for key in row:
        ret.append(row[key])
    return ret


def copyfile(src, dest):
    shutil.copyfile(src, dest)


def removedir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def copytree(src, dest):

    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def get_folders(path, value):
    matches = []
    for root, dirs, files in os.walk(path):             # pylint: disable=W0612
        for dirs in fnmatch.filter(files, value):
            matches.append(root)
    # Sort folder alphabetically
    matches.sort()

    return matches


def get_files(path, value):
    matches = []
    for root, dirs, files in os.walk(path):             # pylint: disable=W0612
        for filename in fnmatch.filter(files, value):
            matches.append(filename)
    # Sort files alphabetically
    matches.sort()

    return matches


def extract_bz2(filename, path="."):
    with tarfile.open(filename, "r:bz2") as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path)


def extract_tar(filename, path="."):
    with tarfile.open(filename) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path)


def extract_zip(filename, path="."):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(path)


def extract_dmg(filename, path="."):
    # hdiutil attach -mountpoint <path-to-desired-mountpoint> <filename.dmg>
    # hdiutil detach <path-to-mountpoint>
    return 1


def extractfile(target, path='.'):

    ret = 0
    filename, file_extension = os.path.splitext(target)  # pylint: disable=W0612

    switcher = {
        '.bz2': extract_bz2,
        '.gz': extract_tar,
        '.tar': extract_tar,
        '.zip': extract_zip
    }

    # Get the function from switcher dictionary
    func = switcher.get(file_extension, lambda: 1)
    # Execute the function
    ret = func(target, path)

    return ret


def sleep(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1, 1, 1) + sec         # pylint: disable=C0103
    print("Sleeping for %02d:%02d" % (d.minute, d.second), flush=True)
    for i in range(seconds, 0, -1):
        sec = timedelta(seconds=int(i))
        d = datetime(1, 1, 1) + sec         # pylint: disable=C0103
        print("%02d:%02d" % (d.minute, d.second), end='\r', flush=True)
        time.sleep(1)
    print('', end='\n')

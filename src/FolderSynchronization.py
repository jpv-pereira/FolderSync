import hashlib
import os
import shutil
import threading
import json
from log import FileLog

SOURCE_DIR = ""
TARGET_DIR = ""
SYNC_TIME = 0
FileLog: FileLog

def load_config():
    global SOURCE_DIR, TARGET_DIR, SYNC_TIME, FileLog

    configFile = open('config.json')
    config = json.load(configFile)

    if not config['SOURCE_DIR'] or not config['TARGET_DIR'] or not config['LOG_DIR'] or config['Sync_sec'] <= 0:
        print("Please configure config.json")
        exit(1)

    SOURCE_DIR = config['SOURCE_DIR']
    TARGET_DIR = config['TARGET_DIR']
    LOG_DIR = config['LOG_DIR']
    FileLog = FileLog(LOG_DIR)
    SYNC_TIME = config['Sync_sec']

    configFile.close()


def main():
    # Repeat main every X seconds
    thread = threading.Timer(SYNC_TIME, main)
    thread.start()

    sourceFiles = os.listdir(SOURCE_DIR)
    targetFiles = os.listdir(TARGET_DIR)

    checkMD5Files = []

    # Files that are to be replaced
    replaceFiles = []

    # Files that are set to be copied
    copyFiles = []

    compare_files(sourceFiles, targetFiles, checkMD5Files, copyFiles)

    compare_md5_hash(checkMD5Files, replaceFiles, copyFiles)

    delete_and_copy_files(replaceFiles, copyFiles)


def get_branching_folder():
    return 0


def compare_files(sourceFiles, targetFiles, checkMD5Files, copyFiles):
    for file in sourceFiles:
        if file not in targetFiles:
            FileLog.log(file + ": set to copy (does not exist in target files)")
            copyFiles.append(file)
        else:
            FileLog.log(file + ": set to compare MD5 hash.")
            checkMD5Files.append(file)
    if not checkMD5Files:
        FileLog.log("No files to check for md5")


def compare_md5_hash(checkMD5Files, replaceFiles, copyfiles):
    allFilesMatch = True

    for file in checkMD5Files:
        sourceMD5 = get_md5_hash(os.path.join(SOURCE_DIR, file))
        checkMD5 = get_md5_hash(os.path.join(TARGET_DIR, file))
        if sourceMD5 != checkMD5:
            FileLog.log("MD5 mismatch, file set to update")
            replaceFiles.append(file)
            allFilesMatch = False

    if allFilesMatch and not copyfiles:
        FileLog.log("All files match")


def delete_and_copy_files(replaceFiles, copyFiles):
    for file in replaceFiles:
        os.remove(os.path.join(TARGET_DIR, file))
        FileLog.log("removed " + file)
        copyFiles.append(file)

    for file in copyFiles:
        shutil.copy(os.path.join(SOURCE_DIR, file), os.path.join(TARGET_DIR, file))
        FileLog.log('copied file "' + file + '" to target folder')


def get_md5_hash(filename):
    with open(filename, "rb") as file:
        bytes = file.read()
        md5 = hashlib.md5(bytes).hexdigest()
        # print(filename + ": " + md5)
        return md5


if __name__ == "__main__":
    load_config()
    main()

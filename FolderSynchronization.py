import hashlib
import os
import shutil
from datetime import datetime

SOURCE_DIR = ""
TARGET_DIR = ""

def main():
    global SOURCE_DIR, TARGET_DIR

    SOURCE_DIR = input("Enter the source directory: ")
    TARGET_DIR = input("Enter the target directory: ")

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
            log(file + ": set to copy (does not exist in target files)")
            copyFiles.append(file)
        else:
            log(file + ": set to compare MD5 hash.")
            checkMD5Files.append(file)
    if not checkMD5Files:
        log("No files to check for md5")


def compare_md5_hash(checkMD5Files, replaceFiles, copyfiles):
    allFilesMatch = True

    for file in checkMD5Files:
        sourceMD5 = get_md5_hash(os.path.join(SOURCE_DIR, file))
        checkMD5 = get_md5_hash(os.path.join(TARGET_DIR, file))
        if sourceMD5 != checkMD5:
            log("MD5 mismatch, file set to update")
            replaceFiles.append(file)
            allFilesMatch = False

    if allFilesMatch and not copyfiles:
        log("All files match")


def delete_and_copy_files(replaceFiles, copyFiles):
    for file in replaceFiles:
        os.remove(os.path.join(TARGET_DIR, file))
        log("removed " + file)
        copyFiles.append(file)

    for file in copyFiles:
        shutil.copy(os.path.join(SOURCE_DIR, file), os.path.join(TARGET_DIR, file))
        log('copied file "' + file + '" to target folder')


def get_md5_hash(filename):
    with open(filename, "rb") as file:
        bytes = file.read()
        md5 = hashlib.md5(bytes).hexdigest()
        #print(filename + ": " + md5)
        return md5

def log(str):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(current_time + ": " + str)


if __name__ == "__main__":
    main()

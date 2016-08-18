#!/usr/bin/env python


import os
import sys
from os import listdir
from os.path import isfile, join
from shutil import copyfile

try:
    script_name = os.path.basename(__file__)

    def getSize(filename):
        return os.path.getsize(filename)
    try:
        folder_path = sys.argv[1]
        os.chdir(folder_path)
        extension=sys.argv[2]
        folder_size = float(sys.argv[3])
        destination = sys.argv[4]
        command = sys.argv[5]

    except:
        print "Invalid command try like  :   python "+script_name+" <<source_folder_path>> <<extension>> <<size_in_mb>> <<destination_path>> <<copy/move>>"
        os._exit(0)


    folder_size= folder_size * 1024 * 1024 #in byte
    folder=0

    files = [f for f in listdir('.') if isfile(join(folder_path, f))]
    size=folder_size

    matched_files=[]

    for file in files:
        if file.endswith(extension) and getSize(file) < folder_size:
            matched_files.append(file)

    if matched_files.__len__()==0:
        print "No matching files"
        if  files.__len__() > matched_files.__len__():
            print "All files are more than "+str(sys.argv[3])+"mb or having some other extension"

        os._exit(0)

    while(matched_files.__len__() >=1 ):


        try:
            folder = folder + 1
            new_folder_name = 'folder_'+str(folder)
            os.mkdir(destination+new_folder_name)
            print "Created folder "+new_folder_name
        except:
            pass

        size = folder_size



        for file in matched_files:
            current_size=getSize(file)
            if current_size < size:
                source_file=folder_path+file
                destination_file = destination+new_folder_name+'/'+file
                if command=='move':
                    os.rename(source_file,destination_file)
                    print "Moved file `" + file + "` having size of " + str(
                        (current_size / 1024) / 1024) + "Mb to folder `" + new_folder_name + '`'
                elif command=='copy':
                    copyfile(source_file, destination_file)
                    print "Copied file `" + file + "` having size of " + str(
                        (current_size / 1024) / 1024) + "Mb to folder `" + new_folder_name + '`'
                else:
                    pass

                size=size-current_size
                matched_files.remove(file)
            else:
                pass


    print "Successfully classified the files"

except Exception as e:
    print e.message

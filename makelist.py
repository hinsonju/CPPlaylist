#!/usr/bin/python
'''This program will create a random playlist of songs from a 
source directory. The size of the playlist is specified by the user
in megabytes'''
#Author: Cody Hinson

import sys
import os
import random
import math
import shutil

#Build a playlist from sourcePath that is no bigger than maxSize in MB
#Does not include duplicate items
def build_playlist(sourcePath, maxSize):
	listIndex = 0
	totalSize = 0
	playlist = dict()
	while True:
		filePath = get_file(sourcePath)
		fileName = os.path.basename(filePath)
		if fileName not in playlist:
			size = convert_B_to_MB(get_size(filePath))
			totalSize += size
			if totalSize >= maxSize: break
			playlist[fileName] = filePath
		print('SIZE: ' , totalSize)
	return playlist
	
#Get a random file from the source directory.
#May also grab a random file from a random directory is source Directory
def get_file(sourcePath):
	f = random.choice(os.listdir(sourcePath))
	newPath = sourcePath + '/' + f
	if os.path.isdir(newPath):
		return get_file(newPath)
	else: return newPath

def get_size(filePath):
	return os.path.getsize(filePath)

def convert_B_to_MB(bytes):
	return (bytes / (math.pow(10, 6)))

#copy files from playlist to target directory
def copy_files(playlist, targetPath):
	for item in playlist:
		path = playlist[item]
		print ('%s  %s' % (path, targetPath))
		shutil.copy2(path, targetPath)
	return
	
def main():
	if len(sys.argv) != 4:
		print ('usage: ./makelist sourceDirectory targetDirectory targetSize')
		sys.exit(1)
		
	sourcePath = os.path.abspath(sys.argv[1])
	targetPath = os.path.abspath(sys.argv[2])
	targetSize = int(sys.argv[3])
	
	if not os.path.exists(targetPath):
		print (targetPath + ' Does not exist. Should I create it? (Y or N)')
		response = input()
		if response.lower() == 'y': 
			os.mkdir(targetPath)
			print(targetPath + ' created.')
		else: 
			print('Aborting')
			sys.exit(1)
			
	playlist = build_playlist(sourcePath, targetSize)
	copy_files(playlist, targetPath)

if __name__ == '__main__':
	main()
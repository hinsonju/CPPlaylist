#!/usr/bin/python3
'''Creates a random playlist of songs from a 
source directory. The size of the playlist is specified by the user
in megabytes.'''
#Author: Cody Hinson

import sys
import os
import random
import shutil

def build_complete_song_list(sourcePath):
	complete_song_list = []
	for root, dirs, files in os.walk(sourcePath):
		for f in files: 
			complete_song_list.append(os.path.join(root, f))
	return complete_song_list


#Build a random playlist from completeList that is no bigger than maxSize in MB
#Does not include duplicate items
def build_playlist(completeList, maxSize):
	playlist = []
	totalSize = 0
	random.shuffle(completeList)
	for song in completeList:
		if song in playlist: continue
		size = convert_B_to_MB(get_size(song))
		totalSize += size
		if totalSize >= maxSize: break
		playlist.append(song)
	return playlist

def get_size(filePath):
	return os.path.getsize(filePath)

def convert_B_to_MB(bytes):
	return (bytes / (10**6))

#copy files from playlist to target directory
def copy_files(playlist, targetPath):
	for item in playlist:
		path = item
		print('Copying ' + item + '...', end = '')
		sys.stdout.flush()
		shutil.copy2(path, targetPath)
		print(' Copied')
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
			
	completeList = build_complete_song_list(sourcePath)
	playlist = build_playlist(completeList, targetSize)
	copy_files(playlist, targetPath)

if __name__ == '__main__':
	main()
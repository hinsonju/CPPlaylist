#!/usr/bin/python3
'''Creates a random playlist of songs from a 
source directory. The size of the playlist is specified by the user
in megabytes.'''
#Author: Cody Hinson

import sys
import os
import random
import shutil

#A MusicFile object has a name, path, and size
class MusicFile:
	def __init__(self, path):
		self.path = path
		self.name = os.path.basename(path)
		self.size = os.path.getsize(path)
		
	def copyTo(self, targetFolder):
		shutil.copy2(self.path, targetFolder)

#Returns a list of all items in sourcePath and subdirectories
def build_complete_song_list(sourcePath):
	complete_song_list = []
	for root, dirs, files in os.walk(sourcePath):
		for f in files:
			song = MusicFile(os.path.join(root, f))
			complete_song_list.append(song)
	return complete_song_list

#Build a random playlist from completeList that is no bigger than maxSize in MB
#Does not include duplicate items
def build_playlist(completeList, maxSize):
	playlist = []
	totalSize = 0
	random.shuffle(completeList)
	for song in completeList:
		if song in playlist: continue
		totalSize += song.size
		if totalSize >= maxSize: break
		playlist.append(song)
	return playlist

#copy files from playlist to target directory
def copy_files(playlist, targetPath):
	for song in playlist:
		print('Copying ' + song.name + '...', end = '')
		sys.stdout.flush()
		song.copyTo(targetPath)
		print(' Copied')
	return
	
def main():
	if len(sys.argv) != 4:
		print ('usage: ./makelist sourceDirectory targetDirectory targetSize')
		sys.exit(1)
		
	sourcePath = os.path.abspath(sys.argv[1])
	targetPath = os.path.abspath(sys.argv[2])
	targetSize = int(sys.argv[3])
	targetSize *= 10**6
	
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
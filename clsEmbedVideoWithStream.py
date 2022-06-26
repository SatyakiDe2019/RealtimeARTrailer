##################################################
#### Written By: SATYAKI DE                   ####
#### Written On: 22-Jun-2022                  ####
#### Modified On 25-Jun-2022                  ####
####                                          ####
#### Objective: This is the main class of     ####
#### python script that will invoke the       ####
#### clsAugmentedReality class to initiate    ####
#### augment reality after splitting the      ####
#### audio & video & then project them via    ####
#### the Web-CAM with a seamless broadcast.   ####
##################################################

# Importing necessary packages
import clsAugmentedReality as ar
from clsConfig import clsConfig as cf

from imutils.video import VideoStream
from collections import deque

import imutils
import time
import cv2
import subprocess
import os
import pygame
import time
import threading
import sys

###############################################
###           Global Section                ###
###############################################
# Instantiating the dependant class

x1 = ar.clsAugmentedReality()

###############################################
###    End of Global Section                ###
###############################################

class BreakLoop(Exception):
	pass

class clsEmbedVideoWithStream:
	def __init__(self):
		self.sep = str(cf.conf['SEP'])
		self.Curr_Path = str(cf.conf['INIT_PATH'])
		self.FileName = str(cf.conf['FILE_NAME'])
		self.CacheL = int(cf.conf['CACHE_LIM'])
		self.FileName_1 = str(cf.conf['FILE_NAME_1'])
		self.audioLen = int(cf.conf['audioLen'])
		self.audioFreq = float(cf.conf['audioFreq'])
		self.videoFrame = float(cf.conf['videoFrame'])
		self.stopFlag=cf.conf['stopFlag']
		self.zFlag=int(cf.conf['zoomFlag'])
		self.title = str(cf.conf['TITLE'])

	def playAudio(self, audioFile, audioLen, freq, stopFlag=False):
		try:
			pygame.mixer.init()
			pygame.init()
			pygame.mixer.music.load(audioFile)

			pygame.mixer.music.set_volume(10)

			val = int(audioLen)
			i = 0

			while i < val:
				pygame.mixer.music.play(loops=0, start=float(i))
				time.sleep(freq)

				i = i + 1

				if (i >= val):
					raise BreakLoop

				if (stopFlag==True):
					raise BreakLoop

			return 0
		except BreakLoop as s:
			return 0
		except Exception as e:
			x = str(e)
			print(x)

			return 1

	def extractAudio(self, video_file, output_ext="mp3"):
	    try:
	        """Converts video to audio directly using `ffmpeg` command
	        with the help of subprocess module"""
	        filename, ext = os.path.splitext(video_file)
	        subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
	                        stdout=subprocess.DEVNULL,
	                        stderr=subprocess.STDOUT)

	        return 0
	    except Exception as e:
	        x = str(e)
	        print('Error: ', x)

	        return 1

	def processStream(self, debugInd, var):
		try:
			sep = self.sep
			Curr_Path = self.Curr_Path
			FileName = self.FileName
			CacheL = self.CacheL
			FileName_1 = self.FileName_1
			audioLen = self.audioLen
			audioFreq = self.audioFreq
			videoFrame = self.videoFrame
			stopFlag = self.stopFlag
			zFlag = self.zFlag
			title = self.title

			print('audioFreq:')
			print(str(audioFreq))

			print('videoFrame:')
			print(str(videoFrame))

			# Construct the source for Video & Temporary Audio
			videoFile = Curr_Path + sep + 'Video' + sep + FileName
			audioFile = Curr_Path + sep + 'Video' + sep + FileName_1

			# Load the Aruco dictionary and grab the Aruco parameters
			print("[INFO] initializing marker detector...")
			arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
			arucoParams = cv2.aruco.DetectorParameters_create()

			# Initialize the video file stream
			print("[INFO] accessing video stream...")
			vf = cv2.VideoCapture(videoFile)

			x = self.extractAudio(videoFile)

			if x == 0:
			    print('Successfully Audio extracted from the source file!')
			else:
			    print('Failed to extract the source audio!')

			# Initialize a queue to maintain the next frame from the video stream
			Q = deque(maxlen=128)

			# We need to have a frame in our queue to start our augmented reality
			# pipeline, so read the next frame from our video file source and add
			# it to our queue
			(grabbed, source) = vf.read()
			Q.appendleft(source)

			# Initialize the video stream and allow the camera sensor to warm up
			print("[INFO] starting video stream...")
			vs = VideoStream(src=0).start()

			time.sleep(2.0)
			flg = 0

			t = threading.Thread(target=self.playAudio, args=(audioFile, audioLen, audioFreq, stopFlag,))
			t.daemon = True

			try:
				# Loop over the frames from the video stream
				while len(Q) > 0:
					try:
						# Grab the frame from our video stream and resize it
						frame = vs.read()
						frame = imutils.resize(frame, width=1020)

						# Attempt to find the ArUCo markers in the frame, and provided
						# they are found, take the current source image and warp it onto
						# input frame using our augmented reality technique
						warped = x1.getWarpImages(
							frame, source,
							cornerIDs=(923, 1001, 241, 1007),
							arucoDict=arucoDict,
							arucoParams=arucoParams,
							zoomFlag=zFlag,
							useCache=CacheL > 0)

						# If the warped frame is not None, then we know (1) we found the
						# four ArUCo markers and (2) the perspective warp was successfully
						# applied
						if warped is not None:
							# Set the frame to the output augment reality frame and then
							# grab the next video file frame from our queue
							frame = warped
							source = Q.popleft()

							if flg == 0:

								t.start()
								flg = flg + 1

						# For speed/efficiency, we can use a queue to keep the next video
						# frame queue ready for us -- the trick is to ensure the queue is
						# always (or nearly full)
						if len(Q) != Q.maxlen:
							# Read the next frame from the video file stream
							(grabbed, nextFrame) = vf.read()

							# If the frame was read (meaning we are not at the end of the
							# video file stream), add the frame to our queue
							if grabbed:
								Q.append(nextFrame)

						# Show the output frame
						cv2.imshow(title, frame)
						time.sleep(videoFrame)

						# If the `q` key was pressed, break from the loop
						if cv2.waitKey(2) & 0xFF == ord('q'):
							stopFlag = True
							break

					except BreakLoop:
						raise BreakLoop
					except Exception as e:
						pass

					if (len(Q) == Q.maxlen):
						time.sleep(2)
						break

			except BreakLoop as s:
				print('Processed completed!')

				# Performing cleanup at the end
				cv2.destroyAllWindows()
				vs.stop()

			except Exception as e:
				x = str(e)
				print(x)

			# Performing cleanup at the end
			cv2.destroyAllWindows()
			vs.stop()

			return 0
		except Exception as e:
			x = str(e)
			print('Error:', x)

			return 1

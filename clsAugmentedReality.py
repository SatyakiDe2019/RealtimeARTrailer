##################################################
#### Written By: SATYAKI DE                   ####
#### Written On: 20-Jun-2022                  ####
#### Modified On 25-Jun-2022                  ####
####                                          ####
#### Objective: This is the main class of     ####
#### python script that will embed the source ####
#### video with the WebCAM streams in         ####
#### real-time.                               ####
##################################################

# Importing necessary packages
import numpy as np
import cv2

from clsConfig import clsConfig as cf

# Initialize our cached reference points
CACHED_REF_PTS = None

class clsAugmentedReality:
	def __init__(self):
		self.TOP_LEFT_X = int(cf.conf['TOP_LEFT_X'])
		self.TOP_LEFT_Y = int(cf.conf['TOP_LEFT_Y'])
		self.TOP_RIGHT_X = int(cf.conf['TOP_RIGHT_X'])
		self.TOP_RIGHT_Y = int(cf.conf['TOP_RIGHT_Y'])
		self.BOTTOM_RIGHT_X = int(cf.conf['BOTTOM_RIGHT_X'])
		self.BOTTOM_RIGHT_Y = int(cf.conf['BOTTOM_RIGHT_Y'])
		self.BOTTOM_LEFT_X = int(cf.conf['BOTTOM_LEFT_X'])
		self.BOTTOM_LEFT_Y = int(cf.conf['BOTTOM_LEFT_Y'])

	def getWarpImages(self, frame, source, cornerIDs, arucoDict, arucoParams, zoomFlag, useCache=False):
		try:
			# Assigning values
			TOP_LEFT_X = self.TOP_LEFT_X
			TOP_LEFT_Y = self.TOP_LEFT_Y
			TOP_RIGHT_X = self.TOP_RIGHT_X
			TOP_RIGHT_Y = self.TOP_RIGHT_Y
			BOTTOM_RIGHT_X = self.BOTTOM_RIGHT_X
			BOTTOM_RIGHT_Y = self.BOTTOM_RIGHT_Y
			BOTTOM_LEFT_X = self.BOTTOM_LEFT_X
			BOTTOM_LEFT_Y = self.BOTTOM_LEFT_Y

			# Grab a reference to our cached reference points
			global CACHED_REF_PTS

			if source is None:
				raise

			# Grab the width and height of the frame and source image,
			# respectively
			# Extracting Frame from Camera
			# Exracting Source from Video
			(imgH, imgW) = frame.shape[:2]
			(srcH, srcW) = source.shape[:2]

			# Detect Aruco markers in the input frame
			(corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

			print('Ids: ', str(ids))
			print('Rejected: ', str(rejected))

			# if we *did not* find our four ArUco markers, initialize an
			# empty IDs list, otherwise flatten the ID list
			print('Detecting Corners: ', str(len(corners)))
			ids = np.array([]) if len(corners) != 4 else ids.flatten()

			# Initialize our list of reference points
			refPts = []
			refPtTL1 = []

			# Loop over the IDs of the ArUco markers in Top-Left, Top-Right,
			# Bottom-Right, and Bottom-Left order
			for i in cornerIDs:
				# Grab the index of the corner with the current ID
				j = np.squeeze(np.where(ids == i))

				# If we receive an empty list instead of an integer index,
				# then we could not find the marker with the current ID
				if j.size == 0:
					continue

				# Otherwise, append the corner (x, y)-coordinates to our list
				# of reference points
				corner = np.squeeze(corners[j])
				refPts.append(corner)

			# Check to see if we failed to find the four ArUco markers
			if len(refPts) != 4:
				# If we are allowed to use cached reference points, fall
				# back on them
				if useCache and CACHED_REF_PTS is not None:
					refPts = CACHED_REF_PTS

				# Otherwise, we cannot use the cache and/or there are no
				# previous cached reference points, so return early
				else:
					return None

			# If we are allowed to use cached reference points, then update
			# the cache with the current set
			if useCache:
				CACHED_REF_PTS = refPts

			# Unpack our Aruco reference points and use the reference points
			# to define the Destination transform matrix, making sure the
			# points are specified in Top-Left, Top-Right, Bottom-Right, and
			# Bottom-Left order
			(refPtTL, refPtTR, refPtBR, refPtBL) = refPts
			dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
			dstMat = np.array(dstMat)

            # For zoom option recalculating all the 4 points
			refPtTL1_L_X = refPtTL[0][0]-TOP_LEFT_X
			refPtTL1_L_Y = refPtTL[0][1]-TOP_LEFT_Y

			refPtTL1.append((refPtTL1_L_X,refPtTL1_L_Y))

			refPtTL1_R_X = refPtTL[1][0]+TOP_RIGHT_X
			refPtTL1_R_Y = refPtTL[1][1]+TOP_RIGHT_Y

			refPtTL1.append((refPtTL1_R_X,refPtTL1_R_Y))

			refPtTD1_L_X = refPtTL[2][0]+BOTTOM_RIGHT_X
			refPtTD1_L_Y = refPtTL[2][1]+BOTTOM_RIGHT_Y

			refPtTL1.append((refPtTD1_L_X,refPtTD1_L_Y))

			refPtTD1_R_X = refPtTL[3][0]-BOTTOM_LEFT_X
			refPtTD1_R_Y = refPtTL[3][1]+BOTTOM_LEFT_Y

			refPtTL1.append((refPtTD1_R_X,refPtTD1_R_Y))

			dstMatMod = [refPtTL1[0], refPtTL1[1], refPtTL1[2], refPtTL1[3]]
			dstMatMod = np.array(dstMatMod)

			# Define the transform matrix for the *source* image in Top-Left,
			# Top-Right, Bottom-Right, and Bottom-Left order
			srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])

			# Compute the homography matrix and then warp the source image to
			# the destination based on the homography depending upon the
			# zoom flag
			if zoomFlag == 1:
				(H, _) = cv2.findHomography(srcMat, dstMat)
			else:
				(H, _) = cv2.findHomography(srcMat, dstMatMod)

			warped = cv2.warpPerspective(source, H, (imgW, imgH))

			# Construct a mask for the source image now that the perspective
			# warp has taken place (we'll need this mask to copy the source
			# image into the destination)
			mask = np.zeros((imgH, imgW), dtype="uint8")
			if zoomFlag == 1:
				cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255), cv2.LINE_AA)
			else:
				cv2.fillConvexPoly(mask, dstMatMod.astype("int32"), (255, 255, 255), cv2.LINE_AA)

			# This optional step will give the source image a black
			# border surrounding it when applied to the source image, you
			# can apply a dilation operation
			rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
			mask = cv2.dilate(mask, rect, iterations=2)

			# Create a three channel version of the mask by stacking it
			# depth-wise, such that we can copy the warped source image
			# into the input image
			maskScaled = mask.copy() / 255.0
			maskScaled = np.dstack([maskScaled] * 3)

			# Copy the warped source image into the input image by
			# (1) Multiplying the warped image and masked together,
			# (2) Then multiplying the original input image with the
			#     mask (giving more weight to the input where there
			#     are not masked pixels), and
			# (3) Adding the resulting multiplications together
			warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
			imageMultiplied = cv2.multiply(frame.astype(float), 1.0 - maskScaled)
			output = cv2.add(warpedMultiplied, imageMultiplied)
			output = output.astype("uint8")

			# Return the output frame to the calling function
			return output

		except Exception as e:

			# Delibarately raising the issue
			# That way the control goes to main calling methods
			# exception section
			raise

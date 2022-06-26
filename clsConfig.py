################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 22-Jun-2022               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### Augmented Reality via WebCAM streaming.####
####                                        ####
################################################

import os
import platform as pl

class clsConfig(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'REPORT_PATH': Curr_Path + sep + 'report',
        'FILE_NAME': 'Feludar Goendagiri.mov',
        'FILE_NAME_1': 'Feludar Goendagiri.mp3',
        'SRC_PATH': Curr_Path + sep + 'data' + sep,
        'FINAL_PATH': Curr_Path + sep + 'Target' + sep,
        'APP_DESC_1': 'Video Emotion Capture!',
        'DEBUG_IND': 'N',
        'INIT_PATH': Curr_Path,
        'SUBDIR': 'data',
        'audioLen': 150,
        'audioFreq': 0.88,
        'videoFrame': 0.013248,
        'stopFlag': False,
        'zoomFlag': 1,
        'SEP': sep,
        'TOP_LEFT_X':20,
        'TOP_LEFT_Y':31,
        'TOP_RIGHT_X':170,
        'TOP_RIGHT_Y':-20,
        'BOTTOM_RIGHT_X':160,
        'BOTTOM_RIGHT_Y':175,
        'BOTTOM_LEFT_X':30,
        'BOTTOM_LEFT_Y':180,
        'TITLE': "Feludar Goendagiri",
        "CACHE_LIM": 1
    }

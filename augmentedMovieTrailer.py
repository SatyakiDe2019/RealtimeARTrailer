#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 22-Jun-2022                     ####
#### Modified On 25-Jun-2022                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsEmbedVideoWithStream class to initiate   ####
#### the augmented reality in real-time          ####
#### & display a trailer on top of any surface   ####
#### via Web-CAM.                                ####
#####################################################

# We keep the setup code in a different class as shown below.
import clsEmbedVideoWithStream as evws

from clsConfig import clsConfig as cf

import datetime
import logging

###############################################
###           Global Section                ###
###############################################
# Instantiating all the main class

x1 = evws.clsEmbedVideoWithStream()

###############################################
###    End of Global Section                ###
###############################################

def main():
    try:
        # Other useful variables
        debugInd = 'Y'
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        var1 = datetime.datetime.now()

        print('Start Time: ', str(var))
        # End of useful variables

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        logging.basicConfig(filename=general_log_path + 'augmentedMovieTrailer.log', level=logging.INFO)

        print('Started augmenting videos!')

        # Execute all the pass
        r1 = x1.processStream(debugInd, var)

        if (r1 == 0):
            print('Successfully identified human emotions!')
        else:
            print('Failed to identify the human emotions!')

        var2 = datetime.datetime.now()

        c = var2 - var1
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', str(minutes))

        print('End Time: ', str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()

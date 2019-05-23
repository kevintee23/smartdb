# User Configuration variable settings for smartdb
# Purpose - Global setting for certain specific parameters
# Updated - 17-May-2019
# Done by - Kevin Tee

#======================================
#   takepicture.py Settings
#======================================


fport = 5000                  # default= 5000 The webserver port that the script will run on
wcurl = 'https://graph-'      # The URL of your smart home piston/rule that the script will send the results of a face match to
POtoken = 'yourTokenHere'     # Your Pushover account Token ID
POuser = 'yourUserKey'        # Your Pushover User Key
ifturl = 'iftttUrlHere'       # Your IFTTT URL
picQuality = 15               # Value range is between 10-100 (default:20)
vflip = '-vf'                 # To vertical flip your picture enter "-vf", otherwise leave blank ("")
hflip = '-hf'                 # To horizontally flip your picture enter "-hf", otherwise leave blank ("")

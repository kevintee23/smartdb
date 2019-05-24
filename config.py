from ConfigParser import ConfigParser

config = ConfigParser()

config.read('config1.ini')

fport = config.get('Webserver', 'fport')
wcurl = config.get('App Settings', 'wcurl')
POtoken = config.get('App Settings', 'POtoken')
POuser = config.get('App Settings', 'POuser')
ifturl = config.get('App Settings', 'ifturl')
iftEvent = config.get('App Settings', 'iftEvent')
picQuality = config.get('Camera Settings', 'picQuality')
vflip = config.get('Camera Settings', 'vflip')
hflip = config.get('Camera Settings', 'hflip')

print("Leave blank (by hitting ENTER) if you do not intend to change any of the values") 

#for section_name in config.sections():
#	print("Section:", section_name)
#	for name, value in config.items(section_name):
#		print("    {} = {}".format(name,value))
#	print()

#webserver port
try:
	new_fport=input("[Current Port: %s] Port: " % fport)
except SyntaxError:
	new_fport=config.get('Webserver', 'fport')

config.set('Webserver', 'fport', new_fport)

#Picture quality
try:
	new_picQuality=input("[Current quality settings: %s] Quality: " % picQuality)
except SyntaxError:
	new_picQuality=config.get('Camera Settings', 'picQuality')

config.set('Camera Settings', 'picQuality', new_picQuality)

#webCoRE piston URL
try:
        new_wcurl=input("Enter/paste webCoRE piston URL: ")
except SyntaxError:
        new_wcurl=config.get('App Settings', 'wcurl')

config.set('App Settings', 'wcurl', new_wcurl)

#Pushover Token settings
try:
        new_POtoken=input("[Current Token: %s] New Token: " % POtoken)
except SyntaxError:
        new_POtoken=config.get('App Settings', 'POtoken')

config.set('App Settings', 'POtoken', new_POtoken)

#Pushover User key
try:
        new_POuser=input("[Current User Key: %s] New User Key: " % POuser)
except SyntaxError:
        new_POuser=config.get('App Settings', 'POuser')

config.set('App Settings', 'POuser', new_POuser)

#IFTTT URL
try:
        new_ifturl=input("Enter/paste your IFTTT Maker URL: ")
except SyntaxError:
        new_ifturl=config.get('App Settings', 'ifturl')

config.set('App Settings', 'ifturl', new_ifturl)

#IFTTT Event Name
try:
        new_iftEvent=input("[Current Event Name: %s] Event Name: " % iftEvent)
except SyntaxError:
        new_iftEvent=config.get('App Settings', 'iftEvent')

config.set('App Settings', 'iftEvent', new_iftEvent)

with open('config1.ini', 'w') as configfile:
	config.write(configfile)

#Picture - Vertical Setting
if vflip == '-vf':
        new_vflip=raw_input("Flip Vertically: TRUE, change(yes/no)")
        if new_vflip == 'no':
                new_vflip='-vf'
                print("Flip Vertically: TRUE")
                
        if new_vflip == 'yes':
        		new_vflip=''
        		print("Flip Vertically: FALSE")
        		
        else:
                new_vflip='-vf'
                print("Flip Vertically: TRUE")
                
else:
        new_vflip=raw_input("Flip Vertically: FALSE, change(yes/no)")
        if new_vflip == 'no':
                new_vflip=''
                print("Flip Vertically: FALSE")
                
        if new_vflip == 'yes':
        		new_vflip='vf'
        		print("Flip Vertically: TRUE")
        		
        else:
                new_vflip=''
                print("Flip Vertically: FALSE")
                
with open('config1.ini', 'w') as configfile:
	config.write(configfile)
                
#Picture - Horizontal Setting
if hflip == '-hf':
        new_hflip=raw_input("Flip Horizontally: TRUE, change(yes/no)")
        if new_hflip == 'no':
                new_hflip='-hf'
                print("Flip Horizontally: TRUE")
                
        if new_hflip == 'yes':
        		new_hflip=''
        		print("Flip Horizontally: FALSE")
        		
        else:
                new_hflip='-hf'
                print("Flip Horizontally: TRUE")
                
else:
        new_hflip=raw_input("Flip Horizontally: FALSE, change(yes/no)")
        if new_hflip == 'no':
                new_hflip=''
                print("Flip Horizontally: FALSE")
                
        if new_hflip == 'yes':
        		new_hflip='hf'
        		print("Flip Horizontally: TRUE")
        		
        else:
                new_hflip=''
                print("Flip Horizontally: FALSE")
                
with open('config1.ini', 'w') as configfile:
	config.write(configfile)

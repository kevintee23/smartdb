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
collectionid = config.get('App Settings', 'collectionid')

print (" ")
print("Leave blank (by hitting ENTER) if you do not intend to change any of the values") 
print("-------------------------------------------------------------------------------")
print(" ")

print("-------------")
print("Port Settings")
print("_____________")
new_fport=raw_input("[Current Port: %s] Port: " % fport)
if new_fport == '':
        new_fport=fport

config.set('Webserver', 'fport', new_fport)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Port: %s" % config.get('Webserver', 'fport'))
print(" ")

print("--------------------")
print("WebCoRE URL Settings")
print("____________________")
new_wcurl=raw_input("Enter/paste webCoRE piston URL: ")
if new_wcurl == '':
        new_wcurl=wcurl

config.set('App Settings', 'wcurl', new_wcurl)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Piston URL: %s" % config.get('App Settings', 'wcurl'))
print(" ")

print("--------------")
print("Pushover Token")
print("______________")
new_POtoken=raw_input("[Pushover Token: %s] New Token: " % POtoken)
if new_POtoken == '':
        new_POtoken=POtoken

config.set('App Settings', 'POtoken', new_POtoken)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Pushover Token: %s" % config.get('App Settings', 'POtoken'))
print(" ")

print("-----------------")
print("Pushover User Key")
print("_________________")
new_POuser=raw_input("[Pushover User Key: %s] New User Key: " % POuser)
if new_POuser == '':
        new_POuser=POuser

config.set('App Settings', 'POuser', new_POuser)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Pushover User Key: %s" % config.get('App Settings', 'POuser'))
print(" ")

print("--------------------------")
print("Picture Setting - Vertical")
print("__________________________")
if vflip == '-vf':
        new_vflip=raw_input("Flip Vertically: TRUE; change(yes/no)")
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
        new_vflip=raw_input("Flip Vertically: FALSE; change(yes/no)")
        if new_vflip == 'no':
                new_vflip=''
                print("Flip Vertically: FALSE")
                
        if new_vflip == 'yes':
        		new_vflip='-vf'
        		print("Flip Vertically: TRUE")
        		
        else:
                new_vflip=''
                print("Flip Vertically: FALSE")
                
config.set('Camera Settings', 'vflip', new_vflip)

with open('config1.ini', 'w') as configfile:
	config.write(configfile)
print(" ")

print("----------------------------")
print("Picture Setting - Horizontal")
print("____________________________")
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
        		new_hflip='-hf'
        		print("Flip Horizontally: TRUE")
        		
        else:
                new_hflip=''
                print("Flip Horizontally: FALSE")
                
config.set('Camera Settings', 'hflip', new_hflip)

with open('config1.ini', 'w') as configfile:
	config.write(configfile)
print(" ")

print("------------------------")
print("Picture Quality (1 - 100)")
print("________________________")
new_picQuality=raw_input("[Current Picture Quality: %s] New Setting: " % picQuality)
if new_picQuality == '':
        new_picQuality=picQuality

config.set('Camera Settings', 'picQuality', new_picQuality)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Picture Quality: %s" % config.get('Camera Settings', 'picQuality'))
print(" ")

print("------------------------")
print("AWS Collection ID")
print("________________________")
new_collectionid=raw_input("[Collection ID used: %s] New Collection ID: " % collectionid)
if new_collectionid == '':
        new_collectionid=collectionid

config.set('App Settings', 'collectionid', new_collectionid)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - Collection ID Used: %s" % config.get('App Settings', 'collectionid'))
print(" ")

print("----------------------------------------")
print("THIS IS YOUR UPDATED SETTINGS")
print("-run: python config.py to change settings")
print("________________________________________")

for section_name in config.sections():
	print("Section:", section_name)
	for name, value in config.items(section_name):
		print("    {} = {}".format(name,value))
	print(" ")
	
print("------------------------------------------------------")	
print("To change IFTTT settings, run: python ifttt-config.py")
print("______________________________________________________")

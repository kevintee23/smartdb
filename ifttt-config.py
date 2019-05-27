from ConfigParser import ConfigParser

config = ConfigParser()

config.read('config1.ini')

ifturl = config.get('App Settings', 'ifturl')
iftEvent = config.get('App Settings', 'iftEvent')
 
print (" ")
print("Leave blank (by hitting ENTER) if you do not intend to change any of the values") 
print("-------------------------------------------------------------------------------")
print(" ")

print("---------------")
print("IFTTT Maker URL")
print("_______________")
new_ifturl=raw_input("Enter/paste IFTTT Maker URL: ")
if new_ifturl == '':
        new_ifturl=ifturl

config.set('App Settings', 'ifturl', new_ifturl)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - IFT Maker URL: %s" % config.get('App Settings', 'ifturl'))
print(" ")

print("----------------")
print("IFTTT Event Name")
print("________________")
new_iftEvent=raw_input("[Event Name: %s] New Event Name: " % iftEvent)
if new_iftEvent == '':
        new_iftEvent=iftEvent

config.set('App Settings', 'iftEvent', new_iftEvent)

with open('config1.ini', 'w') as configfile:
        config.write(configfile)
        print("Saved - IFTTT Event Name: %s" % config.get('App Settings', 'ifturl'))
print(" ")

print("----------------------------------------------")
print("THIS IS YOUR UPDATED SETTINGS")
print("-run python ifttt-config.py to change settings")
print("______________________________________________")

for section_name in config.sections():
	print("Section:", section_name)
	for name, value in config.items(section_name):
		print("    {} = {}".format(name,value))
	print(" ")

print("------------------------------------------------")	
print("To change other settings, run - python config.py")
print("________________________________________________")

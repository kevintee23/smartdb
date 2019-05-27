from ConfigParser import ConfigParser

config = ConfigParser()

config.read('config1.ini')

ifturl = config.get('App Settings', 'ifturl')
iftEvent = config.get('App Settings', 'iftEvent')

print("Leave blank (by hitting ENTER) if you do not intend to change any of the values") 

#IFTTT URL
try:
        new_ifturl=input("Enter/paste your IFTTT Maker URL: ")
except SyntaxError:
        new_ifturl=config.get('App Settings', 'ifturl')

config.set('App Settings', 'ifturl', new_ifturl)

#IFTTT Event Name
try:
        new_iftEvent=input("[IFTTT Event Name: %s] Event Name: " % iftEvent)
except SyntaxError:
        new_iftEvent=config.get('App Settings', 'iftEvent')

config.set('App Settings', 'iftEvent', new_iftEvent)

with open('config1.ini', 'w') as configfile:
	config.write(configfile)

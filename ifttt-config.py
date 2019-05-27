from ConfigParser import ConfigParser

config = ConfigParser()

config.read('config1.ini')

ifturl = config.get('App Settings', 'ifturl')
iftEvent = config.get('App Settings', 'iftEvent')

print("Leave blank (by hitting ENTER) if you do not intend to change any of the values") 

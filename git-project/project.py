import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "ekieae"
deviceType = "samsung"
deviceId = "233078"
authMethod = "token"
authToken = "90163638"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

    
while True:
        pul=random.randrange(55,90)
        #print(pul)
        temp = random.randrange(70,105)    #temp in fahrenheit
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Pulse': pul }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Pulse = %s %%" % pul, "to IBM Watson")
        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if (temp>99 or pul>72):
                r=requests.get("https://www.fast2sms.com/dev/bulk?authorization=SO1CpF52fevPGtRyiwlHXhZ9g7Md4AxTLQKE0rDNJns38qcYW6SQMOGgvipXFm1k0qjolfCyYbLeHuK7&sender_id=FSTSMS&message=Danger&language=english&route=p&numbers=7989233078")
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()

from __future__ import print_function
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt

### Set endpoint, Url, Username, password, clientid, CA File, topic, and port

# mosquitto_endpoint = "mosquitto.thesuavedeveloper.win" 
# url = "https://{}".format(mosquitto_endpoint)
username = "thesuavedeveloper" 
password = "secret_password"
clientId = "thesuavedeveloper"
# cafile="cert.pem"
topic="thesuavedeveloper/test"
# port=8883

### Parameters added/altered for AWS IoT Enhanced Auth
aws_iot_endpoint = "a27icbrpsue2fo-ats.iot.ap-south-1.amazonaws.com"
url = "https://{}".format(aws_iot_endpoint)
alpn_protocol_name_cust_auth = "mqtt" ##
custom_auth_name = "CustomAuth_up" ##
useridParams= "{}?x-amz-customauthorizer-name={}".format(username,custom_auth_name)
cafile="AmazonRootCA1.cer"
port=443

## Set up Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

## Setup SSL ALPN Parameters
def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([alpn_protocol_name_cust_auth])
        ssl_context.load_verify_locations(cafile=cafile)
        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

## Establish Connection and Publish messages
if __name__ == '__main__':
    try:
        mqttc = mqtt.Client(clientId)
        mqttc.username_pw_set(username=useridParams,password=password) ##
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(aws_iot_endpoint, port=port)
        logger.info("connect success")
        mqttc.loop_start()

        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            logger.info("try to publish:{}".format(now))
            mqttc.publish(topic, now, qos=1)
            time.sleep(2)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

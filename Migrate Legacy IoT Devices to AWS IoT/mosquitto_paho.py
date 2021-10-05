from __future__ import print_function
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt

### Set endpoint, Url, Username, password, clientid, CA File, topic, and port

mosquitto_endpoint = "mosquitto.thesuavedeveloper.win" 
url = "https://{}".format(mosquitto_endpoint)
username = "thesuavedeveloper" 
password = "secret_password"
clientId = "thesuavedeveloper"
cafile="cert.pem"
topic="thesuavedeveloper/test"
port=8883

## Set up Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

## Setup SSL Parameters
def ssl_params():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(cafile=cafile)
        return  ssl_context
    except Exception as e:
        print("exception ssl_params()")
        raise e

## Establish Connection and Publish messages
if __name__ == '__main__':
    try:
        mqttc = mqtt.Client(clientId)
        mqttc.username_pw_set(username=username,password=password)
        ssl_context= ssl_params()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(mosquitto_endpoint, port=port)
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
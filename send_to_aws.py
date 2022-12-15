# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import warnings

warnings.filterwarnings("ignore")

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


import serial
import time

import numpy as np

z1baudrate = 9600
z1port = 'COM7'  # set the correct port before run it
arduino_data = 20.2

def send_data():
    # Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
    ENDPOINT = "an1x1nllhpz5q-ats.iot.us-west-1.amazonaws.com"
    CLIENT_ID = "data_from_arduino"
    PATH_TO_CERTIFICATE = "C:\\Users\\ADMIN\\PycharmProjects\\read_serial_data_send_to_aws\\d506557c8433a9a7ff8557324365922a317ab8ab5527d7f10ebcaa88808f0e3f-certificate.pem.crt"
    PATH_TO_PRIVATE_KEY = "C:\\Users\\ADMIN\\PycharmProjects\\read_serial_data_send_to_aws\\d506557c8433a9a7ff8557324365922a317ab8ab5527d7f10ebcaa88808f0e3f-private.pem.key"
    PATH_TO_AMAZON_ROOT_CA_1 = "C:\\Users\\ADMIN\\PycharmProjects\\read_serial_data_send_to_aws\\AmazonRootCA1.pem"
    TOPIC = "sdkTest/sub"

    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERTIFICATE,
                pri_key_filepath=PATH_TO_PRIVATE_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                client_id=CLIENT_ID,
                clean_session=False,
                keep_alive_secs=6
                )
    print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    # Publish message to server desired number of times.
    print('Begin Publish')
    data = arduino_data
    message = {"soilN": data[0], "soilP": data[1], "soilK": data[2], "soilPH": data[3]}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'sdkTest/sub'")
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2  # set read timeout
print(z1serial) # debug serial.
print(z1serial.is_open)  # True if open
if z1serial.is_open:
    while True:
        size = z1serial.inWaiting()
        if size:
            data = z1serial.read(size)
            data = np.array(data.decode().split())
            data = data.astype(np.float).tolist()
            arduino_data = data
            send_data()
            # break
        # else:
        #     print('no data')
        time.sleep(10)
else:
    print('z1serial not open')
z1serial.close()  # close z1serial if z1serial is open.
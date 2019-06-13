# Gjenge

Proof of Concept solution for transport companies to track psv vehicles  with means of IoT components and IOTA. 
Developed by Albert Carlos Omware during the UN Habitat Makerthon Challenge 2019, Nairobi, Kenya.

**WARNING** This is a demo project developed during the UN Habitat Makerthon Challenge, so it does not include some important security aspects, such as the authorization of the roles in the backend, the backend API authorization, and so on.

## Components

### gateway_listener
Node.js daemon running on the Gateway, reads information from MQTT that contains data from the Sensors, and writes the data to IOTA using the MAM protocol. Seed and side key to write the data is fetched from the backend via API for each transportation. A separate restricted channel is created, and transportation data is recorded at fixed intervals (GPS, temperature, gas).

### arduino
The modules that implement the functionality of reading data from Sensors.

### iota_backend_api
Node.js server provides an API for retrieving data from IOTA in JSON format for the backend

### backend
API based on django restframework that provides end-points of active transportation and their current location to 3rd-party solutions. 
The Django web application to implement a demo UI of the Dispatcher od transport company.

## Installation instruction

### gateway_listener
To run gateway_listener you need to install Node.js 8+, install js dependencies and create .env file with parameters.
```
npm install
```\
in the gateway_listener directory, then create .env file with these parameters:<br>

```bash
DEVICE_ID=fee312cf-c9eb-44be-94e8-0a93a6ac8a5f #your device id registered on the backend
BACKEND_URL=http://localhost:8000/api/transportation/control/
IOTA_PROVIDER=https://nodes.devnet.iota.org:443
IOTA_SEND_INTERVAL=15
MQTT_URL=mqtt://localhost
MQTT_USER=user
MQTT_PASSWORD=password
MQTT_PORT=1883
MQTT_SENSOR_TEMPERATURE=mqsens-out/5/2/1/0/0 # sensor id on device
MQTT_SENSOR_GPS=mqsens-out/6/0/1/0/49 # sensor id on device
MQTT_SENSOR_GAS=mqsens-out/5/3/1/0/37 # sensor id on device
```

### iota_backend_api
To run iota_backend_api you need to install Node.js 8+, install js dependencies and create .env file with parameters.
```
npm install
```
in the iota_backend_api directory, then create .env file with these parameters:<br>
```bash
IOTA_PROVIDER=https://nodes.devnet.iota.org:443
```

### backend
To run the backend, you need python 3.6+, PostgreSQL 9+ and install python dependencies, GOOGLE_MAP_API_KEY is used for the widget to select points on the map.
```bash
pip install -r requirements.txt
python manage.py migrate
GOOGLE_MAP_API_KEY=<your google api key> python manage.py runserver
```
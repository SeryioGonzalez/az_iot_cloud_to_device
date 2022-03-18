from azure.iot.hub import IoTHubRegistryManager

import azure.functions as func
import logging
import os

IOT_HUB_CONNECTION_STRING = os.environ.get("IOT_HUB_CONNECTION_STRING")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)
    except ValueError:
        pass
    else:
        device_name    = req_body.get('device_name')
        device_command = req_body.get('device_command')

        data = ''

        message_properties={}
        message_properties['contentType'] = "application/json"

        message_application_properties = {}
        message_application_properties['device_command'] = device_command
        
        message_properties.update(message_application_properties)
        
        registry_manager.send_c2d_message(device_name , data, properties=message_properties)

    if device_name:
        return func.HttpResponse(f"For device: {device_name}. Comand requested: {device_command}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

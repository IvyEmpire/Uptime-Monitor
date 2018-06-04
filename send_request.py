#!/usr/bin/python
from flask import Flask
import sqlite3

class Uptime:
    # GOLBAL VARIABLE
    ENDPOINT = 'http://35.196.174.157/api/v1'  # api endpoint for creating/update incident
    API_TOKEN = 'WaFDMXPvYUYMJCOv8OBi'  # api token for creating/update incident
    COMPONENT_STATUS_PARTIAL_OUTAGE = 3  # partial outage
    COMPONENT_STATUS_OPERATIONAL = 1  # operational
    INCIDENT_STATUS_INVESTIGATING = 1  # new incident status is investigating
    INCIDENT_STATUS_FIXED = 4  # updated incident status is fixed
    NOTIFY = 1  # notify user
    VISIBLE = 1  # visible to public

    # stuff that's set to be global variable for now, might change later
    incident_url = 'http://35.196.174.157/api/v1/incidents?component_id=3&sort=id&order=desc&per_page=1'  # incident url
    # url = 'https://empirelife-prod.auth0.com/testall'  # auth0 testall endpoint for getting status response


    def __init__(self, name, url, expected_status):
        self.url = url
        self.name = name + ' is down.' # name of incident
        self.new_incident_message = 'An new incident has been created for ' + name # message for new incident
        self.update_incident_message = 'The incident for ' + name + ' has been updated' # message for update incident
        self.component_url = 'http://35.196.174.157/api/v1/components?name='+ name # the component url for the passed in api, search based on name
        self.expected_status = expected_status  #the expected response from the input url
        self.FLAG  = False  # flag for if the service is down
        print('after initialization: ',self.url)
        print('after initialization: ', self.name)
        print('after initialization: ', self.expected_status)



    def monitor_uptime (self):
        print('monitor_uptime CALLED')
        print(self.url)
        print(type(self.url))
        response = Uptime.get_response(self,self.url)
        print('RESPONSE', response)

        # if the service is up and the flag is set to DOWN, update the most recent incident
        if response.status_code == self.expected_status:

            if self.FLAG == True:
                component_id = Uptime.get_obj_id(self,self.component_url)
                incident_id = Uptime.get_obj_id(self,'http://35.196.174.157/api/v1/incidents?component_id=' + str(
                    component_id) + '&sort=id&order=desc&per_page=1') #most recent incident
                Uptime.updateincident(self, incident_id, Uptime.INCIDENT_STATUS_FIXED, self.update_incident_message)

        # if the service is down and the flag is set to UP, create a new incident
        else:
            if self.FLAG == False:
                component_id = Uptime.get_obj_id(self,self.component_url)
                Uptime.createincident(self,self.name, self.new_incident_message,
                               Uptime.INCIDENT_STATUS_INVESTIGATING, Uptime.NOTIFY,
                               Uptime.VISIBLE, component_id, Uptime.COMPONENT_STATUS_PARTIAL_OUTAGE)


    def get_obj_id(self, obj_url):
        import requests
        import json
        print(obj_url)
        obj = requests.request("GET", obj_url)
        print('obejct contains: ', obj)
        print('the tpye of the object is', type(obj))

        new_json = json.loads(obj.text)
        obj_id = new_json['data'][0]['id']

        print('the component id is: ', obj_id)

        return obj_id

    # returns the response from a given url
    def get_response(self, url):
        import requests

        response = requests.request("GET", url)

        print(response.text, response.status_code)
        print(type(response))

        return response

    # creates a new incident based on given parameters
    def createincident(self, name, message, status, notify, visible, component_id, component_status):
        import cachetclient.cachet as cachet
        import json
        incidents = cachet.Incidents(endpoint=Uptime.ENDPOINT, api_token=Uptime.API_TOKEN)
        temp_incident = json.loads(incidents.post(name=name,
                                                  message=message,
                                                  status=status,
                                                  visible=visible,
                                                  component_id=component_id,
                                                  component_status=component_status,
                                                  notify=notify
                                                  ))
        print('incident created')
        self.FLAG= True  # update flag

    def updateincident(self,id, status, message):
        import cachetclient.cachet as cachet

        incidents = cachet.Incidents(endpoint=Uptime.ENDPOINT, api_token=Uptime.API_TOKEN)
        new_incident = incidents.put(id=id,
                                     status=status,
                                     message=message)

        print('incident updated')

        self.FLAG = False  # update flag
        print('The flag is set to:',self.FLAG)
        component_id = Uptime.get_obj_id(self, self.component_url)
        # update
        Uptime.updatecomponent(component_id, Uptime.COMPONENT_STATUS_OPERATIONAL)

    def updatecomponent(component_id, component_status):
        import cachetclient.cachet as cachet

        component = cachet.Components(endpoint=Uptime.ENDPOINT, api_token=Uptime.API_TOKEN)
        new_component = component.put(id=component_id,
                                      status=component_status,
                                      )
        print('component status updated')







#uptime_for_auth0 = Uptime ('auth0', 'https://empirelife-prod.auth0.com/testall',200)
#uptime_for_auth0.monitor_uptime()







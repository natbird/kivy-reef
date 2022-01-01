import requests
from kivy.app import App

class AuthenticationException(Exception):
    pass

class ApiConnection():
    """ Creates an API connection to a given reef-pi server """
    auth_url = '/auth/signin' # Path for authentication
    api_url = '/api' # Root path to api
    temperature_url = "/tcs" # Sub=path for temperature queries
    equipment_url = "/equipment" # Sub=path for equipment queries
    phprobe_url = '/phprobes' # Sub=path for pH probe queries
    ato_url = '/atos' # Sub=path for ATO queries
    inlet_url = '/inlets' # Sub=path for inlet queries
    macro_url = '/macros' # Sub=path for macro queries
    doser_url = '/doser/pumps' # Sub=path for doser queries

    def __init__(self, host, user_name, password, timeout):
        self.___host = host
        self.___api_url = self.___host + self.api_url
        self.___user_name = user_name
        self.___password = password
        self.___timeout = timeout
        
        # Create and authenticate a session
        self.___session = requests.Session()
    
    def ___api_get(self, url):
        """ Internal method for GET request """
        try:
            r = self.___session.get(url, timeout=self.___timeout)
            r.raise_for_status()
        except requests.Timeout:
            App.get_running_app().status = "Read error – Connection timed out"
            return False
        except requests.ConnectionError:
            App.get_running_app().status = "Read error – Connection error"
            return False
        except requests.HTTPError:
            return False
        else:
            response = r.json()
            return response
    
    def ___api_post(self, url, data=None):
        """ Internal method for POST request """        
        try:
            r = self.___session.post(url, data, timeout=self.___timeout)
            r.raise_for_status()
        except requests.ConnectionError:
            App.get_running_app().status = "Post error – Connection error"
            raise
        except requests.Timeout:
            App.get_running_app().status = "Post error – Connection timed out"
            raise
        except requests.HTTPError:
            raise
        else:
            return True
    
    def ___api_json_post(self, url, data=None):
        """ Internal method for JSON POST request """
        try:
            r = self.___session.post(url, json=data)
            r.raise_for_status()
        except requests.ConnectionError:
            App.get_running_app().status = "Post error – Connection error"
            raise
        except requests.Timeout:
            App.get_running_app().status = "Post error – Connection timed out"
            raise
        except requests.HTTPError:
            raise
        else:
            return True

    def ___getUrl(self, category):
        """ Returns the correct api url for the given category """
        url = ''

        if category == 'system':
            url = self.___api_url
        if category == 'temperature':
            url = self.___api_url + ApiConnection.temperature_url
        elif category == 'equipment':
            url = self.___api_url + ApiConnection.equipment_url
        elif category == 'ph' or category == 'flowmeter':
            url = self.___api_url + ApiConnection.phprobe_url
        elif category == 'ato':
            url = self.___api_url + ApiConnection.ato_url
        elif category == 'inlet':
            url = self.___api_url + ApiConnection.inlet_url
        elif category == 'macro':
            url = self.___api_url + ApiConnection.macro_url
        elif category == 'doser':
            url = self.___api_url + ApiConnection.doser_url
        
        if url:
            return url
        else:
            print("Error: No such category exists.")
            return False
    
    def authenticate(self):
        """ Obtain an authentication cookie from the reef-pi server for the session """
        login_details = f'{{"user":"{self.___user_name}", "password":"{self.___password}"}}' # This must be passed as a string, not a dictionary.
        url = self.___host + ApiConnection.auth_url

        try:
            self.___api_post(url, data=login_details)
        except requests.ConnectionError:
            App.get_running_app().status = "Connection failed – check host address"
            return False
        except requests.Timeout:
            return False
        except requests.HTTPError:
            App.get_running_app().status = "Authentication failed – check user/password"
            return False
        else:
            return True
    
    def list_query(self, category):
        """ Returns a list of all items of a given cateogry (equipment, timers etc.) """
        url = self.___getUrl(category)
        
        if url:
            r = self.___api_get(url)
            list = []
            
            if r:
                for item in r:
                    if category == 'temperature':
                        list.append({'id':item.get('id'),'name':item.get('name'), 'fahrenheit':item.get('fahrenheit')})
                    elif category == 'equipment':
                        list.append({'id':item.get('id'),'name':item.get('name'), 'state':item.get('on')})
                    elif category == 'ato':
                        list.append({'id':item.get('id'),'name':item.get('name'), 'enabled':item.get('enable'), 'period':item.get('period')})
                    elif category == 'macro':
                        list.append({'id':item.get('id'),'name':item.get('name'), 'reversible':item.get('reversible')})
                    else:
                        list.append({'id':item.get('id'),'name':item.get('name')})
                return list
    
    def read_query(self, category, id):
        """ Returns the value of a given sensor """
        url = self.___getUrl(category)
        if url:
            r = self.___api_get(f'{url}/{id}/read')
            
            if r:
                return r

    def current_read_query(self, category, id):
        """ Returns the current reading of a temperature sensor """
        url = self.___getUrl(category)
        if url:
            r = self.___api_get(f'{url}/{id}/current_reading')
            
            if r:
                return r

    def readings_query(self, category, id):
        """ Returns a list of current and historical readings """
        url = self.___getUrl(category)
        if url:
            r = self.___api_get(f'{url}/{id}/readings')
            
            if r:
                return r
    
    def state_query(self, category, id):        
        """ Return the current state of an entity """
        url = self.___getUrl(category)

        if url:    
            r = self.___api_get(f'{url}/{id}')
            if category == 'equipment':
                state = r.get('on')
                if state:
                    return state
            elif category == 'ato':
                state = r.get('enable')
                if state:
                    return state
            else:
                print(f"Invalid query: {category} does not support state query.")
                return False
    
    def usage_query(self, category, id):
        """ Returns the usage of a given entity """
        url = self.___getUrl(category)
        if url:
            r = self.___api_get(f'{url}/{id}/usage')
            
            if r:
                return r
    
    def system_query(self):
        """ Get information about the reef-pi server """
        url = self.___getUrl('system')
        if url:
            r = self.___api_get(f'{url}/info')
            
            if r:
                return r
    
    def api_post(self, category, command, id=None, post_data=None):
        """ Make a control post request """

        if category == 'system':
            base_url = self.___getUrl(category) + '/admin'

            if command == 'reload':
                url = base_url + '/reload'
            if command == 'restart':
                url = base_url + '/restart'
            if command == 'poweroff':
                url = base_url + '/poweroff'
        
        if category == 'equipment' and command == 'control':
            base_url = self.___getUrl(category) + f'/{id}'
            url = base_url + '/control'
            
            if post_data == True:
                post_data = '{"on":true}'
            elif post_data == False:
                post_data = '{"on":false}'
        
        elif category == 'macro':
            base_url = self.___getUrl(category) + f'/{id}'
            if command == 'run':
                url = base_url + '/run'
            elif command == 'revert':
                url = base_url + '/revert'
        
        if url:    
            try:
                self.___api_post(url, post_data)
            except requests.HTTPError:
                raise
            else:
                return True
    
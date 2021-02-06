import json


with open("config.json") as config_file:
    config_data = json.load(config_file)
    
    
# mail configuration
app_settings = config_data['application']

# database configuration
db_settings = config_data['database']

import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient
import sys
# you might need to change these, but i doubt it
authority_url = 'https://login.microsoftonline.com/common/oauth2/authorize'
resource_url = 'https://analysis.windows.net/powerbi/api'
api_url = 'https://api.powerbi.com'

# change these to your credentials
client_id = 'c4d96e09-6f23-48db-8d9f-71a0d28010c9'
username = 'vijay.kumar@loginworks.com'
password = 'vijaykumar#10'

# first you need to authenticate using adal
context = adal.AuthenticationContext(authority=authority_url,
                                     validate_authority=True,
                                     api_version=None)
print(context)
sys.exit()
# get your authentication token
token = context.acquire_token_with_username_password(resource=resource_url,
                                                     client_id=client_id,
                                                     username=username,
                                                     password=password)

# create your powerbi api client
client = PowerBIClient(api_url, token)
print(token)
sys.exit()
# create your columns
columns = []
columns.append(Column(name='id', data_type='Int64'))
columns.append(Column(name='name', data_type='string'))
columns.append(Column(name='is_interesting', data_type='boolean'))
columns.append(Column(name='cost_usd', data_type='double'))
columns.append(Column(name='purchase_date', data_type='datetime'))

# create your tables
tables = []
tables.append(Table(name='AnExampleTableName', columns=columns))

# create your dataset
dataset = Dataset(name='AnExampleDatasetName', tables=tables)

# post your dataset!
client.datasets.post_dataset(dataset)
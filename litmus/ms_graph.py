import requests
import uuid
import json
from django.conf import settings

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

# SharePoint ID and secret from setting.py
sp_group_id = getattr(settings, 'MCSCIENCE_SHAREPOINT_GROUP_ID')
sp_teamsite_id = getattr(settings, 'MCSCIENCE_SHAREPOINT_ETUDE_TEAMSITE_ID')
sp_drive_id  = getattr(settings, 'MCSCIENCE_SHAREPOINT_ETUDE_EXCEL_DRIVE_ID')
sp_list_id  = getattr(settings, 'MCSCIENCE_SHAREPOINT_ETUDE_EXCEL_LIST_ID')

# Generic API Sending
def make_api_call(method, url, token, payload = None, parameters = None):
  # Send these headers with all API calls
  headers = { 'User-Agent' : 'Chopin/Prelude',
              'Authorization' : 'Bearer {0}'.format(token),
              'Accept' : 'application/json' }

  # Use these headers to instrument calls. Makes it easier
  # to correlate requests and responses in case of problems
  # and is a recommended best practice.
  request_id = str(uuid.uuid4())
  instrumentation = { 'client-request-id' : request_id,
                      'return-client-request-id' : 'true' }

  headers.update(instrumentation)

  response = None

  if (method.upper() == 'GET'):
      response = requests.get(url, headers = headers, params = parameters)
  elif (method.upper() == 'DELETE'):
      response = requests.delete(url, headers = headers, params = parameters)
  elif (method.upper() == 'PATCH'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
  elif (method.upper() == 'POST'):
      headers.update({ 'Content-Type' : 'application/json' })
      response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

  return response

def get_me(access_token):
  get_me_url = graph_endpoint.format('/me')

  # Use OData query parameters to control the results
  #  - Only return the displayName and mail fields
  query_parameters = {'$select': 'displayName,jobTitle, mail'}

  r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_my_messages(access_token):
  get_messages_url = graph_endpoint.format('/me/mailfolders/inbox/messages')

  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the ReceivedDateTime, Subject, and From fields
  #  - Sort the results by the ReceivedDateTime field in descending order
  query_parameters = {'$top': '10',
                      '$select': 'receivedDateTime,subject,from',
                      '$orderby': 'receivedDateTime DESC'}

  r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_users(access_token):
  get_users_url = graph_endpoint.format('/users')

  # Use OData query parameters to control the results
  #  - Retrieves the total count of matching resources
  #  - Only return the displayName, jobTitle, mail, mobilePhone, id fields
  #  - Sort the results by the DisplayName field in descending order
  query_parameters = {'$select': 'displayName,jobTitle,mail,mobilePhone,id',
                      '$orderby': 'displayName asc'}

  r = make_api_call('GET', get_users_url, access_token, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_sp_list(access_token):
  # SharePoint List url
  sp_url = "{0}{1}{2}{3}{4}{5}{6}".format('/groups/', sp_group_id, '/sites/', sp_teamsite_id, '/drives/', sp_drive_id, '/root/children?')
  get_sp_list_url = graph_endpoint.format(sp_url)

  # Use OData query parameters to control the results
  #  - Retrieves the total count of matching resources
  #  - Only return the displayName, jobTitle, mail, mobilePhone, id fields
  #  - Sort the results by the DisplayName field in descending order
  query_parameters = {'$select': 'id,name,createdBy,createdDateTime,lastModifiedBy,lastModifiedDateTime',
                      '$orderby': 'name asc'}

  r = make_api_call('GET', get_sp_list_url, access_token, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)
  
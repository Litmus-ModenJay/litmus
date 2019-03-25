import requests
import uuid
import json

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

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
  # SharePoint List
  get_sp_list_url = graph_endpoint.format('/groups/ce2b52cd-1c1b-4cfd-8fa3-96bc8e6b3b85/sites/mcscience.sharepoint.com,8e26e1d0-373b-40ac-b6bd-b4523483479c,4c63f1f8-9721-403e-a449-63af9610adae/drives/b!0OEmjjs3rEC2vbRSNINHnPjxY0whlz5ApEljr5YQra7jjbA7jDc4SJoPAxz1OeAv/root/children?')
 

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
  
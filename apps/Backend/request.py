import requests

### User ###
url_get = 'http://127.0.0.1:5000/api/users/6'
url_edit = 'http://127.0.0.1:5000/api/users/21'
url_delete = 'http://127.0.0.1:5000/api/users/20'
### Users ###
url_get_all = 'http://127.0.0.1:5000/api/users'
url_add = 'http://127.0.0.1:5000/api/users'
url_delete_all = 'http://127.0.0.1:5000/api/users'

payload = {
    'name': 'Danny',
    'lastname': 'Red'
}
headers = {
    'Content-Type': 'application/json'
}
### USER ###
# response = requests.get(url_get) #get user
# response = requests.post(url_edit, json=payload, headers=headers) #edit user
# response = requests.delete(url_delete) #delete user
### USERS ###
# response = requests.get(url_get_all) #get users
# response = requests.post(url_add, json=payload, headers=headers) #Add user
response = requests.delete(url_delete_all) #delete all users


print(response.status_code)
print(response.json())
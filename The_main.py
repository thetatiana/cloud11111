import requests
#import EVS
#import Auto_scale
#import ECS
#import VPC

ENDPOINT_IAM = "iam.ru-moscow-1.hc.sbercloud.ru"


def auth(domain_name_auth, name_auth, password_auth):
    auth_api = requests.post('https://{endpoint}/v3/auth/tokens'.format(endpoint=ENDPOINT_IAM),
                             json={
                                 "auth": {
                                     "identity": {
                                         "methods": [
                                             "password"
                                         ],
                                         "password": {
                                             "user": {
                                                 "name": name_auth,  # запрашивается у пользователя
                                                 "password": password_auth,  # запрашивается у пользователя
                                                 "domain": {
                                                     "name": domain_name_auth  # запрашивается у пользователя
                                                 }
                                             }
                                         }
                                     },
                                     "scope": {
                                         "project": {
                                             "name": "ru-moscow-1"
                                         }
                                     }
                                 }
                             })
    return auth_api


def project_id_api(token):
    project_id_api = requests.get('https://{endpoint}/v3/projects'.format(endpoint=ENDPOINT_IAM),
                                  headers={'X-Auth-Token': token})
    return project_id_api


def projects_id(TOKEN):
    projects_id = []
    if project_id_api(TOKEN).status_code == 200:
        for i in range(1, len(project_id_api(TOKEN).json()['projects'])):
            projects_id.append(project_id_api(TOKEN).json()['projects'][i]['id'])
    return projects_id


print("IAM Reg")
username = "tttttttttt"  # username = input("Username: ")
password = "saMsuNg2485"  # password = input("Password: ")
domain_name = "ADV-f6d010f5faee4afd8caf"  # domain_name = input("Domain name: ")
auth_end = auth(domain_name, username, password)
print(auth_end.status_code == 201)

if auth_end.status_code == 201:
    TOKEN = auth_end.headers['X-Subject-Token']

current_project = projects_id(TOKEN)[0]  # запрос у пользователя проекта из списка projects_id

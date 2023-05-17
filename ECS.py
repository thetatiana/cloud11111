import requests


def ecs_get_az(current_project, token):
    AZ = requests.get('https://ecs.ru-moscow-1.hc.sbercloud.ru/v2.1/{project_id}/os-availability-zone'.format(project_id=current_project),
                      headers={"X-Auth-Token": token})
    return AZ


def ecs_servers_list(current_project, token):
    servers_list = requests.get("https://ecs.ru-moscow-1.hc.sbercloud.ru/v2.1/{project_id}/servers".format(project_id=current_project),
                                headers={"X-Auth-Token": token})
    return servers_list


def ecs_servers_api(current_project, token):
    ecs_servers_api = requests.get("https://ecs.ru-moscow-1.hc.sbercloud.ru/v2.1/{project_id}/servers".format(project_id=current_project),
                                   headers={"X-Auth-Token": token})
    return ecs_servers_api


def ecs_servers_id(current_project, token):
    servers_id = []
    if ecs_servers_api(current_project, token).status_code == 200:
        for i in range(0, len(ecs_servers_api(current_project, token).json()['servers'])):
            servers_id.append(ecs_servers_api(current_project, token).json()['projects'][i]['id'])
    return servers_id

def ecs_servers_id_by_name(current_project, token, name):
    servers_id = ''
    for i in range(len(ecs_servers_api(current_project, token).json()['servers'])):
        if name == ecs_servers_api(current_project, token).json()['servers'][i]['name']:
            servers_id = ecs_servers_api(current_project, token).json()['projects'][i]['id']
    return servers_id


def ecs_servers_detail(current_project, current_server_id, token):
    ecs_servers_detail = requests.get(
        "https://ecs.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/cloudservers/{server_id}".format(project_id=current_project, server_id=current_server_id),
        headers={"X-Auth-Token": token})

    return ecs_servers_detail.json()


def ecs_create_server(project_id, current_az, server_name):
    create = requests.post(
        "https://ecs.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/cloudservers".format(project_id=project_id),
        json={

            "server": {
                "availability_zone": current_az,
                "name": server_name,
                "imageRef": "1189efbf-d48b-46ad-a823-94b942e2a000",
                "root_volume": {
                    "volumetype": "SSD"
                },
                "data_volumes": [
                    {
                        "volumetype": "SSD",
                        "size": 100,
                        "multiattach": True,
                        "hw:passthrough": True
                    }
                ],
                "flavorRef": "s3.xlarge.2",
                "vpcid": "0dae26c9-9a70-4392-93f3-87d53115d171",
                "security_groups": [
                    {
                        "id": "507ca48f-814c-4293-8706-300564d54620"
                    }
                ],
                "nics": [
                    {
                        "subnet_id": "157ee789-03ea-45b1-a698-76c92660dd83"
                    }
                ],
                "publicip": {
                    "eip": {
                        "iptype": "5_bgp",
                        "bandwidth": {
                            "size": 10,
                            "sharetype": "PER"
                        }
                    }
                },
                "key_name": "sshkey-123",
                "count": 1,
                "server_tags": [
                    {
                        "key": "key1",
                        "value": "value1"
                    }
                ],
                "metadata": {
                    "op_svc_userid": "8ea65f4099ba412883e2a0da72b96873",
                    "agency_name": "test"
                }
            }
        })


def ecs_delete_server(current_project, current_server_id):
    requests.post("https://ecs.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/cloudservers/delete".format(project_id=current_project),
                  json=
                  {
                      "servers": [
                          {
                              "id": current_server_id
                          }
                      ],
                      "delete_publicip": False,
                      "delete_volume": False
                  })

import requests
import The_main

def vpc_api(current_project, TOKEN):
    vpc_api = requests.get(
        'https://vpc.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/vpcs'.format(project_id=current_project),
        headers={'X-Auth-Token': TOKEN})
    return vpc_api.json()


def vpc_id(current_project):
    vpc = []
    for i in range(len(vpc_api(current_project)['vpcs'])):
        vpc.append(vpc_api(current_project)['vpcs'][0]['id'])
    return vpc


def subnet_api(current_project, TOKEN):
    subnet_api = requests.get(
        'https://vpc.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/subnets'.format(project_id=current_project),
        headers={'X-Auth-Token': TOKEN})
    return subnet_api.json()


def subnet_id(current_project):
    subnet = []
    for i in range(len(subnet_api(current_project)['subnets'])):
        subnet.append(subnet_api(current_project)['subnets'][0]['id'])
    return subnet


def as_config_api(current_project, TOKEN):
    as_config_api = requests.get(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{current_project}/scaling_configuration'.format(
            current_project=current_project),
        headers={'X-Auth-Token': TOKEN})
    return as_config_api.json()


def as_config_id(current_project):
    as_config_id = []
    for i in range(as_config_api(current_project)["total_number"]):
        as_config_id.append(as_config_api(current_project)['scaling_configurations'][0]['scaling_configuration_id'])
    return as_config_id


def create_as_group(current_project, TOKEN):
    name = "GroupNameTest1"
    current_scaling_conf = as_config_id()[0]
    desire_instance_number = 0
    min_instance_number = 0
    max_instance_number = 10
    cool_down_time = 300  # min 0, max 86400, default 300
    health_periodic_audit_method_list = ['NOVA_AUDIT', 'ELB_AUDIT']
    health_periodic_audit_method = health_periodic_audit_method_list[0]
    current_vpc = vpc_id(current_project)[0]
    current_subnet = subnet_id(current_project)[0]
    health_periodic_audit_time_list = [0, 1, 5, 15, 60, 180]
    health_periodic_audit_time = health_periodic_audit_time_list[2]  # default 5
    instance_terminate_policy_list = ['OLD_CONFIG_OLD_INSTANCE', 'OLD_CONFIG_NEW_INSTANCE', 'OLD_INSTANCE',
                                      'NEW_INSTANCE']
    instance_terminate_policy = instance_terminate_policy_list[3]  # default OLD_CONFIG_OLD_INSTANCE
    delete_publicip_list = ['true', 'false']
    delete_publicip = delete_publicip_list[1]
    delete_volume_list = ['true', 'false']
    delete_volume = delete_volume_list[1]
    description = "description"
    create_scaling_group_api = requests.post(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{project_id}/scaling_group'.format(
            project_id=current_project),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN},
        json={
            "scaling_group_name": "{name}".format(name=name),
            "scaling_configuration_id": "{current_scaling_conf}".format(current_scaling_conf=current_scaling_conf),
            "desire_instance_number": desire_instance_number,
            "min_instance_number": min_instance_number,
            "max_instance_number": max_instance_number,
            "cool_down_time": cool_down_time,
            "health_periodic_audit_method": "{health_periodic_audit_method}".format(
                health_periodic_audit_method=health_periodic_audit_method),
            "health_periodic_audit_time": "{health_periodic_audit_time}".format(
                health_periodic_audit_time=health_periodic_audit_time),
            "delete_publicip": "{delete_publicip}".format(delete_publicip=delete_publicip),
            "instance_terminate_policy": "{instance_terminate_policy}".format(
                instance_terminate_policy=instance_terminate_policy),
            "delete_volume": "{delete_volume}".format(delete_volume=delete_volume),
            "description": "{description}".format(description=description),
            "vpc_id": "{current_vpc}".format(current_vpc=current_vpc),
            "networks": [
                {
                    "id": "{current_subnet}".format(current_subnet=current_subnet)
                }
            ],
            "multi_az_priority_policy": "PICK_FIRST"
        })
    return create_scaling_group_api


def querying_as_groups(current_project, TOKEN):
    querying_as_groups_api = requests.get(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{current_project}/scaling_group'.format(
            current_project=current_project),
        headers={'X-Auth-Token': TOKEN})
    return querying_as_groups_api.json()


def as_id(current_project):
    as_id = []
    for i in range(querying_as_groups(current_project)["total_number"]):
        as_id.append(querying_as_groups(current_project)["scaling_groups"][i]["scaling_group_id"])
    return as_id

def as_id_by_name(current_project, name, TOKEN):
    as_id = ''
    for i in range(querying_as_groups(current_project, TOKEN)["total_number"]):
        if querying_as_groups(current_project, TOKEN)["scaling_groups"][i]["scaling_group_name"] == name:
            as_id = querying_as_groups(current_project, TOKEN)["scaling_groups"][i]["scaling_group_id"]
            break
    return as_id



def querying_specified_as_groups(current_project, current_as_id, TOKEN):
    querying_as_groups_api = requests.get(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{current_project}/scaling_group/{as_id}'.format(
            current_project=current_project, as_id=current_as_id),
        headers={'X-Auth-Token': TOKEN})
    return querying_as_groups_api.json()


def modify_as_groups(current_project, current_as_id, TOKEN):
    name = "GroupNameTest1"
    current_scaling_conf = as_config_id()[0]
    desire_instance_number = 0
    min_instance_number = 0
    max_instance_number = 10
    cool_down_time = 300  # min 0, max 86400, default 300
    health_periodic_audit_method_list = ['NOVA_AUDIT', 'ELB_AUDIT']
    health_periodic_audit_method = health_periodic_audit_method_list[0]
    health_periodic_audit_time_list = [0, 1, 5, 15, 60, 180]
    health_periodic_audit_time = health_periodic_audit_time_list[2]  # default 5
    instance_terminate_policy_list = ['OLD_CONFIG_OLD_INSTANCE', 'OLD_CONFIG_NEW_INSTANCE', 'OLD_INSTANCE',
                                      'NEW_INSTANCE']
    instance_terminate_policy = instance_terminate_policy_list[3]  # default OLD_CONFIG_OLD_INSTANCE
    delete_publicip_list = ['true', 'false']
    delete_publicip = delete_publicip_list[1]
    delete_volume_list = ['true', 'false']
    delete_volume = delete_volume_list[1]
    description = "description"
    querying_as_groups_api = requests.put(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{current_project}/scaling_group/{as_id}'.format(
            current_project=current_project, as_id=current_as_id),
        headers={'X-Auth-Token': TOKEN},
        json={
            "scaling_group_name": "{name}".format(name=name),
            "scaling_configuration_id": "{current_scaling_conf}".format(current_scaling_conf=current_scaling_conf),
            "desire_instance_number": desire_instance_number,
            "min_instance_number": min_instance_number,
            "max_instance_number": max_instance_number,
            "cool_down_time": cool_down_time,
            "health_periodic_audit_method": "{health_periodic_audit_method}".format(
                health_periodic_audit_method=health_periodic_audit_method),
            "health_periodic_audit_time": "{health_periodic_audit_time}".format(
                health_periodic_audit_time=health_periodic_audit_time),
            "delete_publicip": "{delete_publicip}".format(delete_publicip=delete_publicip),
            "instance_terminate_policy": "{instance_terminate_policy}".format(
                instance_terminate_policy=instance_terminate_policy),
            "delete_volume": "{delete_volume}".format(delete_volume=delete_volume),
            "description": "{description}".format(description=description),
        })
    return querying_as_groups_api.json()


def delete_as_group(current_project, current_as_id, TOKEN):
    delete_as_group_api = requests.delete(
        'https://as.ru-moscow-1.hc.sbercloud.ru/autoscaling-api/v1/{current_project}/scaling_group/{as_id}'.format(
            current_project=current_project, as_id=current_as_id),
        headers={'X-Auth-Token': TOKEN})
    return delete_as_group_api.json()

import requests
from The_main import *

TOKEN = token()

name = "ft"
size = 30
az = "ru-moscow-1b"
count = 1
description = "new evs az2"
volumeType = "SSD"


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


def vpc_subnet_id(current_project):
    subnet = []
    for i in range(len(subnet_api(current_project)['subnets'])):
        subnet.append(subnet_api(current_project)['subnets'][0]['id'])
    return subnet


# print(vpc_subnet_id(current_project))


def create_cluster(current_project, TOKEN):
    name = 'mycluster'  # запрос названия кластера (Enter 4 to 128 characters starting
    # with a letter and not ending with a hyphen (-).
    # Only lowercase letters, digits, and hyphens (-) are allowed)
    annotations = {
        "foo2": "bar2"}  # необязательно, запрос дополнительных установок в кластер в виде ключ-значение, необязательный параметр
    type_of_cluster = ['VirtualMachine', 'ARM64']
    current_type_of_cluster = type_of_cluster[0]  # запрос у пользователя параметра type из списка type_of_cluster
    flavors = ['cce.s1.small', 'cce.s1.medium', 'cce.s2.small', 'cce.s2.medium', 'cce.s2.large', 'cce.s2.xlarge']
    current_flavor = flavors[2]  # запрос у пользователя параметра flavor из списка flavors
    versions = ['v1.21', 'v1.23']
    current_version = versions[1]  # запрос у пользователя параметра version из списка versions
    description = 'description'  # необязательно, запрос у пользователя описания кластера
    current_vpc = vpc_id(current_project)[0]  # запрос у пользователя vpc из списка vpc_id
    current_subnet = vpc_subnet_id(current_project)[0]  # запрос у пользователя subnet из списка subnet_id
    networkModes = ['overlay_l2', 'vpc-router']
    current_network_mode = networkModes[0]  # запрос у пользователя параметра mode из списка modes
    authModes = ['rbac', 'authenticating_proxy']
    current_auth_mode = authModes[0]  # запрос у пользователя параметра mode из списка modes
    cidrs = ['10.0.0.0/12-19', '172.16.0.0/16-19', '192.168.0.0/16-19']
    current_cidr = cidrs[0]  # запрос у пользователя параметра cidr из списка cidrs
    kubeProxyModes = ['iptables', 'ipvs']
    current_kubeProxyModes = kubeProxyModes[0]  # запрос у пользователя параметра kubeProxyMode из списка kubeProxyModes
    create_cluster_api = requests.post(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters'.format(
            project_id=current_project),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN},
        json={
            "kind": "Cluster",  # не запрашивается, без вариантов выбора
            "apiVersion": "v3",  # не запрашивается, без вариантов выбора
            "metadata": {
                "name": "{name}".format(name=name),
                "annotations": {
                    "{annotations}".format(annotations=annotations)
                }
            },
            "spec": {
                "flavor": "{flavors}".format(flavors=current_flavor),
                "version": "{current_version}".format(current_version=current_version),
                "description": "{description}".format(description=description),
                "hostNetwork": {
                    "vpc": "{vpc}".format(vpc=current_vpc),
                    "subnet": "{current_subnet}".format(current_subnet=current_subnet)
                },
                "containerNetwork": {
                    "mode": "{current_network_mode}".format(current_network_mode=current_network_mode)
                },
                "authentication": {
                    "mode": "{current_auth_mode}".format(current_auth_mode=current_auth_mode),
                    "cidrs":
                        {
                            "cidr": "{current_cidr}".format(current_cidr=current_cidr)
                        }

                },
                "kubeProxyMode": "{current_kubeProxyModes}".format(current_kubeProxyModes=current_kubeProxyModes),
                "extendParam": {
                    "clusterAZ": "multi_az"
                }
            }
        })
    return create_cluster_api.json()


def listing_clusters_of_project_api(current_project, TOKEN):
    listing_clusters_of_project_api = requests.get(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters'.format(
            project_id=current_project),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN})
    return listing_clusters_of_project_api.json()


def clusters_id(current_project):
    clusters_id = []
    for i in range(len(listing_clusters_of_project_api(current_project).json()['items'])):
        clusters_id.append(listing_clusters_of_project_api(current_project).json()['items'][i]['metadata']['uid'])
    return clusters_id


# current_cluster = clusters_id(current_project, TOKEN)[0]  # запрос у пользователя кластера из списка clusters_id


def reading_specified_cluster(current_project, current_cluster, TOKEN):
    reading_specified_cluster_api = requests.get(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters/{cluster_id}'.format(
            project_id=current_project, cluster_id=current_cluster),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN})
    return reading_specified_cluster_api.json()


new_description = "neww description"  # запрашивается у пользователя


def updating_cluster_description(current_project, current_cluster, TOKEN, new_description):
    updating_cluster_description_api = requests.put(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters/{cluster_id}'.format(
            project_id=current_project, cluster_id=current_cluster),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN},
        json={
            "spec": {
                "description": "{description}".format(description=new_description)
            }
        })
    return updating_cluster_description_api.json()


def delete_cluster(current_project, current_cluster, TOKEN):
    delete_cluster_api = requests.delete(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters/{cluster_id}'.format(
            project_id=current_project, cluster_id=current_cluster),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN})
    return delete_cluster_api.json()


duration = 30  # запрашивается у пользователя, min = 1, max = 1825


def cluster_certificate(current_project, current_cluster, duration, TOKEN):
    cluster_certificate_api = requests.put(
        'https://cce.ru-moscow-1.hc.sbercloud.ru/api/v3/projects/{project_id}/clusters/{cluster_id}/clustercert'.format(
            project_id=current_project, cluster_id=current_cluster),
        headers={'Content-Type': 'application/json', 'X-Auth-Token': TOKEN},
        json={
            "duration": duration
        })
    return cluster_certificate_api.json()


def ecс_id_by_name(current_project, name, TOKEN):
    as_id = ''
    for i in range(listing_clusters_of_project_api(current_project, TOKEN)["total_number"]):
        if listing_clusters_of_project_api(current_project, TOKEN)["scaling_groups"][i]["scaling_group_name"] == name:
            as_id = listing_clusters_of_project_api(current_project, TOKEN)["scaling_groups"][i]["scaling_group_id"]
            break
    return as_id

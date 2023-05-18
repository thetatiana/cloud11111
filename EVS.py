import requests
from The_main import *

TOKEN = token()

name = "ft"
size = 30
az = "ru-moscow-1b"
count = 1
description = "new evs az2"
volumeType = "SSD"

def createEVSDisk(current_project, TOKEN, name, size, az, count, description, volumeType):
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes'.format(project_id=current_project)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    json = {
        "volume": {
            # "backup_id": null,
            # "snapshot_id": null,   в целом важные параметры, но не уверен, что это всё будет прописано в итоге
            # "imageRef": null,
            "count": count,
            "description": "{description}".format(description = description),
            "availability_zone": "{az}".format(az = az),  # not requested from user
            "size": size,
            "name": "{name}".format(name = name),
            "volume_type": "{vt}".format(vt = volumeType)
        }
    }
    createDisk = requests.post(url, headers=header, json=json)
    return createDisk


def listing_volumes_of_project_api(current_project, TOKEN):  # подробная информация обо всех машинах
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes/detail'.format(project_id=current_project)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    listing_volumes_of_project_api = requests.get(url, headers=header)
    return listing_volumes_of_project_api


def volumes_id(current_project):
    volumes_id = []
    for i in range(len(listing_volumes_of_project_api(current_project).json()['volumes'])):
        volumes_id.append(listing_volumes_of_project_api(current_project).json()['volumes'][i]['id'])
    return volumes_id


def getvolumeIdByName(current_project, name, TOKEN):
    info = getDiskInformationByName(current_project, name, TOKEN)
    return info['id']


def deleteEVSDisk(current_project, name, TOKEN):
    current_volume = getvolumeIdByName(current_project, name, TOKEN)
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes/{volume_id}'.format(
        project_id=current_project, volume_id=current_volume)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    deleteDisk = requests.delete(url, headers=header)
    return deleteDisk


def getDiskInformationByName(current_project, name, TOKEN):
    allDisks = listing_volumes_of_project_api(current_project, TOKEN)
    diskNames = []
    for i in range(len(allDisks.json()['volumes'])):
        diskNames.append(allDisks.json()['volumes'][i]['name'])
    for i in range(len(diskNames)):
        if diskNames[i] == name:
            return allDisks.json()['volumes'][i]
    return "No disk with such name"

nameUp = "test-put"
descUp = "test"

def updateInfo(current_project, name, TOKEN, newName, newDescription):
    current_volume = getvolumeIdByName(current_project, name, TOKEN)
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes/{volume_id}'.format(
        project_id=current_project, volume_id=current_volume)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    json = {
        "volume": {
            "name": "{name}".format(name = newName),
            "description": "{desc}".format(desc = newDescription)  # запрашиваются
        }
    }
    updateDisk = requests.put(url, headers=header, json=json)
    return updateDisk

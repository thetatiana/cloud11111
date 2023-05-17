import requests
import The_main

def createEVSDisk(endpoint, current_project, TOKEN):
    url = 'https://{endpoint}/v2/{project_id}/volumes'.format(endpoint=endpoint, project_id=current_project)
    name = "ft"
    size = 30
    az = "ru-moscow-1b"
    count = 1
    description = "new evs az2"
    volumeType = "SSD"
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    json = {
        "volume": {
            # "backup_id": null,
            # "snapshot_id": null,   в целом важные параметры, но не уверен, что это всё будет прописано в итоге
            # "imageRef": null,
            "count": count,
            "description": "new evs az2",
            "availability_zone": "ru-moscow-1b",  # not requested from user
            "size": 12,
            "name": "ft",
            "volume_type": "SSD"
        }
    }
    createDisk = requests.post(url, headers=header, json=json)
    return createDisk


def listing_volumes_of_project_api(endpoint, current_project, TOKEN):  # подробная информация обо всех машинах
    url = 'https://{endpoint}/v2/{project_id}/volumes/detail'.format(endpoint=endpoint, project_id=current_project)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    listing_volumes_of_project_api = requests.get(url, headers=header)
    return listing_volumes_of_project_api


def volumes_id(current_project):
    volumes_id = []
    for i in range(len(listing_volumes_of_project_api(current_project).json()['volumes'])):
        volumes_id.append(listing_volumes_of_project_api(current_project).json()['volumes'][i]['id'])
    return volumes_id


def getvolumeIdByName(current_project, name):
    info = getDiskInformationByName(current_project, name)
    return info['id']


def deleteEVSDisk(current_project, name, TOKEN):
    current_volume = getvolumeIdByName(current_project, name)
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes/{volume_id}'.format(
        project_id=current_project, volume_id=current_volume)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    deleteDisk = requests.delete(url, headers=header)
    return deleteDisk


def getDiskInformationByName(current_project, name):
    allDisks = listing_volumes_of_project_api(current_project)
    diskNames = []
    for i in range(len(allDisks.json()['volumes'])):
        diskNames.append(allDisks.json()['volumes'][i]['name'])
    for i in range(len(diskNames)):
        if diskNames[i] == name:
            return allDisks.json()['volumes'][i]
    return "No disk with such name"


def updateInfo(current_project, name, TOKEN):
    current_volume = getvolumeIdByName(current_project, name)
    url = 'https://evs.ru-moscow-1.hc.sbercloud.ru/v2/{project_id}/volumes/{volume_id}'.format(
        project_id=current_project, volume_id=current_volume)
    header = {'Content-Type': 'application/json', 'X-Auth-Token': TOKEN}
    json = {
        "volume": {
            "name": "test_put",
            "description": "test"  # запрашиваются
        }
    }
    updateDisk = requests.put(url, headers=header, json=json)
    return updateDisk

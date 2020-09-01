import csv
import sys
import configparser
import requests



config = configparser.ConfigParser()
config.read('okta-config.txt')
url = config.get('General', 'url')
token = config.get('General', 'token')
groupName = config.get('General', 'group_name')
fileName = config.get('General', 'filename')



def getUserId (userName):    
    res = requests.get(url+'/api/v1/users?q='+userName,headers={'Accept':'application/json','Content-Type':'application/json', 'Authorization': 'SSWS '+token})
    dictFromServer = res.json()
    try:
        userId = dictFromServer[0]['id']
    except IndexError:
        userId = 'Invalid'
    return userId

def getGroupId (groupName):
    res = requests.get(url+'/api/v1/groups?q='+groupName,headers={'Accept':'application/json','Content-Type':'application/json', 'Authorization': 'SSWS '+token})
    dictFromServer = res.json()
    try:
        groupId = dictFromServer[0]['id']
    except IndexError:
        groupId = 'Invalid'
    return groupId

def performUpdate (userId,groupId):
    res = requests.put(url+'/api/v1/groups/'+groupId+'/users/'+userId,headers={'Accept':'application/json','Content-Type':'application/json', 'Authorization': 'SSWS '+token})
    return res.status_code

groupId=getGroupId(groupName)

list1=[]
list2=[]

with open(fileName, 'r') as File:
    reader = csv.reader(File, delimiter=',')
    for row in reader:
        userId = getUserId(row[0])
        if userId=='Invalid':
            with open('UserNotFound.txt', 'a') as f:
                f.write(row[0] + '\n')
                list1.append(row[0])
        else:
            performUpdate(userId,groupId)
            with open('UserAddedToGroup.txt', 'a') as f:
                f.write(row[0] + '\n')
                list2.append(row[0])


with open('UserCountNotSuccessfullyAdded.txt', 'w') as f:
    f.write('Count of users who did not get added to group ' +groupName + " " +'are ' + str(len(list1)))

with open('UserCountSuccessfullyAdded.txt', 'w') as f:
    f.write('Count of users who got added to group ' +groupName + " " +'are ' + str(len(list2)))

import requests
import json

# ISO categories structure
IsoCategories = [{'title': 'Categories', 
'categories': [
{'title': 'WIP', 'categories': [
    {'title': 'S0', 'categories': []}]}, 

{'title': 'Shared (non-contractual)', 'categories': [
    {'title': 'S1 - Suitable for coordination', 'categories': []}, 
    {'title': 'S2 - Suitable for information', 'categories': []}, 
    {'title': 'S3 - Suitable for review and comment', 'categories': []}, 
    {'title': 'S4 - Suitable for stage approval', 'categories': []}, 
    {'title': 'S6 - Suitable for PIM authorization', 'categories': []}, 
    {'title': 'S7 - Suitable for AIM authorization', 'categories': []}]}, 

{'title': 'Published (contractual)', 'categories': [ 
    {'title': 'A1 - Accepted stage 1', 'categories': []}, 
    {'title': 'A2 - Accepted stage 2', 'categories': []}, 
    {'title': 'A3 - Accepted stage 3', 'categories': []}, 
    {'title': 'A4 - Accepted stage 4', 'categories': []}, 
    {'title': 'A5 - Accepted stage 5', 'categories': []}, 
    {'title': 'A6 - Accepted stage 6', 'categories': []}]}, 

{'title': 'Archive', 'categories': []}, 

{'title': 'Reference data', 'categories': []}]}]

# generate token function can be used once to get a token of your portal using rest api. 
def generateToken(username, password, portalUrl):
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Host': 'www.arcgis.com', 'Content-Length': '[]' }
    parameters = {'username': username,
                  'password': password,
                  'client': 'referer',
                  'referer': portalUrl,
                  'expiration': '60',
                  'f': 'json'}
    url = portalUrl + '/sharing/rest/generateToken?'
    response = requests.post(url, data=parameters, headers=headers)

    try:
        jsonResponse = response.json()
        if 'token' in jsonResponse:
            return jsonResponse['token']
        elif 'error' in jsonResponse:
            print (jsonResponse['error']['message'])
            for detail in jsonResponse['error']['details']:
                print (detail)
    except ValueError:
        print('An unspecified error occurred.')
        print(ValueError)


# assignin ISO using REST API in python
def assignISO19650StatesAndStatusRESTapi(AuthenticationToken , group,
                                         categories= IsoCategories, portal_URL = r"https://www.arcgis.com"):
    Rest_API_Parameter = {"categorySchema": categories}
    Parameter          = {"categorySchema": json.dumps(Rest_API_Parameter)}
    Parameter['token'] = AuthenticationToken
    url                = portal_URL + r"/sharing/rest/community/groups/" + group + "/assignCategorySchema?f=json"
    response = requests.post(url, params= Parameter)
    try:
        jsonResponse = response.json()
        if 'success' in jsonResponse:
            return jsonResponse['success']
        elif 'error' in jsonResponse:
            print (jsonResponse['error']['message'])
            for detail in jsonResponse['error']['details']:
                print (detail)
    except ValueError:
        print('An unspecified error occurred. \nValueError')

# assign state and status to an Item in a group! 
def updateItemsCategoriesOfGroup(AuthenticationToken , group, itemid, state = None , status =None , portal_URL = r"https://www.arcgis.com", isoStateStatus = IsoCategories):
    def CheckStateStatusValidity(Ste,stus, isoStateStatus ):
        for i in isoStateStatus[0]['categories']:
            if i["title"] == Ste:
                if stus != None:
                    for j in i["categories"]:
                        if j["title"] == stus:
                            return True
                else: return True
        return

    if state != None: 
        itemsID_Categories  = [{itemid: ["/Categories/"+ state]}]
    else:
        print("Error: provide a state")
        return 
    if status != None:
        itemsID_Categories[0][itemid][0] += "/" + status
    if CheckStateStatusValidity (state, status,isoStateStatus ):
        Parameter           = {'items': json.dumps(itemsID_Categories)}
        Parameter['token']  = AuthenticationToken
        url                 = portal_URL + r"/sharing/rest/content/groups/" + group + "/updateCategories?f=json"
        response = requests.post(url, params= Parameter)
        try:
            jsonResponse = response.json()
            if 'results' in jsonResponse:
                if status == None: status = "" 
                else:status = "and status " + "\"" + status + "\""
                print ("Item " + jsonResponse['results'][0]['itemId'] + f" has been updated with state \"{state}\" {status}")
                return True
            elif 'error' in jsonResponse:
                print (jsonResponse['error']['message'], " ", jsonResponse['error']['details'] )
                return 
        except ValueError:
            print('An unspecified error occurred. \nValueError')
            return 
    print ("State and/or status of the item are not valid")
    return

# update the snippet/description with metadata
def update_Snippet_Or_Description_SRC(AuthenticationToken, itemid, userName, tags = None,  SRC = "Revision: P.00.00, Approved: True, Last updated by: UserName, Container classification: Not defined",
                                SnippetOrDescription = "snippet", portal_URL = r"https://www.arcgis.com" ):
    Parameter           = {SnippetOrDescription: SRC} 
    Parameter['token']  = AuthenticationToken
    # Parameter['tags']   = "Shared (non-contractual),Published (contractual)"
    if tags:
        if len (tags) ==1:
            tagsString = tags[0]
            Parameter['tags'] = tagsString
        elif len (tags) >1:
            tagsString = tags[0]
            for tag in tags[1:]:
                tagsString = tagsString + "," + tag 
            Parameter['tags'] = tagsString

    url                 = portal_URL + "/sharing/rest/content/users/" + userName + "/items/" + itemid + "/update?f=json"
    response            = requests.post(url, params= Parameter)
    try:
        jsonResponse = response.json()
        if 'success' in jsonResponse:
            return jsonResponse['success']
    except ValueError:
        print('An unspecified error occurred. \nValueError')

# update the revision in the meta data based on the state assigned to it (the current one and the next one) 
def updateRevision (CurrectState, NextState, revision, categories = IsoCategories):
    WIPrevision   = int (revision[-2:])
    sharedRevison = int (revision[-5:-3])
    if NextState == categories[0]['categories'][0]['title']: #WIP 
        
        if CurrectState == categories[0]['categories'][0]['title']: # WIP
            return revision[:-5] + str (f"{sharedRevison:02}") + "." + str (f"{WIPrevision+1:02}")
        else:
            return revision[:-5] + str (f"{sharedRevison:02}") + "." + str(f"{0:02}")
    
    elif NextState == categories[0]['categories'][1]['title']: # Shared
        return revision[:-5] + str (f"{sharedRevison+1:02}") + "." + str (f"{0:02}")
    elif NextState == categories[0]['categories'][2]['title']: # Published
        if revision[-7:-5] == "C.": return revision[:-5] + str (f"{sharedRevison+1:02}") + "." + str (f"{0:02}")
        return revision[:-7] + "C." + str (f"{1:02}") + "." + str (f"{0:02}")
    else:
        print ("Error: revision function works only between WIP, Shared and Published environment.\nCheck revision structure in the metadata it should be something like \"Revision: P.00.00\"" )
        return revision

# list all items in a group return a list of items (note this is different from the info of an item itself even tho there are many common attributes)
# so you can see the returned info as item details for arranging the items inside a group 
def list_ItemsInGroup(AuthenticationToken, groupid, portal_URL = r"https://www.arcgis.com"):
    Parameter        = {'token': AuthenticationToken}
    url              = portal_URL + r"/sharing/rest/content/groups/" + groupid + "?f=json"
    response = requests.post(url, params= Parameter)
    try:
        jsonResponse = response.json()
        if 'total' in jsonResponse:
            if jsonResponse["total"] > 0:
                return jsonResponse ['items']
        else: return
    except ValueError:
        print('An unspecified error occurred. \nValueError')

# this function adds a comment to an item 
def addComment(AuthenticationToken, itemid, Comment = "No comment provided",  portal_URL = r"https://www.arcgis.com"):
    Parameter            = {'token': AuthenticationToken, 'Comment': Comment}
    url                  = portal_URL + r"/sharing/rest/content/items/" + itemid + "/addComment?f=json"
    response = requests.post(url, params= Parameter)
    jsonResponse = response.json()
    try:
        if 'success' in jsonResponse:
                return jsonResponse['success'], jsonResponse['commentId']
    except ValueError:
        print('An unspecified error occurred. \nValueError')

def approve(AuthenticationToken, itemid, userName, portal_URLApprove = r"https://www.arcgis.com"): 
    metadata = getItemMetadataAndTags(AuthenticationToken, itemid, snippetOrdisc = "snippet", portal_URL = portal_URLApprove)[0]
    revision, approved, lastUpdate, containerClass = metadata.split(",")
    if "False" in approved.split(":")[1]: 
        approved = " Approved: True"
        SRCReturned = revision + "," + approved + "," + lastUpdate + "," + containerClass
        commentUsser = input("Add a comment: ...")
        if commentUsser == "": commentUsser = "No comment" 
        commentUsser = "Approved by" + userName + ":" + commentUsser
        addComment(AuthenticationToken, itemid, commentUsser, portal_URLApprove)
        return update_Snippet_Or_Description_SRC(AuthenticationToken, itemid, userName, tags=None, SRC=SRCReturned, portal_URL=portal_URLApprove )
    elif "True" in approved.split(":")[1]: 
        print ("Information container is already approved")
        return 
    else:
        print ("Error: something went wrong, check on the metadata")
        return 

# create a group or update an existing one with states and status of ISO 19650 standards/ return True / error
def CreateISO19650Based_Group(AuthenticationToken, titleOritemID,
                            description = "group for managing ISO 19650 workflows", Categories =IsoCategories,  
                            portal_URL = r"https://www.arcgis.com" ):
    url                 = portal_URL + "/sharing/rest/community/createGroup?f=json"
    Parameter           = {"title": titleOritemID, 'token':AuthenticationToken, 'description': description, "access":"account"}
    response            = requests.post(url, params= Parameter)
    JsonResponse        = response.json()
    try:
        if 'success' in JsonResponse:
            return  assignISO19650StatesAndStatusRESTapi (AuthenticationToken, JsonResponse['group']['id'], Categories)
        else:
            if 'error' in JsonResponse:
                print (JsonResponse['error']['message'],"\n",JsonResponse['error']['details'][0] )
    except ValueError:
        print('An unspecified error occurred. \nValueError')

# function that return metadata from Snippet and tags of an item 
def getItemMetadataAndTags(AuthenticationToken, itemid, snippetOrdisc = "snippet", portal_URL = r"https://www.arcgis.com"):
    Parameter            = {'token': AuthenticationToken}
    url                  = portal_URL + r"/sharing/rest/content/items/" + itemid + "?f=json"
    response = requests.post(url, params= Parameter)
    try:
        jsonResponse = response.json()
        # print (jsonResponse)
        if snippetOrdisc in jsonResponse:
            return jsonResponse[snippetOrdisc], jsonResponse['tags']
        elif 'error'in jsonResponse:
            return jsonResponse
    except ValueError:
        print('An unspecified error occurred. \nValueError')

# return the state (category) of an item - True (if WIP, shared or published) / False (if other states e.g archive), None if state does not exist.  
def getItemsState(AuthenticationToken, itemid, groupid, portal_URL = r"https://www.arcgis.com", categories = IsoCategories):
    itemsIngroug = list_ItemsInGroup(AuthenticationToken, groupid, portal_URL)
    for item in itemsIngroug:
        if item['id']== itemid:
            if len(item['groupCategories']) ==1:
                state = item['groupCategories'][0].split("/")[2]
                if state == categories[0]['categories'][0]['title'] or state == categories[0]['categories'][1]['title'] or state == categories[0]['categories'][2]['title']:return True, state
                elif state == categories[0]['categories'][3]['title'] or state == categories[0]['categories'][4]['title']: return False, state
                else:
                    print (f"Error: item is not assigned one of the states specified {categories[0]['categories'][0]['title'], categories[0]['categories'][1]['title'], categories[0]['categories'][2]['title']}")
                    return False, None
            return False, None

# takes a as in put current state, next state and the list of the tags of the incident item, it reurns a list of the updated tags accordingly 
def updateTags(current, next_, tagsList_, categories = IsoCategories):
    for tag in tagsList_:
        if current != tag:
            if tag in [categories[0]['categories'][0]['title'], categories[0]['categories'][1]['title'], categories[0]['categories'][2]['title']]:
                tagsList_.remove(tag)
    counter = 0
    for tag2 in tagsList_:
        if current == tag2:
            tagsList_[counter] = next_
            return tagsList_
        counter += 1
    if next_ in [categories[0]['categories'][0]['title'], categories[0]['categories'][1]['title'], categories[0]['categories'][2]['title']]: 
        tagsList_.append(next_)
        print ("Tags has no tag of the current state")
        return tagsList_


# main Push functionalities that is used to transition items between ISO 19650 states (WIP, shared, published)  
# It updates the metadata of an item (information container) such as revision,
# if approved of the metadata true it becomes False
def push (AuthenticationToken, itemid, groupid, userName, NextState, statusPush =None, 
    categories = IsoCategories, snippetOrDisc = "snippet", portal_URL= r"https://www.arcgis.com"):
    def checkStateStatusValidityPush(stateCheck, statusCheck, categories2 = categories):
    # checks if status and state of the information container (item) are valid for the push function
        for i in categories2[0]['categories'][:3]:
            if i["title"] == stateCheck:
                if statusCheck != None:
                    for j in i["categories"]:
                        if j["title"] == statusCheck:
                            return True
                else: return True
    # check the validity of the state and status provided by the user
    if checkStateStatusValidityPush(NextState, statusPush, categories):
        # Getting the current state of an item and check its validity for push function
        TrOrFa, CurrectState = getItemsState(AuthenticationToken, itemid, groupid)
        if TrOrFa: metadata, tagsList = getItemMetadataAndTags(AuthenticationToken, itemid)
        else:
            print("Error: Item has invalid state\nWarning: push function works only between WIP, shared, and published states\nConsider initializing metadata using initilizemetadataOfitem() function")
        # update tags list with the next state / return updated list
        tagsL = updateTags(CurrectState, NextState, tagsList)

        # devide the metadata into parameters to be updated and check the structure 
        parameters = len (metadata.split(","))
        if parameters == 3:
            revision, Approved, lastUpdate = metadata.split(",")
            if "Revision:" not in revision or "Approved:" not in Approved or "Last updated by" not in lastUpdate: 
                print ("structure of the metadata in snippet is wrong")
                return  
        elif parameters == 4:
            revision, Approved, lastUpdate, containerClass = metadata.split(",")
            if "Revision:" not in revision or "Approved:" not in Approved or "Last updated by:" not in lastUpdate or "Container classification:" not in containerClass: 
                print ("structure of the metadata in snippet is wrong")
                return 
        else:
            print ("Error: structure of metadata is wrong, \neach field should devided with \",\" and each object is devided with \":\"", "\nFor example: Revision: P.00.00, Approved: True")
        # Check if item has not been approved before transitioning between states
        if "False" in Approved and NextState != CurrectState: 
            warning = "With warning: the information container had not been approved before transitioning!"
            print ("Warning: the information container has not been approved!")
        else:warning = None

        # updating metadata with required data accordingly  
        revision         = updateRevision(CurrectState, NextState,revision, categories)
        lastUpdate       = lastUpdate.split(":")[0] + ": "+ userName
        Approved         = Approved.split(":")[0] + ": " + "False"

        # composing metadat of the updated parameters 
        if parameters == 4: returnedMetadata = revision + "," + Approved + "," + lastUpdate + "," + containerClass
        else:returnedMetadata = revision + "," + Approved + "," + lastUpdate
        # update item with updated metadata
        update_Snippet_Or_Description_SRC(AuthenticationToken, itemid, userName, tags=tagsL, SRC=returnedMetadata, SnippetOrDescription=snippetOrDisc, portal_URL= portal_URL)
        # update the item category in the group 
        updateItemsCategoriesOfGroup(AuthenticationToken, groupid, itemid, state = NextState, status =statusPush, portal_URL = portal_URL, isoStateStatus = categories)
        # ask the user for adding comment to register the transionning action of the container
        commentUsser = input("Add a comment...")
        if commentUsser == "": commentUsser = "No comment" 
        commentUsser = f"{CurrectState} to {NextState}: {commentUsser}"
        if warning:  commentUsser = commentUsser + f"\n{warning}"
        addComment(AuthenticationToken, itemid=itemid, Comment=commentUsser , portal_URL=portal_URL)
    else:
        print ("Error: Invalid state or incompatible state and status provided\nWarning: push function works only between WIP, shared, and published states")
    # to be continueed

# This function makes the item reference data for the project (existing project related data)
def makeReferenceData(AuthenticationToken,  itemID, GroupID,  userName,  ContainerClassification = None, categories = IsoCategories, portal_URL = r"https://www.arcgis.com"):
    if ContainerClassification:update_Snippet_Or_Description_SRC(AuthenticationToken, itemID, userName, tags=[categories[0]['categories'][4]['title']],
                SRC=f"{categories[0]['categories'][4]['title']}, Last updated by: {userName}, Container classification: {ContainerClassification}", portal_URL=portal_URL)

    else:update_Snippet_Or_Description_SRC(AuthenticationToken, itemID, userName, tags=[categories[0]['categories'][4]['title']],
                SRC=f"{categories[0]['categories'][4]['title']}, Last updated by: {userName}", portal_URL=portal_URL)
    return updateItemsCategoriesOfGroup(AuthenticationToken, GroupID, itemID, categories[0]['categories'][4]['title'], portal_URL = portal_URL, isoStateStatus= categories ) 

# This function intialize the required metadata for an item
def initilizemetadataOfitem(AuthenticationToken, itemID, GroupID, userName,  ContainerClassification = None, categories = IsoCategories, portal_URL = r"https://www.arcgis.com"):
    tags = getItemMetadataAndTags(AuthenticationToken, itemID, portal_URL=portal_URL)[1]
    tags = updateTags(categories[0]['categories'][0]['title'], categories[0]['categories'][0]['title'],tags )
    if ContainerClassification: update_Snippet_Or_Description_SRC(AuthenticationToken, itemID, userName, tags=tags, 
                SRC=f"Revision: P.00.00, Approved: False, Last updated by: {userName}, Container classification: {ContainerClassification}", portal_URL=portal_URL)
    else:update_Snippet_Or_Description_SRC(AuthenticationToken, itemID, userName, tags=tags,
                SRC=f"Revision: P.00.00, Approved: False, Last updated by: {userName}", portal_URL=portal_URL)
    return updateItemsCategoriesOfGroup(AuthenticationToken, GroupID, itemID, categories[0]['categories'][0]['title'], portal_URL = portal_URL, isoStateStatus= categories )
    

if __name__ == '__main__':
    pass

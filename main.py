
from   arcgis.gis import GIS
import json
import ArcGIS_GroupAs_ISO19650_CDE


if __name__ == '__main__':
    # defaul ISO 19650 standards for metadata
    default_ISO19650BritishAnnex = True

    token           = r"DT5Z8c3BB9QMIAE31Iy-9efZZqRivQc_t8zPE6_Iwps0FYpSRcPb0WroQ9i-fEsi0Ym8lneCqHur4_eBc2HKxQ_5zCzoGDAWkBDURiIBIySnAlCum5LIGLU9uZw6zDofyff_q9le7qKCIuJqJbBsxPKjbgIiZsHhhJpuA6MS3INoJGUqufDAE-vj_3MT4siX-ispQIasWL5CDg-0y2JV1Lzrfr-jSBIbmmeeJgzU2Kc"
    GroupID         = r"38d66a69c5e5457a90dcf0970e4d215f"
    userName        = r"alhoz_esrinederland"
    ItemID          = r"dd4df552575b4d71944a51731b0a4e59"

    JSONportal_URL  = r"https://www.arcgis.com"
    metadat         = r"Revision: P.00.00, Approved: False, Last updated by: username, Container classification: ____"

    # # getting the data (iso 19650 structure/categories (state & status)) from the json file
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    jsonData = open (dir_path + r"/ISOCategories.json",)
    if default_ISO19650BritishAnnex is True:
        IsoCategories = [json.load(jsonData)]

    import sys 
    ##### function 1 ##############
    # creating group ISO 19650 based structured
    ###################
    if sys.argv[1] == "ISO 19650 group":
        if len(sys.argv) == 4:
            if sys.argv[2] == "New" or sys.argv[2] == "new": ArcGIS_GroupAs_ISO19650_CDE.CreateISO19650Based_Group( token, titleOritemID = sys.argv[3], portal_URL= JSONportal_URL)
            else:
                if sys.argv[2] == "existing" or sys.argv[2] == "Existing": ArcGIS_GroupAs_ISO19650_CDE.assignISO19650StatesAndStatusRESTapi(token, 
                group = sys.argv[3], categories= IsoCategories, portal_URL= JSONportal_URL)
        elif len(sys.argv) == 5:
            if sys.argv[2] == "New" or sys.argv[2] == "new": ArcGIS_GroupAs_ISO19650_CDE.CreateISO19650Based_Group(token, titleOritemID =sys.argv[3], description=sys.argv[4], portal_URL= JSONportal_URL )
        else: print ('Error: Incorrect number of arguments passed.')
    ###################
    # example of parameteriztion 
    # "ISO 19650 group" "new/existing" "TitleOrItemID" "Description (optional)" 


    ######## function 2 #############
    # update items with initail metadata all/one
    ####################
    if sys.argv[1] == "initialize metadata":
        if len (sys.argv) == 5 or len (sys.argv) == 4:
            if sys.argv[2] == "all" or sys.argv[2] == "All":
                Items = ArcGIS_GroupAs_ISO19650_CDE.list_ItemsInGroup(token, sys.argv[3], portal_URL=JSONportal_URL)
                # print (Items)
                if len (sys.argv) == 5:
                    for Item in Items:
                        ArcGIS_GroupAs_ISO19650_CDE.initilizemetadataOfitem(token, Item["id"],sys.argv[3], userName, ContainerClassification = sys.argv[4], portal_URL = JSONportal_URL)
                else:
                    for Item in Items:
                        ArcGIS_GroupAs_ISO19650_CDE.initilizemetadataOfitem(token, Item["id"], sys.argv[3],  userName, portal_URL = JSONportal_URL)
            else:
                if len (sys.argv) == 5:ArcGIS_GroupAs_ISO19650_CDE.initilizemetadataOfitem(token, sys.argv[2],sys.argv[3], userName, ContainerClassification = sys.argv[4], portal_URL = JSONportal_URL)
                else:ArcGIS_GroupAs_ISO19650_CDE.initilizemetadataOfitem(token, sys.argv[2], sys.argv[3], userName, portal_URL = JSONportal_URL)
        else: print ('Error: Incorrect number of arguments passed.')
    ####################
    # example of parameteriztion
    # "initialize metadata" "all" "groupID" "Architecture(optional)"
    # "initialize metadata" "itemID" "groupID" "Architecture(optional)"


    ######## function 3 #############
    # push function
    #################
    if sys.argv[1] == "Push" or sys.argv[1] == "push":
        if len (sys.argv) == 6 or len (sys.argv) == 5:
            if len (sys.argv) == 6: statusPush = sys.argv[5]
            else:statusPush = None
            ArcGIS_GroupAs_ISO19650_CDE.push(token, sys.argv[2], sys.argv[3], userName, sys.argv[4], statusPush, categories=IsoCategories, snippetOrDisc="snippet", portal_URL=JSONportal_URL)
        else: print ('Error: Incorrect number of arguments passed.')
    ###################
    # example of parameteriztion 
    # "Push" "ItemID" "gorupID" "Published (contractual)" "A1 - Accepted stage 1"

    ######## function 4 ############# 
    # aprove function 
    #####################
    if sys.argv[1] == "approve" or sys.argv[1] == "Approve":
        if len(sys.argv) == 2:
            ArcGIS_GroupAs_ISO19650_CDE.approve(token, sys.argv[2], userName, portal_URLApprove = JSONportal_URL)
        else: print ('Error: Incorrect number of arguments passed.')
    ###################
    # example of parameteriztion 
    # "approve" "ItemID" 

    ######## function 5 ############# 
    # Make reference data 
    #####################
    if sys.argv[1] == "Make reference data" or sys.argv[1] == "Make reference data":
        if len(sys.argv) == 4 or len(sys.argv) == 5:
            if len(sys.argv) == 4:
                ArcGIS_GroupAs_ISO19650_CDE.makeReferenceData(token, sys.argv[2], sys.argv[3], userName, categories = IsoCategories, portal_URL = JSONportal_URL)
            else: ArcGIS_GroupAs_ISO19650_CDE.makeReferenceData(token, sys.argv[2], sys.argv[3], userName, ContainerClassification= sys.argv[4], categories = IsoCategories, portal_URL = JSONportal_URL)
        else:print ('Error: Incorrect number of arguments passed.')
    ###################
    # example of parameteriztion 
    # "Make reference data" "itemID" "groupID" "Architecture(optional)"

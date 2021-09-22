# ArcGIS_ISO-19650-workflows

This repository contains proof of concept funcationalities for my thesis on the topic _**The role of Web GIS in project information management aligned with ISO 19650 standards**_. 
The funcationalities are implemented using ArcGIS [Rest API](https://developers.arcgis.com/rest/) and Python as a scripting language.
The created functionalities can be utilized to support information workflows aligned with ISO 19650 standards (UK national annex) in ArcGIS platform.
Therefore, the Group feature is seen as a single ISO 19650 CDE in which items are considered information containers (see figure below). 
For the implementation, the UK national annex conventions are used. 
The functionalities are tested on ArcGIS Online platform, however, they should be fully functional in ArcGIS Enterprise. 
The idea behind creating these functionalities is to be utilized in Web-based applications. 
An example of these applications is [ArcGIS Hub](https://hub.arcgis.com/), as part of the implementation [this Hub](https://hubiso-19650-example-esrinederland.hub.arcgis.com/) was created as template example of UI for information management workflows. 
Moreover, a detailed description of the implementation is to find in this [StoryMap - ISO 19650 standards in the ArcGIS Platform](https://storymaps.arcgis.com/stories/f973462663af453a92b14ff107621a4b/).
##### Credits (Attribution)
For this work, I would like to express my great appreciation to Frank de Zoeten (content supervisor) & Niels van der Vaart for sharing their expertise on the field and the used platform/software; and enabling all kinds of research practicalities within the company. I would also like to thank Eelco Berghuis for sharing his knowledge and the collaboration on the innovation competition, which significantly supported this research. I would also like to thank Stelios Vitalis & Dr. Francesca Noardo for their supervision of the scientific approach to this research.

![Figure](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/fig/ArcGISOnlineVsISO.png).  

#### This repo contains the following files:
* This **readme.md** file. 
* main.py # main Python file contains the [main functionalities](#functionalities) created for the purpose of this thesis. Instructions can be found in [usage](#usage) section. 
* ArcGIS_GroupAs_ISO19650_CDE.py # Python file contains many functions to retrieve and update data in the ArcGIS Platform portals (note that all functions are tested on ArcGIS Online only). The functions in this file are used to construct the main ISO 19650 functionalities that can be utilized from the main file. If desired, you can use these functions separately. More details provided in the comments above each function in the file. 
* ISOCategories.json # JSON file contains objects that represent **States (WIP, Shared, Published, Archive and Reference data)** and **Statuses (S0, S1, ... etc)** of ISO 19650 standards as described in the British national annex. The maind document used is [Guidance Part C - Facilitating the common data environment (workflow and technical solutions)](https://ukbimframework.org/wp-content/uploads/2020/09/Guidance-Part-C_Facilitating-the-common-data-environment-workflow-and-technical-solutions_Edition-1.pdf)
 of **Information management according to BS EN ISO 19650**. 
* LICENSE 
* Fig folders 

### Usage 
There are two ways:
##### > Using this [Python Notebook](https://esrinederland.maps.arcgis.com/home/item.html?id=1325cacd64164187a7888b83d2399318)  
This method is more straightforward as the required parameters are automatically derived from the portal, all further instructions are to find in the notebook.

##### > Using the Command Prompt
###### update the required parameters in _**main.py**_ file 
* Required parameters  
  
    * token for accessing the AcrGIS protal  
**token** = "" 
    * Your ArcGIS username   
**userName**        = " " # e.g "kalhoz_esrinederland"
    * Portal url (defaul arcgis online) should be changed if using enterprise
**JSONportal_URL**  = r"https://www.arcgis.com"  
* Optional parameters
    * defaul ISO 19650 standards for metadata (set on "True" and configure your own statuses in json file)  
**default_ISO19650BritishAnnex** = False

###### follow the instruction for each function [main functionalities](#functionalities)
   
### Functionalities
#### function 1 "ISO 19650 group"
creating group with ISO 19650 based structure  
This function can be used for creating new ISO 19650 based goup (or structuring an existing one). This is done using Group Categories feature (object of represnting json file of a group) which is a feature (JSON object) used to filter the items in a group, e.g each item can be assigned one of the categories and filtered out accordingly. 
It adds the categories WIP, shared, published etc to the created group according to the British national annex of ISO 19650 standards, see default ISO 19650 cagegories in the [JSON](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/ISOCategories.json) file if you desire to make changes on **status categories**. Example of the ISO 19650 categories in a group  
In the command prompt, provide the parameters _**ISO 19650 group**_ either **new** with **title** or **existing** with **GroupID**  
example:  
> "Python.exe" "path_to_this_main_file/main.py" "ISO 19650 group" "new/existing" "Title/GroupID" "Description (optional)"   

here is an example of how the categories are configured in a group as a CDE  

![](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/fig/CategoriesStatesStatusExample.PNG)

#### function 2 "initialize metadata"
update items in a group with initail metadata all items/one item.  
After adding items to the created ISO 19650 based group, this function initiate metadata of an item (or all items). This function addes the metadata according to ISO 19650 requirements in the field "snippet" (brief description over an item field). Example metadata of the [json response](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/fig/metadataJSONResponse.PNG) and the UI of the item  
In the command prompt, provide the parameters _**initialize metadata**_ either **all** or **itemID**  **groupID** **ContainerClassification**  
example:  
> "Python.exe" "path_to_this_main_file/main.py" "initialize metadata" "all/itemID" "groupID" "Architecture(optional)"   

here is an example of how metadata placed in snippet field of an item looks like  
![](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/fig/MetadataItemExample.PNG).


#### Function 3 "Push" function 
Push an item from/to one of the states WIP, Shared, or Published with a specified status (S0, S1, etc) have a look at the [JSON](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/ISOCategories.json) file for viewing and changing the status if you desire to.
This function does the following when it runs:
* Change the groupCategories (state and status) of the item (information container) provided 
* Updates the **revision**, **Approved** and **last updated by**, of metadata accordingly.
* Add comments that shows **state to state** and ask for comment from the user to add with the actions. This is used for version history control of items' workflows. 
* Add tag of the pushed-to state and remove the tag of the current state from tags (this is importatnt for filtering items according to the state they are at in the Hub Page).  

In the command prompt, provide the parameters _**"Push"**_ **ItemID** **gorupID**  **State** **Status**  
example:  
> "Python.exe" "path_to_this_main_file/main.py" "Push" "ItemID" "gorupID" "Published (contractual)" "A1 - Accepted stage 1"

#### function 4 "aprove" function
This function approves the item by changing **Approved: False** to **Approved: True**. It also add a comment: Approved by **UserName**.
Returns a warning if the item had been approved. 
In the command prompt, provide the parameters **_approve_** **ItemID**  
example:  
> "Python.exe" "path_to_this_main_file/main.py" "approve" "ItemID"  

#### function 5 "makeReferenceData" function
This function makes projects related data available for usage or referenecing. For example, items of the existing situation of a project or documents/instructions (items) on deliverables that should be read by the project team (delivery team).  
In the command prompt, provide the parameters **_Make reference data_** **ItemID** **groupID** **ContainerClassification**
example:  
> "Python.exe" "path_to_this_main_file/main.py" "Make reference data" "ItemID" "groupID" "Architecture(optional)" 



# ArcGIS_ISO-19650-workflows

This repository is the resulted work for my thesis on the topic _**The role of Web GIS in project information management aligned with ISO 19650 standards**_. 
The created functionalities can be utilized to support information workflows aligned with ISO 19650 standards in ArcGIS platform.
Therefore, the Group feature is seen as a single ISO 19650 CDE in which items are considered information containers. The workflow are tested in ArcGIS Online, however, they should be fully functional in ArcGIS Enterprise 

![Fingure](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/fig/ArcGISOnlineVsISO.png) .  

#### This repo contains the following files:
* This **readme.md** file. 
* main.py # main Python file contains the [main functionalities](#functionalities) created for the purpose of this thesis. Instructions can be found in [usage](#usage) section. 
* ArcGIS_GroupAs_ISO19650_CDE.py # Python file contains many functions to retrieve and update data in the ArcGIS Platform portals (note that all functions are tested on ArcGIS Online only). The functions in this file are used to construct the main ISO 19650 functionalities that can be utilized from the main file. If desired, you can use these functions separately. More details provided in the comments above each function in the file. 
* ISOCategories.json # JSON file contains objects that represent **States (WIP, Shared, Published, Archive and Reference data)** and **Statuses (S0, S1, ... etc)** of ISO 19650 standards as described in the British national annex. The maind document used is [Guidance Part C - Facilitating the common data environment (workflow and technical solutions)](https://ukbimframework.org/wp-content/uploads/2020/09/Guidance-Part-C_Facilitating-the-common-data-environment-workflow-and-technical-solutions_Edition-1.pdf)
 of **Information management according to BS EN ISO 19650**. 
* LICENSE 
* Fig folders 

#### Functionalities
##### function 1 "ISO 19650 group"
creating group with ISO 19650 based structure  
This function can be used for creating new ISO 19650 based goup (or structuring an existing one). This is done using Group Categories feature (object of represnting json file of a group) which is a feature (JSON object) used to filter the items in a group, e.g each item can be assigned one of the categories and filtered out accordingly. 
It adds the categories WIP, shared, published etc to the created group according to the British national annex of ISO 19650 standards, see default ISO 19650 cagegories in the [JSON](https://github.com/khalhoz/ArcGIS_ISO-19650-workflows/blob/main/ISOCategories.json) file if you desire to make changes on **status categories**
##### function 2 "initialize metadata"
update items in a group with initail metadata all items/one item

#### Usage

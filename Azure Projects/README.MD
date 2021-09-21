![image](https://user-images.githubusercontent.com/80606434/134220753-f5969be5-85bf-4e64-ab50-242a4ad29169.png)
## Purpose
The goal of this Azure project is to build an end to end Azure pipeline with the basic functionalities required of a Microsoft Azure environment. This includes the design and setup of storage, NoSQL/SQL, key vaults, and other interlinking softwares and services that are designed to ingest, store, and process data.

## Overview
As a generalized overview, the steps taken are listed below in creating the Azure environment

**Step 1 -** This first step includes creating a subscription that will manage all other resources and groups and is the first layer in creating the environment. From here, we will also want to instantiate other items such as:

   -**Resource Group** which will allow us to further control and monitor resource consumption once the environment is set up. 
  
   -**Storage containers** which will store our datasets as well as other storage items in formats such as Parquet, CSV, Avro, Binary, JSON, ORC, XML, and delimited text.
  
   -**Azure Data Factory** will help us monitor the overall health of the pipeline. It will allow us to integrate our different technologies in a simple, easy to use interface and allows for customization. Think of it as a one-stop-shop for systems integrations. For example, if you have various SQL dataset jobs that need to be run, you can configure them all at once through the data factory via single linked service as opposed to updating each SQL job individually.
  
   -**Azure Key Vault** increases security by restricting apps from having direct access to keys. It also reduces latency, allows for the creation and import of encryption keys quickly and allows easy monitoring over the status of all online keys.
 
We will also use an instantiation of PySpark run in a Jupyter notebook in HDInsight to run some rudimentary SQL and other data wrangling over some financial data, just to ensure that the cluster is working as expected.
 
 **Note:** *For the HDInsight cluster, it is important to note that if the cluster is not in use, **YOU SHOULD SHUT IT DOWN**. This will avoid any unecessary costs as you will be charged, in addition for the hours spent using the resource, but as well as just the cluster being in existence. Spinning up/shutting down a cluster does not take much time and may save a lot of resources in the future. If you choose not to do this, be sure to monitor expenses through the 'Cost Management + Billing' page in your Azure portal.*



**Step 2 -**

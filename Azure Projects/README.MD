![image](https://user-images.githubusercontent.com/80606434/134220753-f5969be5-85bf-4e64-ab50-242a4ad29169.png)
## Purpose
The goal of this Azure project is to build an end to end Azure pipeline with the basic functionalities required of a Microsoft Azure environment. This includes the design and setup of storage, NoSQL/SQL, key vaults, and other interlinking softwares and services that are designed to ingest, store, and process data.

## Overview
As a generalized overview, the steps taken are listed below in creating the Azure environment

**HDInsight -** This first step includes creating a subscription that will manage all other resources and groups and is the first layer in creating the environment. From here, we will also want to instantiate a resource group which will allow us to further control and monitor resource consumption once the environment is set up. We will also want to set up storage accounts as well as the HDInsight cluster. 
  - *For the HDInsight cluster, it is important to note that if the cluster is not in use, YOU SHOULD SHUT IT DOWN. This will avoid any unecessary costs as you will be charged, in addition for the hours spent using the resource, but as well as just the cluster being in existence. Spinning up/shutting down a cluster does not take much time and may save a lot of resources in the future. If you choose not to do this, be sure to monitor expenses through the 'Cost Management + Billing' page in your Azure portal.

We will also use an instantiation of PySpark run in a Jupyter notebook in HDInsight to run some rudimentary SQL and other data wrangling over some financial data, just to ensure that the cluster is working as expected.

**Step 1 -**

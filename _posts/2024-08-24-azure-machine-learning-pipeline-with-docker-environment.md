---
layout: post
title: Building an End-to-End Machine Learning Pipeline in Azure ML with a Dockerized Linux Environment
date: 2099-08-24 00:00:00 +09:00
tags: [azure, docker, githubaction, automl]            
mermaid: true
---

> In this article, I will walk through the details of an Azure Machine Learning pipeline that automates the entire process of deploying an AutoML model in Azure. The challenges were to set up the execution context for the pipeline tasks within a properly authenticated Linux environment, while also ensuring that all necessary dependencies and configurations are correctly implemented within the containerized environment. 
> 
> The Linux container, containing configuration files for Azure CLI commands and the dataset for AutoML training, is built and pushed to Azure Container Registry using a GitHub Action runner. Additionally, the Azure ML compute environment and scheduling specifications are also set up by the GitHub Action runner. The pipeline tasks are then executed on the Azure ML compute environment, following the behavior defined in its script.
>
> The requirement to use only the Azure Machine Learning CLI instead of the Python SDK introduced several pathing challenges that had to be addressed entirely through Bash scripting in a Linux environment. Overcoming these obstacles provided notable insights, so let's get started with going through details of the project!

## 0. Project Architecture 

- GitHub Action script: [azure-ml-setup.yml](https://github.com/CynicDog/Azure-ML-automation-research/blob/main/.github/workflows/azure-ml-setup.yml)
- Azure ML Pipeline script: [scheduled_pipeline_job.yml](https://github.com/CynicDog/Azure-ML-automation-research/blob/main/scripts/scheduled_pipeline_job.yml)

```mermaid
C4Context
    title  
    
    Deployment_Node(github, "GitHub") {
        Component(githubaction, "GitHub Action", "azure-ml-setup.yml", "")
    }

    Enterprise_Boundary(azure, "Azure") {
        
        Container(acr, "Acure Container Registry")

        Deployment_Node(azml, "Azure Machine Learning") {
            
            Component(compute, "Compute Cluster")
            
            Component(pipeline, "Pipeline")
            
            Component(scheduler, "Scheduler")
        }
    }

    Rel(githubaction, acr, "Linux env. with configs and data")
    UpdateRelStyle(githubaction, acr, $textColor="grey", $offsetX="-80", $offsetY="10")

    Rel(githubaction, compute, "Create compute cluster")
    UpdateRelStyle(githubaction, compute, $textColor="grey", $offsetX="-80", $offsetY="10")

    Rel(githubaction, scheduler, "Set up schedule")
    UpdateRelStyle(githubaction, scheduler, $textColor="grey", $offsetX="-80", $offsetY="10")

    Rel(acr, pipeline, "Provdes containerized Linux environment")
    UpdateRelStyle(acr, pipeline, $textColor="grey", $offsetX="-150", $offsetY="-80")

    Rel(scheduler, pipeline, "Triggers on cron event")
    UpdateRelStyle(scheduler, pipeline, $textColor="grey", $offsetX="-100", $offsetY="30")

    Rel(compute, pipeline, "Provides compute resource")
    UpdateRelStyle(compute, pipeline, $textColor="grey", $offsetX="-70", $offsetY="10")
```

More of the article is coming up 👨🏻‍💻...

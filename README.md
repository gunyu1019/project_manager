# Project Manager
A project manager based on web APIs.<br/> 

This project has two features.
* Read Project Status
* Auto Continuous Deployment (based git-action)

Project Manager uses two ways to manage projects.
* ~~PM2 (Package Manager)~~ (Working In Process)
* systemctl (org.freedesktop.systemd1)

## How to add project at Project Manager for continuous deployment?
1. Add service infomation at `config/project.ini`

```ini
[PROJECT_ID]
name = Project Name
package_id = project_id.service
type = systemctl
token = token (need generate)
directory = project's directory
auto_contiuous_deployment = True
```
2. Add Serect Key (Token and Project Token). <br/>
    `Settings > Security > Secrets and Variables > Actions`

3. Add github actions at `workflows/deploy.yml` Here is an example.

```yml
on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      ProjectID: PROJECT_ID
      Host: HOST URL
    steps:
      - name: Deploy to Virtual Private Server(VPS)
        run: |
          deployment_response=$(curl ${{ env.Host }}/deploy?project_id=${{ env.ProjectID }} \
            -H 'Project-Token: ${{ secrets.PROJECT_TOKEN }}' \
            -H 'Token: ${{ secrets.TOKEN }}')
          
          if [ $deployment_response -eq "11" ];  then
            echo "This project has disabled Automatic Continuous Deployment."
            exit 11
          elif [ $deployment_response -eq "12" ]; then
            echo "No fetch result."
            exit 12
          elif [ $deployment_response -eq "13" ]; then
            echo "Already Update"
            exit 13
          elif [ $deployment_response -eq "14" ]; then
            echo "An error occurred during pull request."
            exit 14
          elif [ $deployment_response -eq "15" ]; then
            echo "Unknown flags."
            exit 15
          elif [ $deployment_response -eq "43" ]; then
            echo "Forbidden Access."
            exit 43
          elif [ $deployment_response -eq "44" ]; then
            echo "Not Found."
            exit 44
          elif [ $deployment_response -eq "0" ]; then
            echo "Success Deployment"
          else
            echo "Wrong Response."
            exit 1
          fi
        shell: bash
      - name: Apply a New Version
        run: |
          restart_response=$(curl ${{ env.Host }}/restart?project_id=${{ env.ProjectID }} \
            -H 'Project-Token: ${{ secrets.PROJECT_TOKEN }}' \
            -H 'Token: ${{ secrets.TOKEN }}')
          
          if [ $restart_response -eq "11" ]; then
            echo "Unknown Project Type."
            exit 21
          elif [ $restart_response -eq "43" ]; then
            echo "Forbidden Access."
            exit 43
          elif [ $restart_response -eq "44" ]; then
            echo "Not Found."
            exit 44
          elif [ $restart_response -eq "0" ]; then
            echo "Success Apply a New Version."
          else
            echo "Wrong Response."
            exit 2
          fi
        shell: bash
      - name: Waiting for restart project (5 seconds minimum)
        run: sleep 5s
        shell: bash
      - name: Checking Status
        run: |
          state_response=$(curl ${{ env.Host }}/state?project_id=${{ env.ProjectID }})
          
          if [ $state_response -eq "0" ]; then
            echo "Success Deployment (Congratulations!)"
            exit 0
          elif [ $state_response -eq "15" ]; then
            echo "Success Deployment (but still turning on)"
            exit 0
          elif [ $state_response -eq "12" ]; then
            echo "Success Deployment However, You need verify that it works."
            exit 0
          elif [ $state_response -eq "13" ]; then
            echo "Failure Deployment Please check the logs."
            exit 33
          elif [ $state_response -eq "14" ]; then
            echo "Failure Deployment Please check the logs."
            exit 34
          elif [ $state_response -eq "16" ]; then
            echo "Failure Deployment Please check the logs."
            exit 36
          elif [ $state_response -eq "17" ]; then
            echo "Unknown Project Status Flags."
            exit 37
          elif [ $state_response -eq "11" ]; then
            echo "Unknown Project Type."
            exit 31
          else
            echo "Wrong Response."
            exit 3
          fi
        shell: bash

```

## How to get the service status?
* **[GET]** https://host_url/status?project_id=PROJECT_ID
    ```json
    {
      "current_memory": 0,
      "pid": 0,
      "started": "2024-07-01T00:00:00",
      "state": "active",
      "uptime": 0
    }
    ```
    * current_memory(Optional): A memory used by the service.
    * pid(Optional): A pid number of the service
    * started(Optional): The time the service started 
    * state: A state of service. 
        The states are active, reloading, inactive, failed, activating, and deactivating.<br/>
        * "active" means that the service is working without problems.<br/>
        * "reloading" means that the systemctl service settings have changed and are being reloaded.<br/>
        * "inactive" means the service is down.<br/>
        * "failed" means that the service threw an exception and stopped.<br/>
        * "activating" means that the service is transitioning from disabled to enabled.<br/>
        * "deactivating" means that the service is transitioning from enabled to disabled.<br/>
    * uptime(Optional): A uptime of the service
# sonar-action

### Static Code Analysis

Static code analysis ensures bug-free and secure code is checked into the master or respective branch. SonarQube is currently used to run the Static Code Analysis.

We need to pass the values of SONAR_HOST_URL, SONAR_TOKEN, SONAR_PROJECT_KEY & SONAR_PROJECT_NAME.

Please refer below for more details, 
[**Static Code Analysis (SonarQube Scan)**](https://hv-eng.atlassian.net/wiki/spaces/MCI/pages/30584439068/Static+Code+Analysis+SonarQube+Scan)

#### To perform the sonar analysis on your project, you need to add this step into the workflow after the Build step.

For MR Request :

```
- name: Sonarqube Scan
  uses: lumada-common-services/gh-composite-actions@develop
  env:
    sonar_utility: sonar-scanner
    sonar_commands: '("-Dsonar.projectKey=${{env.SONAR_PROJECT_KEY}} -Dsonar.host.url=${{env.SONAR_HOST_URL}}  -Dsonar.login=${{env.SONAR_LOGIN}}")'
```

For PR Request : 

```
- name: Sonarqube
  uses: lumada-common-services/gh-composite-actions@develop
  env:  
    sonar_utility: sonar-scanner
    sonar_commands: '("-Dsonar.projectKey=${{env.SONAR_PROJECT_KEY}} -Dsonar.host.url=${{env.SONAR_HOST_URL}}  -Dsonar.login=${{env.SONAR_LOGIN}}  -Dsonar.pullrequest.key=${{github.event.number}} -Dsonar.pullrequest.branch=${{github.event.pull_request.head.ref}} -Dsonar.pullrequest.base=${{github.event.pull_request.base.ref}}")'
```

# gh-composite-actions
As part of bootstrapped [container approach](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30584472476/Implementation+Architecture+of+Containerization+Theme) we shall use Composite Actions which allows you to modularise a predefined repeated task  into a single action, combining multiple run commands into a single reusable action. However, they are different from workflow reuse, so you will need a separate repository to manage them. For easy maintenance these composite actions can be populated in an `action.yaml` in separate repo. These composite actions have to be called from the Workflow where the pipeline has to be implemented by passing the necessary variables required for the pipeline to run.

Advantages:

1. Breakdown complex workflows into simple self contained modules;

2. Create templatized actions which can be called from multiple workflows there by enhancing the reusability;

3. The descriptive nature of an `action.yml` file improves the readability of a GitHub workflow when understanding necessary inputs and outputs.


List of Composite Actions:

1. Build: Please refer to the link how we defined the composite action for [build](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30470897989/Build);
2. Unit Test: Please refer to the link how we defined the composite action for [unit test](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30471323921/Testing);

      ```
      eg.
        - name: Unit Test Maven
          uses: lumada-common-services/gh-composite-actions@develop
          with:
            command: |
              mvn verify -B -Daudit -amd -Dmaven.test.failure.ignore=true 
          env:
            cmd_type: UNIT_TEST 
            unit_test_reporter: 'java-junit'
            unit_test_report_path: '**/target/*/*.xml'
            unit_test_copy_to_target_path: './test_report'
            unit_test_fail_on_error: 'false'
            unit_test_fail_on_empty: 'false'
      ```
      Note:

      1. unit_test_reporter: Supported options for the format of test results:(dart-json,dotnet-trx,flutter-json,java-junit,jest-junit,mocha-json).

      2. unit_test_report_path: Folder path where the complete test reports are automatically generated upon the execution of test cases.

      3. unit_test_copy_to_target_path: Destination folder path where the reports need to be copied from their default location.

      4. unit_test_fail_on_error: It's boolean-type parameter that determines whether the workflow should be marked as failed if there are any test cases that have failed. The default value for this parameter is set to `false`.
  
      5. unit_test_fail_on_empty: It's boolean-type parameter that determines whether the workflow should be marked as failed if no report is found. It will fail the build after not finding reports. The default value for this parameter is set to `false`.

3. Integration Test: Please refer to the link how we defined the composite action for [Integration Test](https://hv-eng.atlassian.net/wiki/spaces/MCI/pages/30781997882/KIND+Kubernetes+in+Docker);

      ```
      eg.
        - name: Integration Test Maven
          uses: lumada-common-services/gh-composite-actions@develop
          with:
            command: |
              mvn verify -DrunITs -Dit.test=EditorBeanIT 
          env:
            cmd_type: INTEGRATION_TEST 
            int_test_reporter: 'java-junit'
            int_test_report_path: '**/integration/target/*/*.xml'
            int_test_copy_to_target_path: './test_report'
            int_test_fail_on_error: 'false'
            int_test_fail_on_empty: 'false'
      ```
   
4. Generic Test: This composite action is designed to run any test step other than unit test and integration test. It introduces the new cmd_type `TEST` to the composite action for tracking any generic test step. Additionally, it utilizes the `TEST_DESC` environment variable to include additional descriptions along with the 'Test' keyword in the reporting. This generic test step will only be tracked if it is executed.
      
      ```
      eg.

        - name: Test
          uses: lumada-common-services/gh-composite-actions@develop
          with:
            command: |
              mvn test -Dkarma.file.config=karma.conf.js
          env:
            cmd_type: TEST    
            test_reporter: 'java-junit'
            test_report_path: '**/karma/target/surefire-reports/*.xml' 
            TEST_DESC: '- karma'
            test_copy_to_target_path: './karma_test_report'

      ```
5. Deploy: This composite action is to execute Deploy commands. It introduces the new cmd_type `DEPLOY` to the composite action for tracking any generic deploy step. Additionally, it includes the `DEPLOY_DESC` environment variable to include additional descriptions along with the 'Deploy' keyword in the reporting.
      
      ```
      eg.

        - name: Deploy
          uses: lumada-common-services/gh-composite-actions@develop
          with:
            command: |
              kubectl apply -f dotnet/deployment.yaml --namespace honeycomb-demo-deploy --kubeconfig $RUNNER_TEMP/config        
          env:
            cmd_type: DEPLOY
            DEPLOY_DESC: to jarjar Cluster

      ```
6. Sonarqube Scan: Please refer to the link how we defined the composite action for [sonar scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30584439068/Static+Code+Analysis+SonarQube+Scan);

7. Citadel Scan: Please refer to the link how we defined the composite action for [Citadel scan](https://hv-eng.atlassian.net/wiki/spaces/MCI/pages/30890459190/Honeycomb+and+Citadel+integration)

<!-- Blackduck Scan: Please refer to the link how we defined the composite action for [blackduck scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30471291264/Software+Composition+Analysis+Blackduck); -->

8. OWASP Scan: Please refer the to link how we defined the composite action for [owasp scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30577266601/Software+Composition+Analysis+OWASP+dependency+check);

9. Publish Artifacts to Registry: Please refer the to link how we defined the composite action for [Publish Artifacts to Registry](https://hv-eng.atlassian.net/wiki/spaces/LSH/pages/30508254316/Manifest+Defined+Package+Deployment);                                                                                     
10. Frogbot: It will scan for the vulnerable dependencies and report if any issues in the PR   [Frogbot](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30698047820/Git+Repository+scanning+with+JFRrog+Xray+for+security+vulnerabilities);                                                   
      ```
      eg.
        - name: FrogBot
          uses: jfrog/frogbot@v2.8.4
          env:
            JF_URL: ${{ secrets.JF_URL }}
            JF_ACCESS_TOKEN: ${{ secrets.JF_ACCESS_TOKEN }}
            JF_GIT_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            JF_WORKING_DIR: ./frontend
      ```
      Note:

      1. JF_WORKING_DIR: we need to explicitly mention the WORK_DIR for the scan as mentioned above or else it will scan the entire root directory.

      2. When using Frogbot scan with `changed_modules`, the bootstrap image must have both Python and the PYYAML package installed. And we need to use these env variable `JF_CHANGED_PATHS: "${{ steps.change_detection.outputs.changed_modules }}"` to scan only for changed_modules.

11. Tag: Commit the changes available in the workspace and tag the code as per the latest commit id. You have also the possibility of pushing to a tag only, by setting `push_tag_only` to `true`.

12. Reporting: Aims to send messages to a Microsoft Teams channel and/or a Slack channel to help users keep track of all the defined steps in a workflow, along with additional workflow details. A summary table will also be added to the job's summary after the execution of the job, consisting of the same details.

      ```
      - name: Reporting
        if: always()
        uses: lumada-common-services/gh-composite-actions@develop
        env:
          Slack_Token: ${{ secrets.SLACK_TOKEN }}                 # Secret Token for Slack channel
          Slack_Channel: yukon-test                               # The slack channel to receive notifications. 
          steps_json: '${{ toJson(steps) }}'
          teams_Webhook_Url: '${{ secrets.TEAMS_WEBHOOK_URL }}'   #Incoming Webhook URL for Teams channel 
          report: true
          
      ```

Sample code snippet for Calling Composite Actions:

You can call a Composite Action from a Workflow just like any other Action. 


main workflow:
```
- name: Sonarqube scan
  id: Sonarqube
  uses: lumada-common-services/gh-composite-actions@develop
  env:
    sonar_utility: sonar-scanner
    sonar_commands: '("-Dsonar.projectBaseDir=./gradle -Dsonar.projectKey=${{env.SONAR_PROJECT_KEY}} -Dsonar.host.url=${{env.SONAR_HOST_URL}} -Dsonar.token=${{env.SONAR_LOGIN}}")'

```

that correspond to in the composite action:

```
# sonar section
- name: Sonar Scan
  if: ${{ env.sonar_commands }}
  id: sonar-scan
  uses: lumada-common-services/gh-composite-actions@sonar-action
```

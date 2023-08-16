# gh-composite-actions
As part of bootstrapped [container approach](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30584472476/Implementation+Architecture+of+Containerization+Theme) we shall use Composite Actions which allows you to modularise a predefined repeated task  into a single action, combining multiple run commands into a single reusable action. However, they are different from workflow reuse, so you will need a separate repository to manage them. For easy maintenance these composite actions can be populated in an `action.yaml` in separate repo. These composite actions have to be called from the Workflow where the pipeline has to be implemented by passing the necessary variables required for the pipeline to run.

Advantages:

1. Breakdown complex workflows into simple self contained modules;

2. Create templatized actions which can be called from multiple workflows there by enhancing the reusability;

3. The descriptive nature of an `action.yml` file improves the readability of a GitHub workflow when understanding necessary inputs and outputs.


List of Composite Actions:

1. Build: Please refer to the link how we defined the composite action for [build](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30470897989/Build);
2. Unit Test: Please refer to the link how we defined the composite action for [unit tests](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30471323921/Testing);

      ```
      eg.
        - name: Unit Test Maven
          uses: lumada-common-services/gh-composite-actions@develop
          with:
            command: |
              mvn verify -B -Daudit -amd -Dmaven.test.failure.ignore=true 
          env:
            cmd_type: UNIT_TEST 
            reporter: 'java-junit'
            test_report_path: '**/target/*/*.xml'
            copy-to-target-path: './test_report'
            fail-on-error: 'false'
      ```
      Note:

      1. reporter: Supported options for the format of test results:(dart-json,dotnet-trx,flutter-json,java-junit,jest-junit,mocha-json).

      2. test_report_path: Folder path where the complete test reports are automatically generated upon the execution of test cases.

      3. copy-to-target-path: Destination folder path where the reports need to be copied from their default location.

      4. fail-on-error: It's boolean-type parameter that determines whether the workflow should be marked as failed if there are any test cases that have failed.


3. Sonarqube Scan: Please refer to the link how we defined the composite action for [sonar scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30584439068/Static+Code+Analysis+SonarQube+Scan);

4. Blackduck Scan: Please refer to the link how we defined the composite action for [blackduck scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30471291264/Software+Composition+Analysis+Blackduck);

5. OWASP Scan: Please refer the to link how we defined the composite action for [owasp scan](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30577266601/Software+Composition+Analysis+OWASP+dependency+check);

6. Publish Artifacts to Registry: Please refer the to link how we defined the composite action for [Publish Artifacts to Registry](https://hv-eng.atlassian.net/wiki/spaces/LSH/pages/30508254316/Manifest+Defined+Package+Deployment);                                                                                     
7. Frogbot: It will scan for the vulnerable dependencies and report if any issues in the PR   [Frogbot](https://hv-eng.atlassian.net/wiki/spaces/LFCP/pages/30698047820/Git+Repository+scanning+with+JFRrog+Xray+for+security+vulnerabilities);                                                   
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

8. Tag: Commit the changes available in the workspace and tag the code as per the latest commit id. You have also the possibility of pushing to a tag only, by setting `push_tag_only` to `true`.


Sample code snippet for Calling Composite Actions:

You can call a Composite Action from a Workflow just like any other Action. 


main workflow:
```
- name: Blackduck Scan
  uses: lumada-common-services/gh-composite-actions@develop
  env:  
    BlackDuck_Project_Version: "${{ env.BLACKDUCK_PROJ_VERSION }}"
    BlackDuck_Project_Name: "${{ env.BLACKDUCK_PROJ_NAME }}"
    BlackDuck_Api_Token: "${{ secrets.ORION_BLACKDUCK_TOKEN }}"
    BlackDuck_Url: "${{ env.BLACKDUCK_SERVER_URL }}"
```

that correspond to in the composite action:

```
# Blackduck section
- name: Blackduck Scan
  if: ${{ env.BlackDuck_Project_Name }}
  id: blackduck-scan
  uses: addnab/docker-run-action@v3
  with:
    image: docker.repo.orl.eng.hitachivantara.com/blackducksoftware/detect:8
    options: --entrypoint "/bin/bash" -v ${{ github.workspace }}:/workdir
    run: |
      java -jar /synopsys-detect.jar \
      --detect.source.path=${{ env.BlackDuck_Source_Path || '/workdir' }} \
      --detect.project.version.name="${{ env.BlackDuck_Project_Version }}" \
      --detect.project.name="${{ env.BlackDuck_Project_Name }}" \
      --blackduck.api.token="${{ env.BlackDuck_Api_Token }}" \
      --blackduck.url="${{ env.BlackDuck_Url }}" \
      --detect.blackduck.signature.scanner.snippet.matching="NONE" ${{ env.ADDITIONAL_ARGS }}
```

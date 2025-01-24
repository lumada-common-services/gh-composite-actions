## 2.1.7 🐝 - 2025-01-24

### What's Changed

#### 🚀 Features

- [(Pull Request 154)](https://github.com/lumada-common-services/gh-composite-actions/pull/154)
   
- …t reports checks [(Pull Request 153)](https://github.com/lumada-common-services/gh-composite-actions/pull/153)
  

## 2.1.6 🐝 - 2024-08-12

### What's Changed

#### 🐛 Bug Fixes

- …ate limit." error [(Pull Request 152)](https://github.com/lumada-common-services/gh-composite-actions/pull/152)

#### 🧰 Maintenance

- …ate limit." error [(Pull Request 152)](https://github.com/lumada-common-services/gh-composite-actions/pull/152)

## 2.1.5 🐝 - 2024-05-07

### What's Changed

#### 🚀 Features

- Updated the frogbot step from the `gh-composite-actions` to use the frogbot CLI. [(Pull Request 150)](https://github.com/lumada-common-services/gh-composite-actions/pull/150)

## 2.1.4 🐝 - 2024-04-02

### What's Changed

#### 🐛 Bug Fixes

- Fixing the GitHub workspace variable in the Git tag process. [(Pull Request 148)](https://github.com/lumada-common-services/gh-composite-actions/pull/148)

## 2.1.3 🐝 - 2024-04-02

### What's Changed

#### 🚀 Enhancement

- Create a process for building Pentaho CUST cases. Additionally, recreate an already existing tag. [(Pull Request 146)](https://github.com/lumada-common-services/gh-composite-actions/pull/146)

## 2.1.2 🐝 - 2024-04-02

### What's Changed

#### 🚀 Enhancement

- Updated the Slack message to make it look simpler.  [(Pull Request 147)](https://github.com/lumada-common-services/gh-composite-actions/pull/147)

## 2.1.1 🐝 - 2024-03-11

### What's Changed

#### 🐛 Bug Fixes

- Fixed the variable name value for the test reporter, as it was showing an incorrect variable name. It should show the variable name in the warning message as `unit_test_reporter`, not `unit_reporter`. [(Pull Request 144)](https://github.com/lumada-common-services/gh-composite-actions/pull/144)

## 2.1.0 🐝 - 2024-03-04

### What's Changed

#### 🚀 Features

- Update the Citadel scan script to fetch plugin names from the manifest file and determine the artifact zip URL for those plugins. The script will only update the values if the Citadel config YAML file contains the specific placeholder mentioned below for each particular key. For more information, refer to [this.](https://hv-eng.atlassian.net/wiki/spaces/MCI/pages/30890459190/Honeycomb+and+Citadel+integration#Updating-values-in-the-config-file)   [(Pull Request 143)](https://github.com/lumada-common-services/gh-composite-actions/pull/143)

## 2.0.1 🐝 - 2024-02-28

### What's Changed

#### 🐛 Bug Fixes

- Updated hv-actions/slack-action to use `stable` tag. [(Pull Request 142)](https://github.com/lumada-common-services/gh-composite-actions/pull/142)

## 2.0.0 🐝 - 2024-02-27

### What's Changed

#### 🚀 Features

- Updated the composite action to track steps (BUILD, UNIT_TEST, INTEGRATION_TEST, TEST, DEPLOY) using comma-separated values. Now, we can track one or multiple cmd_type in a single step. For e.g., `cmd_type: BUILD,UNIT_TEST,DEPLOY`.
- Added the new cmd_type 'TEST' to the composite action for tracking any generic test step. Also added the new 'TEST_DESC' environment variable to include additional descriptions along with the 'Test' keyword in the reporting. This generic test step will only be tracked if it is run. [(Pull Request 141)](https://github.com/lumada-common-services/gh-composite-actions/pull/141)

## 1.9.0 🐝 - 2024-01-30

### What's Changed

#### 🚀 Features

- Updated the composite action by adding deployment step tracking to reporting. Define the DEPLOY_DESC environment variable to include additional descriptions along with the "Deploy" keyword in the reporting. [(Pull Request 137)](https://github.com/lumada-common-services/gh-composite-actions/pull/137)

## 1.8.1 🐝 - 2023-12-20

### What's Changed

#### 🚀 Enhancement

- Replacing all references pointing to Orlando's Artifactory with one.hitachivantara.com. [(Pull Request 135)](https://github.com/lumada-common-services/gh-composite-actions/pull/135)

## 1.8.0 🐝 - 2023-11-30

### What's Changed

#### 🚀 Features

- Added the INTEGRATION_TEST command type to the composite action for tracking in the reporting step. This integration step will only be tracked if it is run. [(Pull Request 133)](https://github.com/lumada-common-services/gh-composite-actions/pull/133)

## 1.7.5 🐝 - 2023-11-28

### What's Changed

#### 🐛 Bug Fixes

- Update the conditions to display the correct summary link and symbol when we are passing `fail-on-error = true`. [(Pull Request 131)](https://github.com/lumada-common-services/gh-composite-actions/pull/131)

## 1.7.4 🐝 - 2023-11-27

### What's Changed

#### 🐛 Bug Fixes

- Update the composite action to display a 'boom 💥' symbol in the unit test step if the unit test command is successful but there are failed test cases [(Pull Request 129)](https://github.com/lumada-common-services/gh-composite-actions/pull/129)

## 1.7.3 🐝 - 2023-11-22

### What's Changed

#### 🐛 Bug Fixes

- Added some extra validation, so it will not fail the UNIT_TEST step even if it does not find any reports; instead, it will set an error message. [(Pull Request 127)](https://github.com/lumada-common-services/gh-composite-actions/pull/127)

## 1.7.2 🐝 - 2023-11-21

### What's Changed

#### 🧰 Maintenance

- Updated Synopsys Detect scanner to v9 to support npm 9 [(Pull Request 125)](https://github.com/lumada-common-services/gh-composite-actions/pull/125)

## 1.7.1 🐝 - 2023-11-03

### What's Changed

#### 🐛 Bug Fixes

- Include Citadel step tracking in GitHub summaries, Slack, and Teams. Additionally, based on team discussions, remove the Blackduck step from the merge workflow tracking. [(Pull Request 118)](https://github.com/lumada-common-services/gh-composite-actions/pull/118)
  
- Fixed Issue You are not currently on a branch. [(Pull Request 117)](https://github.com/lumada-common-services/gh-composite-actions/pull/117)
  

## 1.7.0 🐝 - 2023-10-27

### What's Changed

#### 🚀 Features

- Enhanced citadel integration step. [(Pull Request 111)](https://github.com/lumada-common-services/gh-composite-actions/pull/111)

#### 🐛 Bug Fixes

- Enhanced branch protection in the gh-composite-action repository for improved release automation. [(Pull Request 114)](https://github.com/lumada-common-services/gh-composite-actions/pull/114)

## 1.6.0 🐝 - 2023-10-10

### What's Changed

- The Release Automation Process is designed to streamline the release management workflow for our product. It automates various tasks related to labeling PRs, generating release notes, updating documentation, and notifying relevant stakeholders. [(Pull Request 109)](https://github.com/lumada-common-services/gh-composite-actions/pull/109)
  
- Added  Integration test step Documentation to Readme file. [(Pull Request 101)](https://github.com/lumada-common-services/gh-composite-actions/pull/101)
  
- Added note about GITHUB_TOKEN parameter in Unit Test step. The unit test step requires the GitHub App installation access token (GITHUB_TOKEN) to be passed in order to function correctly. [(Pull Request 107)](https://github.com/lumada-common-services/gh-composite-actions/pull/107)
  

#### 🐛 Bug Fixes

- Hyperlink for the unit test is not generating for the pull request workflow. [(Pull Request 110)](https://github.com/lumada-common-services/gh-composite-actions/pull/110)

## 1.5.0 🐝 - 2023-09-27

### What's Changed

- Added Teams Notify action to send messages to a Microsoft Teams channel to help users keep track of all the defined steps in a workflow, along with additional workflow details. Additionally, 'Blackduck Fix' adding an additional parameter `detect.accuracy.required=NONE`. [(Pull Request 104)](https://github.com/lumada-common-services/gh-composite-actions/pull/104)

## 1.4.1 🐝 - 2023-08-29

### What's Changed

- The "Result" column has been renamed to "Status," and a new "Note" section has been introduced in the summary for each icon description. Also added Citadel json triggering to the composite workflow. [(Pull Request 100)](https://github.com/lumada-common-services/gh-composite-actions/pull/100)

## 1.4.0 🐝 - 2023-08-17

### What's Changed

- Updated a unit test report generation step that displays the test results on the Github summary and sends notifications on Slack.
  Also, fix issues for incorrect Sonar summary links when manually triggered and wrong summary data when pull_request_target is the event that triggered the workflow. [(Pull Request 95)](https://github.com/lumada-common-services/gh-composite-actions/pull/95)

## 1.3.1 🐝 - 2023-07-31

### What's Changed

- Updated the Slack notifications and GitHub summary for the manual trigger, and fixed the commit message part in Slack messages to handle multi-line commits correctly. [(Pull Request 90)](https://github.com/lumada-common-services/gh-composite-actions/pull/90)

## 1.3.0 🐝 - 2023-07-20

### What's Changed

- Add kind integration code to gh-composite-action. [(Pull Request 82)](https://github.com/lumada-common-services/gh-composite-actions/pull/82)

## 1.0.1 🐝 - 2023-03-16

### What's Changed

- lumada-common-services/gh-composite-actions@1.0.0 fails… by @cardosov in [(Pull Request 52)](https://github.com/lumada-common-services/gh-composite-actions/pull/52)

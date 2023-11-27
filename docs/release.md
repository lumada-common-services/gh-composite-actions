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

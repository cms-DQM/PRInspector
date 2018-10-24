# A tool to review PRs in CMSSW DQM

CMSSW DQM pull request review tool that aggregates and displays information about pull requests from Github, TagCollector and other sources.

## Before running

Before running there should be a `private/` folder inside `src/` containing these files:
* `private/cert.key` - GRID certificate key file
* `private/cert.pem` - GRID certificate file
* `private/github_oauth_data.txt` - Github OAuth credentials. Second line should contain client_id and third line should contain client_secret. First line is just informational message that will be ignored.

## How to run

Run this by executing `run.sh`. 

`-r` option will reload the web app if it crashes each time any file is updated and saved. `fswatch` is used to observe file changes. `-d` will run the web app in debug mode. **Both options should be used only in development.**

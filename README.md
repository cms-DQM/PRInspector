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

## Package instalation

Packages listed in `requirements.txt` have to be installed like this:

``` bash
python3 -m pip install -r requirements.txt -t .python_packages
```

## Where is this service hosted?

The service is hosted on an OpenStack machine called `prinspector`. To get to this machine you have to execute this from `lxplus`: `ssh prinspector`.

Source code for the service is located here: `/srv/PRInspector/`.

## How to update

When the code in this repository changes and you want the changes to be reflected in a running service, execute the following instructions:

```bash
ssh prinspector
cd /srv/PRInspector/
./update.sh
```

If the update has some unwanted behaviour, you can rollback to the latest working version like so: `./rollback.sh`

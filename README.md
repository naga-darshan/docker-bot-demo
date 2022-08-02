# DockerBot Automation
High-level step
  1. Complete `PRE-REQUISITE 1` and `PRE-REQUISITE 2`
  2. Confirm the update of `../app/auth/info.json`; details below
  3. RUN the project

<br>
<h3><b>PRE-REQUISITE 1: </b>Setting up your <b>local dev</b> environment</h3>

- Clone this repo onto your local using the following command
  `git clone https://github.com/NagasCodeHub/DockerBotTest.git`
- Open the project in any python compatible IDE you prefer like `PyCharm` or `VS Code`
- Install python 3.7 by from [here](https://www.python.org/downloads/) | [Additional resource for help with setup](https://phoenixnap.com/kb/how-to-install-python-3-windows) 


<h3><b>PRE-REQUISITE 2: </b>Create & setup new Spot Exchange account</h3>
- Navigate to the website and create/sign-up for a new account
- Activate and Login to your account
<br>


<h4>Setup 2FA for Sign-in section, to setup 2FA using `2FA app` </h4>
  * Once logged in, navigate to Security settings using the drop down on top right corner (click on your username)
  * Select 2FA from the option
  * Under Sign-in section click on `Activate now`
  * On the pop-up click `View Setup Key`
  * Copy the <sign_in_setup_key> into clipboard or a local notepad
  * In terminal from <b>PREREQUISITE 1:</b> navigate to `..\app\auth\`
  * run `python .\botAuthenticator.py -s <sign_in_setup_key>`
  * copy the 6-digit OTP from terminal and paste it in the browser pop-up for 2FA setup under `Enter code from 2FA app`
  * Click confirm
  * Navigate to `..\app\auth\info.json` and paste the <sign_in_setup_key> as value for `SETUP_KEY` variable in the json
    `{'SETUP_KEY' : '<sign_in_setup_key>'}`
  * You can consider to erase the notepad data from the earlier step


<h4>Setup `TRADING_2FA` for static 2FA Authentication</h4>
  * Under Trading 2FA section click on toggle button to enable it
  * On the pop-up select `Password` option for static 2FA
  * Enter the trading password you wish to keep and Confirm to finsh the static 2FA
  * In terminal from <b>PREREQUISITE 1:</b> navigate to `..\app\auth\`
  * run ` python .\requestHandler.py -e <trading_password>`
  * copy the encoded code from terminal and update `info.json`
  * Navigate to `..\app\auth\info.json` and update the <encode_code> as value for `TRADING_2FA` variable in the json; 
    `{'TRADING_2FA' : '<encoded_2fa_code>'}`


<h4>Setup `API_KEY` and `API_SECRET`for project to work with APIs</h4>
  * Select `API` from the tabs on the exchange security settings screen
  * Click on `ADD KEY`
  * Under Key Permissions check `Query open orders & trades` option
  * Copy the `API Key` and `Private Key` into clipboard or a local notepad
  * Navigate to `..\app\auth\info.json` and update
  * Navigate to `..\app\auth\info.json` and upate the <api_key> as value for `API_KEY` and <private_key> as a value for `API_SECRET` variable in the json; 
    `{'API_KEY' : '<api_key>', 'API_SECRET' : '<private_key>'}`
  * Click Save
  * You can now consider to erase the notepad data from the earlier step

<br>

# RUN the project
To run this project, do the following steps:
- open terminal and navigate root directory of the project `..\DockerBot>`
- Install `virtualenv` by running these commands in terminal:
   * `pip install virtualenv`
   * `python -m virtualenv venv`
   * <b>WINDOWS `.\venv\Scripts\activate`  MAC/UBUNTU `.venv\bin\activate`
   * Virtual (vnenv) should be activated
   * RUN `pip install -r requirements.txt`
   * Navigate into app folder `cd app`
   * RUN `pytest --html=report_file_name.html --capture=tee-sys`
- Locate the new report file in project `..\app\tests\dockerBotTestReport.html` and open this file in a browser to see the results

# Run using Dockerized Version
- Download `Docker Desktop` compatible with your machine; [reference](https://www.docker.com/get-started/)
- Follow installation guide to complete Docker Setup [WINDOWS](https://docs.docker.com/desktop/install/windows-install/) | [MAC](https://docs.docker.com/desktop/install/mac-install/)
- Verify installation by `docker --version` in terminal
- Create an account on login into to local `Docker Desktop`
- Do not close/terminate the Docker Desktop application
- Pull the latest docker image to current project `docker pull nagadarshan/docker-bot-demo`
- Build the image into a container by `docker build -t nagadarshan/docker-bot-demo .`
- Run the container image ` docker run --name=demoCont -it nagadarshan/docker-bot-demo:latest /bin/bash` this open the terminal of the new container
- Once the docker container terminal is open, navigate to app folder
- ****COMPLETE*** the steps for `PRE-REQUISITE 2` but update the values of the file `info.json` inside the docker container
  - if editing (vim) is disable then to enable editing in bash of container, run the following
    
    `apt-get update`
  
    `apt-get install vim`
  
    `vim /dockerbot/auth/info.json`
    
    Insert the empty params with valid values `"SETUP_KEY" "API_KEY" "API_SECRET" "TRADING_2FA"` save and exit
- from `../app` RUN command `pytest --html=report_file_name.html --capture=tee-sys`
- Locate the new report file in project `..\app\tests\report_file_name.html` and open this file in a browser to see the results


<h3>Note:</h3>
While writing test steps for validation of response with step params:
The function accepts a `list` of `{key:value}` pairs to validate,
this can be scaled to any number of body param based on the requirement

Current default setup: The Last Step in validate open order will fail since there will be a new account, it `would need atleast one pending OPEN order` for the test case
<br>

-     @then : Response "header" has "[{'Content-Type':'application/json'}]" //EXAMPLE
      listOfHeadersToVerify =[{key: expectedValue},{key: expectedValue},{key: expectedValue}....]
      
-      @then : Response "body" has "[{'result.unixtime':'non-zero-number'}]" //EXAMPLE
       listOfBodyParamsToVerify = [{path.to.node: expectedValue},{path.to.node: expectedValue},{path.to.node: expectedValue}....]
                                  path to a node to be verified is given in dot seperator format

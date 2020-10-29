# Dumb Remote Execution Agent

DREA(Dumb Remote Execution Agent) is little python script that I made for doing some remote process execution (Minecraft server to be specific) on a remote server. I am open sourcing DREA mainly to preserve this miserable piece of codes, but hey, if this fits your usage, you might get some use out of it. right?

It can run or stop an application via WebSocket. That's all.

There is no client provided; you must create one by yourself in order to use DREA.

## No security at all!

Security was NOT considered at all while making DREA, so it is NOT RECOMMENDED to use DREA on some big important server or something. Use DREA at your own risk.

## How to use

### 1. Setting up DREA

To setup DREA, all you need to do is change "Change here" section accordingly. Default values are:

```python
pwd = 'password'
procpath = ['/path/to/process', '--arguments']
proccwd = None
port = 20003
```

```pwd``` is password that is required to control DREA. it is stored as plaintext(remember: no security at all), so do not use your personal favorite passwords here. if set as ```None```, password check will be skipped.

```procpath``` is the path of the application that DREA will run. must be an absolute path. arguments should be placed as additional elements of the array.

```proccwd``` is the working directory of the application. can be ```None```.

```port``` is where DREA should listen for connections. default is 20003.

After changing all three variables, you can simply run the script on remote server to start DREA.

### 2. Controlling DREA

Client can connect to DREA by connecting to specified port using WebSocket. (e.g. ```ws://example.com:20003```)

If password is set, DREA will send ```pwd```, asking for password. sending wrong password will make DREA repeat ```pwd```.

If password is not set or correct password has been sent, DREA will send ```cmd```, asking for your command. There are four commands available:

- ```stat``` asks whether the process is running or not. DREA will send ```yes``` if process is running, ```no``` else.

- ```run``` starts the process. DREA will send ```ok``` if process has started successfully, ```ar``` if process is already running.

- ```stop``` stops the process. DREA will send ```ok``` if process has stopped successfully(this may take some time), ```nr``` if process is not running.

- ```bye``` closes the connection.

### 3. An other thing

Currently there is no proper way to stop DREA. You can always force close it or whatever.

# License

DREA is distributed under the terms of the Do What The Fuck You Want To Public License, Version 2.
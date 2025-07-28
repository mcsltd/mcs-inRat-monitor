# mcs-inRat-monitor
Show signal from inRat monitor

## Functional

`InRat monitor` supports the following functions\:
2. Showing real-time signal from InRat
2. Save signal from InRat in two data format: edf, wfdb


## Running

You can launch the application in two ways:

### First way (easy)

0. Download file in `InRat monitor.exe`
1. Create .env file in dir when you start application and fill in the fields
```.env
BLE_KEY=...
DATA_PATH=...
```

`BLE_KEY` - requested from the company MCS ltd.

`DATA_PATH` - file save location, you can specify `.\`

2. Double-click `InRat monitor.exe`

### Second way (for developers)
1. Download files from repo
2. Install libs in requirements.txt
2. Run code in your idle (see Dependencies)

## Dependencies

### Requirements
* filled .env file
* Python 3.13

### System requirements
* OS: Windows 10

### Requirements for libraries
You can find other requirements for the library in the [requirements.txt](requirements.txt).


## Release History
### v0.0.1
* First release, add ui and other files


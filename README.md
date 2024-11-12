# Script to interact with Cisco IOS XE device using RESTCONF API

The provided code is a Python script designed to interact with a Cisco IOS XE device using RESTCONF API.

The script defines several functions to perform various operations on the device, such as retrieving and displaying interfaces, editing an interface, changing the hostname, changing the IP domain, and showing the device configuration.

### How to run the project:

1. Create a virtual environment inside the root folder:

```
python3 -m venv .venv
```

2. Activate the virtual environment:

```
source .venv/bin/activate
```

3. Install required dependencies:

```
pip install -r requirements.txt
```

4. Run the main script:

```
python src/main.py
```

5. Deactivate virtual environment:

```
deactivate
```

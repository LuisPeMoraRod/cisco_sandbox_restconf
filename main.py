"""
The provided code is a Python script designed to interact with a Cisco IOS XE device using RESTCONF API. 

The script defines several functions to perform various operations on the device, such as retrieving and displaying interfaces, editing an interface, changing the hostname, changing the IP domain, and showing the device configuration.
"""

import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth

# Define Sandbox credentials
HOST = "devnetsandboxiosxe.cisco.com"
USERNAME = "admin"
PASSWORD = "C1sco12345"


BASE_URL = f"https://{HOST}/restconf/data"

# Headers required for RESTCONF requests
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}

# Status codes
STATUS_CODES = {
    "OK": 200,
    "NO_CONTENT": 204,
}


requests.packages.urllib3.disable_warnings()


def show_interfaces():
    """
    Method to retrieve and print the interfaces of the device
    """
    url = f"{BASE_URL}/ietf-interfaces:interfaces"  # URL to retrieve the interfaces
    response = requests.get(
        url, headers=headers, auth=(USERNAME, PASSWORD), verify=False
    )
    if (
        response.status_code == STATUS_CODES["OK"]
    ):  # Check if the request was successful
        interfaces = response.json()
        print(json.dumps(interfaces, indent=4))
    else:
        print(f"Error retrieving interfaces: {response.status_code}")
        print(response.text)


def edit_interface():
    """
    Method to edit an interface on the device.

    This method retrieves the current interfaces from the device, displays them in a tabular format, and prompts the user to input the name of the interface to edit along with the new description, IP address, and netmask.

    It then sends a PUT request to update the interface with the provided
    details.
    """

    url = f"{BASE_URL}/ietf-interfaces:interfaces"  # URL to retrieve the interfaces
    response = requests.get(
        url, headers=headers, auth=(USERNAME, PASSWORD), verify=False
    )

    interfaces = response.json()  # Parse the response as JSON
    interfaces = interfaces["ietf-interfaces:interfaces"][
        "interface"
    ]  # Extract the interfaces

    rows = []
    for interface in interfaces:
        row = {
            "Name": interface["name"],
            "Description": interface.get("description", ""),
            "Type": interface["type"],
            "Enabled": interface["enabled"],
            "IPv4 Address": interface.get("ietf-ip:ipv4", {})
            .get("address", [{}])[0]
            .get("ip", ""),
            "IPv4 Netmask": interface.get("ietf-ip:ipv4", {})
            .get("address", [{}])[0]
            .get("netmask", ""),
        }
        rows.append(row)

    df = pd.DataFrame(
        rows
    )  # Create dataframe from the list of interfaces to display in a tabular format

    show_interfaces(df)  # Show table of interfaces

    interface_name, description, ip_address, netmask = (
        get_user_input()
    )  # Get user input for the interface details

    payload = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": description,
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": ip_address, "netmask": netmask}]},
        }
    }

    url = f"{BASE_URL}/ietf-interfaces:interfaces/interface={interface_name}"  # URL to edit the interface
    response = requests.put(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        verify=False,
    )
    if response.status_code == STATUS_CODES["NO_CONTENT"]:
        print("The interface has been successfully edited.")
    else:
        print(f"Error editing the interface: {response.status_code}")
        print(response.text)


def show_interfaces(df: pd.DataFrame):

    print("\n\t\t\t\t\t\tAvailable Interfaces\n")
    print(df)
    print("\n")


def get_user_input():
    interface_name = input("Enter the name of the interface (e.g., GigabitEthernet1): ")
    description = input("Enter the new description of the interface: ")
    ip_address = input("Enter the new IP address (e.g., 192.0.2.1): ")
    netmask = input("Enter the new netmask (e.g., 255.255.255.0):")

    return interface_name, description, ip_address, netmask


def change_hostname():
    """
    Method to change the hostname of the device
    """
    hostname = input("Enter the new hostname: ")

    payload = {"hostname": hostname}

    url = f"{BASE_URL}/Cisco-IOS-XE-native:native/hostname"
    response = requests.put(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=(USERNAME, PASSWORD),
        verify=False,
    )
    if response.status_code == STATUS_CODES["NO_CONTENT"]:
        print("Hostname changed successfully.")
    else:
        print(f"Error updtading hostname: {response.status_code}")
        print(response.text)


def change_ip_domain():
    """
    Method to change the IP domain of the device
    """
    domain = input("Enter the new IP domain: ")

    url = f"https://{HOST}/restconf/data/Cisco-IOS-XE-native:native/ip/domain"

    payload = {"domain": {"name": domain}}

    response = requests.put(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=(USERNAME, PASSWORD),
        verify=False,
    )
    if response.status_code == 204:
        print("IP domain changed successfully.")
    else:
        print(f"Error updating IP domain: {response.status_code}")
        print(response.text)


def show_config():
    """
    Method to retrieve and print the configuration of the device
    """

    # URL to issue GET request
    url = f"https://{HOST}/restconf/data/Cisco-IOS-XE-native:native"

    response = requests.get(
        url, auth=(USERNAME, PASSWORD), headers=headers, verify=False
    )

    if response.status_code == STATUS_CODES["OK"]:
        print(response.text)
    else:
        print(f"Error retrieving configuration: {response.status_code}")
        print(response.text)


def menu():
    exit = False
    while not exit:
        print("\n--- Menu ---")
        print("1. Show device configuration")
        print("2. Show interfaces")
        print("3. Edit an interface")
        print("4. Change hostname")
        print("5. Change ip domain")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            show_config()
        elif choice == "2":
            show_interfaces()
        elif choice == "3":
            edit_interface()
        elif choice == "4":
            change_hostname()
        elif choice == "5":
            change_ip_domain()
        elif choice == "6":
            exit = True
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()

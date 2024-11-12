import os
import socket
import platform
import pywifi
from pywifi import const, Profile
import time


def get_hostname():
    """Retrieve the current hostname of the device."""
    return socket.gethostname()


def set_hostname(new_hostname):
    """Set a new hostname for the device."""
    try:
        os.system(f"sudo hostnamectl set-hostname {new_hostname}")
        print(f"Hostname changed to {new_hostname}. Please restart for changes to take effect.")
    except Exception as e:
        print(f"Failed to change hostname: {e}")


def get_ip_address():
    """Retrieve the IP address of the device."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f'Unable to get IP address:{e}')
        return "Unavailable"

    return socket.gethostbyname(hostname)


def connect_to_wifi(ssid, password):
    """Connect to a Wi-Fi network with the specified SSID and password."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    if iface.status() == const.IFACE_DISCONNECTED:
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()  # Clean existing profiles
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)
        print(f"Connecting to {ssid}...")

        # Wait for connection
        for _ in range(10):
            if iface.status() == const.IFACE_CONNECTED:
                print("Connected to Wi-Fi successfully!")
                return True
            time.sleep(1)
        print("Failed to connect to Wi-Fi.")
        return False
    else:
        print("Interface is already connected.")
        return True


# def get_unique_networks():
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0]
#     iface.scan()
#     scan_results = iface.scan_results()

#     # Use a dictionary to filter out duplicates
#     networks = {}
#     ssidList=[]
#     for network in scan_results:
#         networks[network.ssid] = network


#     # Convert dictionary back to a list
#     unique_networks = list(networks.values())

#     # Sort the list by signal strength (optional)
#     unique_networks.sort(key=lambda x: x.signal, reverse=True)

#     return unique_networks

# def get_ssid_list(networks):
#     ssid_list = [network.ssid for network in networks]
#     return ssid_list


def get_unique_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    scan_results = iface.scan_results()

    # Use a set to filter out duplicates
    ssids = set()
    for network in scan_results:
        ssids.add(network.ssid)

    return list(ssids)


def get_ssid_list(networks):
    ssid_list = [network for network in networks]
    return ssid_list


def print_networks(networks):
    for network in networks:
        print(f"SSID: {network.ssid}, Signal: {network.signal}")


# Usage examples
if __name__ == "__main__":
    # Get current hostname and IP
    print("Current hostname:", get_hostname())
    print("Current IP address:", get_ip_address())
    networks = get_unique_networks()
    # print_networks(networks)
    # set_hostname('Christopher2')
    # connect_to_wifi('iot-ict-lab24g','iot#labclass')

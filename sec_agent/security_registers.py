import os
import json
import time
from typing import Annotated
from autogen import register_function
import requests
import shodan



def register_functions(assistant, user_proxy):
    '''
    Register function for Autogen
    '''

    register_function(
        vt_get_hash,
        caller = assistant,
        executor = user_proxy,
        description = "given a hash, return the likleyhood the information \
            and likleyhood of it being malicious"
    )

    register_function(
        circl_get_hash,
        caller = assistant,
        executor = user_proxy,
        description = "given a hash, return the data available from circl.lu"
    )

    register_function(
        type_of_hash,
        caller = assistant,
        executor = user_proxy,
        description = "given a hash, return the hash type (sha1, sha256, or md5)"
    )

    register_function(
        shodan_ip_lookup,
        caller = assistant,
        executor = user_proxy,
        description = "given an IP Address, return the details of the IP Address from Shodan.io"
    )

    register_function(
        urlscan_url_lookup,
        caller = assistant,
        executor = user_proxy,
        description = "given a URL or domain, return the details of the analysis done by URLScan.io"
    )

    register_function(
        ipapi,
        caller = assistant,
        executor = user_proxy,
        description = "given an IP Address, return the details of the IP Address from ipapi"
    )

    register_function(
        abuse_ip,
        caller = assistant,
        executor = user_proxy,
        description = "given an IP Address, return the details of the IP Address from AbuseIPDB, \
            a higher abuseConfidenceScore out of 100 is malcious \
                although a higher number of abuse reports can still be considered malicous"
    )


def vt_get_hash(hashn: Annotated[str, "Hash Value for checking the hash information"]) -> json:
    '''
    Function call to get hash information from Virustotal to use in autogen AI
    '''

    hash_id = hashn
    headers = {"accept": "application/json",
               "x-apikey": os.environ.get("VT_API_KEY")
    }
    r = requests.get(f"https://www.virustotal.com/api/v3/files/{hash_id}",
                     headers=headers, timeout=600)
    return r.json()

def type_of_hash(hashn: Annotated[str, "Get the hash type (sha1, sha256, md5) from hash value"]) -> str:
    '''
    get hash type based on length of hash
    '''

    if len(hashn) == 64:
        return "sha256"
    elif len(hashn) == 40:
        return "sha1"
    elif len(hashn) == 32:
        return "md5"
    return "not a valid hash, TERMINATE"

def circl_get_hash(hashn: Annotated[str, "Hash Value for checking the \
                    hash information from circl.lu"],
                   hash_type: Annotated[str, "Type (valid: sha256, sha1, md5) \
                    of the hash from the hash value"]) -> json:
    '''
    Function call to get hash information from Virustotal to use in autogen AI
    '''

    hash_id = hashn
    headers = {"accept": "application/json"}
    r = requests.get(f"https://hashlookup.circl.lu/lookup/{hash_type}/{hash_id}",
                     headers=headers, timeout=600)
    return r.json()

def shodan_ip_lookup(ipaddr: Annotated[str, "IP Address for searching \
                                       the Shodan database"]) -> json:
    '''
    Using the Shodan API pull back information about a specific IP Address. 
    '''

    shodan_api = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))
    info = shodan_api.host(ipaddr)

    if info['data']:
        return info['data']
    else:
        return "No data found, possible API issue."

def urlscan_url_lookup(url: Annotated[str, "URL or domain to search in URLScan"]) -> json:
    '''
    Used to lookup a URL in URLScan.io
    '''
    headers = {'API-Key':os.environ.get("URLSCAN_API_KEY"),'Content-Type':'application/json'}
    data = {"url": f"{url}", "visibility": "public"}
    r = requests.post('https://urlscan.io/api/v1/scan/',headers=headers,
                    data=json.dumps(data), timeout=600)
    if r.json()['message'] == "Submission successful":
        time.sleep(10)

        while True:
            get_scan = requests.get(f"https://urlscan.io/api/v1/result/{r.json()['uuid']}/",
                                    headers=headers, timeout=60)

            if get_scan.status_code == 200:
                data = []
                data.append(get_scan.json()['lists'])
                data.append(get_scan.json()['verdicts'])
                return data
            elif get_scan.status_code == 404:
                time.sleep(2)
            else:
                return "Status code other than 200 or 404, \
                    which indicates there is an issue with the API"

def ipapi(ipaddr: Annotated[str, "IP Address for searching the IPAPI"]) -> json:
    '''
    Using the IPAPI pull back information about a specific IP Address. 
    '''

    ipapi_response = requests.get(f"https://ipapi.co/{ipaddr}/json/", timeout=600)

    if ipapi_response.json():
        return ipapi_response.json()
    return "No data found, possible API issue."

def abuse_ip(ipaddr: Annotated[str, "IP Address for searching the AbuseIPDB, \
                    a higher abuseConfidenceScore out of 100 is malcious, \
                    although a higher number of abuse reports can still be considered malicous"]):
    '''
    Using the AbuseIPDB pull back information about a specific IP Address.
    '''
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': f'{ipaddr}',
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': f'{os.environ.get("ABUSEIPDB_API_KEY")}'
    }

    response = requests.get(url=url, headers=headers, params=querystring, timeout=600)

    if response:
        return response.json()
    return "No Data Available for AbuseIPDB"

if __name__ == "__main__":
    pass

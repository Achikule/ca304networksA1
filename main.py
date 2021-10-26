
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
# BaseModel helps to consolidate the expected JSON structure

# Description for SwaggerUI
description = """
This script requires the following modules to run: Pydantic, typing and FastAPI
"""
# Tag metadata for SwaggerUI
tags_metadata = [
    {
        "name": "ipcalc",
        "description": """This endpoint determines the class of an IP address passed to it and also returns the
                    number of hosts, networks and first and last addresses of that class.It accepts a single IP 
                    address as input and returns the class corresponding to it. To determine the class, 
                    the function finds the prefix and converts it to binary. The binary prefix is then matched 
                    with the prefix that corresponds to the correct network class (as per the lecture notes).
                    Example input: 
                    {
                    "address":"136.206.18.7"
                    }
                    Output: {"class": "B","num_networks": 16384,"num_hosts": 65536,"first_address": 
                    "128.0.0.0","last_address": "191.255.255.255"}""",
    },
    {
        "name": "subnet",
        "description": """This endpoint subnets a given IP address using a given subnet mask and returns the
        cidr, number of subnets, number of hosts per subnet, valid subnets, broadcast addresses, first addresses 
        and last addresses. The cidr is determined by converting the subnet mask to binary and summing up the'1's 
        (slide 26). The number of subnets is given by 2 ^ (cidr - x) where (cidr - x) is the number of subnet bits. 
        The value of x depends on the address class. The number of hosts per subnet is given by 2 ^ (x - num of subnet
         bits) - 2, where (x - num of subnet bits) is the number of unmasked bits. 2 is subtracted for the subnet &
         broadcast address. The various types of addresses are determined by a secondary function; 
         find_subnetworks(3_args). Essentially, it uses parameters like the address class, subnet length, blocksize,
         and original address length to determine which part of the IP address the subnet mask iterates on. The 
         resulting addresses are all passed as values to the appropriate dictionary key and once complete, the 
         dictionary is returned as output. Example Input {"address": "192.168.10.0","mask": "255.255.255.192"} Output: 
         {
          "address_cidr": "192.168.10.0/26",
          "num_subnets": 4,
          "addressable_hosts_per_subnet": 62,
          "valid_subnets": [
            "192.168.10.0",
            "192.168.10.64",
            "192.168.10.128",
            "192.168.10.192"
          ],
          "broadcast_addresses": [
            "192.168.10.63",
            "192.168.10.127",
            "192.168.10.191",
            "192.168.10.255"
          ],
          "first_addresses": [
            "192.168.10.1",
            "192.168.10.65",
            "192.168.10.129",
            "192.168.10.193"
          ],
          "last_addresses": [
            "192.168.10.62",
            "192.168.10.126",
            "192.168.10.190",
            "192.168.10.254"
          ]
        }
        """


    },
    {
        "name": "supernet",
        "description": """This endpoint supernets a given list of contiguous (slide 31) IP addresses. The first 
        (smallest) and last (largest) addresses are taken out, converted to binary format and each bit is compared
        to find the number of common pairs of bits. The number of matching pairs is the cidr and will be the 
        number of bits in the network prefix. The network mask in binary form is given by a list of '1s' with the length
        of cidr plus padding as required. This is converted to decimal to give the final subnet mask. Example input:
        {
        "addresses":["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"]
        }
        Output:
        {
        "address": "205.100.0.0/22",
        "mask": "255.255.252.0"
        }""",
    },
]

app = FastAPI(title="Alen Joy CA304 Assessment 1",
              description=description,
              openapi_tags=tags_metadata)

# Since every class has a determined set of properties, they can be defined in dicts here
classA = {"class": "A",
          "num_networks": 126,
          "num_hosts": 16777214,
          "first_address": "0.0.0.0",
          "last_address": "127.255.255.255"
          }

classB = {"class": "B",
          "num_networks": 16384,
          "num_hosts": 65536,
          "first_address": "128.0.0.0",
          "last_address": "191.255.255.255"
          }

classC = {"class": "C",
          "num_networks": 2097152,
          "num_hosts": 256,
          "first_address": "192.0.0.0",
          "last_address": "223.255.255.255"
          }

classD = {"class": "D",
          "num_networks": "N/A",
          "num_hosts": "N/A",
          "first_address": "244.0.0.0",
          "last_address": "239.255.255.255"
          }

classE = {"class": "E",
          "num_networks": "N/A",
          "num_hosts": "N/A",
          "first_address": "240.0.0.0",
          "last_address": "255.255.255.255"
          }

# Dict defining the basic structure for returning subnet properties
subnet_props = {"address_cidr": "",
                "num_subnets": "",
                "addressable_hosts_per_subnet": "",
                "valid_subnets": [],
                "broadcast_addresses": [],
                "first_addresses": [],
                "last_addresses": []
                }
# Dict for defining the basic structure for returning supernet properties
supernet_props = {"address": "",
                  "mask": ""
                  }


# Expected JSON input structure for Q1 & 2
class Input(BaseModel):
    address: str
    mask: Optional[str]


# Expected JSON input structure for Q3
class SuperNet(BaseModel):
    addresses: list


# Identifying the network bits and converting to binary
# Searches for a match to determine network class
def class_calc(ip):
    netbit = int(ip.address.split(".")[0])
    binary = str(f"{netbit:08b}")

    if binary[0] == "0":
        return classA
    elif binary[:2] == "10":
        return classB
    elif binary[0:3] == "110":
        return classC
    elif binary[0:4] == "1110":
        return classD
    else:
        return classE


# Initialises required lists
# copy_sub = list of non 0 subnet mask parts used to determine what part of IP to change
# z = to determine part of original IP to leave unchanged
# b = mapping unchanged parts
# index num = length of submask (starting point of where to change original IP
# len(z) = helps identify address class, determining from where submask acts on
# Values are assigned to keys in the dict
def find_subnetworks(a_split, s_split_int, address_class):
    copy_sub_split_int = s_split_int.copy()
    broadcast_addresses = []
    first_addresses = []
    last_addresses = []
    valid_subnets = []

    copy_sub = [i for i in copy_sub_split_int if i > 0]
    index_num = len(copy_sub) - 1

    if address_class == "A":
        z = [a_split[0]]
        z = list(map(int, z))

    elif address_class == "B":
        z = a_split[:2]
        z = list(map(int, z))

    else:
        z = a_split[:3]
        z = list(map(int, z))

    block_size = 256 - int(copy_sub_split_int[index_num])

    b = [0] * 4

    for i in range(len(z)):
        b[i] = z[i]

    x = copy_sub_split_int[index_num]
    if index_num == 0:
        str_b = list(map(str, b))
        valid_subnets.append(".".join(str_b))
        if len(z) == 1:
            b[-1] = b[-1] + 1
            str_b = list(map(str, b))
            first_addresses.append(".".join(str_b))

            b[1], b[2], b[3] = 255, 255, 255
            str_b = list(map(str, b))
            broadcast_addresses.append(".".join(str_b))

            b[-1] = b[-1] - 1
            str_b = list(map(str, b))
            last_addresses.append(".".join(str_b))

    if index_num == 1:
        for i in range(0, x + 1, block_size):

            if len(z) == 2:
                str_b = list(map(str, b))
                valid_subnets.append(".".join(str_b))

                b[-1] = b[-1] + 1
                str_b = list(map(str, b))
                first_addresses.append(".".join(str_b))

                b[2], b[3] = 255, 255
                str_b = list(map(str, b))
                broadcast_addresses.append(".".join(str_b))

                b[-1] = b[-1] - 1
                str_b = list(map(str, b))
                last_addresses.append(".".join(str_b))
                break

            b[2], b[3] = 0, 0
            b[index_num] = i
            str_b = list(map(str, b))
            valid_subnets.append(".".join(str_b))

            b[-1] = b[-1] + 1
            str_b = list(map(str, b))
            first_addresses.append(".".join(str_b))

            tmp = i + block_size - 1
            b[index_num] = tmp
            b[2], b[3] = 255, 255
            str_b = list(map(str, b))
            broadcast_addresses.append(".".join(str_b))

            b[-1] = b[-1] - 1
            str_b = list(map(str, b))
            last_addresses.append(".".join(str_b))

    if index_num == 2:
        for n in range(1, 257, 1):
            for i in range(0, x + 1, block_size):

                if len(z) == 3:
                    str_b = list(map(str, b))
                    valid_subnets.append(".".join(str_b))

                    b[-1] = b[-1] + 1
                    str_b = list(map(str, b))
                    first_addresses.append(".".join(str_b))

                    b[3] = 255
                    str_b = list(map(str, b))
                    broadcast_addresses.append(".".join(str_b))

                    b[-1] = b[-1] - 1
                    str_b = list(map(str, b))
                    last_addresses.append(".".join(str_b))
                    break

                b[3] = 0
                b[index_num] = i
                str_b = list(map(str, b))
                valid_subnets.append(".".join(str_b))

                b[-1] = b[-1] + 1
                str_b = list(map(str, b))
                first_addresses.append(".".join(str_b))

                tmp = i + block_size - 1
                b[index_num] = tmp
                b[3] = 255
                str_b = list(map(str, b))
                broadcast_addresses.append(".".join(str_b))

                b[-1] = b[-1] - 1
                str_b = list(map(str, b))
                last_addresses.append(".".join(str_b))

            if len(z) == 2:
                break

            if len(z) == 3:
                break

            i = 0
            b[1] = n

    if index_num == 3:
        for m in range(1, 257, 1):
            for n in range(1, 257, 1):
                for i in range(0, x + 1, block_size):
                    b[index_num] = i
                    str_b = list(map(str, b))
                    valid_subnets.append(".".join(str_b))

                    b[-1] = b[-1] + 1
                    str_b = list(map(str, b))
                    first_addresses.append(".".join(str_b))

                    tmp = i + block_size - 1
                    b[index_num] = tmp
                    str_b = list(map(str, b))
                    broadcast_addresses.append(".".join(str_b))

                    b[-1] = b[-1] - 1
                    str_b = list(map(str, b))
                    last_addresses.append(".".join(str_b))

                if len(z) == 3:
                    break

                i = 0
                b[2] = n

            if len(z) == 3:
                break
            if len(z) == 2:
                break

            n = 0
            b[1] = m

    subnet_props["valid_subnets"] = valid_subnets
    subnet_props["broadcast_addresses"] = broadcast_addresses
    subnet_props["first_addresses"] = first_addresses
    subnet_props["last_addresses"] = last_addresses


# First and last address converted to binary version to compare which bits are common
# a = list of bits that are common in both, len(a) = cidr
# Enough empty bits added to make a valid address in a
# a is split and each part is converted to decimal to get subnet mask
def calc_supernet(int_addresses, address_one):

    address_first = int_addresses[0]
    address_last = int_addresses[-1]

    bin_first = [list(f"{i:08b}") for i in address_first]
    bin_last = [list(f"{i:08b}") for i in address_last]

    a = []
    s = True
    for i in range(len(bin_first)):
        for j in range(len(bin_first[0])):

            if bin_first[i][j] != bin_last[i][j]:
                s = False
                break

            a.append(int(bin_first[i][j]))

        if not s:
            break

    supernet_props["address"] = address_one + "/" + str(len(a))

    for n in range(len(a)):
        a[n] = 1

    padding = 8 - len(a) % 8

    for n in range(padding):
        a.append(0)

    j = 8
    a = list(map(str, a))
    split = [a[i:i + j] for i in range(0, len(a), j)]

    c = ["0"] * 4
    b = ["".join(i) for i in split]
    b = [str(int(i, 2)) for i in b]

    for i in range(len(b)):
        c[i] = b[i]

    supernet_props["mask"] = ".".join(c)


# Non-functional home page
@app.get("/")
def home():
    return {"Data": "Home"}


# Endpoint for ipcalc, expects an IP as input and performs class_calc on it
@app.post("/ipcalc", tags=["ipcalc"])
def ipcalc(ip: Input):
    return class_calc(ip)


# Endpoint for subnet, takes IP and mask as input
# Both split and mask converted to binary format(requires python 3.6+)
# Each individual binary char in binmask added to a. Sum of 1s in a = cidr
# Function called to compute other subnet properties
# Subnets and hosts calculated depending on address class
@app.post("/subnet", tags=["subnet"])
def subcalc(sub: Input):

    sub_split = sub.mask.split(".")
    address_split = sub.address.split(".")
    sub_split_int = list(map(int, sub_split))
    binmask = [f"{i:08b}" for i in sub_split_int]

    a = []
    for j in range(4):
        for i in binmask[j]:
            a.append(int(i))

    cidr = sum(a)
    subnet_props["address_cidr"] = sub.address + "/" + str(cidr)

    address_class = ipcalc(sub)["class"]
    find_subnetworks(address_split, sub_split_int, address_class)

    if address_class == "A":
        subnet_props["num_subnets"] = 2 ** (cidr - 8)
        subnet_iter = 2 ** (24 - (cidr - 8))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2

    elif address_class == "B":
        subnet_props["num_subnets"] = 2 ** (cidr - 16)
        subnet_iter = 2 ** (16 - (cidr - 16))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2

    elif address_class == "C":
        subnet_props["num_subnets"] = 2 ** (cidr - 24)
        subnet_iter = 2 ** (8 - (cidr - 24))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2

    return subnet_props


# Endpoint for supernet, takes list of IPs as input
# addresses = split of every address into 4 parts and converted to int
# Function called to find cidr and mask
@app.post("/supernet", tags=["supernet"])
def supercalc(super_a: SuperNet):

    addresses = []
    for n in range(len(super_a.addresses)):
        a = super_a.addresses[n].split(".")
        a = list(map(int, a))
        addresses.append(a)

    calc_supernet(addresses, super_a.addresses[0])
    return supernet_props

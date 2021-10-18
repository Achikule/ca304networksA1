
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

classA = {"class": "A",
          "num_networks": 126,
          "num_hosts": 16777214,
          "first_address": "0.0.0.0",
          "last_address": "127.255.255.255"}

classB = {"class": "B",
          "num_networks": 16384,
          "num_hosts": 65536,
          "first_address": "128.0.0.0",
          "last_address": "191.255.255.255"}

classC = {"class": "C",
          "num_networks": 2097152,
          "num_hosts": 256,
          "first_address": "192.0.0.0",
          "last_address": "223.255.255.255"}

classD = {"class": "D",
          "num_networks": "N/A",
          "num_hosts": "N/A",
          "first_address": "244.0.0.0",
          "last_address": "239.255.255.255"}

classE = {"class": "E",
          "num_networks": "N/A",
          "num_hosts": "N/A",
          "first_address": "240.0.0.0",
          "last_address": "255.255.255.255"}

subnet_props = {"address_cidr": "",
                "num_subnets": "",
                "addressable_hosts_per_subnet": "",
                "valid_subnets": [],
                "broadcast_addresses": [],
                "last_addresses": []}


class Input(BaseModel):
    address: str
    mask: Optional[str]


def classcalc(ip):
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
    elif binary[0:5] == "1111":
        return classE


def find_subnetworks(a_split, s_split_int):
    copy_sub_split_int = s_split_int.copy()
    index_num = 0
    for n in copy_sub_split_int:
        if int(n) < 255:
            index_num = copy_sub_split_int.index(n)
            break
    a_split = a_split[: index_num]

    block_size = 256 - int(copy_sub_split_int[index_num])
    valid_subnets = []
    q = 0
    x = ".0"
    while q <= copy_sub_split_int[index_num]:
        valid_subnets.append(".".join(a_split) + "." + str(q) + (3 - index_num) * x)
        q = q + block_size
    subnet_props["valid_subnets"] = valid_subnets


@app.get("/")
def home():
    return {"Data": "Home"}


@app.post("/ipcalc")
def ipcalc(ip: Input):
    return classcalc(ip)


@app.post("/subnet")
def subcalc(sub: Input):
    sub_split = sub.mask.split(".")
    address_split = sub.address.split(".")
    sub_split_int = list(map(int, sub_split))
    binmask = [f"{i:08b}" for i in sub_split_int]

    a = []
    j = 0
    while j < 4:
        for i in binmask[j]:
            a.append(int(i))
        j = j + 1


    cidr = sum(a)
    subnet_props["address_cidr"] = sub.address + "/" + str(cidr)

    address_class = ipcalc(sub)["class"]
    find_subnetworks(address_split, sub_split_int)

    if address_class == "A":
        subnet_props["num_subnets"] = 2 ** (cidr - 8)
        subnet_iter = 2 ** (24 - (cidr - 8))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2

        return subnet_props,

    elif address_class == "B":
        subnet_props["num_subnets"] = 2 ** (cidr - 16)
        subnet_iter = 2 ** (16 - (cidr - 16))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2

        return subnet_props

    elif address_class == "C":
        subnet_props["num_subnets"] = 2 ** (cidr - 24)
        subnet_iter = 2 ** (8 - (cidr - 24))
        subnet_props["addressable_hosts_per_subnet"] = subnet_iter - 2
        valid_subnets = []
        return subnet_props

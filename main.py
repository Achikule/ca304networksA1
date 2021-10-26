
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
                "first_addresses": [],
                "last_addresses": []
                }

supernet_props = {"address": "",
                  "mask": ""
                  }


class Input(BaseModel):
    address: str
    mask: Optional[str]


class SuperNet(BaseModel):
    address: list


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


def find_subnetworks(a_split, s_split_int, address_class):
    copy_sub_split_int = s_split_int.copy()
    broadcast_addresses = []
    first_addresses = []
    last_addresses = []
    valid_subnets = []

    copybinary_sub = [i for i in copy_sub_split_int if i > 0]
    index_num = len(copybinary_sub) - 1

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


@app.post("/supernet")
def supercalc(super_a: SuperNet):

    addresses = []
    for n in range(len(super_a.address)):
        a = super_a.address[n].split(".")
        a = list(map(int, a))
        addresses.append(a)

    address_first = addresses[0]
    address_last = addresses[-1]

    binmask_first = [list(f"{i:08b}") for i in address_first]
    binmask_last = [list(f"{i:08b}") for i in address_last]

    a = []
    s = True
    for i in range(len(binmask_first)):
        for j in range(len(binmask_first[0])):

            if binmask_first[i][j] != binmask_last[i][j]:

                s = False
                break

            a.append(int(binmask_first[i][j]))

        if not s:
            break

    supernet_props["address"] = super_a.address[0] + "/" + str(len(a))

    for n in range(len(a)):
        a[n] = 1

    padding = 8 - len(a) % 8

    for n in range(padding):
        a.append(0)

    j = 8
    a = list(map(str, a))
    split = [a[i:i+j] for i in range(0, len(a), j)]

    c = ["0"] * 4
    b = ["".join(i) for i in split]
    b = [str(int(i, 2)) for i in b]

    for i in range(len(b)):
        c[i] = b[i]

    supernet_props["mask"] = ".".join(c)

    print(binmask_first, "\n", binmask_last, "\n", b, c)
    return supernet_props

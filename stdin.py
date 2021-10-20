#!usr/bin/env python3

address = "192.168.0.1"
subnet = "255.255.255.192"
asplit = address.split(".")
sub_split = subnet.split(".")
binary_sub = list(map(int, sub_split))
bi = [f"{i:08b}" for i in binary_sub]
a = []
j = 0
classA = ["101.221.3.2", "17.82.244.1"]
classB = ["133.1.45.0", "130.234.7.12"]
classC = ["192.168.0.1", "199.168.35.33"]
while j < 4:
    for i in bi[j]:
        a.append(int(i))
    j = j + 1


broadcast_addresses = []
first_addresses = []
last_addresses = []
subnet_iter = 2 ** (8 - (sum(a) - 24))
cidr = subnet_iter - 2

copybinary_sub = [i for i in binary_sub if i > 0]
ind = len(copybinary_sub) - 1

if address in classA:
    z = [asplit[0]]
    z = list(map(int, z))

elif address in classB:
    z = asplit[:2]
    z = list(map(int, z))

else:
    z = asplit[:3]
    z = list(map(int, z))


blocksize = 256 - int(binary_sub[ind])
b = [0] * 4

for i in range(len(z)):
    b[i] = z[i]

print(b)
x = binary_sub[ind]
valid_subnets = []
if ind == 0:
    str_b = list(map(str, b))
    valid_subnets.append(".".join(str_b))

if ind == 1:
    for i in range(0, x + 1, blocksize):

        if len(z) == 2:
            str_b = list(map(str, b))
            valid_subnets.append(".".join(str_b))
            break

        b[ind] = i
        str_b = list(map(str, b))
        valid_subnets.append(".".join(str_b))


if ind == 2:
    for n in range(1, 257, 1):
        for i in range(0, x + 1, blocksize):

            if len(z) == 3:
                str_b = list(map(str, b))
                valid_subnets.append(".".join(str_b))
                break

            b[ind] = i
            str_b = list(map(str, b))
            valid_subnets.append(".".join(str_b))

        if len(z) == 2:
            break

        if len(z) == 3:
            break

        i = 0
        b[1] = n

if ind == 3:
    for m in range(1, 257, 1):
        for n in range(1, 257, 1):
            for i in range(0, x + 1, blocksize):
                b[ind] = i
                str_b = list(map(str, b))
                valid_subnets.append(".".join(str_b))

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



print(bi, sum(a), cidr, blocksize, ind, copybinary_sub, z, len(valid_subnets), "\n", valid_subnets[-50:], "\n", first_addresses, "\n", broadcast_addresses, "\n",
      last_addresses)
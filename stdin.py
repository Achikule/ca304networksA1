#!usr/bin/env python3

address = "12.1.2.3"
subnet = "255.252.0.0 "
asplit = address.split(".")
sub_split = subnet.split(".")
binary_sub = list(map(int, sub_split))
bi = [f"{i:08b}" for i in binary_sub]
a = []
j = 0

while j < 4:
    for i in bi[j]:
        a.append(int(i))
    j = j + 1

valid_subnets = []
broadcast_addresses = []
first_addresses = []
last_addresses = []
subnet_iter = 2 ** (8 - (sum(a) - 24))
cidr = subnet_iter - 2
ind = 0
copybinary_sub = binary_sub.copy()
for n in copybinary_sub:
    if int(n) < 255:
        ind = copybinary_sub.index(n)
        break

z = asplit[0]
blocksize = 256 - int(copybinary_sub[ind])
q = 0
x = ".0"
y = ".255"
while q <= copybinary_sub[ind]:
    if ind == 2:
        z = z + ".0"
    tmp = z + "." + str(q) + (3 - ind) * x
    valid_subnets.append(z + "." + str(q) + (3 - ind) * x)
    first_addresses.append(z + "." + str(q) + (2 - ind) * x + ".1")
    q = q + blocksize
    broadcast_addresses.append(z + "." + str(q - 1) + (3 - ind) * y)
    last_addresses.append(z + "." + str(q - 1) + (2 - ind) * y + ".254")

print(bi, sum(a), cidr, blocksize, ind, "\n", valid_subnets, "\n", first_addresses, "\n", broadcast_addresses, "\n",
      last_addresses)
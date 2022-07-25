# id_list = ["zander", "gumi", "bomba", "test"]

# with open("idfile.txt", "w") as f:
#     for id in id_list:
#         f.write(id + "\n")

# print("bomba")

# with open("idfile.txt", "r") as f:
#     nueva_lista = f.readlines()
#     print(nueva_lista)

import json

names = ["Jessa", "Eric", "Bob"]


def write_list(a_list):
    print("Started writing list data into a json file")
    with open("names.json", "w") as f:
        json.dump(a_list, f)
        print("Done writing JSON data into .json file")


def read_list():
    # for reading also binary mode is important
    with open("names.json", "rb") as fp:
        n_list = await json.load(fp)

    return n_list


# write_list(names)

r_names = read_list()
print("List is", r_names)

bomba = read_list()
bomba.append("hola")
print(bomba)
write_list(bomba)

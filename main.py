import sys

if __name__ != "__main__":
    print("This is the main module. Do not call.")
    sys.exit()

import csv

def initialize():
    # Attempts to load logins
    logins_file_err_msg = "ERROR LOADING USERNAMES AND PASSWORDS\n\nPassword file is missing or corrupt. Contact Matt Skaggs (matt.reword@gmail.com) to resolve this.\n\nTruckin' Trucco will not function without a valid logins file.\n\nPress Enter to exit.\n"

    logins_dict = {}
    try:
        with open("logins.csv", newline = "") as logins_file:
            csv_reader = csv.reader(logins_file, delimiter = ",")
            for ele in csv_reader: logins_dict[ele[0]] = ele[1]
    except Exception as load_logins_e:
        input(f"{load_logins_e}\n\nlogins_file_err_msg")
        sys.exit()

    # There should be an even number of elements (username and password combinations)
    if len(list(logins_dict.keys())) % 2 == 1:
        input(logins_file_err_msg)
        sys.exit()

    from menus import Menus

    # Starts up the menu
    starting_menus = Menus(logins_dict)

initialize()

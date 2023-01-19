import datetime
import sys

if __name__ == "__main__":
    print("This is a supporting module. Do not execute.")
    sys.exit()

import csv

from pcc_interact import PccInteract
from data_validation import DataValidation
from mis_menus import MN_ITS_Menu
from background_check import BackgroundCheck

# This class displays all menus the user will navigate
# Different menus are all different methods, despite being very similar. Using one method with parameters to accommodate all menus won't work with the menu dictionaries; this results in circular references.
class Menus:
    def __init__(self,
                 logins_dict,
                 webdriver_settings_pcc,
                 settings_background_check,
                 settings_mnits
                 ):
        self.logins_dict = logins_dict

        self.settings_background_check = settings_background_check
        self.settings_mnits = settings_mnits

        self.pcc_interact = PccInteract(self.logins_dict["PCC_USERNAME"], self.logins_dict["PCC_PASSWORD"], webdriver_settings_pcc)
        self.pcc_interact.pcc_login()

        self.data_validation = DataValidation()

        self.menu_invalid_user_input = "Please enter a valid selection from the menu.\n\n(Press Enter.)\n"
        self.invalid_lic_msg = "******WARNING******\nThis software is only licensed for use at the Estates at Chateau.\n\nAll capabilities are disabled until Truckin' Trucco validates that your PCC account is logged into EAC.\n"

        # All menus are set up as dictionaries and follow this format:
            # The key is the option the user will select. The key must be capitalized (but the user's input is not case-sensitive)
            # The value is a tuple. First element is text displayed to user. Second is the function/method to be called.
        self.reports_menu_opt = {
            "1": ("1: Start-Of-A-Good-Day reports", self.pcc_interact.start_of_good_day),
            "2": ("2: Daily Census Report", self.pcc_interact.run_daily_census_rep),
            "3": ("3: Case Mix Details Report", self.pcc_interact.run_case_mix_detail),
            "4": ("4: 24-Hr. Summary (24 hours)", self.pcc_interact.run_24_72_report_24),
            "5": ("5: 24-Hr. Summary (72 hours)", self.pcc_interact.run_24_72_report_72),
            "M": ("\nM: Main Menu\n", self.main_menu)
        }
        self.main_menu_opt = {
            "1": ("1: PCC reports", self.reports_menu),
            "2": ("2: MN-ITS in Seconds", self.mn_its_in_secs),
            "3": ("3: Background check", self.background_check),
            "P": ("\nP: Password change", self.update_logins),
            "R": ("R: Restart PCC webdriver", self.pcc_interact.driver.restart_driver),
            "L": ("L: Attempt PCC login again\n", self.pcc_interact.pcc_login)
        }

        self.main_menu()

    # Displays main menu options.
    def main_menu(self):
        valid_input = False
        while valid_input == False:
            self.program_enabled = self.fac_check()

            self.pcc_interact.clear_console()

            if self.program_enabled == False: print(self.invalid_lic_msg)

            # Displays menu to the user.
            for menu_items in self.main_menu_opt: print(self.main_menu_opt[menu_items][0])

            # Obtains user's input. If input is invalid, loop repeats.
            self.user_input = self.data_validation.validate_user_input_custom(
                input(),
                list(self.main_menu_opt.keys()),
                allow_exit = True
            )
            if self.user_input == False:
                # input(self.menu_invalid_user_input)
                continue

            if self.user_input == "exit": self.close_out()

            # If code is continuing, then the input must be valid. Loop ends.
            valid_input = True

        # Prepares self.user_input to be used to access self.main_menu_opt key
        self.user_input = self.user_input.upper()

        # Executes whatever valid input received from the user
        if self.program_enabled == True: self.main_menu_opt[self.user_input][1]()

        # Allows login attempt even without validating the software
        elif self.user_input.upper() == "L": self.main_menu_opt[self.user_input.upper()][1]()

        self.user_input = None

        # If the code is still executing here, then the user is still in this menu, with a method having finished running (self.pcc_interact.driver.restart_driver() or self.pcc_interact.pcc_login()). Restarts this method/the above loop.
        self.main_menu()

    # Displays reports menu
    def reports_menu(self):
        valid_input = False
        while valid_input == False:
            self.program_enabled = self.fac_check()

            self.pcc_interact.clear_console()

            if self.program_enabled == False: print(self.invalid_lic_msg)

            # Displays menu to the user.
            for menu_items in self.reports_menu_opt: print(self.reports_menu_opt[menu_items][0])

            # Obtains user's input. If input is invalid, loop repeats.
            self.user_input = self.data_validation.validate_user_input_custom(
                input(),
                list(self.reports_menu_opt.keys()),
                allow_exit = True
            )
            if self.user_input == False:
                # input(self.menu_invalid_user_input)
                continue

            # If code is continuing, then the input must have been valid. Loop ends.
            valid_input = True

        if self.user_input == "exit": self.close_out()

        # "back" is equivalent to selecting "M" (Main Menu)
        if self.program_enabled == True:
            if self.user_input == "back": self.reports_menu_opt["M"][1]()

        # Executes whatever valid input received from the user
        if self.program_enabled == True:
            self.user_input = self.user_input.upper()
            self.reports_menu_opt[self.user_input][1]()

        self.user_input = None

        # If the code is still executing here, the user is still in this menu, with report(s) finished running. Restarts method/above loop.
        self.reports_menu()

    # Allows user to change a username's password
    def update_logins(self):
        self.pcc_interact.clear_console()
        valid_input = False
        while valid_input == False:
            passwords = []
            print("Current username(s):\n")
            # Loops through dictionary of passwords, only printing those on even numbered indices (and 0), which should be usernames. Saves passwors to a list to overwrite later if the user changes a password.
            for i, username in enumerate(list(self.logins_dict.keys())):
                if i % 2 == 0:
                    print(f"{int((i + 2) / 2)}. {username}: {self.logins_dict[username]}")
                else: passwords.append(username)
            user_input = self.data_validation.validate_user_input_num(
                input("\nWhich username needs a new password?\n"),
                float_num = False,
                negative_num = False,
                zero_num = False,
                min_num = 1,
                max_num = len(passwords),
                allow_back = True,
                allow_exit = True
            )
            if user_input == "exit":
                self.pcc_interact.driver.close_out()
                sys.exit()
            if user_input == "back": return
            if user_input != False: valid_input = True

        # Get and validate new password
        new_password = input("\nWhat is the new password?\n")
        if new_password.strip().lower() == "exit":
            self.pcc_interact.driver.close_out()
            sys.exit()
        if new_password.strip().lower() == "back": return
        new_password_confirm = input("\nPlease enter the new password again to confirm.\n")

        # If passwords match, writes full logins dictionary to CSV. If they don't match, returns to previous menu.
        if new_password_confirm == new_password:
            self.logins_dict[passwords[int(user_input) - 1]] = new_password

            with open("logins.csv", "w", newline="") as logins_file:
                csv_writer = csv.writer(logins_file, delimiter=",")
                for ele in self.logins_dict.keys():
                    csv_writer.writerow([ele, self.logins_dict[ele]])

            input("\nPassword changed!\n\nPress Enter.")
        else:
            input("\nThe passwords you entered did not match. Start the password change process again.\n\nPress Enter.")

    def fac_check(self):
        page_title = self.pcc_interact.driver.driver.title
        if page_title == "PointClickCare Login": return True

        fac_name = self.pcc_interact.driver.find_ele(
            self.pcc_interact.driver.main_win_handle,
            "id",
            "pccFacLink",
            "facility information"
        )
        if fac_name == False: return False
        if "estates at chateau" not in fac_name.text.lower(): return False
        return True

    def mn_its_in_secs(self):
        self.mis_main_menu = MN_ITS_Menu(self.logins_dict["MNITS_USERNAME"], self.logins_dict["MNITS_PASSWORD"], self.settings_mnits)
        self.main_menu()

    # Sets up (pre-fills) three background checks
    def background_check(self):
        self.pcc_interact.driver.clear_console()
        print("**Background check search**.\n\nType 'back' to return to the previous menu -- if you have any background check results open, typing 'back' will close that window.")

        bg_check = {
            "First name": "",
            "Last name": "",
            "DOB": ""
        }

        # Obtains search criteria
        for ele in list(bg_check.keys()):
            # Any string is allowed for first and last name. Data validation required for DOB.
            if ele != "DOB": user_input = input(f"\nEnter {ele.lower()}:\n")
            else:
                user_input = False
                while user_input == False:
                    user_input = self.data_validation.validate_user_input_date(
                        input(f"\nEnter a valid {ele.lower()}:\n"),
                        allow_back = True,
                        allow_exit = True
                    )

                # If date was entered, properly formats it. (Only other options are "back" or "exit.)
                if type(user_input) == datetime.datetime: user_input = datetime.datetime.strftime(user_input, "%m/%d/%Y")

            user_input = user_input.strip()
            user_input_l = user_input.lower()

            if user_input_l == "exit": self.close_out()

            if user_input_l == "back": return

            bg_check[ele] = user_input

        # Starts a new webdriver for the background check
        self.background_checker = BackgroundCheck(self.settings_background_check)

        self.background_checker.mpch_search(bg_check["First name"], bg_check["Last name"], bg_check["DOB"])
        self.background_checker.nsopw_search(bg_check["First name"], bg_check["Last name"])
        self.background_checker.mtcpa_search(bg_check["First name"], bg_check["Last name"], bg_check["DOB"])

        input("\nBackground searches completed and/or pre-filled. You may have captchas to complete.\n\nPress Enter to continue.\n")

        self.background_check()

    def close_out(self):
        try: self.pcc_interact.driver.close_out()
        except: pass
        try: self.mis_main_menu.driver.close_out()
        except: pass
        sys.exit()
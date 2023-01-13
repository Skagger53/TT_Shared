import sys

if __name__ == "__main__":
    print("This is a supporting module. Do not execute directly.")
    sys.exit()

import datetime
from selenium.webdriver.common.keys import Keys
from time import sleep

from logo import logo
from webdriver_framework import WebdriverMain
from data_validation import DataValidation

# Main menu class
class MN_ITS_Menu():
    def __init__(self, username, password):
        # MN-ITS login information
        self.mn_its_username = username
        self.mn_its_password = password

        if "mskaggs" not in self.mn_its_username and "ktrucco" not in self.mn_its_username:
            input("This program is not licensed for you to use.\n\nPlease contact Matt Skaggs (matt.reword@gmail.com) if you would like to license this software.\n\nPress Enter to close.\n")
            return

        # MN-ITS eligibility query page
        self.query_url = "https://mn-its.dhs.state.mn.us/pr/trans/elig/eligrequest"

        # Sets all variables used to submit a query to None
        self.setup_submission_vars()

        # If window is too narrow, webdriver can't find the Lookup button in the query page.
        self.driver = WebdriverMain(window_x = 1000, window_y = 800)
        self.mn_its_login()
        self.data_validation = DataValidation()

        self.main_menu_opt = {
            "1": ["1. Name", self.enter_name],
            "2": ["2. DOB", self.enter_dob],
            "3": ["3. SSN", self.enter_ssn],
            "4": ["4. PMI\n", self.enter_pmi],
            "C": ["C. Clear select values", self.clear_values],
            "E": ["E. Execute MN-ITS query\n", self.submit_query],
            "R": ["R. Restart MN-ITS in Seconds webdriver", self.driver.restart_driver],
            "L": ["L. Attempt MN-ITS login\n", self.mn_its_login],
            # Using None due to intercepting this selection in main_menu(). See comments there.
            "B": ["B. Back to Truckin' Trucco main menu", None]
        }

        self.main_menu()

    # Sets all variables used to submit a query to None
    def setup_submission_vars(self):
        self.submissions_fname = None
        self.submissions_lname = None
        self.submissions_dob = None
        self.submissions_ssn = None
        self.submissions_pmi = None

    # Navigates to login page and logs in.
    def mn_its_login(self):
        # If a user is already logged in, navigating to this page reaches the "home"/main page within of MN-ITS (for a logged-in user).
        if self.driver.get_url(self.driver.main_win_handle, "https://mn-its.dhs.state.mn.us/gatewayweb/login", fail_msg = "Attempt login again?\n\nPress Enter.\n") == False: return
        username_login = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "userid",
            "MN-ITS username login field. Is the site down or are you already logged in?"
        )
        if username_login == False: return

        # Entering username and password
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                username_login,
                self.mn_its_username,
                "MN-ITS username login field."
        ) == False: return
        password_login = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "password",
            "MN-ITS password field."
        )
        if password_login == False: return
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                password_login,
                self.mn_its_password,
                "MN-ITS password login field."
        ) == False: return
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                password_login,
                Keys.ENTER,
                "MN-ITS password login field."
        ) == False: return

        # After login, checks to see if the user is at the "home"/main page for logged-in users. Looks for the "MN-ITS" drop-down menu button in the left navigation pane.
        if self.driver.find_ele(
                self.driver.main_win_handle,
                "id",
                "mnitsId",
                "MN-ITS home page (after login). Is the site down?",
                wait_time = 10
        ) == False: return

        # Navigates to the query page. No need to check for a False return (failed navigation); user will be informed within WebdriverFramework, and this method ends anyway.
        self.driver.get_url(self.driver.main_win_handle, self.query_url)

    # Main menu for the user.
    def main_menu(self):
        valid_input = False
        while valid_input == False:
            self.driver.clear_console()
            print(logo)

            # Prints all information entered so far to use in MN-ITS query
            self.print_submission_info()

            # Displays menu to the user based on self.main_menu_opt dictionary.
            for menu_ele in self.main_menu_opt.values(): print(menu_ele[0])

            user_input = self.data_validation.validate_user_input_custom(
                input().upper(),
                list(self.main_menu_opt.keys()),
                allow_exit = True,
                allow_back = True
            )

            if user_input == False: input("\nPlease enter a valid option.\n\nPress Enter.\n")
            elif user_input == "exit":
                self.driver.close_out()
                sys.exit()
            # If the user selects "B" to go back, I intercept it here rather than execute a method from the main_menu_opt dictionary as usual. This allows me to simply use "return" to get back to the main main menu.
            elif user_input == "back" or user_input.upper() == "B":
                self.driver.close_out()
                return
            else: valid_input = True

        # Executes user's selection
        self.main_menu_opt[user_input.upper()][1]()

        # Restarts this menu after user's selection is completed.
        self.main_menu()

    # Gets a name from the user for the query. This is called twice for first and last names. Accepts anything except an empty string.
    def get_name(self, name_needed):
        valid_input = False
        while valid_input == False:
            user_input = input(f"\nEnter {name_needed}:\n")
            if user_input == "": print(f"\nPlease enter a string for {name_needed}.\n")
            else: valid_input = True

        # If the user enters "back", this allows them to return to the main menu with nothing entered for first or last name.
        if user_input.strip().lower() == "back":
            self.submissions_fname, self.submissions_lname = None, None
        else: return user_input

    # Allows entering the name for the query.
    def enter_name(self):
        self.submissions_fname = self.get_name("first name")
        if self.submissions_fname == None: return # Catches "back" from user
        self.submissions_lname = self.get_name("last name")

    # Allows date of birth to be entered
    def enter_dob(self):
        valid_input = False
        while valid_input == False:
            print("\nPlease enter a valid date.\n")
            user_input = self.data_validation.validate_user_input_date(input(), allow_back = True, allow_exit = True)

            if user_input == "back": return
            if user_input == "exit": sys.exit()

            elif user_input != False:
                self.submissions_dob_dt_obj = user_input
                self.submissions_dob = datetime.datetime.strftime(user_input, "%m/%d/%Y")
                valid_input = True

    # Accepts SSN (with or without hyphens)
    def enter_ssn(self):
        valid_input = False
        while valid_input == False:
            user_input = input("\nEnter Social Security Number:\n").replace("-", "")
            if self.data_validation.validate_user_input_num(
                    user_input,
                    float_num = False,
                    negative_num = False,
                    allow_back = True,
                    allow_exit = True
            ) != False:
                if user_input == "back": return
                if user_input == "exit": sys.exit()
                if len(user_input) == 9:
                    # Ensures format will be accepted by MN-ITS query page
                    self.submissions_ssn = user_input[:3] + "-" + user_input[3:5] + "-" + user_input[5:]
                    valid_input = True

    # Accepts PMI for query
    def enter_pmi(self):
        valid_input = False
        while valid_input == False:
            user_input = input("\nEnter a valid PMI:\n")
            if self.data_validation.validate_user_input_num(
                    user_input,
                    float_num = False,
                    negative_num = False,
                    allow_back = True,
                    allow_exit = True
            ) != False:
                if user_input == "back": return
                if user_input == "exit": sys.exit()
                if len(user_input) == 8:
                    self.submissions_pmi = user_input
                    valid_input = True
                # Allows PMI lengths of less than 8 but prepends 0s to reach 8 characters
                elif len(user_input) < 8:
                    zeros = "".join(["0" for i in range(8 - len(user_input))])
                    self.submissions_pmi = zeros + user_input
                    valid_input = True

    # Allows user to clear some or all values already entered
    def clear_values(self):
        # Checks that at least one identifier has been entered
        if self.submissions_lname == None and \
            self.submissions_dob == None and \
            self.submissions_ssn == None and \
            self.submissions_pmi == None:
            input("\nYou have not entered any identifiers to clear yet.\n\nPress Enter to return to the main menu.\n")
            return

        valid_input = False
        while valid_input == False:
            print("\nValue to clear:\n\n1. Name\n2. DOB\n3. SSN\n4. PMI\n5. All\n")
            user_input = self.data_validation.validate_user_input_num(
                input(),
                float_num = False,
                negative_num = False,
                zero_num = False,
                min_num = 1,
                max_num = 5,
                allow_back = True,
                allow_exit = True
            )

            if user_input != False:
                if user_input == "back": return
                if user_input == "exit": sys.exit()
                if user_input == "1": self.submissions_fname, self.submissions_lname = None, None # Name
                elif user_input == "2": self.submissions_dob = None # DOB
                elif user_input == "3": self.submissions_ssn = None # SSN
                elif user_input == "4": self.submissions_pmi = None # PMI
                elif user_input == "5": # All
                    confirm_clear = self.data_validation.validate_user_input_custom(
                        input("\nAre you sure you want to clear all?\n").lower(),
                        ("yes", "y", "no", "n"),
                        allow_back = True,
                        allow_exit = True
                    )
                    if confirm_clear == False: input("\nPlease enter yes or no.\n")
                    elif confirm_clear == "back" or confirm_clear[0] == "n": return
                    elif confirm_clear == "exit": sys.exit()
                    else: self.setup_submission_vars()

                valid_input = True

    # Prints all information entered so far for MN-ITS query
    def print_submission_info(self):
        if self.submissions_fname != None: print(f"Name: {self.submissions_fname} {self.submissions_lname}")
        if self.submissions_dob != None: print(f"DOB: {datetime.datetime.strftime(self.submissions_dob_dt_obj, '%#m/%#d/%Y')}")
        if self.submissions_ssn != None: print(f"SSN: {self.submissions_ssn}")
        if self.submissions_pmi != None: print(f"PMI: {self.submissions_pmi}")
        print()

    # Submits query to MN-ITS
    def submit_query(self):
        # Checks that enough data has been entered for at least a possibly successful query
        submissions = len([val_present for val_present in (self.submissions_lname, self.submissions_dob, self.submissions_ssn, self.submissions_pmi) if val_present != None])
        if submissions < 2:
            if submissions == 1: s_or_p = "identifier"
            else: s_or_p = "identifiers"
            input(f"\nYou have provided {submissions} {s_or_p}. A minimum of two is required.\n\nPress Enter to return to the main menu.")
            return

        # If current window is not already at the query page, navigates to the query page
        if self.driver.driver.current_url != self.query_url:
            if self.driver.get_url(self.driver.main_win_handle, self.query_url) == False: return

        # Need an element to click, mainly for DOB below, since a date selector pop-up appears and needs to be removed to ensure no accidental clicks or blocked clicks. The H5 element selection for this is arbitrary.
        click_me = self.driver.find_ele(
            self.driver.main_win_handle,
            "tag_name",
            "h5",
            "MN-ITS eligibility query page H5 tag (page title beginning 'Minnesota Department of...'). Is the MN-ITS query page open?"
        )
        if click_me == False: return

        # Lookup button (to select facility in Provider Address)
        lookup_button = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[4]/td[2]/table/tbody/tr/td[2]/input",
            "MN-ITS eligibility query page Lookup button.",
            wait_time = 10
        )
        if lookup_button == False: return
        if self.driver.click_ele(
                self.driver.main_win_handle,
                lookup_button,
                "MN-ITS eligibility query page Lookup button."
        ) == False: return

        # Navigating the new window that appears when clicking the Lookup button
        lookup_popup_win = self.driver.driver.window_handles[-1]
        radio_button_eac = self.driver.find_ele(
            lookup_popup_win,
            "xpath",
            "/html/body/div/div[3]/div[2]/div[2]/div/table/tbody/tr/td[1]/input",
            "facility radio button selection in MN-ITS query pop-out window (from Lookup button)."
        )
        if radio_button_eac == False: return
        if self.driver.click_ele(
                lookup_popup_win,
                radio_button_eac,
                "facility radio button selection in MN-ITS query pop-out window (from Lookup button)."
        ) == False: return
        npi_select_submit_btn = self.driver.find_ele(
            lookup_popup_win,
            "id",
            "submitButton",
            "Submit button in MN-ITS query pop-out window (from Lookup button)."
        )
        if self.driver.click_ele(
                lookup_popup_win,
                npi_select_submit_btn,
                "Submit button in MN-ITS query pop-out window (from Lookup button)."
        ) == False: return

        # Taxonomy Code Qualifier drop-down menu
        code_qualifier_dropdown = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[6]/td[2]/div/button/div/div/div",
            "MN-ITS eligibility query page Taxonomy Code Qualifier drop-down menu."
        )
        if code_qualifier_dropdown == False: return
        if self.driver.click_ele(
                self.driver.main_win_handle,
                code_qualifier_dropdown,
                "MN-ITS eligibility query page Taxonomy Code Qualifier drop-down menu."
        ) == False: return
        sleep(0.5)
        ad_admitting_opt = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[6]/td[2]/div/div/div/ul/li[2]",
            "MN-ITS eligibility query page AD Admitting option from Taxonomy Code Qualifier drop-down menu."
        )
        if ad_admitting_opt == False: return
        if self.driver.click_ele(
                self.driver.main_win_handle,
                ad_admitting_opt,
                "MN-ITS eligibility query page AD Admitting option from Taxonomy Code Qualifier drop-down menu."
        ) == False: return

        # Clicks outside the selection just in case (due to drop-down menu potentially covering other elements)
        if self.driver.click_ele(
                self.driver.main_win_handle,
                click_me,
                "MN-ITS eligibility query page body tag. Is the window open?"
        ) == False: return

        # Enters all user-entered elements (PMI, DOB, SSN, name)
        # Set up by tuple with nested tuples in this format: (text-to-enter, id-to-find-on-page, fail-msg-to-display-via-WebdriverFramework)
        ele_to_enter = (
            (self.submissions_pmi, "eligibilityRequest.subs_id", "MN-ITS eligibility query page Subscriber ID field."),
            (self.submissions_dob, "eligibilityRequest.subs_birth_date", "MN-ITS eligibility query page Birth Date field."),
            (self.submissions_ssn, "eligibilityRequest.soc_security_number", "MN-ITS eligibility query page Social Security Number field."),
            (self.submissions_lname, "eligibilityRequest.subs_last_name", "MN-ITS eligibility query page Last Name field."),
            (self.submissions_fname, "eligibilityRequest.subs_first_name", "MN-ITS eligibility query page First Name field.")
        )

        # Loops through all 5 elements to enter. If user hasn't entered anything, then skips that element.
        for ele in ele_to_enter:
            if ele[0] == None: continue
            ele_id = self.driver.find_ele(
                self.driver.main_win_handle,
                "id",
                ele[1],
                ele[2]
            )
            if ele_id == False: return
            ele_id.clear()
            if self.driver.enter_text_ele(
                    self.driver.main_win_handle,
                    ele_id,
                    ele[0],
                    ele[2]
            ) == False: return
            if self.driver.click_ele(
                    self.driver.main_win_handle,
                    click_me,
                    "MN-ITS eligibility query page body tag. Is the window open?"
            ) == False: return

        # Clicks Submit button, informs user, waits for Enter press.
        submit_btn = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[26]/td/input[1]",
            "MN-ITS eligibility query page Submit button."
        )
        if submit_btn == False: return
        if self.driver.click_ele(
                self.driver.main_win_handle,
                submit_btn,
                "MN-ITS eligibility query page Submit button."
        ) == False: return
        input("\nQuery submitted. Press Enter to return to MN-ITS in Seconds main menu.\n")
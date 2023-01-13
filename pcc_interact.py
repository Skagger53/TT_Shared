import sys

if __name__ == "__main__":
    print("This is a supporting module. Do not execute.")
    sys.exit()

from time import sleep
import datetime

from logo import logo
from webdriver_framework import WebdriverMain

# Class for interacting with PCC: logging in, navigating to locations, finding/clicking/entering text on elements, etc.
class PccInteract:
    def __init__(self, username, password):
        self.pcc_login_url = "https://login.pointclickcare.com/home/userLogin.xhtml?_gl=1*1n0q4b8*_ga*MTgzNzMwOTY1Ny4xNjU4ODQzNTI2*_ga_NBXHRQDSJE*MTY2MTE3Nzc1NC4zNi4wLjE2NjExNzc3NTQuNjAuMC4w&_ga=2.234057950.1359605354.1661177755-1837309657.1658843526"
        self.username = username
        self.password = password
        self.driver = WebdriverMain(window_x = 1200, window_y = 900)

    # Logs into PCC with above username data
    def pcc_login(self):
        # This is for other PCC login (non-remote access)
        # if self.driver.get_url(self.driver.main_win_handle, "https://www24.pointclickcare.com/home/login.jsp") == False: return False

        if self.driver.get_url(
                self.driver.main_win_handle,
                self.pcc_login_url
        ) == False: return False

        # Enters username
        # This is for non-remote access PCC login
        # username = self.driver.find_ele(self.driver.main_win_handle, "id", "un", "username entry") # Finds username login

        username = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "username",
            "username entry"
        )  # Finds username login
        next_button = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "id-next",
            "username entry"
        ) # Finds next button
        if username == False or next_button == False: return False
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                username,
                self.username,
                "username entry"
        ) == False: return False
        if self.driver.click_ele(
                self.driver.main_win_handle,
                next_button,
                "next button"
        ) == False: return False
        sleep(1)

        # username2 = self.driver.find_ele(self.driver.main_win_handle, "id", "un", "username entry") # Finds next username entry (identical to first?)
        # if self.driver.enter_text_ele(self.driver.main_win_handle, username2, self.username, "username entry") == False: return False # Enters username

        password = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "password",
            "password entry"
        ) # Finds password entry
        if password == False: return False

        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                password,
                self.password,
                "password entry"
        ) == False: return False # Enters password
        if self.driver.press_enter_ele(
                self.driver.main_win_handle,
                password,
                "password entry"
        ) == False: return False # Presses Enter on password entry

        # Check to see if successfully logged in (invalid password, etc.)
        if self.driver.find_ele(
                self.driver.main_win_handle,
                "id",
                "QTF_FacilityMessages",
                "login page. Invalid credentials or denied PCC connection attempt?"
        ) == False: return False

    # Locates the search box. If fails, displays error to user and returns False. If successful, returns the search box webdriver object.
    def find_search_box(self, window_handle):
        search_field = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "searchField",
            "search entry"
        )
        if search_field == False: return False
        return search_field

    # Executes PCC search for something
    def exec_search(self, window_handle, user_text):
        if self.driver.switch_window(self.driver.main_win_handle, window_handle) == False: return False

        # Finds the search box
        search_box = self.find_search_box(self.driver.main_win_handle)
        if search_box == False: return False

        # Enters text into the search box and presses Enter
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                search_box,
                user_text,
                "search box"
        ) == False: return False
        if self.driver.press_enter_ele(self.driver.main_win_handle, search_box, "search box") == False: return False

#-----------------------------REPORTS-----------------------------
    def start_of_good_day(self):
        self.run_daily_census_rep()
        self.run_case_mix_detail()
        self.run_24_72_report()
        input("\nFinished all three reports. Keep on truckin'!\n\n(Press Enter.)\n")

    # Runs the Daily Census report. Default values are acceptable; once the page loads, all that happens is the Run button is clicked.
    def run_daily_census_rep(self):
        print("\nAttempting to run Daily Census report...")

        if self.driver.get_url(self.driver.main_win_handle, "https://www24.pointclickcare.com/enterprisereporting/setup.xhtml?reportId=1014") == False: return

        # When the report is run the first time, no problems. When run again, without a delay, an error is thrown ("element click intercepted...is not clickable...Other element would receive the click"). Never quite figured out why, so this delay is for running the report again.
        sleep(1)

        run_button = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[2]/div[2]/div/div[1]/div/div/div[1]/div[4]/button[1]",
            f"Daily Census run report button. Report will not be run."
        )
        if run_button == False: return False
        if self.driver.click_ele(
                self.driver.main_win_handle,
                run_button,
                "the Daily Census run report button. Report will not be run."
        ) == False: return False

        # PCC takes a moment loading the report, and if self.driver navigates to another tab and begins working there too quickly, the report will not generate; this tab appears to get caught in a loop.
        sleep(2)

    def run_24_72_report_72(self): self.run_24_72_report(rep_24_or_72 = "72")

    def run_24_72_report_24(self): self.run_24_72_report(rep_24_or_72 = "24")

    def run_24_72_report(self, rep_24_or_72 = None):
        print("\nAttempting to run 24-Hour Summary report...")

        if self.driver.get_url(
                self.driver.main_win_handle,
                "https://www24.pointclickcare.com/enterprisereporting/setup.xhtml?reportId=2024"
        ) == False: return False

        if rep_24_or_72 == None:
            if datetime.datetime.now().weekday() == 0:
                last_72_hours_button = self.driver.find_ele(
                    self.driver.main_win_handle,
                    "xpath",
                    "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[3]/span[4]",
                    "Last 72 hours radio button"
                )
                if last_72_hours_button == False: return False
                if self.driver.click_ele(
                        self.driver.main_win_handle,
                        last_72_hours_button,
                        "Last 72 hours radio button"
                ) == False: return False
            else:
                last_24_hours_button = self.driver.find_ele(
                    self.driver.main_win_handle,
                    "xpath",
                    "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[2]/span[4]",
                    "Last 24 hours radio button"
                )
                if last_24_hours_button == False: return False
                if self.driver.click_ele(
                        self.driver.main_win_handle,
                        last_24_hours_button,
                        "last 24 hours radio button"
                ) == False: return False
        elif rep_24_or_72 == "24":
            last_24_hours_button = self.driver.find_ele(
                self.driver.main_win_handle,
                "xpath",
                "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[2]/span[4]",
                "Last 24 hours radio button"
            )
            if last_24_hours_button == False: return False
            if self.driver.click_ele(
                    self.driver.main_win_handle,
                    last_24_hours_button,
                    "last 24 hours radio button"
            ) == False: return False
        else:
            last_72_hours_button = self.driver.find_ele(
                self.driver.main_win_handle,
                "xpath",
                "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[3]/span[4]",
                "Last 72 hours radio button"
            )
            if last_72_hours_button == False: return False
            if self.driver.click_ele(
                    self.driver.main_win_handle,
                    last_72_hours_button,
                    "Last 72 hours radio button"
            ) == False: return False

        run_now_button = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/div[2]/div[2]/div/div[1]/div/div/div[1]/div[4]/button[1]/span",
            "RUN NOW button"
        )
        if run_now_button == False: return False
        if self.driver.click_ele(
                self.driver.main_win_handle,
                run_now_button,
                "RUN NOW button"
        ) == False: return False

    def run_case_mix_detail(self):
        print("\nAttempting to run Case Mix Detail report...")

        if self.driver.get_url(
                self.driver.main_win_handle,
                "https://www24.pointclickcare.com/care/reports/rp_censuscasemix.jsp"
        ) == False: return False

        run_report_button = self.driver.find_ele(
            self.driver.main_win_handle,
            "id",
            "runButton",
            "Run Report button"
        )
        if run_report_button == False: return False
        if self.driver.click_ele(
                self.driver.main_win_handle,
                run_report_button,
                "Run Report button"
        ) == False: return False

# -----------------------------MISC METHODS-----------------------------
    # Easy way to clear the console anytime.
    def clear_console(self):
        self.driver.clear_console()
        print(logo)
        print("********************************************************************************\n**********************************BETA VERSION**********************************\n********************************************************************************\n")
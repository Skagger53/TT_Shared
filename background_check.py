import sys

if __name__ == "__main__":
    print("This is a supporting module. Do not execute.")
    sys.exit()

from webdriver_framework import WebdriverMain
from time import sleep

class BackgroundCheck:
    def __init__(self):
        self.driver = WebdriverMain(window_x = 1000, window_y = 800)

    # Opens a new tab and updates self.driver.main_win_handle to that new tab
    def new_tab(self):
        self.driver.driver.execute_script("window.open('');")

        try:
            self.driver.switch_window(self.driver.main_win_handle, self.driver.driver.window_handles[-1])
            self.driver.main_win_handle = self.driver.driver.current_window_handle
        except Exception as switch_to_new_tab_e:
            self.driver.display_err_msg(switch_to_new_tab_e, "Failed to switch to newly opened tab.\n\nPress Enter.\n")

    # MN Public Criminal History search
    def mpch_search(self, first_name, last_name, dob):
        if self.driver.get_url(self.driver.main_win_handle, "https://chs.state.mn.us/Search/ChsSearch") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "xpath", "/html/body/div/form/div[1]/input", last_name, "MN Public Criminal History last name field") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "xpath", "/html/body/div/form/div[2]/input", first_name, "MN Public Criminal History first name field") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "xpath", "/html/body/div/form/div[4]/input", dob, "MN Public Criminal History DOB field") == False: return

        sleep(1) # Pressing the Search button immediately doesn't seem to work properly; the site doesn't register it. One second seems to work. (Also using self.driver.find_enter_text_enter() above doesn't seem to work.)
        submit_btm = self.driver.find_ele(self.driver.main_win_handle, "xpath", "/html/body/div/form/button", "MN Public Criminal History Submit Button")
        if submit_btm == False: return
        self.driver.click_ele(self.driver.main_win_handle, submit_btm, "MN Public Criminal History Submit Button")

    def nsopw_search(self, first_name, last_name): # National Sex Offender Public Website
        self.new_tab()

        if self.driver.get_url(self.driver.main_win_handle, "https://www.nsopw.gov/") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "id", "searchFirstName", first_name, "National Sex Offender Public Website first name field") == False: return

        self.driver.find_enter_text_enter(self.driver.main_win_handle, "id", "searchLastName", last_name, "National Sex Offender Public Website last name field")

    def mtcpa_search(self, first_name, last_name, dob): # Minnesota Trial Court Public Access
        self.new_tab()

        if self.driver.get_url(self.driver.main_win_handle, "https://pa.courts.state.mn.us/") == False: return

        if self.driver.find_click(self.driver.main_win_handle, "link_text", "Criminal/Traffic/Petty Case Records", "MN Trial Court Public Access 'Criminal/Traffic/Petty Case Records' link text") == False: return

        search_by_dropdown = self.driver.find_ele(self.driver.main_win_handle, "id", "SearchBy", "MN Trial Court Public Access search by drop-down menu")
        defendant_option = self.driver.find_ele(self.driver.main_win_handle, "xpath", "/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[4]/td[2]/table/tbody/tr/td[2]/select/option[2]", "MN Trial Court Public Access defendant option in search by drop-down menu")
        if search_by_dropdown == False or defendant_option == False: return
        if self.driver.click_ele(self.driver.main_win_handle, search_by_dropdown, "MN Trial Court Public Access search by drop-down menu") == False: return
        sleep(.25)
        if self.driver.click_ele(self.driver.main_win_handle, defendant_option, "MN Trial Court Public Access defendant option in search by drop-down menu") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "id", "LastName", last_name, "MN Trial Court Public Access last name field") == False: return

        if self.driver.find_enter_text(self.driver.main_win_handle, "id", "FirstName", first_name, "MN Trial Court Public Access first name field") == False: return

        self.driver.find_enter_text(self.driver.main_win_handle, "id", "DateOfBirth", dob, "MN Trial Court Public Access date of birth field")
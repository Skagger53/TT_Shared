import sys

if __name__ == "__main__":
    print("This is a supporting module. Do not execute.")
    sys.exit()

from webdriver_framework import WebdriverMain
from time import sleep

class BackgroundCheck:
    def __init__(self, settings_background_check):
        self.settings_background_check = settings_background_check

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
        if self.driver.get_url(
                self.driver.main_win_handle,
                self.settings_background_check["url_mpch"]
        ) == False: return

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mpch_lname"][0],
                self.settings_background_check["ele_mpch_lname"][1],
                last_name,
                self.settings_background_check["ele_mpch_lname"][2]
        ) == False: return

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mpch_fname"][0],
                self.settings_background_check["ele_mpch_fname"][1],
                first_name,
                self.settings_background_check["ele_mpch_fname"][2]
        ) == False: return

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mpch_dob"][0],
                self.settings_background_check["ele_mpch_dob"][1],
                dob,
                self.settings_background_check["ele_mpch_dob"][2]
        ) == False: return

        sleep(1) # Pressing the Search button immediately doesn't seem to work properly; the site doesn't register it. One second seems to work. (Also using self.driver.find_enter_text_enter() above doesn't seem to work.)
        submit_btm = self.driver.find_ele(
            self.driver.main_win_handle,
            self.settings_background_check["ele_mpch_submit_button"][0],
            self.settings_background_check["ele_mpch_submit_button"][1],
            self.settings_background_check["ele_mpch_submit_button"][2]
        )
        if submit_btm == False: return
        self.driver.click_ele(
            self.driver.main_win_handle,
            submit_btm,
            "MN Public Criminal History Submit Button"
        )

    def nsopw_search(self, first_name, last_name): # National Sex Offender Public Website
        self.new_tab()

        if self.driver.get_url(
                self.driver.main_win_handle,
                self.settings_background_check["url_nsopw"]
        ) == False: return

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_nsopw_fname"][0],
                self.settings_background_check["ele_nsopw_fname"][1],
                first_name,
                self.settings_background_check["ele_nsopw_fname"][2]
        ) == False: return

        self.driver.find_enter_text_enter(
            self.driver.main_win_handle,
            self.settings_background_check["ele_nsopw_lname"][0],
            self.settings_background_check["ele_nsopw_lname"][1],
            last_name,
            self.settings_background_check["ele_nsopw_lname"][2]
        )

    def mtcpa_search(self, first_name, last_name, dob): # Minnesota Trial Court Public Access
        self.new_tab()

        if self.driver.get_url(
                self.driver.main_win_handle,
                self.settings_background_check["url_mtcpa"]
        ) == False: return


        if self.driver.find_click(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mtcpa_ctpc_link"][0],
                self.settings_background_check["ele_mtcpa_ctpc_link"][1],
                self.settings_background_check["ele_mtcpa_ctpc_link"][2]
        ) == False: return

        search_by_dropdown = self.driver.find_ele(
            self.driver.main_win_handle,
            self.settings_background_check["ele_mtcpa_drop_down"][0],
            self.settings_background_check["ele_mtcpa_drop_down"][1],
            self.settings_background_check["ele_mtcpa_drop_down"][2]
        )
        defendant_option = self.driver.find_ele(
            self.driver.main_win_handle,
            "xpath",
            "/html/body/form/table[4]/tbody/tr/td/table/tbody/tr[4]/td[2]/table/tbody/tr/td[2]/select/option[2]",
            "MN Trial Court Public Access defendant option in search by drop-down menu"
        )
        if search_by_dropdown == False or defendant_option == False: return
        if self.driver.enter_text_ele(
                self.driver.main_win_handle,
                search_by_dropdown,
                "D",
                "MN Trial Court Public Access search by drop-down menu"
        ) == False: return
        sleep(.25)

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mtcpa_lname"][0],
                self.settings_background_check["ele_mtcpa_lname"][1],
                last_name,
                self.settings_background_check["ele_mtcpa_lname"][2]
        ) == False: return

        if self.driver.find_enter_text(
                self.driver.main_win_handle,
                self.settings_background_check["ele_mtcpa_fname"][0],
                self.settings_background_check["ele_mtcpa_fname"][1],
                first_name,
                self.settings_background_check["ele_mtcpa_fname"][2]
        ) == False: return

        self.driver.find_enter_text(
            self.driver.main_win_handle,
            self.settings_background_check["ele_mtcpa_dob"][0],
            self.settings_background_check["ele_mtcpa_dob"][1],
            dob,
            self.settings_background_check["ele_mtcpa_dob"][2]
        )
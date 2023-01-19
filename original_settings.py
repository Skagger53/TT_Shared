webdriver_settings_pcc = {
    "pcc_login_url": "https://login.pointclickcare.com/home/userLogin.xhtml?_gl=1*1n0q4b8*_ga*MTgzNzMwOTY1Ny4xNjU4ODQzNTI2*_ga_NBXHRQDSJE*MTY2MTE3Nzc1NC4zNi4wLjE2NjExNzc3NTQuNjAuMC4w&_ga=2.234057950.1359605354.1661177755-1837309657.1658843526",
    "username": ("id", "username", "username entry"),
    "next_button": ("id", "id-next", "next button"),
    "password": ("id", "password", "password entry"),
    "login_validation": ("id", "QTF_FacilityMessages", "login page. Invalid credentials or denied PCC connection attempt?"),
    "search_box": ("id", "searchField", "search entry"),
    "url_daily_census": "https://www24.pointclickcare.com/enterprisereporting/setup.xhtml?reportId=1014",
    "ele_daily_census_run_report": ("xpath", "/html/body/div[2]/div[2]/div/div[1]/div/div/div[1]/div[4]/button[1]", f"Daily Census run report button. Report will not be run."),
    "url_24_72_report": "https://www24.pointclickcare.com/enterprisereporting/setup.xhtml?reportId=2024",
    "ele_72_report_radio": ("xpath", "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[3]/span[4]", "Last 72 hours radio button"),
    "ele_24_report_radio": ("xpath", "/html/body/div[2]/div[2]/div/div[2]/div/div[5]/div[1]/label[2]/span[4]", "Last 24 hours radio button"),
    "ele_24_72_report_run_now_button": ("xpath", "/html/body/div[2]/div[2]/div/div[1]/div/div/div[1]/div[4]/button[1]/span", "RUN NOW button"),
    "url_case_mix_detail": "https://www24.pointclickcare.com/care/reports/rp_censuscasemix.jsp",
    "ele_case_mix_detail_run_button": ("id", "runButton", "Run Report button"),
    "window_x": 1200,
    "window_y": 900
}

settings_background_check = {
    "url_mpch": "https://chs.state.mn.us/Search/ChsSearch",
    "ele_mpch_lname": ("xpath", "/html/body/div/form/div[1]/input", "MN Public Criminal History last name field"),
    "ele_mpch_fname": ("xpath", "/html/body/div/form/div[2]/input", "MN Public Criminal History first name field"),
    "ele_mpch_dob": ("xpath", "/html/body/div/form/div[4]/input", "MN Public Criminal History DOB field"),
    "ele_mpch_submit_button": ("xpath", "/html/body/div/form/button", "MN Public Criminal History Submit Button"),
    "url_nsopw": "https://www.nsopw.gov/",
    "ele_nsopw_fname": ("id", "searchFirstName", "National Sex Offender Public Website first name field"),
    "ele_nsopw_lname": ("id", "searchLastName", "National Sex Offender Public Website last name field"),
    "url_mtcpa": "https://pa.courts.state.mn.us/",
    "ele_mtcpa_ctpc_link": ("link_text", "Criminal/Traffic/Petty Case Records", "MN Trial Court Public Access 'Criminal/Traffic/Petty Case Records' link text"),
    "ele_mtcpa_drop_down": ("id", "SearchBy", "MN Trial Court Public Access search by drop-down menu"),
    "ele_mtcpa_lname": ("id", "LastName", "MN Trial Court Public Access last name field"),
    "ele_mtcpa_fname": ("id", "FirstName", "MN Trial Court Public Access first name field"),
    "ele_mtcpa_dob": ("id", "DateOfBirth", "MN Trial Court Public Access date of birth field")
}

settings_mnits = {
    "url_mnits": "https://mn-its.dhs.state.mn.us/pr/trans/elig/eligrequest",
    "ele_username": ("id", "userid", "MN-ITS username login field. Is the site down or are you already logged in?"),
    "ele_password": ("id", "password", "MN-ITS password field."),
    "ele_validation_item": ("id", "mnitsId", "MN-ITS home page (after login). Is the site down?"),
    "ele_clickable": ("tag_name", "h5", "MN-ITS eligibility query page H5 tag (page title beginning 'Minnesota Department of...'). Is the MN-ITS query page open?"),
    "ele_lookup_button": ("xpath", "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[4]/td[2]/table/tbody/tr/td[2]/input", "MN-ITS eligibility query page Lookup button."),
    "ele_fac_radio": ("xpath", "/html/body/div/div[3]/div[2]/div[2]/div/table/tbody/tr/td[1]/input", "facility radio button selection in MN-ITS query pop-out window (from Lookup button)."),
    "ele_submit_button": ("id", "submitButton", "Submit button in MN-ITS query pop-out window (from Lookup button)."),
    "ele_taxon_code": ("xpath", "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[6]/td[2]/div/button/div/div/div", "MN-ITS eligibility query page Taxonomy Code Qualifier drop-down menu."),
    "ele_taxon_ad": ("xpath", "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[6]/td[2]/div/div/div/ul/li[2]", "MN-ITS eligibility query page AD Admitting option from Taxonomy Code Qualifier drop-down menu."),
    "ele_submit": ("xpath", "/html/body/div[3]/div[3]/div[1]/form/table/tbody/tr[26]/td/input[1]", "MN-ITS eligibility query page Submit button.")
}
# constant parameters
import subprocess
import time
from appium.webdriver.common.appiumby import AppiumBy

DEVICE1_NAME = "PT99653CA1AC1800106"
PLATFORM_VERSION_1 = "11"
DEVICE2_NAME = "PT99652CA1AC0700134"
PLATFORM_VERSION_2 = "11"
# different app packages
DIALER_APP_PACKAGE = 'com.google.android.dialer' # or "com.android.phone"
MSG_APP_PACKAGE = "com.android.mms"
CONTACTS_APP_PACKAGE = "com.google.android.contacts"
PLAYSTORE_APP_PACKAGE = "com.android.vending"
PLAYSTORE_APP_ACTIVITY = "com.google.android.finsky.activities.MainActivity"
CAMERA_APP_PACKAGE = "com.huawei.camera"
CHROME_APP_PACKAGE = "com.android.chrome"
BG_APPS = [CONTACTS_APP_PACKAGE, MSG_APP_PACKAGE, CAMERA_APP_PACKAGE, CHROME_APP_PACKAGE, PLAYSTORE_APP_PACKAGE]

PH_NUMBER = "9614929765"
CALL_DURATION = 5
APP_NAME = "Sudoku offline"  # Complete name of the app available in PlayStore(** Case Sensitive)

# desired capabilities dictionary
desired_cap = {
    "appium:deviceName": DEVICE1_NAME,
    "platformName": "Android",
    "appium:platformVersion": PLATFORM_VERSION_1,
    "appium:adbExecTimeout": "30000",
    "appium:automationName": "UiAutomator2",
    "appium:uiautomator2ServerInstallTimeout": "90000",
    "appium:noReset": "true",
    "appium:fullReset": "false"
}

desired_cap_2 = desired_cap.copy()
desired_cap_2["appium:deviceName"] = DEVICE2_NAME
desired_cap_2["appium:platformVersion"] = PLATFORM_VERSION_2

desired_cap_PlayStore = desired_cap.copy()
desired_cap_PlayStore["appium:appPackage"] = PLAYSTORE_APP_PACKAGE
desired_cap_PlayStore["appium:appActivity"] = PLAYSTORE_APP_ACTIVITY
desired_cap_PlayStore["appium:automationName"] = "Appium"

# Initiating test report
report = ['Main test case', 'Detailed step', 'Intended number of tests', 'Start Time', 'End Time', 'Duration',
          'Actual number of tests', 'Pass', 'Fail', 'Success Rate', 'Remarks', 'Details']


def create_contact(driver, n=50):
    # driver.press_keycode(3)
    itr = 1
    while itr <= n:
        driver.press_keycode(207)
        time.sleep(1)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Create contact").click()
        time.sleep(1)
        [i.send_keys(f"test{itr}") for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText") if
         i.text == "First name"]
        time.sleep(1)
        [i.send_keys(PH_NUMBER) for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText") if
         i.text == "Phone"]
        time.sleep(1)
        driver.find_element(AppiumBy.ID, "com.google.android.contacts:id/menu_save").click()
        driver.press_keycode(3)
        itr += 1

def contacts():
    # contact list
    contacts = subprocess.check_output(
        f"adb -s {DEVICE1_NAME} shell content query --uri content://com.android.contacts/data/phones/ --projection display_name",
        shell=True)
    l = str(contacts).split("Row:")
    count = len([i for i in l if i.split("=")[-1][:4] == 'test'])
    return count
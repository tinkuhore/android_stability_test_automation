# constant parameters
import subprocess
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

DEVICE1_NAME = "PT99653CA1AC1800106"
PLATFORM_VERSION_1 = "11"
DEVICE2_NAME = "PT99652CA1AC0700134"
PLATFORM_VERSION_2 = "11"
DEVICE3_NAME = "PT19655DA11B0700037"
PLATFORM_VERSION_3 = "12"
# different app packages
DIALER_APP_PACKAGE = 'com.google.android.dialer'  # or "com.android.phone"
MSG_APP_PACKAGE = "com.google.android.apps.messaging"
CONTACTS_APP_PACKAGE = "com.google.android.contacts"
PLAYSTORE_APP_PACKAGE = "com.android.vending"
PLAYSTORE_APP_ACTIVITY = "com.google.android.finsky.activities.MainActivity"
CAMERA_APP_PACKAGE = "com.huawei.camera"
CHROME_APP_PACKAGE = "com.android.chrome"
GMAIL_APP_PACKAGE = "com.google.android.gm"
BG_APPS = [CONTACTS_APP_PACKAGE, MSG_APP_PACKAGE, CAMERA_APP_PACKAGE, CHROME_APP_PACKAGE, PLAYSTORE_APP_PACKAGE]

PH_NUMBER_1 = "7029972335"
PH_NUMBER_2 = "9614929765"
PH_NUMBER_3 = "8240452780"
CALL_DURATION = 5
# Type the body of your message here.
MSG_TEXT = "Nam quis nulla. Integer malesuada. In in enim a arcu imperdiet malesuada. Sed vel lectus. Donec odio urna, tempus molestie, porttitor ut, iaculis quis, sem. Phasellus rhoncus. Aenean id metus id velit"
# Complete name of the app available in PlayStore(** Case Sensitive)
APP_NAME = "Google Tasks"

# Download Links
## 100kb file
# https://file-examples.com/storage/fe8c7eef0c6364f6c9504cc/2017/10/file_example_JPG_100kB.jpg

## 1MB files
# "https://file-examples.com/wp-content/uploads/2017/11/file_example_MP3_1MG.mp3"
# "https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4"
# "https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_1MB.jpg"

## 5MB files


## 10 MB files
# https://freetestdata.com/wp-content/uploads/2022/02/Free_Test_Data_10MB_MP4.mp4

## 30 MB files
# http://mirrors.standaloneinstaller.com/video-sample/jellyfish-25-mbps-hd-hevc.mp4

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

desired_cap_3 = desired_cap.copy()
desired_cap_3["appium:deviceName"] = DEVICE3_NAME
desired_cap_3["appium:platformVersion"] = PLATFORM_VERSION_3

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
        [i.send_keys(PH_NUMBER_2) for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText") if
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


def enable_chat_feature(driver):
    driver.press_keycode(3)
    driver.activate_app(MSG_APP_PACKAGE)
    time.sleep(2)
    driver.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/og_apd_internal_image_view").click()
    time.sleep(1)
    for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
        if i.text == "Messages settings":
            i.click()
            break
    time.sleep(1)
    for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
        if i.text == "Chat features":
            i.click()
            break
    time.sleep(1)
    flag = False
    if driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Switch").get_attribute("checked") == "false":
        driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Switch").click()
        time.sleep(20)
    for i in driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.TextView'):
        if 'Status' in i.text:
            print("Chat Feature -->> ", i.text)
            if i.text.split(' ')[1] == 'Connected':
                flag = True
            else:
                print("You are requested to Verify & Connect Chat Feature.")

    time.sleep(2)
    driver.press_keycode(4)
    driver.press_keycode(4)
    return flag


def disable_chat_feature(driver):
    driver.press_keycode(3)
    driver.activate_app(MSG_APP_PACKAGE)
    time.sleep(2)
    driver.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/og_apd_internal_image_view").click()
    time.sleep(1)
    for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
        if i.text == "Messages settings":
            i.click()
            break
    time.sleep(1)
    for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
        if i.text == "Chat features":
            i.click()
            break
    time.sleep(1)
    if driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Switch").get_attribute("checked") == "true":
        driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Switch").click()
        time.sleep(1)
        driver.find_element(AppiumBy.ID, "android:id/button1").click()
    print("Chat Feature -->> Disabled")
    time.sleep(2)
    driver.press_keycode(4)
    driver.press_keycode(4)
    return True



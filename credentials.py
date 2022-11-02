# constant parameters
DEVICE1_NAME = "J9F4C18206001450"
PLATFORM_VERSION_1 = "9"
DEVICE2_NAME = "Y3215A0210MS040998192"
PLATFORM_VERSION_2 = "6"
HOME_APP_PACKAGE = "com.huawei.android.launcher"
HOME_APP_ACTIVITY = ".unihome.UniHomeLauncher"
# different app packages
DIALER_APP_PACKAGE = 'com.samsung.android.dialer' # or "com.android.phone"
MSG_APP_PACKAGE = "com.android.mms"
CONTACTS_APP_PACKAGE = "com.android.contacts"
PLAYSTORE_APP_PACKAGE = "com.android.vending"
PLAYSTORE_APP_ACTIVITY = "com.google.android.finsky.activities.MainActivity"
CAMERA_APP_PACKAGE = "com.huawei.camera"
CHROME_APP_PACKAGE = "com.android.chrome"
BG_APPS = [CONTACTS_APP_PACKAGE, MSG_APP_PACKAGE, CAMERA_APP_PACKAGE, CHROME_APP_PACKAGE, PLAYSTORE_APP_PACKAGE]

PH_NUMBER = "121"
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

desired_cap_2 = desired_cap
desired_cap_2["appium:deviceName"] = DEVICE2_NAME
desired_cap_2["appium:platformVersion"] = PLATFORM_VERSION_2

desired_cap_PlayStore = desired_cap
desired_cap_PlayStore["appium:appPackage"] = PLAYSTORE_APP_PACKAGE
desired_cap_PlayStore["appium:appActivity"] = PLAYSTORE_APP_ACTIVITY
desired_cap_PlayStore["appium:automationName"] = "Appium"
# Initiating test report
report = ['Main test case', 'Detailed step', 'Intended number of tests', 'Start Time', 'End Time', 'Duration',
          'Actual number of tests', 'Pass', 'Fail', 'Success Rate', 'Remarks', 'Details']

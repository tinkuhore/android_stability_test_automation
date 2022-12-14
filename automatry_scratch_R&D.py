import datetime
import subprocess
import time
import os
from credentials import *
from csv import writer
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

# create csv file if not exists
if not os.path.isfile('automation_stability_test.csv'):
    with open('automation_stability_test.csv', 'a') as f:
        writer(f).writerow(report)


def wifi(iterate):
    """This function Automatically turns ON the WIFI for 10 sec and turns it OFF"""
    print("\n", "-" * 10, ">> WiFi Stability Test <<", "-" * 10)
    # test report
    report[0] = 'Toggle wifi'
    report[1] = 'Turn on wifi, wait for 10 sec, turn off wifi'
    report[2] = iterate
    report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Starting Appium webdriver
    driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
    driver.press_keycode(3)
    driver.set_network_connection(0)

    pass_count, fail_count, test_count = 0, 0, 0
    start = datetime.datetime.now()
    while test_count < iterate:
        try:
            driver.toggle_wifi()
            time.sleep(10)
            driver.toggle_wifi()
            time.sleep(2)
            pass_count += 1

        except Exception as e:
            print(f"Iteration = {test_count}| WIFI ON-OFF Failed! | with Error : {e}")
            fail_count += 1
        test_count += 1
    end = datetime.datetime.now()
    driver.quit()

    # finishing test report
    report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    report[5] = str(end - start).split('.')[0]
    report[6] = test_count
    report[7] = pass_count
    report[8] = fail_count
    report[9] = round((pass_count / test_count) * 100, 2)
    report[10] = None
    report[11] = None

    # insert test report to csv file
    with open('automation_stability_test.csv', 'a') as f:
        writer(f).writerow(report)
        f.close()
    print("\n", "WiFi Testing completed!")


def playstore_test():
    """
    Store front / Download Stability Test
    event 1 -> open and close Play Store
    event 2 -> download and install any native application
    event 3 -> open downloaded application
    event 4 -> delete downloaded application
    """
    print("\n", "-" * 10, ">> Store front / Download Stability Test <<", "-" * 10)
    # test report
    report[0] = 'Store front / Download Stability Test'

    def event1(iterate=20):
        print('\n', " Event 1 : Open and close Play Store")
        report[1] = 'Open and close Play Store'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Starting Appium webdriver
        driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver.press_keycode(3)
        driver.set_network_connection(6)

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Automation Code
                # launch Play Store app
                driver.activate_app("com.android.vending")
                time.sleep(5)

                # PASS or FAIL
                status = driver.query_app_state("com.android.vending")
                if status == 2 or status == 3 or status == 4:
                    pass_count += 1
                else:
                    fail_count += 1

                # Close Play Store
                driver.terminate_app("com.android.vending", timeout=1000)
                time.sleep(2)
            except Exception as e:
                driver.press_keycode(3)
                fail_count += 1
                print(f"Iteration No. {test_count} Failed! with ERROR : {e}")

            test_count += 1
        end = datetime.datetime.now()
        driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", f" Event 1 finished in {report[5]}.")

    def event2(iterate=10):
        print("\n", " Event 2 : download and install any native application")
        report[1] = 'download and install any native application'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # initiate loop variables
        pass_count, fail_count, test_count = 0, 0, 1
        start = datetime.datetime.now()
        while test_count <= iterate:
            # Starting Appium webdriver
            driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_PlayStore)
            try:
                # Automation Code
                driver.set_network_connection(6)
                time.sleep(3)
                # search for given app
                driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Button").click()
                time.sleep(2)
                driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys(APP_NAME.lower())
                time.sleep(2)
                driver.press_keycode(66)
                time.sleep(2)
                # select the exact app
                l1 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                for i in l1:
                    if i.text == APP_NAME:
                        i.click()
                        # start the download if not installed already
                        time.sleep(3)
                        for j in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"):
                            if j.text == "Install":
                                j.click()
                                break
                        time.sleep(5)
                        # PASS or FAIL
                        while True:
                            print("tic tic ")
                            time.sleep(3)
                            play_button = [i.is_enabled() for i in
                                           driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
                                           if i.text == "Play"]
                            if play_button[0]:
                                print("App installed")
                                pass_count += 1
                                # uninstall the app
                                time.sleep(2)
                                for y in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"):
                                    if y.text == "Uninstall":
                                        y.click()
                                time.sleep(2)
                                for y in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"):
                                    if y.text == "Uninstall":
                                        y.click()

                                while True:
                                    print("tic tic ")
                                    time.sleep(3)
                                    install_button = [i.is_enabled() for i in
                                                      driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
                                                      if i.text == "Install"]
                                    if install_button[0]:
                                        print("App uninstalled")
                                        break
                                break
            except Exception as e:
                fail_count += 1
                print(f"Iteration No. {test_count} Failed! with ERROR : {e}")

            # return to play store home page
            # for y in range(2):
            #     driver.press_keycode(4)
            #     time.sleep(2)
            # driver.press_keycode(3)
            test_count += 1
            driver.quit()
        end = datetime.datetime.now()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", f" Event 2 finished in {report[5]}.")

    def event3(iterate=20):
        print("\n", "-" * 50, '\n', "Play Store Event 3 executing ...")
        report[1] = 'open downloaded application'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Starting Appium webdriver
        driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver.press_keycode(3)
        driver.set_network_connection(6)
        # initiate loop variables
        pass_count, fail_count, test_count = 0, 0, 1
        start = datetime.datetime.now()
        try:
            # Automation Code
            # launch Play Store app
            driver.activate_app("com.android.vending")
            time.sleep(5)
            # search for given app
            driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Button").click()
            driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys(APP_NAME.lower())
            time.sleep(2)
            driver.press_keycode(66)
            time.sleep(3)
            # select the exact app
            l1 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            time.sleep(5)
            for i in l1:
                if i.text == APP_NAME:
                    i.click()
                    break

            # get app size and estimate approx download time assuming internet speed > 100 kbps
            wait = 10
            time.sleep(3)
            l2 = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for i in l2:
                print(i.text)
                if "MB" in i.text or "GB" in i.text:
                    app_size = i.text
                    wait = float(app_size.split(" ")[0]) * 10
                    break

            # start the download
            buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
            time.sleep(3)
            buttons[3].click()
            time.sleep(wait)
            open_button = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")[-1]
            time.sleep(3)
            open_button.click()
            time.sleep(3)
            pass_count += 1
            app_id = driver.current_package
            print(app_id)

            while pass_count + fail_count != iterate:
                try:
                    driver.press_keycode(3)
                    driver.activate_app(app_id)
                    time.sleep(5)
                    pass_count += 1
                except Exception as e:
                    driver.press_keycode(3)
                    fail_count += 1
                    print(f"Iteration No. {test_count} Failed! with ERROR : {e}")
                test_count += 1
            driver.remove_app(app_id, timeout=5000)
            end = datetime.datetime.now()
        except Exception as e:
            end = datetime.datetime.now()
            print(f"Failed to download the App with Error - {e}")
        driver.activate_app("com.android.vending")
        driver.press_keycode(4)
        driver.quit()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", f"Event 3 finished in {report[5]}.")

    def event4(iterate=1):
        report[1] = 'delete downloaded application'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    event1(2)
    event2(2)
    event3(2)


def Multitasking_Stability_Test():
    """
    1. Make a call
    2. switch background Apps least 50 times
    3. End the call
    4. Open browser and load Home page
    5. witch background Apps least 50 times
    6. Close browser
    :return: App switch test report in csv file
    """

    def switch_bg_apps(wdriver, iteration=2):
        # test report
        report[0] = 'Multitasking'
        report[1] = 'switch background apps least 50 times'
        report[2] = iteration
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pass_count, fail_count = 0, 0
        start = datetime.datetime.now()
        while pass_count + fail_count < iteration:
            for i in BG_APPS:
                try:
                    wdriver.press_keycode(187)
                    time.sleep(2)
                    wdriver.press_keycode(3)
                    wdriver.activate_app(i)
                    time.sleep(4)
                    wdriver.terminate_app(i, timeout=2000)
                    pass_count += 1
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration - {pass_count + fail_count} Failed! with ERROR : {e}")
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = pass_count + fail_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / (pass_count + fail_count)) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Multitasking Testing completed!")

    print('\n', "-" * 10, ">> Multitasking Stability Test <<", "-" * 10, '\n')

    # Starting Appium webdriver
    driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
    if driver.is_locked():
        driver.unlock()
    driver.press_keycode(3)
    driver.set_network_connection(6)

    # # MAKE A CALL
    try:
        driver.activate_app(DIALER_APP_PACKAGE)
        time.sleep(2)
        [i.click() for i in driver.find_elements(AppiumBy.ID, "androidhwext:id/content") if i.text == "Phone"]
        time.sleep(2)
        [driver.find_element(AppiumBy.ACCESSIBILITY_ID, i).click() for i in PH_NUMBER_1]  # dialing ph no
        driver.find_element(AppiumBy.ID, "com.android.contacts:id/dialButton").click()  # tab dial button
        time.sleep(5)
    except Exception as e:
        print("Unable to make the call. ERROR - ", e)

    # # SWITCH BG APPs
    switch_bg_apps(driver)  # You can change the Iteration value here, default value = 50

    # # END THE CALL
    try:
        driver.press_keycode(6)
        time.sleep(2)
    except Exception as e:
        print("Unable to End the Call. ERROR - ", e)

    # # OPEN BROWSER AND LOAD HOME PAGE
    try:
        driver.activate_app(CHROME_APP_PACKAGE)
        time.sleep(3)
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Home").click()
        time.sleep(3)
    except Exception as e:
        print("Failed to OPEN Browser. ERROR - ", e)

    # # SWITCH BG APPs
    switch_bg_apps(driver)  # You can change the Iteration value here, default value = 50

    # # CLOSE BROWSER
    try:
        driver.terminate_app(CHROME_APP_PACKAGE, timeout=2000)
    except Exception as e:
        print("Failed to CLOSE the BROWSER. ERROR - ", e)
    driver.quit()
    print('\n', "-" * 10, ">> Multitasking Stability Test Completed! <<", "-" * 10, '\n')


def Multimedia_Stability_Test():
    """
    Multimedia Stability Test
    """
    print('\n', "-" * 10, ">> Multimedia Stability Test <<", "-" * 10, '\n')
    report[0] = "Multimedia Stability Test"
    desired_cap_video_camera = {
        "appium:deviceName": DEVICE1_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION_1,
        "appium:appPackage": "com.sec.android.app.camera",
        "appium:appActivity": "com.sec.android.app.camera.Camera",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_Browser = {
        "appium:deviceName": DEVICE1_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION_1,
        "appium:appPackage": "com.android.chrome",
        "appium:appActivity": "com.google.android.apps.chrome.Main",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "Appium",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_mediaplayer = {
        "appium:deviceName": DEVICE1_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION_1,
        "appium:appPackage": "com.kapp.youtube.final",
        "appium:appActivity": "com.kapp.youtube.ui.MainActivity",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_MyFiles = {
        "appium:deviceName": DEVICE1_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION_1,
        "appium:appPackage": "com.sec.android.app.myfiles",
        "appium:appActivity": "com.sec.android.app.myfiles.external.ui.MainActivity",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"

    }
    desired_cap_Theme = {
        "appium:deviceName": DEVICE1_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION_1,
        "appium:appPackage": "com.samsung.android.themestore",
        "appium:appActivity": "com.samsung.android.themestore.activity.LauncherfromSetting",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"

    }

    def record_video_30s(iterate=1):
        print("Event 1 : Record a 30s Video ")
        # test report initiation
        report[1] = 'Record a 30s Video'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                video_mode = driver1.find_element(AppiumBy.XPATH,
                                                  '//android.widget.SeekBar[@content-desc="Photo, Mode"]/android.view.ViewGroup[3]/android.widget.LinearLayout')
                video_mode.click()
                time.sleep(2)
                capture_start = driver1.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/center_button')
                capture_start.click()
                time.sleep(30)
                capture_stop = driver1.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/center_button')
                capture_stop.click()
                driver1.press_keycode(4)
                pass_count += 1
                driver1.quit()
                # pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Video Recording Failed! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Video Recording completed!")

    def play_last_video(iterate=1):
        print("Event 2 : Play back a 30s Video ")
        # test report initiation
        report[1] = 'Play back a 30s Video'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver1.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                time.sleep(2)
                play_video = driver1.find_element(AppiumBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup[2]/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout')
                play_video.click()
                time.sleep(30)
                driver1.press_keycode(4)
                driver1.press_keycode(4)
                pass_count += 1

                driver1.quit()
                # pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Video Play back Failed! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Video playback completed!")

    def delete_last_video(iterate=1):
        print("Event 3 : Delete a Video ")
        # test report initiation
        report[1] = 'Delete a Video'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver1.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                time.sleep(2)
                delete_video = driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                delete_video.click()
                time.sleep(2)
                move = driver1.find_element(AppiumBy.ID, 'android:id/button1')
                move.click()
                driver1.press_keycode(4)
                driver1.press_keycode(4)
                driver1.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Video Play back Failed! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Video Deleted Successfully!")

    def take_picture(iterate=20):
        print("Event 4 : Take a picture ")
        # test report initiation
        report[1] = 'Take a picture'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                # front_rotate=driver2.find_element(AppiumBy.ID,'com.sec.android.app.camera:id/right_button')
                # front_rotate.click()
                capture_start = driver1.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/normal_overlap_image')
                capture_start.click()
                time.sleep(5)
                driver1.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to take picture! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Picture clicking automation completed!")

    def open_picture(iterate=20):
        print("Event 5 : Open picture ")
        # test report initiation
        report[1] = 'Open picture'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver1.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                driver1.press_keycode(4)
                driver1.press_keycode(4)
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to open pictures! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Picture opening automation completed!")

    def delete_picture(iterate=20):
        print("Event 6 : Delete picture ")
        # test report initiation
        report[1] = 'Delete picture'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver1.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                time.sleep(2)
                delete_video = driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                delete_video.click()
                time.sleep(2)
                move = driver1.find_element(AppiumBy.ID, 'android:id/button1')
                move.click()
                driver1.press_keycode(4)
                driver1.press_keycode(4)
                driver1.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to Delete pictures! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Picture deleting automation completed!")

    def youtube_stream_browser(iterate=10):
        print("Event 7 : Play video streaming using device browser ")
        # test report initiation
        report[1] = 'Play video streaming using device browser'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_Browser)
                driver1.set_network_connection(6)  # Turn on Wi-Fi and mobile data
                driver1.get("https://m.youtube.com/watch?v=Ro971vwsgPg")
                driver1.press_keycode(66)
                time.sleep(15)

                driver1.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to play video! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Play video streaming automation completed!")

    def open_close_music_player(iterate=20):
        print("Event 8 : Open and Close Music plyer ")
        # test report initiation
        report[1] = 'Open and Close Music plyer'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_mediaplayer)
                driver1.press_keycode(209)
                time.sleep(4)
                driver1.press_keycode(128)
                driver1.press_keycode(86)
                driver1.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to open & close Music player! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Open & Close Music player automation completed!")

    def open_musicplayer_play_music(iterate=50):
        print("Event 9 : Open Music player and play a song ")
        # test report initiation
        report[1] = 'Open Music player and play a song'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver3 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_MyFiles)
                driver3.press_keycode(209)  # open
                driver3.press_keycode(222)  # switch track
                driver3.press_keycode(85)  # play
                time.sleep(15)
                driver3.press_keycode(87)
                driver3.press_keycode(127)
                # driver3.press_keycode(86)
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to play music! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Open and play music automation completed!")

    def close_music_player(iterate=1):
        print("Event 10 : Close Music Player ")
        # test report initiation
        report[1] = 'Close Music Player'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver4 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_mediaplayer)
                driver4.press_keycode(209)
                time.sleep(4)
                driver4.press_keycode(128)
                driver4.press_keycode(86)
                driver4.quit()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to Close Music player! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Close music player automation completed!")

    def set_theme(iterate=20):
        print("Event 11 : Set Theme ")
        # test report initiation
        report[1] = 'Set Theme'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_Theme)
                time.sleep(7)
                downloaded_theme = driver.find_element(AppiumBy.XPATH,
                                                       '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]')
                downloaded_theme.click()
                time.sleep(3)
                try:
                    select_theme = driver.find_element(AppiumBy.XPATH,
                                                       '//android.view.ViewGroup[@content-desc="Default"]/android.widget.ImageView')
                    select_theme.click()
                    time.sleep(2)
                    Apply_confirm = driver.find_element(AppiumBy.ID, 'android:id/button1')
                    Apply_confirm.click()
                except:
                    select_theme = driver.find_element(AppiumBy.XPATH,
                                                       '//android.view.ViewGroup[@content-desc="Video Dark technology light HD blue"]/android.widget.ImageView')
                    select_theme.click()
                    time.sleep(2)
                    Apply_theme = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Apply')
                    Apply_theme.click()
                    time.sleep(2)
                    Apply_confirm = driver.find_element(AppiumBy.ID, 'android:id/button1')
                    Apply_confirm.click()
                pass_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to Set Theme! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Set Theme automation completed!")

    record_video_30s(2)
    play_last_video(2)
    delete_last_video(2)
    take_picture(2)
    open_picture(2)
    delete_picture(2)
    youtube_stream_browser(2)
    open_close_music_player(2)
    open_musicplayer_play_music(2)
    close_music_player(2)
    set_theme(2)
    print('\n', "-" * 10, ">> Multimedia Stability Test Completed! <<", "-" * 10, '\n')


def Menu_Navigation_Stability_Test():
    def Meny_Nav_Browser():
        pass

    def Meny_Nav_Calculator():
        pass

    def Meny_Nav_Calender():
        pass

    def Meny_Nav_Camera():
        pass

    def Meny_Nav_Clock():
        pass

    def Meny_Nav_Contact():
        pass

    def Meny_Nav_Downloads():
        pass

    def Meny_Nav_Email():
        pass

    def Meny_Nav_Files():
        pass

    def Meny_Nav_Messaging():
        pass

    def Meny_Nav_Music():
        pass

    def Meny_Nav_Phone():
        pass

    def Meny_Nav_Photos():
        pass

    def Meny_Nav_Radio():
        pass

    def Meny_Nav_Settings():
        pass


def Browser_Stability_Test():
    """
    Browser Stability Test
    :return:
    """
    print('\n', "-" * 10, ">> Browser Stability Test <<", "-" * 10, '\n')
    report[0] = "Browser Stability Test"
    desired_cap_Browser = desired_cap
    desired_cap_Browser["appium:appPackage"] = "com.android.chrome"
    desired_cap_Browser["appium:appActivity"] = "com.google.android.apps.chrome.Main"

    def open_nativeBrowser_ATT_homepage(iterate):
        print("Event 1 : Open Native Browser ATT Homepage ")
        # test report initiation
        report[1] = 'Open Native Browser ATT Homepage'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver3 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_Browser)
                driver3.set_network_connection(6)  # Turn on wifi and mobile data
                driver3.get("https://www.att.com")
                # driver3.press_keycode(66)
                time.sleep(4)

                driver3.quit()
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count}| Failed to open ! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Open Native Browser automation completed!")

    def navigte_link_to_link_ATT_homepage(iterate):
        print('\n', "Event 2 : Navigate Link to Link ATT Homepage ")
        # test report initiation
        report[1] = 'Navigate Link to Link ATT Homepage'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver3 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_Browser)
                driver3.set_network_connection(6)
                # Turn on wifi and mobile data
                # time.sleep(2)
                driver3.get("https://www.att.com")
                # driver3.press_keycode(66)
                time.sleep(4)
                first_link = driver3.find_element(AppiumBy.ACCESSIBILITY_ID, 'Phones & devices')
                first_link.click()
                time.sleep(3)
                second_link = driver3.find_element(AppiumBy.ACCESSIBILITY_ID, 'Wireless')
                second_link.click()
                time.sleep(3)
                third_link = driver3.find_element(AppiumBy.ACCESSIBILITY_ID, 'Internet')
                third_link.click()
                time.sleep(3)
                pass_count += 1

                driver3.quit()

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to Navigate Link to Link ATT Homepage ! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Navigate Link to Link ATT Homepage automation completed!")

    def top_websites(iterate):
        print('\n', "Event 3 : Top websites ")
        # test report initiation
        report[1] = 'Top websites'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver3 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_Browser)
                driver3.set_network_connection(6)  # Turn on wifi and mobile data
                driver3.get("https://www.cricketwireless.com")
                time.sleep(4)
                driver3.get("https://www.att.com")
                time.sleep(4)
                driver3.get("https://www.amazon.com")
                time.sleep(4)
                driver3.get("https://www.youtube.com")
                time.sleep(4)
                driver3.get("https://www.cnn.com")
                time.sleep(4)
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count}| Failed to open Top websites ! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Top websites automation completed!")

    open_nativeBrowser_ATT_homepage(2)
    navigte_link_to_link_ATT_homepage(2)
    top_websites(2)
    print('\n', "-" * 10, ">> Browser Stability Test Completed! <<", "-" * 10, '\n')


def Email_Stability_Test():
    """
    Email Stability Test
    """
    print('\n', "-" * 10, ">> Email Stability Test <<", "-" * 10, '\n')
    report[0] = "Email Stability Test"

    def send_email_no_attachment(iterate=40):
        print("Event 1 : Send mail without attachment ")
        # test report initiation
        report[1] = 'Send mail without attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.press_keycode(3)
                driver1.set_network_connection(6)  # turn on both, WiFi & Cellular Data
                time.sleep(3)
                driver1.activate_app(GMAIL_APP_PACKAGE)
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, 'com.google.android.gm:id/compose_button').click()
                time.sleep(2)
                driver1.find_element(AppiumBy.XPATH,
                                     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.EditText").send_keys(
                    'swarnendu0298@gmail.com')
                driver1.press_keycode(66)
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText"):
                    if i.text == "Subject":
                        i.send_keys("Here is my subject line!!")
                    if i.text == "Compose email":
                        i.send_keys("Hello This is my message of 30 characters. This is pre-loaded message using "
                                    "automation concept.//Thanks ")

                time.sleep(2)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send').click()
                time.sleep(3)
                # Pass or Fail & delete mail
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer').click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Sent":
                        i.click()
                        break
                time.sleep(2)
                try:
                    for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                        if i.text == "Here is my subject line!!":
                            pass_count += 1
                            i.click()
                            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete').click()
                            break
                    time.sleep(2)
                    driver1.press_keycode(4)
                    driver1.press_keycode(3)
                    driver1.quit()
                except:
                    print("Failed to Delete as touch sensor did not work.")
                    fail_count += 1

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to sent Mail! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Send mail without attachment automation completed!")

    def send_email_with_attachment(iterate=40):
        print("Event 2 : Send mail with attachment ")
        # test report initiation
        report[1] = 'Send mail with attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.press_keycode(3)
                driver1.set_network_connection(6)  # turn on both, WiFi & Cellular Data
                time.sleep(3)
                driver1.activate_app(GMAIL_APP_PACKAGE)
                time.sleep(2)
                compose_button = driver1.find_element(AppiumBy.ID, 'com.google.android.gm:id/compose_button')
                compose_button.click()
                time.sleep(2)
                to_cc_bcc = driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Add Cc/Bcc')
                to_cc_bcc.click()
                receipent = driver1.find_element(AppiumBy.XPATH,
                                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.EditText')
                receipent.send_keys("swarnendu0298@gmail.com")
                driver1.press_keycode(66)
                subject = driver1.find_element(AppiumBy.ID, 'com.google.android.gm:id/subject')
                subject.send_keys("Here is my subject line!!")
                time.sleep(2)
                message_body = driver1.find_element(AppiumBy.XPATH,
                                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.widget.EditText')
                message_body.send_keys(
                    "Hello This is my message of 30 characters. This is pre-loaded message using automation concept.//Thanks ")
                time.sleep(2)
                attachment = driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Attach file')
                attachment.click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Attach file":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                time.sleep(1)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Downloads":
                        i.click()
                        break
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "sample-pdf-file.pdf":
                        i.click()
                        break
                time.sleep(2)
                send_email = driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send')
                send_email.click()
                time.sleep(5)
                # Pass or Fail & delete mail
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer').click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Sent":
                        i.click()
                        break
                time.sleep(2)
                try:
                    for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                        if i.text == "Here is my subject line!!":
                            pass_count += 1
                            i.click()
                            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete').click()
                            break
                    time.sleep(2)
                    driver1.press_keycode(4)
                    driver1.press_keycode(3)
                    driver1.quit()
                except:
                    print("Failed to Delete as touch sensor did not work.")
            except Exception as e:
                print(f"Iteration = {test_count}| Failed to sent Mail! | with Error : {e}")
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Send mail with attachment automation completed!")

    def open_email(iterate=40):
        print("Event 3 : Open mail ")
        # test report initiation
        report[1] = 'Open mail'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.press_keycode(3)
                driver1.set_network_connection(6)  # turn on both, WiFi & Cellular Data
                time.sleep(4)
                driver1.activate_app(GMAIL_APP_PACKAGE)
                time.sleep(2)
                # actions = TouchAction(driver1)
                # actions.tap(x=399, y=626)
                # actions.release().perform()
                # time.sleep(3)
                pass_count += 1
                driver1.terminate_app(GMAIL_APP_PACKAGE)
                driver1.set_network_connection(0)
                driver1.quit()

            except Exception as e:
                print(f"Iteration = {test_count}| Failed to sent Mail! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Open Mail automation completed!")

    # send_email_no_attachment()
    # send_email_with_attachment()
    open_email(2)
    print('\n', "-" * 10, ">> Email Stability Test Completed! <<", "-" * 10, '\n')


def Messaging_Stability_Tests():
    """
    Messaging Stability Tests
    1.Send an SMS maximum number of characters without requiring the message to be segmented from the DUT (50)
    2.Send a MMS with an audio attachment from the device under test (50)
    3.Send a MMS with a video attachment from the device under test (50)
    4.Send a MMS with a picture attachment from the device under test (50)
    5.Open a MMS with a 1MB audio attachment or largest size supported by the device (50)
    6.Open a MMS with 1MB video or largest size supported by the device (50)
    7.Open a MMS with a 1MB image or largest size supported by the device (50)
    8.Open a SMS (50)
    """
    print('\n', "-" * 10, ">> Messaging Stability Tests <<", "-" * 10, '\n')
    report[0] = 'Messaging Stability Test'

    def send_sms_maxChar(iterate=20):
        """This function Automatically test the SMS service of the Messaging app."""
        print('\n', "Event 1 : Add an appointment to the Calender ")
        # test report initiation
        report[
            1] = 'Send an SMS maximum number of characters with out requiring the message to be segmented from the DUT.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Automation Code
                # send the message
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                    PH_NUMBER_2)
                driver1.press_keycode(66)
                time.sleep(1)
                driver1.find_element(AppiumBy.ID,
                                     'com.google.android.apps.messaging:id/compose_message_text').send_keys(
                    '1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,./;12345678901234567890!@#$%^&*('
                    ')qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfgjklzxcvbnm1234567890qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm12345678901!@#$%^&*()_+asdfghjklqwertyuopzxcvbnm')

                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send SMS').click()
                time.sleep(4)

                # SENT or FAILED
                try:
                    if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Now, SMS').is_enabled():
                        pass_count += 1
                except:
                    fail_count += 1

                # Delete the message
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'More conversation options').click()
                time.sleep(1)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                test_count += 1
                driver1.press_keycode(4)
                driver1.quit()
            except Exception as e:
                fail_count += 1
                print(f"Iteration = {test_count + 1}| Failed to Send an SMS! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def send_mms_with_audio(iterate=20):
        """This function Automatically test the MMS (Audio) service of the Messaging app."""
        print('\n', "Event 2 : Send a MMS with an audio attachment")
        # test report initiation
        report[1] = 'Send a MMS with an audio attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Automation Code
                # send the MMS
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                    PH_NUMBER_2)
                driver1.press_keycode(66)
                time.sleep(2)
                # attatchment section
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.XPATH,
                                     '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                time.sleep(2)
                # file selection
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")[1:]:
                    print(i.text)
                    if i.text == "Downloads":
                        i.click()
                        break
                try:
                    driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "List View").click()
                except:
                    print("List View Enabled")

                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "file_example_MP3_1MG.mp3":
                        print(i.text)
                        i.click()
                        break
                time.sleep(5)
                driver1.find_element(AppiumBy.ID,
                                     'com.google.android.apps.messaging:id/compose_message_text').send_keys(
                    "1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,"
                    "./;12345678901234567890!@#$%^&*(")
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send SMS').click()
                time.sleep(4)

                # SENT or FAILED
                try:
                    if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Now, SMS').is_enabled():
                        pass_count += 1
                except:
                    fail_count += 1

                # Delete the message
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'More conversation options').click()
                time.sleep(1)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                test_count += 1
                driver1.press_keycode(4)
                driver1.quit()
            except Exception as e:
                fail_count += 1
                print(
                    f"Iteration = {test_count + 1}| Failed to 'Send a MMS with an audio attachment'! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def send_mms_with_video(iterate=20):
        """This function Automatically test the MMS (Video) service of the Messaging app."""
        print('\n', "Event 3 : Send a MMS with a video attachment")
        # test report initiation
        report[1] = 'Send a MMS with a video attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Automation Code
                # send the MMS
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                    PH_NUMBER_2)
                driver1.press_keycode(66)
                time.sleep(2)
                # attatchment section
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.XPATH,
                                     '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                time.sleep(2)
                # file selection
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                time.sleep(3)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    print(i.text)
                    if i.text == "Downloads":
                        i.click()
                        break
                # try:
                #     driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "List View").click()
                # except:
                #     print("List View Enabled")
                time.sleep(3)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "file_example_MP4_480_1_5MG.mp4":
                        print(i.text)
                        i.click()
                        break
                time.sleep(5)
                driver1.find_element(AppiumBy.ID,
                                     'com.google.android.apps.messaging:id/compose_message_text').send_keys(
                    "1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,"
                    "./;12345678901234567890!@#$%^&*(")
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send SMS').click()
                time.sleep(4)

                # SENT or FAILED
                try:
                    if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Now, SMS').is_enabled():
                        pass_count += 1
                except:
                    fail_count += 1

                # Delete the message
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'More conversation options').click()
                time.sleep(1)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                test_count += 1
                driver1.press_keycode(4)
                driver1.quit()
            except Exception as e:
                fail_count += 1
                print(f"Iteration = {test_count + 1}| Failed to Send a MMS with a video attachment! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    def send_mms_with_picture(iterate=20):
        """This function Automatically test the MMS (Picture) service of the Messaging app."""
        print('\n', "Event 4 : Send a MMS with a picture")
        # test report initiation
        report[1] = 'Send a MMS with a picture'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Automation Code
                # send the MMS
                driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
                driver1.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                    PH_NUMBER_2)
                driver1.press_keycode(66)
                time.sleep(2)
                # attachment section
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                time.sleep(1)
                driver1.find_element(AppiumBy.XPATH,
                                     '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                time.sleep(2)
                # file selection
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                time.sleep(3)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    print(i.text)
                    if i.text == "Downloads":
                        i.click()
                        break
                try:
                    driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "List View").click()
                except:
                    print("List View Enabled")
                time.sleep(3)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "file_example_JPG_1MB.jpg":
                        print(i.text)
                        i.click()
                        break
                time.sleep(5)
                driver1.find_element(AppiumBy.ID,
                                     'com.google.android.apps.messaging:id/compose_message_text').send_keys(
                    "1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,"
                    "./;12345678901234567890!@#$%^&*(")
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send SMS').click()
                time.sleep(4)

                # SENT or FAILED
                try:
                    if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'Now, SMS').is_enabled():
                        pass_count += 1
                except:
                    fail_count += 1

                # Delete the message
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, 'More conversation options').click()
                time.sleep(1)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                test_count += 1
                driver1.press_keycode(4)
                driver1.quit()
            except Exception as e:
                fail_count += 1
                print(f"Iteration = {test_count + 1}| Failed to Send a MMS with a picture! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 4 completed!")

    def open_mms_with_audio(iterate=50):
        """This function Automatically test the read MMS Audio service of the Messaging app."""
        print('\n', "Event 5 : Open a MMS with a 1MB audio attachment")
        # test report initiation
        report[1] = 'Open a MMS with a 1MB audio attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
                driver2.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/open_search_bar_text_view").click()
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/zero_state_search_box_auto_complete").send_keys(
                    PH_NUMBER_1)
                driver2.press_keycode(66)
                time.sleep(1)
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if PH_NUMBER_1 in i.text:
                        i.click()
                        break
                pass_count += 1

            except Exception as e:
                fail_count += 1
                print(
                    f"Iteration = {test_count + 1}| Failed to Open a MMS with a 1MB audio attachment! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 5 completed!")

    def open_mms_with_video(iterate=50):
        """This function Automatically test the read MMS Video service of the Messaging app."""
        print('\n', "Event 6 : Open a MMS with 1MB video attachment")
        # test report initiation
        report[1] = 'Open a MMS with 1MB video attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
                driver2.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/open_search_bar_text_view").click()
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/zero_state_search_box_auto_complete").send_keys(
                    PH_NUMBER_1)
                driver2.press_keycode(66)
                time.sleep(1)
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if PH_NUMBER_1 in i.text:
                        i.click()
                        break
                pass_count += 1

            except Exception as e:
                fail_count += 1
                print(
                    f"Iteration = {test_count + 1}| Failed to Open a MMS with 1MB video attachment! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 6 completed!")

    def open_mms_with_video(iterate=50):
        """This function Automatically test the read MMS Image service of the Messaging app."""
        print('\n', "Event 6 : Open a MMS with a 1MB image attachment")
        # test report initiation
        report[1] = 'Open a MMS with a 1MB image attachment'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
                driver2.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/open_search_bar_text_view").click()
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/zero_state_search_box_auto_complete").send_keys(
                    PH_NUMBER_1)
                driver2.press_keycode(66)
                time.sleep(1)
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if PH_NUMBER_1 in i.text:
                        i.click()
                        break
                pass_count += 1

            except Exception as e:
                fail_count += 1
                print(
                    f"Iteration = {test_count + 1}| Failed to Open a MMS with a 1MB image attachment! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 7 completed!")

    def open_sms(iterate=50):
        """This function Automatically test the read SMS service of the Messaging app."""
        print('\n', "Event 8 : Open a SMS (MT)")
        # test report initiation
        report[1] = 'Open a SMS (MT)'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
                driver2.activate_app(MSG_APP_PACKAGE)
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/open_search_bar_text_view").click()
                time.sleep(1)
                driver2.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/zero_state_search_box_auto_complete").send_keys(
                    PH_NUMBER_1)
                driver2.press_keycode(66)
                time.sleep(1)
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if PH_NUMBER_1 in i.text:
                        i.click()
                        break
                pass_count += 1

            except Exception as e:
                fail_count += 1
                print(f"Iteration = {test_count + 1}| Failed to Open a SMS (MT)! | with Error : {e}")
            test_count += 1
        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 8 completed!")

    def MMS_with_MAXCHAR_AUDIO(iterate=20):
        """This function Automatically test the MMS service of Messaging app."""
        # test report
        report[0] = 'MMS Automation'
        report[
            1] = 'Send an SMS maximum number of characters with out requiring the message to be segmented from the DUT.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_message_stability)

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            # Automation Code
            # send the MMS
            driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap_message_stability)
            MT_contact = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="???My Jio???"]')
            MT_contact.click()
            time.sleep(2)
            other_option = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Other options')
            other_option.click()
            time.sleep(2)
            audio = driver.find_element(AppiumBy.XPATH,
                                        '//android.widget.LinearLayout[@content-desc="Audio"]/android.widget.RelativeLayout')
            audio.click()
            time.sleep(2)
            voice_recorder_folder = driver.find_element(AppiumBy.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[7]')
            voice_recorder_folder.click()
            time.sleep(2)
            select_audio = driver.find_element(AppiumBy.ID, 'com.sec.android.app.myfiles:id/ripple')
            select_audio.click()
            time.sleep(2)
            done = driver.find_element(AppiumBy.XPATH,
                                       '//android.widget.Button[@content-desc="Done"]/android.view.ViewGroup/android.widget.TextView')
            done.click()
            time.sleep(2)
            text_box = driver.find_element(AppiumBy.ID, 'com.samsung.android.messaging:id/message_edit_text')
            text_box.send_keys(
                '1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,./;12345678901234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfgjklzxcvbnm1234567890qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm12345678901!@#$%^&*()_+asdfghjklqwertyuopzxcvbnm')
            send_message = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send')
            send_message.click()
            time.sleep(20)
            # driver.press_keycode(4)

            # SENT or FAILED
            try:
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Sending') or driver.find_element(
                    AppiumBy.ACCESSIBILITY_ID, 'Sending failed')
                fail_count += 1
            except:
                pass_count += 1
            time.sleep(10)
            delete_settings = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Conversation settings')
            delete_settings.click()
            time.sleep(2)
            delete_message = driver.find_element(AppiumBy.XPATH,
                                                 '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ImageView')
            delete_message.click()
            select_last_message = driver.find_element(AppiumBy.XPATH,
                                                      '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.CheckBox')
            select_last_message.click()
            delete_all = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
            delete_all.click()
            time.sleep(2)
            move_to_recycle = driver.find_element(AppiumBy.ID, 'android:id/button1')
            move_to_recycle.click()
            test_count += 1
            driver.press_keycode(4)
            driver.quit()

        end = datetime.datetime.now()
        # driver.quit()

        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()

    # send_sms_maxChar()
    # send_mms_with_audio()
    # send_mms_with_video()
    # send_mms_with_picture()
    # open_sms()
    # MMS_with_MAXCHAR_AUDIO(2)
    print('\n', "-" * 10, ">> Messaging Stability Tests Completed! <<", "-" * 10, '\n')


def Telephony_Stability_Test():
    """
    Telephony Stability Test
    """
    print('\n', "-" * 10, ">> Telephony Stability Test <<", "-" * 10, '\n')
    report[0] = "Telephony Stability Test"

    def call_from_phone_book(iterate=50):
        print('\n', "Event 1 : Make a Call from Phone Book. ")
        # test report initiation
        report[1] = 'Make a Call from Phone Book.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        if contacts() != iterate:
            create_contact(driver=driver1, n=iterate)
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver1.press_keycode(3)
                time.sleep(1)
                driver1.press_keycode(207)  # contacts
                time.sleep(2)
                driver1.find_element(AppiumBy.ID,
                                     "com.google.android.contacts:id/open_search_bar_text_view").click()  # Search
                time.sleep(3)
                [driver1.press_keycode(ord(i) - 36) for i in "TEST"]
                [driver1.press_keycode(int(i) + 7) for i in str(test_count + 1)]
                driver1.press_keycode(66)  # Enter
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == f"test{test_count + 1}":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Call").click()  # Call
                time.sleep(2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = str(output).split(" ")[4].split("=")[-1][0]  # this can lead to Error
                    if call_state == '1':
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        time.sleep(CALL_DURATION)  # Call Duration
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = str(output).split(" ")[8].split("=")[-1][0]  # this can lead to Error
                        if call_state == '2':
                            pass_count += 1
                            driver1.press_keycode(6)
                        else:
                            fail_count += 1

                        flag = False

                time.sleep(2)
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(3)  # Home

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to make Call from Phone Book ! | with Error : {e}")
            test_count += 1
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def call_from_history(iterate=50):
        print('\n', "Event 2 : Make a Voice Call from History List. ")
        # test report initiation
        report[1] = 'Make a Voice Call from History List.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                driver1.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                [i.click() for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView") if
                 i.text == "Recent"]
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "call test1").click()  # making a Call
                time.sleep(3)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = str(output).split(" ")[4].split("=")[-1][0]  # this can lead to Error
                    if call_state == '1':
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        time.sleep(6)
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = str(output).split(" ")[8].split("=")[-1][0]  # this can lead to Error
                        if call_state == '2':
                            pass_count += 1
                            driver1.press_keycode(6)
                        else:
                            fail_count += 1

                        flag = False
                    # else:
                    #     print(f"Unable to find the Device with name - {DEVICE2_NAME}.")

                driver1.press_keycode(4)

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to make Call from History! | with Error : {e}")
            test_count += 1

        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def receive_a_call(iterate=50):
        print('\n', "Event 3 : Receive a Call ")
        # test report initiation
        report[1] = 'Receive a Call'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                driver1.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "dial").click()  # tab dial button
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = str(output).split(" ")[4].split("=")[-1][0]  # this can lead to Error
                    if call_state == '1':
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        time.sleep(6)
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = str(output).split(" ")[8].split("=")[-1][0]  # this can lead to Error
                        if call_state == '2':
                            pass_count += 1
                            driver1.press_keycode(6)
                        else:
                            fail_count += 1

                        flag = False
                    # else:
                    #     print(f"Unable to find the Device with name - {DEVICE2_NAME}.")

                driver1.press_keycode(4)

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Receive Call ! | with Error : {e}")
            test_count += 1

        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    # Check VoLTE Status
    VoLTE = str(
        subprocess.check_output(f"adb -s {DEVICE1_NAME} shell settings get global volte_vt_enabled", shell=True))
    if '1' in VoLTE:
        print("VoLTE is Enabled.")
        call_from_phone_book(3)
        call_from_history(3)
        receive_a_call(3)
        print('\n', "-" * 10, ">> Telephony Stability Test Completed! <<", "-" * 10, '\n')
    else:
        print(f"VoLTE is Disabled. "
              "Please turn it ON to perform Telephony_Stability_Test")


def Video_Telephony_Stability_Test():
    """
    Telephony Stability Test
    """
    print('\n', "-" * 10, ">> Video Telephony Stability Test <<", "-" * 10, '\n')
    report[0] = "Video Telephony Stability Test"

    def make_vcall_from_phonebook(iterate=50):
        print('\n', "Event 1 : Make a Video Call from Phone Book. ")
        # test report initiation
        report[1] = 'Make a Video Call from Phone Book.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        driver1.set_network_connection(0)
        driver2.set_network_connection(0)

        if contacts() != iterate:
            create_contact(driver=driver1, n=iterate)
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                time.sleep(1)
                driver1.press_keycode(207)  # contacts
                time.sleep(2)
                driver1.find_element(AppiumBy.ID,
                                     "com.google.android.contacts:id/open_search_bar_text_view").click()  # Search
                time.sleep(3)
                [driver1.press_keycode(ord(i) - 36) for i in "TEST"]
                [driver1.press_keycode(int(i) + 7) for i in str(test_count + 1)]
                driver1.press_keycode(66)  # Enter
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == f"test{test_count + 1}":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ID, "com.google.android.contacts:id/verb_video").click()  # Call
                print("-----> MO Called.")
                time.sleep(2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)  # Call Duration
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in
                                      [4, 8]]  # this can lead to Error
                        if '2' in call_state:
                            pass_count += 1
                            driver1.press_keycode(6)
                            print("-----> MO Disconnected.")
                        else:
                            fail_count += 1

                        flag = False

                time.sleep(2)
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(3)  # Home

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to make Video Call from Phone Book ! | with Error : {e}")
            test_count += 1
        driver1.press_keycode(207)  # contacts
        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More options").click()
        time.sleep(1)
        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
            if i.text == "Select all":
                i.click()
                break
        time.sleep(1)
        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Delete").click()
        time.sleep(1)
        driver1.find_element(AppiumBy.ID, "android:id/button1").click()
        time.sleep(1)
        driver1.press_keycode(3)  # Home
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def make_vcall_from_dialer(iterate=50):
        print('\n', "Event 2 : Make a Video Call from Dialer ")
        # test report initiation
        report[1] = 'Make a Video Call from Dialer '
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        driver1.set_network_connection(0)
        driver2.set_network_connection(0)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                [i.click() for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView") if
                 i.text == "Video call"]  # tab dial button
                print("-----> MO Called.")
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            pass_count += 1
                            driver1.press_keycode(6)
                            print("-----> MO Disconnected.")
                        else:
                            fail_count += 1

                        flag = False

                driver1.press_keycode(4)
                driver1.press_keycode(3)
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Make a Video Call from Dialer ! | with Error : {e}")
            test_count += 1

        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def receive_vcall(iterate=50):
        print('\n', "Event 3 : Receive a Video Call ")
        # test report initiation
        report[1] = 'Receive a Video Call'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        driver1.set_network_connection(0)
        driver2.set_network_connection(0)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                [i.click() for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView") if
                 i.text == "Video call"]  # tab dial button
                print("-----> MO Called.")
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        output = subprocess.check_output(
                            f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            pass_count += 1
                            driver2.press_keycode(6)
                            print("-----> MT Disconnected.")
                        else:
                            fail_count += 1

                        flag = False

                driver1.press_keycode(4)

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Receive a Video Call ! | with Error : {e}")
            test_count += 1
        driver1.toggle_wifi()
        driver2.toggle_wifi()
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    def receive_vcall_wifi(iterate=50):
        print('\n', "Event 4 : Receive a Video Call - WiFi. ")
        # test report initiation
        report[1] = 'Receive a Video Call - WiFi.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Video call":
                        i.click()  # tab dial button
                        break
                print("-----> MO Called.")
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        time.sleep(2)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        try:
                            if 'Wi-Fi' in driver2.find_element(AppiumBy.ID,
                                                               "com.google.android.dialer:id/contactgrid_status_text").text:
                                pass_count += 1
                        except:
                            print("VoWiFi Not Active.")
                            fail_count += 1

                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            driver1.press_keycode(6)
                            print("-----> M0 Disconnected.")

                        flag = False

                driver1.press_keycode(4)
                driver1.press_keycode(3)

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Receive a Video Call ! | with Error : {e}")
            test_count += 1

        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 4 completed!")

    def make_vcall_from_dialer_wifi(iterate=50):
        print('\n', "Event 5 : Make a Video Call from Dialer - WiFi ")
        # test report initiation
        report[1] = 'Make a Video Call from Dialer - WiFi '
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Video call":
                        i.click()  # tab dial button
                        break
                print("-----> MO Called.")
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        # Checking VoWiFi Status
                        try:
                            if 'Wi-Fi' in driver1.find_element(AppiumBy.ID,
                                                               "com.google.android.dialer:id/contactgrid_status_text").text:
                                pass_count += 1
                        except:
                            print("VoWiFi Not Active.")
                            fail_count += 1

                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            driver1.press_keycode(6)
                            print("-----> M0 Disconnected.")

                        flag = False

                driver1.press_keycode(4)
                driver1.press_keycode(3)

            except Exception as e:
                print(
                    f"Iteration = {test_count + 1}| Failed to Make a Video Call from Dialer - WiFi ! | with Error : {e}")
            test_count += 1
        driver1.toggle_wifi()
        driver2.toggle_wifi()
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 5 completed!")

    # Check VoLTE Status
    VoLTE = str(
        subprocess.check_output(f"adb -s {DEVICE1_NAME} shell settings get global volte_subscription1", shell=True))
    if '1' in VoLTE:
        print("VoLTE is Enabled.")
        make_vcall_from_phonebook(3)
        make_vcall_from_dialer(3)
        receive_vcall(3)
    else:
        print(f"VoLTE is Disabled. "
              "Please turn it ON to perform Video_Telephony_Stability_Test over VoLTE.")

    # Check WiFi Status
    WIFI = str(
        subprocess.check_output(f"adb -s {DEVICE1_NAME} shell settings get global wifi_on", shell=True))
    if '1' in WIFI:
        print("WIFI is Enabled.")
        receive_vcall_wifi(3)
        make_vcall_from_dialer_wifi(3)
    else:
        print(f"WIFI is Disabled. "
              "Please turn it ON to perform Video_Telephony_Stability_Test over WIFI.")

    print('\n', "-" * 10, ">> Video Telephony Stability Test Completed! <<", "-" * 10, '\n')


def wifi_calling_stability_test():
    """
    Wi-Fi Calling WFC Stability Test
    """
    print('\n', "-" * 10, ">> WiFi Calling WFC Stability Test <<", "-" * 10, '\n')
    report[0] = "WiFi Calling WFC Stability Test"

    def wifi_call_from_phone_book(iterate=25):
        print('\n', "Event 1 : Make a WiFi Call from Phone Book. ")
        # test report initiation
        report[1] = 'Make a WiFi Call from Phone Book.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # Enable Flight Mode
        # driver1.set_network_connection(1)
        # driver2.set_network_connection(1)

        # Enable WiFi
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        time.sleep(3)

        if contacts() != iterate:
            create_contact(driver=driver1, n=iterate)
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                time.sleep(1)
                driver1.press_keycode(207)  # contacts
                time.sleep(2)
                driver1.find_element(AppiumBy.ID,
                                     "com.google.android.contacts:id/open_search_bar_text_view").click()  # Search
                time.sleep(3)
                [driver1.press_keycode(ord(i) - 36) for i in "TEST"]
                [driver1.press_keycode(int(i) + 7) for i in str(test_count + 1)]
                driver1.press_keycode(66)  # Enter
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == f"test{test_count + 1}":
                        i.click()
                        break
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Call").click()  # Call
                print("-----> MO Called.")
                time.sleep(2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)

                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)  # Call Duration
                        # Checking VoWiFi Status
                        try:
                            if 'Wi-Fi' in driver1.find_element(AppiumBy.ID,
                                                               "com.google.android.dialer:id/contactgrid_status_text").text:
                                pass_count += 1
                        except:
                            print("VoWiFi Not Active.")
                            fail_count += 1
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            driver1.press_keycode(6)
                            print("-----> MO Disconnected.")
                        flag = False

                time.sleep(2)
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(4)  # Back
                driver1.press_keycode(3)  # Home

            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to make WiFi Call from Phone Book ! | with Error : {e}")
            test_count += 1
        driver1.press_keycode(207)  # contacts
        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More options").click()
        time.sleep(1)
        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
            if i.text == "Select all":
                i.click()
                break
        time.sleep(1)
        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Delete").click()
        time.sleep(1)
        driver1.find_element(AppiumBy.ID, "android:id/button1").click()
        time.sleep(1)
        driver1.press_keycode(3)  # Home
        # Disable WiFi
        driver1.toggle_wifi()
        driver2.toggle_wifi()
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def wifi_make_call_from_dialer(iterate=25):
        print('\n', "Event 2 : Make a WiFi Call from Dialer ")
        # test report initiation
        report[1] = 'Make a WiFi Call from Dialer '
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # Enable Flight Mode
        # driver1.set_network_connection(1)
        # driver2.set_network_connection(1)

        # Enable WiFi
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        time.sleep(3)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "dial").click()  # tab dial button
                print("-----> MO Called.")
                time.sleep(2)
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        # Checking VoWiFi Status
                        try:
                            if 'Wi-Fi' in driver1.find_element(AppiumBy.ID,
                                                               "com.google.android.dialer:id/contactgrid_status_text").text:
                                pass_count += 1
                        except:
                            print("VoWiFi Not Active in MO.")
                            fail_count += 1
                        output = subprocess.check_output(
                            f"adb -s {DEVICE1_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            driver1.press_keycode(6)
                            print("-----> MO Disconnected.")

                        flag = False

                driver1.press_keycode(4)
                driver1.press_keycode(3)
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Make a WiFi Call from Dialer ! | with Error : {e}")
            test_count += 1
        # Disable WiFi
        driver1.toggle_wifi()
        driver2.toggle_wifi()
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def receive_a_wifi_call(iterate=25):
        print('\n', "Event 3 : Receive a Call from WiFi.")
        # test report initiation
        report[1] = 'Receive a Call from WiFi.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)

        # Enable Flight Mode
        # driver1.set_network_connection(1)
        # driver2.set_network_connection(1)

        # Enable WiFi
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        time.sleep(3)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                # Make Phone Call(Device 1)
                print("Iteration Count : ", test_count + 1)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                driver1.activate_app(DIALER_APP_PACKAGE)
                time.sleep(1)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "key pad").click()
                time.sleep(2)
                [driver1.press_keycode(int(i) + 7) for i in PH_NUMBER_2]  # dialing ph no
                time.sleep(2)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "dial").click()  # tab dial button
                print("-----> MO Called.")
                # Detect Phone Call (Device 2)
                flag = True
                while flag:
                    output = subprocess.check_output(
                        f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                        shell=True)
                    call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]  # this can lead to Error
                    if '1' in call_state:
                        # Answer the call
                        time.sleep(3)
                        driver2.press_keycode(5)
                        time.sleep(2)
                        print("-----> MT Received.")
                        time.sleep(CALL_DURATION)
                        try:
                            if 'Wi-Fi' in driver2.find_element(AppiumBy.ID,
                                                               "com.google.android.dialer:id/contactgrid_status_text").text:
                                pass_count += 1
                        except:
                            print("VoWiFi Not Active in MT.")
                            fail_count += 1

                        output = subprocess.check_output(
                            f"adb -s {DEVICE2_NAME} shell " + 'dumpsys telephony.registry | grep ' + "'mCallState'",
                            shell=True)
                        call_state = [str(output).split(" ")[i].split("=")[-1][0] for i in [4, 8]]
                        if '2' in call_state:
                            driver2.press_keycode(6)
                            print("-----> MT Disconnected.")

                        flag = False

                driver1.press_keycode(3)
                driver2.press_keycode(3)
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Receive a Call from WiFi ! | with Error : {e}")
            test_count += 1
        # Disable WiFi
        driver1.toggle_wifi()
        driver2.toggle_wifi()
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    wifi_call_from_phone_book(3)
    wifi_make_call_from_dialer(3)
    receive_a_wifi_call(3)
    print('\n', "-" * 10, ">> WiFi Calling WFC Stability Test Completed! <<", "-" * 10, '\n')


def PIM_stability_test():
    """
    PIM Stability Test
    """
    print('\n', "-" * 10, ">> PIM Stability Test <<", "-" * 10, '\n')
    report[0] = "PIM Stability Test"
    driver = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)

    def make_an_appointment_calender(iterate=5):
        print('\n', "Event 1 : Add an appointment to the Calender ")
        # test report initiation
        report[1] = 'Add an appointment to the Calender'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.press_keycode(3)
                driver.activate_app('com.google.android.calendar')
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Create new event and more').click()
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Task button').click()
                driver.find_element(AppiumBy.ID, 'com.google.android.calendar:id/title').send_keys(
                    "Dentist Appointment")

                # enter todays date in below format
                today_date = driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                                 f'Start date: {datetime.datetime.today().strftime("%a, %-d %b %Y")}')
                today_date.click()
                time.sleep(2)
                # enter appointment date in below format
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, '12 November 2022').click()
                time.sleep(2)
                driver.find_element(AppiumBy.ID, 'android:id/button1').click()
                time.sleep(1)
                driver.find_element(AppiumBy.ID, 'com.google.android.calendar:id/save').click()
                time.sleep(1)
                driver.terminate_app('com.google.android.calendar')
                driver.press_keycode(3)
                pass_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Iteration = {test_count + 1}| Failed to Add an appointment to the Calender! | with Error : {e}")
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    '''
    Need to install google task from playstore
    '''

    def delete_an_appointment_calender(iterate=5):
        print('\n', "Event 2 : Delete an appointment in the Calender ")
        # test report initiation
        report[1] = 'Delete an appointment in the Calender'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.press_keycode(3)
                driver.activate_app('com.google.android.apps.tasks')
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'My Tasks').click()
                for i in driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Dentist Appointment":
                        i.click()
                        break
                time.sleep(1)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete').click()
                driver.terminate_app('com.google.android.apps.tasks')
                pass_count += 1
            except Exception as e:
                print(
                    f"Iteration = {test_count + 1}| Failed to Delete an appointment in the Calender! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def set_alarm(iterate=1):
        print('\n', "Event 3 : Set an Alarm ")
        # test report initiation
        report[1] = 'Set an Alarm'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.activate_app('com.google.android.deskclock')
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Alarm').click()
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Add alarm').click()
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Switch to text input mode for the time input.').click()
                time.sleep(1)
                driver.find_element(AppiumBy.ID, 'android:id/input_hour').send_keys("22")
                driver.find_element(AppiumBy.ID, 'android:id/input_minute').send_keys("24")
                driver.find_element(AppiumBy.ID, 'android:id/button1').click()
                driver.terminate_app('com.google.android.deskclock')
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Set an Alarm! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    def delete_alarm(iterate=1):
        print('\n', "Event 4 : Delete an Alarm ")
        # test report initiation
        report[1] = 'Delete an Alarm'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.activate_app('com.google.android.deskclock')
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Alarm').click()
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Expand alarm').click()
                driver.find_element(AppiumBy.ID, 'com.google.android.deskclock:id/delete').click()
                driver.terminate_app('com.google.android.deskclock')
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Delete an Alarm! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 4 completed!")

    def add_contact_phonebook(iterate=20):
        print('\n', "Event 5 : Add Contact to the Phone Book ")
        # test report initiation
        report[1] = 'Add Contact to the Phone Book'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.activate_app('com.google.android.contacts')
                time.sleep(2)
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Create contact').click()
                time.sleep(2)
                driver.find_element(AppiumBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.EditText').send_keys(
                    "Test")
                driver.find_element(AppiumBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText').send_keys(
                    "12345678")
                driver.find_element(AppiumBy.ID, 'com.google.android.contacts:id/toolbar_button').click()
                driver.terminate_app('com.google.android.contacts')
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Add Contact to the Phone Book! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 5 completed!")

    def delete_contact_phonebook(iterate=20):
        print('\n', "Event 6 : Delete Contact from the Phone Book ")
        # test report initiation
        report[1] = 'Delete Contact from the Phone Book'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
                driver.activate_app('com.google.android.contacts')
                time.sleep(2)
                driver.find_element(AppiumBy.ID, 'com.google.android.contacts:id/open_search_bar').click()
                time.sleep(2)
                driver.press_keycode(48)
                driver.press_keycode(33)
                driver.press_keycode(47)
                driver.press_keycode(48)
                # below line is error
                # driver3.find_element(AppiumBy.ID,'com.google.android.contacts:id/open_search_bar_text_view').send_keys("Test")
                driver.find_element(AppiumBy.ID, 'com.google.android.contacts:id/alert_text').click()
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'More options').click()
                time.sleep(2)
                driver.find_element(AppiumBy.XPATH,
                                    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout').click()
                driver.find_element(AppiumBy.ID, 'android:id/button1').click()
                driver.terminate_app('com.google.android.contacts')
                pass_count += 1
            except Exception as e:
                print(f"Iteration = {test_count + 1}| Failed to Delete Contact from the Phone Book! | with Error : {e}")
                fail_count += 1
            test_count += 1

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 6 completed!")

    make_an_appointment_calender()
    delete_an_appointment_calender()
    set_alarm()
    delete_alarm()
    add_contact_phonebook()
    delete_contact_phonebook()
    print('\n', "-" * 10, ">> PIM Stability Test Completed! <<", "-" * 10, '\n')


def IPME_Wave1_stability_test():
    """
    IPME (Wave 1) Stability Test
    Events:

    ** using Cellular network
    1.Texting - Chat mode : Send a chat message to another IPME enabled device with 200 characters
    2.Texting - Pager mode : Send a pager mode message to a non-IPME enabled device with 200 characters
    3.File Transfer - Send a 10MB file to another IPME enabled device
    4.Large message mode : end a 1MB file to a non IPME enabled device

    ** Use a Wi-Fi network for the following tests
    5.Texting ??? Chat Mode over Wi-Fi : Send a chat message to another IPME enabled device with 200 characters
    6.File Transfer over Wi-Fi : Send a 10MB file to another IPME enabled device
    """

    print('\n', "-" * 10, ">> IPME (Wave 1) Stability Test <<", "-" * 10, '\n')
    report[0] = "IPME (Wave 1) Stability Test"

    def texting_chat_mode(iterate=80):
        print('\n', "Event 1 : Texting Chat mode ")
        # test report initiation
        report[1] = 'Texting Chat mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                        time.sleep(7)
                        # check sent or failed
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, Read").text == "Now ??? Read":
                            pass_count += 1
                        else:
                            fail_count += 1
                    else:
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # check sent or failed
                        time.sleep(5)
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, Read").text == "Now ??? Read":
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Chat mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver2.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver2.press_keycode(4)
            driver1.press_keycode(3)
            driver2.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def texting_pager_mode(iterate=80):
        print('\n', "Event 2 : Texting Pager mode ")
        # test report initiation
        report[1] = 'Texting Pager mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver3 = webdriver.Remote("http://0.0.0.0:4729/wd/hub", desired_cap_3)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver3.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = disable_chat_feature(driver3)
        time.sleep(6)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()

                        # check sent or failed
                        time.sleep(2)
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                    else:
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        # check sent or failed
                        time.sleep(2)
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Pager mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver3.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver3.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver3.press_keycode(4)
            driver1.press_keycode(3)
            driver3.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver3.quit()

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def file_transfer(iterate=20):
        print('\n', "Event 3 : File Transfer ")
        # test report initiation
        report[1] = 'File Transfer'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            # open MT chat box
                            driver1.activate_app(MSG_APP_PACKAGE)
                            time.sleep(2)
                            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                                if PH_NUMBER_1[:5] in i.text:
                                    i.click()
                                    flag = False
                                    break
                        time.sleep(5)
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Seen" in status:
                            pass_count += 1
                        else:
                            fail_count += 1

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/message_status").text
                            if "Seen" in status:
                                flag = False
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Seen" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| File Transfer Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 3 : File Transfer  "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 3 : File Transfer  "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 3 : File Transfer  "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    def large_msg_mode(iterate=80):
        print('\n', "Event 4 : Large message mode ")
        # test report initiation
        report[1] = 'Large message mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver3 = webdriver.Remote("http://0.0.0.0:4729/wd/hub", desired_cap_3)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver3.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = disable_chat_feature(driver3)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(2)
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(1)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "file_example_JPG_100kB.jpg":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        # open MT chat box
                        time.sleep(2)
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(10)
                        for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                        # check sent or failed
                        time.sleep(15)
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, SMS").text == "Now ??? SMS":
                            pass_count += 1
                        else:
                            fail_count += 1
                    else:
                        time.sleep(1)
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(1)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "sample-pdf-file.pdf":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        # check sent or failed
                        time.sleep(10)
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, SMS").text == "Now ??? SMS":
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Large message mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver3.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver3.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver3.press_keycode(4)
            driver1.press_keycode(3)
            driver3.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 4 : Large message mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 4 : Large message mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 4 : Large message mode"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver3.quit()

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / iterate) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 4 completed!")

    def texting_chat_mode_wifi(iterate=75):
        print('\n', "Event 5 : Texting Chat mode over WiFi")
        # test report initiation
        report[1] = 'Texting Chat mode over WiFi'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable WiFi only
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        print("-->> Only WiFi Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                        time.sleep(7)
                        # check sent or failed
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, Read").text == "Now ??? Read":
                            pass_count += 1
                        else:
                            fail_count += 1
                    else:
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # check sent or failed
                        time.sleep(5)
                        if driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Now, Read").text == "Now ??? Read":
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Chat mode over WiFi Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver2.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver2.press_keycode(4)
            driver1.press_keycode(3)
            driver2.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 1 : Texting Chat mode over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 1 : Texting Chat mode over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 1 : Texting Chat mode over WiFi "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 5 completed!")

    def file_transfer_wifi(iterate=20):
        print('\n', "Event 6 : File Transfer over WiFi")
        # test report initiation
        report[1] = 'File Transfer over WiFi'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable WiFi only
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        print("-->> Only WiFi Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            # open MT chat box
                            driver1.activate_app(MSG_APP_PACKAGE)
                            time.sleep(2)
                            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                                if PH_NUMBER_1[:5] in i.text:
                                    i.click()
                                    flag = False
                                    break
                        time.sleep(5)
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Seen" in status:
                            pass_count += 1
                        else:
                            fail_count += 1

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Seen" in status:
                                flag = False
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Seen" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| File Transfer over WiFi Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 6 : File Transfer over WiFi "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 6 : File Transfer over WiFi "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 6 : File Transfer over WiFi "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 6 completed!")

    texting_chat_mode(3)
    texting_pager_mode(3)
    file_transfer(3)
    large_msg_mode(3)
    texting_chat_mode_wifi(3)
    file_transfer_wifi(3)


def IPME_Wave2_stability_test():
    """
    IPME (Wave 2) Stability Test
    Events:

    ** using Cellular network
    1.Texting - Chat mode : Send a chat message to another IPME enabled device with 200 characters
    2.Texting - Pager mode : Send a pager mode message to a non-IPME enabled device with 200 characters
    3.HTTP File Transfer - 10MB : Send a 10MB file to another IPME wave 2 enabled device
    4.HTTP File Transfer - 30 MB Video transfer : Send a 30MB Video clip to another IPME wave 2 enabled device
    5.Large message mode : Send a 1MB file to a non IPME enabled device

    ** Use a Wi-Fi network for the following tests
    6.Texting ??? Chat Mode over Wi-Fi : Send a chat message to another IPME enabled device with 200 characters
    7.HTTP File Transfer over Wi-Fi (10 MB) : Send a 10MB file to another IPME wave 2 enabled device
    8.HTTP File Transfer over Wi-Fi (30 MB)  : Send a 30MB file to another IPME wave 2 enabled device

    ** using Cellular network
    9.Open Group Chat : Send an open group chat of 50 characters to 2 IPME Wave 2 devices
    10.Group Messaging  : Send a 50 character text message to 2 non-IPME devices
    """

    print('\n', "-" * 10, ">> IPME (Wave 2) Stability Test <<", "-" * 10, '\n')
    report[0] = "IPME (Wave 2) Stability Test"

    def texting_chat_mode(iterate=50):
        print('\n', "Event 1 : Texting Chat mode ")
        # test report initiation
        report[1] = 'Texting Chat mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(3)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        time.sleep(2)
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Chat mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver2.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver2.press_keycode(4)
            driver1.press_keycode(3)
            driver2.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 1 completed!")

    def texting_pager_mode(iterate=50):
        print('\n', "Event 2 : Texting Pager mode ")
        # test report initiation
        report[1] = 'Texting Pager mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver3 = webdriver.Remote("http://0.0.0.0:4729/wd/hub", desired_cap_3)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver3.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = disable_chat_feature(driver3)
        time.sleep(6)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_3)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()

                        # check sent or failed
                        time.sleep(2)
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                    else:
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        # check sent or failed
                        time.sleep(2)
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Pager mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver3.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver3.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver3.press_keycode(4)
            driver1.press_keycode(3)
            driver3.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 2 : Texting Pager mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver3.quit()

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 2 completed!")

    def http_file_transfer_10mb(iterate=20):
        print('\n', "Event 3 : HTTP File Transfer (10MB) ")
        # test report initiation
        report[1] = 'HTTP File Transfer (10MB)'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| HTTP File Transfer (10MB) Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (10MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (10MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (10MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 3 completed!")

    def http_file_transfer_30mb(iterate=10):
        print('\n', "Event 4 : HTTP File Transfer (30MB) ")
        # test report initiation
        report[1] = 'HTTP File Transfer (30MB)'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "jellyfish-25-mbps-hd-hevc.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "jellyfish-25-mbps-hd-hevc.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| HTTP File Transfer (30MB) Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB)"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 4 completed!")

    def large_msg_mode(iterate=50):
        print('\n', "Event 5 : Large message mode ")
        # test report initiation
        report[1] = 'Large message mode'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver3 = webdriver.Remote("http://0.0.0.0:4729/wd/hub", desired_cap_3)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver3.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = disable_chat_feature(driver3)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_3)
                        driver1.press_keycode(66)
                        time.sleep(2)
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(1)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "file_example_JPG_100kB.jpg":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        flag = True
                        while flag:
                            driver3.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Now" in status or "SMS" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Now" in status or "SMS" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break
                    else:
                        time.sleep(1)
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(1)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "file_example_JPG_100kB.jpg":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send SMS").click()
                        flag = True
                        while flag:
                            driver3.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Now" in status or "SMS" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Now" in status or "SMS" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Large message mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver3.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver3.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver3.press_keycode(4)
            driver1.press_keycode(3)
            driver3.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 4 : Large message mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 4 : Large message mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 4 : Large message mode"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver3.quit()

        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / iterate) * 100, 2)
        report[10] = None
        report[11] = None

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 5 completed!")

    def texting_chat_mode_wifi(iterate=50):
        print('\n', "Event 6 : Texting Chat mode over WiFi")
        # test report initiation
        report[1] = 'Texting Chat mode over WiFi'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        print("-->> Only WiFi Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        time.sleep(2)
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Chat mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            # Delete msg on both MO & MT
            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(2)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(2)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver2.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(2)
            driver1.press_keycode(4)
            driver2.press_keycode(4)
            driver1.press_keycode(3)
            driver2.press_keycode(3)
            report[10] = None
            report[11] = None
        elif f1:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 1 : Texting Chat mode "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 6 completed!")

    def http_file_transfer_10mb_wifi(iterate=20):
        print('\n', "Event 7 : File Transfer (10MB) over WiFi")
        # test report initiation
        report[1] = 'File Transfer (10MB) over WiFi'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        print("-->> Only WiFi Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Free_Test_Data_10MB_MP4.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| HTTP File Transfer (10MB) Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 7 : HTTP File Transfer (10MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 7 : HTTP File Transfer (10MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 7 : HTTP File Transfer (10MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 7 completed!")

    def http_file_transfer_30mb_wifi(iterate=20):
        print('\n', "Event 8 : File Transfer (30MB) over WiFi")
        # test report initiation
        report[1] = 'File Transfer (30MB) over WiFi'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        # enable cellular network only
        driver1.set_network_connection(2)
        driver2.set_network_connection(2)
        print("-->> Only WiFi Enabled on both MO & MT")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("MT Device :")
        f2 = enable_chat_feature(driver2)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(66)
                        time.sleep(3)

                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Show roots").click()
                        time.sleep(3)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Downloads":
                                i.click()
                                break
                        time.sleep(2)
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "jellyfish-25-mbps-hd-hevc.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat box
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if PH_NUMBER_1[:5] in i.text:
                                i.click()
                                break

                    else:
                        # attachment section
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Add files, location and more").click()
                        time.sleep(1)
                        driver1.find_element(AppiumBy.XPATH,
                                             '//android.view.ViewGroup[@content-desc="Files"]/android.widget.ImageView').click()
                        time.sleep(2)
                        # file selection
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "jellyfish-25-mbps-hd-hevc.mp4":
                                i.click()
                                break
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send end-to-end encrypted message").click()
                        flag = True
                        while flag:
                            driver2.activate_app(MSG_APP_PACKAGE)
                            status = driver1.find_element(AppiumBy.ID,
                                                          "com.google.android.apps.messaging:id/message_status").text
                            if "Sent" in status or "Delivered" in status or "Read" in status:
                                flag = False
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                    driver1.press_keycode(4)
                except Exception as e:
                    fail_count += 1
                    print(f"Iteration = {test_count + 1}| HTTP File Transfer (30MB) over WiFi Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
            try:
                # Delete msg on both MO & MT
                time.sleep(3)
                driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
                time.sleep(2)
                for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                    if i.text == "Delete":
                        i.click()
                        break
                time.sleep(2)
                driver1.find_element(AppiumBy.ID, "android:id/button1").click()
                driver2.find_element(AppiumBy.ID, "android:id/button1").click()
                time.sleep(2)
                driver1.press_keycode(4)
                driver2.press_keycode(4)
                driver1.press_keycode(3)
                driver2.press_keycode(3)
                report[10] = None
                report[11] = None
            except:
                print("Failed to Delete messages")
        elif f1:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in MT."
        elif f2:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        else:
            report[10] = "Unable to perform Event 3 : HTTP File Transfer (30MB) over WiFi"
            report[11] = "Bcoz, Chat Feature is not CONNECTED in both MO & MT."
        driver1.quit()
        driver2.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / test_count) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 6 completed!")

    def open_group_chat(iterate=20):
        print('\n', "Event 9 : Open Group Chat")
        # test report initiation
        report[1] = 'Open Group Chat'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # connecting devices
        driver1 = webdriver.Remote("http://0.0.0.0:4727/wd/hub", desired_cap)
        driver2 = webdriver.Remote("http://0.0.0.0:4728/wd/hub", desired_cap_2)
        driver3 = webdriver.Remote("http://0.0.0.0:4729/wd/hub", desired_cap_3)
        # enable cellular network only
        driver1.set_network_connection(4)
        driver2.set_network_connection(4)
        driver3.set_network_connection(4)
        print("-->> Only Cellular Network Enabled on 1 MO & 2 MTs")
        # enable chat features if disabled & check status
        print("MO Device :")
        f1 = enable_chat_feature(driver1)
        print("1st MT Device :")
        f2 = enable_chat_feature(driver2)
        driver1.activate_app(MSG_APP_PACKAGE)
        print("2nd MT Device :")
        f3 = enable_chat_feature(driver3)

        # loop variable initiation
        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()

        if f1 & f2 & f3:
            while test_count < iterate:
                try:
                    if test_count == 0:
                        # launch message app
                        driver1.activate_app(MSG_APP_PACKAGE)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Start chat").click()
                        time.sleep(1)
                        # click create group
                        for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if i.text == "Create group":
                                i.click()
                                break
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/recipient_text_view").send_keys(
                            PH_NUMBER_2)
                        driver1.press_keycode(55)
                        time.sleep(2)
                        [driver1.press_keycode(int(i)+7) for i in PH_NUMBER_3]
                        driver1.press_keycode(66)
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/container_action_button").click()
                        time.sleep(3)
                        driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/name_edit").send_keys("TEST GROUP")
                        time.sleep(1)
                        driver1.find_element(AppiumBy.ID,
                                     "com.google.android.apps.messaging:id/container_action_button").click()
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT[:50])
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send message").click()
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID, "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                        # open MT chat boxes
                        time.sleep(2)
                        driver2.activate_app(MSG_APP_PACKAGE)
                        driver3.activate_app(MSG_APP_PACKAGE)
                        time.sleep(2)
                        for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if "TEST GROUP" in i.text:
                                i.click()
                                break
                        for i in driver3.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                            if "TEST GROUP" in i.text:
                                i.click()
                                break

                    else:
                        driver1.find_element(AppiumBy.ID,
                                             "com.google.android.apps.messaging:id/compose_message_text").send_keys(
                            MSG_TEXT[:50])
                        time.sleep(2)
                        driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "Send message").click()
                        time.sleep(2)
                        # check sent or failed
                        status = driver1.find_element(AppiumBy.ID,
                                                      "com.google.android.apps.messaging:id/message_status").text
                        if "Sent" in status or "Delivered" in status or "Read" in status:
                            pass_count += 1
                        else:
                            fail_count += 1
                except Exception as e:
                    print(f"Iteration = {test_count + 1}| Texting Chat mode Failed! | with Error : {e}")
                test_count += 1
                time.sleep(3)
                # Delete msg on both MO & MT

            time.sleep(3)
            driver1.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver2.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            driver3.find_element(AppiumBy.ACCESSIBILITY_ID, "More conversation options").click()
            time.sleep(1)
            for i in driver1.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            for i in driver2.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView"):
                if i.text == "Delete":
                    i.click()
                    break
            time.sleep(1)
            driver1.find_element(AppiumBy.ID, "android:id/button1").click()
            driver2.find_element(AppiumBy.ID, "android:id/button1").click()
            driver3.find_element(AppiumBy.ID, "android:id/button1").click()
            time.sleep(1)
            driver1.press_keycode(4)
            driver2.press_keycode(4)
            driver3.press_keycode(4)
            driver1.press_keycode(3)
            driver2.press_keycode(3)
            driver3.press_keycode(3)
            report[10] = None
            report[11] = None

        elif f1 & f2:
            report[10] = "Unable to perform Event 9 : Open Group Chat "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in 2nd MT."
        elif f2 & f3:
            report[10] = "Unable to perform Event 9 : Open Group Chat "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in M0."
        elif f1 & f3:
            report[10] = "Unable to perform Event 9 : Open Group Chat "
            report[11] = "Bcoz, Chat Feature is not CONNECTED in 1st MT."
        else:
            report[10] = "Unable to perform Event 9 : Open Group Chat "
            report[11] = "Bcoz, Chat Feature is not CONNECTED on 1 MO & 2 MTs."
        driver1.quit()
        driver2.quit()
        driver3.quit()
        end = datetime.datetime.now()
        # finishing test report
        report[4] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        report[5] = str(end - start).split('.')[0]
        report[6] = test_count
        report[7] = pass_count
        report[8] = fail_count
        report[9] = round((pass_count / (test_count + 1)) * 100, 2)

        # insert test report to csv file
        with open('automation_stability_test.csv', 'a') as f:
            writer(f).writerow(report)
            f.close()
        print("\n", "Event 9 completed!")

    def group_messaging(iterate=20):
        pass

    texting_chat_mode(3)
    texting_pager_mode(3)
    http_file_transfer_10mb(3)
    http_file_transfer_30mb(3)
    large_msg_mode(3)
    texting_chat_mode_wifi(3)
    http_file_transfer_10mb_wifi(3)
    http_file_transfer_30mb_wifi(3)
    # open_group_chat(3)
    # group_messaging()


# Messaging_Stability_Tests()
# Email_Stability_Test()
# Browser_Stability_Test()
# Multimedia_Stability_Test()
# Multitasking_Stability_Test()
# wifi(2)
# playstore_test()
# Telephony_Stability_Test()
# Video_Telephony_Stability_Test()
# wifi_calling_stability_test()
# PIM_stability_test()
# IPME_Wave1_stability_test()
IPME_Wave2_stability_test()

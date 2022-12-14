import datetime
import time
import os
from csv import writer
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from credentials import *

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
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.press_keycode(3)
    driver.set_network_connection(0)

    pass_count, fail_count, test_count = 0, 0, 0
    start = datetime.datetime.now()
    while test_count < iterate:
        try:
            driver.toggle_wifi()
            time.sleep(10)
            driver.toggle_wifi()
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
        driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
        driver.press_keycode(3)
        driver.set_network_connection(6)

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            try:
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
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_PlayStore)
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
                                        time.sleep(4)
                                driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")[-1].click()
                                time.sleep(2)

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
        driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
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

    # event1(2)
    event2(2)
    # event3(2)


def Messaging_Stability_Tests():
    """
    Messaging Stability Tests
    1.
    2.
    3.Send an SMS maximum number of characters with out requiring the message to be segmented from the DUT.
    4.
    """
    print('\n', "-" * 10, ">> Messaging Stability Tests <<", "-" * 10, '\n')

    desired_cap_message_stability = {
        "appium:deviceName": "RZ8N91E8TPM",
        "platformName": "Android",
        "appium:appPackage": "com.samsung.android.messaging",
        "appium:appActivity": "com.android.mms.ui.ConversationComposer",
        "appium:platformVersion": "12",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }

    def mobile_originating_message_maxCharacters(iterate=20):
        """This function Automatically test the SMS service of the Messaging app."""
        # test report
        report[0] = 'SMS Automation'
        report[
            1] = 'Send an SMS maximum number of characters with out requiring the message to be segmented from the DUT.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_message_stability)

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            # Automation Code
            # send the message
            MT_contact = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="???My Jio???"]')
            MT_contact.click()
            time.sleep(2)
            text_box = driver.find_element(AppiumBy.ID, 'com.samsung.android.messaging:id/message_edit_text')
            text_box.send_keys(
                '1234567890@#$%^&*()qwertyuiop[]sdfghjkl;qwertyuiopasdfghjklzxcvbnm,./;12345678901234567890!@#$%^&*('
                ')qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfgjklzxcvbnm1234567890qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm12345678901!@#$%^&*()_+asdfghjklqwertyuopzxcvbnm')
            send_message = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send')
            send_message.click()
            time.sleep(4)

            # SENT or FAILED
            try:
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Sending failed')
                fail_count += 1
            except:
                pass_count += 1

            # Delete the message
            delete_settings = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Conversation settings')
            delete_settings.click()
            time.sleep(2)
            delete_message = driver.find_element(AppiumBy.XPATH,
                                                 '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android'
                                                 '.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                                                 '/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android'
                                                 '.widget.FrameLayout['
                                                 '2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget'
                                                 '.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout'
                                                 '/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ImageView')
            delete_message.click()
            select_last_message = driver.find_element(AppiumBy.XPATH,
                                                      '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout'
                                                      '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                                      '.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.CheckBox')
            select_last_message.click()
            delete_all = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
            delete_all.click()
            time.sleep(2)
            move_to_recycle = driver.find_element(AppiumBy.ID, 'android:id/button1')
            move_to_recycle.click()
            test_count += 1
            driver.press_keycode(4)
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

    def MMS_with_MAXCHAR_AUDIO(iterate=20):
        """This function Automatically test the MMS service of Messaging app."""
        # test report
        report[0] = 'MMS Automation'
        report[
            1] = 'Send an SMS maximum number of characters with out requiring the message to be segmented from the DUT.'
        report[2] = iterate
        report[3] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_message_stability)

        pass_count, fail_count, test_count = 0, 0, 0
        start = datetime.datetime.now()
        while test_count < iterate:
            # Automation Code
            # send the MMS
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
            time.sleep(60)

            # SENT or FAILED
            try:
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Sending failed')
                fail_count += 1
            except:
                pass_count += 1

            # Delete the message
            time.sleep(200)
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

    mobile_originating_message_maxCharacters(20)
    MMS_with_MAXCHAR_AUDIO(20)
    print('\n', "-" * 10, ">> Messaging Stability Tests Completed! <<", "-" * 10, '\n')


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

    def switch_bg_apps(wdriver, iteration=50):
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
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    if driver.is_locked():
        driver.unlock()
    driver.press_keycode(3)
    driver.set_network_connection(6)

    # # MAKE A CALL
    try:
        driver.activate_app(PHONE_APP_PACKAGE)
        time.sleep(2)
        [i.click() for i in driver.find_elements(AppiumBy.ID, "androidhwext:id/content") if i.text == "Phone"]
        time.sleep(2)
        [driver.find_element(AppiumBy.ACCESSIBILITY_ID, i).click() for i in PH_NUMBER]  # dialing ph no
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
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:appPackage": "com.sec.android.app.camera",
        "appium:appActivity": "com.sec.android.app.camera.Camera",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_Browser = {
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:appPackage": "com.android.chrome",
        "appium:appActivity": "com.google.android.apps.chrome.Main",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "Appium",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_mediaplayer = {
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:appPackage": "com.kapp.youtube.final",
        "appium:appActivity": "com.kapp.youtube.ui.MainActivity",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }
    desired_cap_MyFiles = {
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:appPackage": "com.sec.android.app.myfiles",
        "appium:appActivity": "com.sec.android.app.myfiles.external.ui.MainActivity",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"

    }
    desired_cap_Theme = {
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                video_mode = driver2.find_element(AppiumBy.XPATH,
                                                  '//android.widget.SeekBar[@content-desc="Photo, Mode"]/android.view.ViewGroup[3]/android.widget.LinearLayout')
                video_mode.click()
                time.sleep(2)
                capture_start = driver2.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/center_button')
                capture_start.click()
                time.sleep(30)
                capture_stop = driver2.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/center_button')
                capture_stop.click()
                driver2.quit()
                pass_count += 1

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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver2.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                play_video = driver2.find_element(AppiumBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup[2]/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout')
                play_video.click()
                time.sleep(30)
                driver2.quit()
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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver2.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                delete_video = driver2.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                delete_video.click()
                time.sleep(2)
                move = driver2.find_element(AppiumBy.ID, 'android:id/button1')
                move.click()
                driver2.quit()
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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                # front_rotate=driver2.find_element(AppiumBy.ID,'com.sec.android.app.camera:id/right_button')
                # front_rotate.click()
                capture_start = driver2.find_element(AppiumBy.ID, 'com.sec.android.app.camera:id/normal_overlap_image')
                capture_start.click()
                time.sleep(5)
                driver2.quit()
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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver2.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                driver2.press_keycode(4)
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
                driver2 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_video_camera)
                time.sleep(2)
                open_last_gallery = driver2.find_element(AppiumBy.XPATH,
                                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[2]')
                open_last_gallery.click()
                delete_video = driver2.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                delete_video.click()
                time.sleep(2)
                move = driver2.find_element(AppiumBy.ID, 'android:id/button1')
                move.click()
                driver2.press_keycode(4)
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
                driver3 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Browser)
                driver3.set_network_connection(6)  # Turn on Wi-Fi and mobile data
                driver3.get("https://m.youtube.com/watch?v=Ro971vwsgPg")
                driver3.press_keycode(66)
                time.sleep(15)

                driver3.quit()
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
                driver4 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_mediaplayer)
                driver4.press_keycode(209)
                time.sleep(4)
                driver4.press_keycode(128)
                driver4.press_keycode(86)
                driver4.quit()
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
                driver3 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_MyFiles)
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
                driver4 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_mediaplayer)
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
                driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Theme)
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

    record_video_30s()
    play_last_video()
    delete_last_video()
    take_picture()
    open_picture()
    delete_picture()
    youtube_stream_browser()
    open_close_music_player()
    open_musicplayer_play_music()
    close_music_player()
    set_theme()
    print('\n', "-" * 10, ">> Multimedia Stability Test Completed! <<", "-" * 10, '\n')


def Email_Stability_Test():
    """
    Email Stability Test
    """
    print('\n', "-" * 10, ">> Email Stability Test <<", "-" * 10, '\n')
    report[0] = "Email Stability Test"
    desired_cap_Email = {
        "appium:deviceName": DEVICE_NAME,
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:appPackage": "com.google.android.gm",
        "appium:appActivity": "com.google.android.gm.ConversationListActivityGmail",
        "appium:adbExecTimeout": "30000",
        "appium:automationName": "UiAutomator2",
        "appium:uiautomator2ServerInstallTimeout": "90000",
        "appium:noReset": "true",
        "appium:fullReset": "false"
    }

    def send_email_no_attachment(iterate):
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
                driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Email)
                compose_button = driver.find_element(AppiumBy.ID, 'com.google.android.gm:id/compose_button')
                compose_button.click()
                time.sleep(2)
                to_cc_bcc = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Add Cc/Bcc')
                to_cc_bcc.click()

                receipent = driver.find_element(AppiumBy.XPATH,
                                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.EditText')
                receipent.send_keys('swarnendu0298@gmail.com')
                driver.press_keycode(66)
                subject = driver.find_element(AppiumBy.ID, 'com.google.android.gm:id/subject')
                subject.send_keys('Here is my subject line!!')
                time.sleep(2)
                message_body = driver.find_element(AppiumBy.XPATH,
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.widget.EditText')
                message_body.send_keys(
                    "Hello This is my message of 30 characters. This is pre-loaded message using automation concept.//Thanks ")
                send_email = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send')
                send_email.click()
                time.sleep(3)
                # Pass or Fail
                try:
                    driver.find_element(AppiumBy.XPATH,
                                        '//android.widget.LinearLayout[@content-desc="Sent"]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]')
                    pass_count += 1
                except:
                    fail_count += 1
                # delete mail
                menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer')
                menu.click()
                time.sleep(2)
                sent_mails = driver.find_element(AppiumBy.XPATH,
                                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[10]/android.widget.LinearLayout')
                sent_mails.click()
                time.sleep(3)
                try:
                    actions = TouchAction(driver)
                    actions.tap(x=97, y=710)
                    actions.release().perform()
                    time.sleep(2)
                    Delete = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                    Delete.click()
                    time.sleep(3)
                except:
                    print("Failed to Delete as touch sensor did not work.")

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

    def send_email_with_attachment(iterate):
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
                driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Email)
                compose_button = driver.find_element(AppiumBy.ID, 'com.google.android.gm:id/compose_button')
                compose_button.click()
                time.sleep(2)
                receipent = driver.find_element(AppiumBy.ID,
                                                'com.google.android.gm:id/peoplekit_autocomplete_chip_group')
                receipent.send_keys("swarnendu0298@gmail.com")
                subject = driver.find_element(AppiumBy.ID, 'com.google.android.gm:id/subject')
                subject.send_keys("Here is my subject line!!")
                message_body = driver.find_element(AppiumBy.ID, 'com.google.android.gm:id/composearea_tap_trap_bottom')
                message_body.send_keys(
                    "Hello This is my message of 30 characters. This is pre-loaded message using automation concept.//Thanks ")
                attachment = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Attach file')
                attachment.click()
                time.sleep(2)
                attach_file = driver.find_element(AppiumBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout')
                attach_file.click()
                time.sleep(2)
                doc = driver.find_element(AppiumBy.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.CompoundButton[4]')
                doc.click()
                time.sleep(2)
                choose_file = driver.find_element(AppiumBy.XPATH,
                                                  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/androidx.cardview.widget.CardView[4]/androidx.cardview.widget.CardView/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.ImageView[1]')
                choose_file.click()
                send_email = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Send')
                send_email.click()
                time.sleep(8)
                # Sent or Failed
                try:
                    driver.find_element(AppiumBy.XPATH,
                                        '//android.widget.LinearLayout[@content-desc="Sent"]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]')
                    pass_count += 1
                except:
                    fail_count += 1
                    # delete mail
                    menu = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer')
                    menu.click()
                    time.sleep(2)
                    sent_mails = driver.find_element(AppiumBy.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[10]/android.widget.LinearLayout')
                    sent_mails.click()
                    time.sleep(2)
                    try:
                        actions = TouchAction(driver)
                        actions.tap(x=97, y=710)
                        actions.release().perform()
                        time.sleep(2)
                        Delete = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Delete')
                        Delete.click()
                        time.sleep(3)
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

    def open_email(iterate):
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
                driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Email)
                time.sleep(2)
                actions = TouchAction(driver)
                actions.tap(x=542, y=492)
                actions.perform()
                time.sleep(3)
                driver.quit()
                pass_count += 1
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

    send_email_no_attachment(10)
    send_email_with_attachment(10)
    open_email(10)
    print('\n', "-" * 10, ">> Email Stability Test Completed! <<", "-" * 10, '\n')


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
                driver3 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Browser)
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
                driver3 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Browser)
                driver3.set_network_connection(6)  # Turn on wifi and mobile data
                driver3.get("https://www.att.com")
                # driver3.press_keycode(66)
                time.sleep(3)
                first_link = driver3.find_element(AppiumBy.ACCESSIBILITY_ID, 'Phones & devices')
                first_link.click()
                time.sleep(2)
                second_link = driver3.find_element(AppiumBy.ID, 'Categories-1')
                second_link.click()
                time.sleep(2)
                third_link = driver3.find_element(AppiumBy.ID, 'Categories-0')
                third_link.click()

                driver3.quit()
                pass_count += 1
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
                driver3 = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap_Browser)
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


# wifi(30)
playstore_test()
# Messaging_Stability_Tests()
# Multitasking_Stability_Test()
# Multimedia_Stability_Test()
# Email_Stability_Test()
# Browser_Stability_Test()

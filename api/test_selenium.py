import os
import sys
import django
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)).rsplit(os.sep, 1)[0])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from api.models import FriendRequest


#-------------------Selenium Tests-------------------

# THIS HAS BEEN DEMONSTRATED IN A YOUTUBE VIDEO. https://www.youtube.com/watch?v=zmCv9vd88_g

class SeleniumTests(unittest.TestCase):

    def setUp(self):
        # initial setup for chrome.
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome()
        self.baseUrl = "http://localhost:5173/"  

    def testSignupAndLogin(self):
        driver = self.driver

        # go to signup page.
        driver.get(self.baseUrl + "signup/")

        #  fill in with user details
        driver.find_element(By.XPATH, '//label[contains(text(), "Name:")]/input').send_keys("Test User")
        driver.find_element(By.XPATH, '//label[contains(text(), "Email:")]/input').send_keys("johnny@example.com")
        driver.find_element(By.XPATH, '//label[contains(text(), "Password:")]/input').send_keys("Password123")
        driver.find_element(By.XPATH, '//label[contains(text(), "Date of Birth:")]/input').send_keys("02-05-2007")

        # select one hobby just to make sure it works
        hobbyCheckboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
        if hobbyCheckboxes:
            hobbyCheckboxes[0].click()  

        # find signup button
        signupButton = driver.find_element(By.XPATH, '//button[text()="Signup"]')

        # click the signup button .
        driver.execute_script("arguments[0].scrollIntoView(true);", signupButton)
        driver.find_element(By.XPATH, '//form').submit()

        time.sleep(3)
            
        # go back to the homepage after signup.
        self.assertIn("/", driver.current_url.lower(), "sign up does not redirect to login!.")

        # logout
        logoutButton = driver.find_element(By.XPATH, '//button[text()="Logout"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", logoutButton)
        logoutButton.click()

        # wait a bit for home page to load
        driver.implicitly_wait(5)
        self.assertIn("/", driver.current_url.lower(), "logout did not redirect to home page!")

        # click login button
        loginLink = driver.find_element(By.XPATH, '//a[contains(text(), "Login")]')
        driver.execute_script("arguments[0].click();", loginLink)

        # wait a bit again
        driver.implicitly_wait(5)
        self.assertIn("login", driver.current_url.lower(), "login link didn’t navigate to the login page.")

        # login again
        driver.find_element(By.XPATH, '//label[contains(text(), "Email:")]/input').send_keys("habibi@example.com")
        driver.find_element(By.XPATH, '//label[contains(text(), "Password:")]/input').send_keys("Password123")
        driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # wait for the login to send you to home page again
        driver.implicitly_wait(5)
        self.assertIn("/", driver.current_url.lower(), "login didn’t redirect to the home page.")

    def testEditProfile(self):
        driver = self.driver
        self.login(driver, "joshua@gmail.com", "J05_hua")  # login 

        # go to the profile page.
        driver.get(self.baseUrl + "profile/")

        time.sleep(3)  

        # change the name
        nameInput = driver.find_element(By.XPATH, '//input[@id="name"]')
        nameInput.clear()
        nameInput.send_keys("Updated User")

        # change dob
        dobInput = driver.find_element(By.XPATH, '//input[@id="dob"]')
        dobInput.clear()
        dobInput.send_keys("15-05-2005") 

        # select some hobbies.. i chose 4 and 5
        hobbyCheckbox4 = driver.find_element(By.XPATH, '//input[@id="hobby-4"]')
        hobbyCheckbox5 = driver.find_element(By.XPATH, '//input[@id="hobby-5"]')

        if hobbyCheckbox4.is_selected():
            hobbyCheckbox4.click()
        hobbyCheckbox4.click()

        if hobbyCheckbox5.is_selected():
            hobbyCheckbox5.click()
        hobbyCheckbox5.click()

        # submit
        saveButton = driver.find_element(By.XPATH, '//button[contains(text(), "Save Changes")]')
        driver.execute_script("arguments[0].scrollIntoView(true);", saveButton)
        saveButton.click()

        time.sleep(1)  
        alert = driver.switch_to.alert
        self.assertEqual(alert.text, "Profile updated successfully!", "error.")
        alert.accept()  

        time.sleep(2)

        # check the name
        updatedName = driver.find_element(By.XPATH, '//input[@id="name"]').get_attribute("value")
        self.assertEqual(updatedName, "Updated User", "name isn’t changed.")

        # check the dob
        updatedDob = driver.find_element(By.XPATH, '//input[@id="dob"]').get_attribute("value")
        self.assertEqual(updatedDob, "2005-05-15", "dob isn’t changed.")

        # check the hobbies
        isHobby4Selected = driver.find_element(By.XPATH, '//input[@id="hobby-4"]').is_selected()
        isHobby5Selected = driver.find_element(By.XPATH, '//input[@id="hobby-5"]').is_selected()
        self.assertTrue(isHobby4Selected, "hobby 4 not selected.")
        self.assertTrue(isHobby5Selected, "hobby 5 not selected.")



    def testAgeFilter(self):

        driver = self.driver
        self.login(driver, "joshua@gmail.com", "J05_hua")  # login

        # go to users page
        driver.get(self.baseUrl + "users/")
        driver.implicitly_wait(5)  

        # enter filter (i have made it 10 and 25)
        minAgeInput = driver.find_element(By.XPATH, '//input[@placeholder="Enter minimum age"]')
        maxAgeInput = driver.find_element(By.XPATH, '//input[@placeholder="Enter maximum age"]')
        filterButton = driver.find_element(By.XPATH, '//button[@class="filter-button"]')

        minAgeInput.clear()
        minAgeInput.send_keys("10")
        maxAgeInput.clear()
        maxAgeInput.send_keys("25")
        filterButton.click()

        time.sleep(3)  

        # check if correct
        users = driver.find_elements(By.XPATH, '//li[contains(@class, "user-item")]')
        self.assertGreater(len(users), 0, "no one in the filter range was found...")

        for user in users:
            try:
                
                ageText = user.find_element(By.XPATH, './/p[strong[contains(text(), "Age:")]]').text
                print(f"user in range found: {ageText}")  
                age = int(ageText.split(":")[1].strip().split(" ")[0])  
                self.assertTrue(15 <= age <= 20, f"age {age} isn’t in the range")
            except Exception as e:
                print(f"error: {e}")

        # do pagination buttons exist?
        paginationButtons = driver.find_elements(By.XPATH, '//button[contains(@class, "pagination-button")]')
        self.assertGreater(len(paginationButtons), 0, "no pagination buttons.")

        # does the next button work?
        nextButton = driver.find_element(By.XPATH, '//button[text()="Next"]')
        if nextButton.is_enabled():
            nextButton.click()
            time.sleep(3)  
            self.assertIn("users", driver.current_url.lower(), "cannot go to next page.")

    def testSendFriendRequest(self):
        driver = self.driver
        self.login(driver, "joshua@gmail.com", "J05_hua")  # login

        # send the request
        sendButton = driver.find_element(By.XPATH, '//button[contains(text(), "Send Friend Request")]')
        sendButton.click()

        time.sleep(2)
        print(driver.page_source)

        # check if request sent is there
        successMessage = driver.find_element(By.XPATH, '//div/em[contains(text(), "Request Sent")]')
        self.assertIsNotNone(successMessage, "Friend request success message not found.")

    def testAcceptFriendRequest(self):
        driver = self.driver

        # log in (this will be another user in the case of the marks scheme)
        self.login(driver, "brodyfoxx@gmail.com", "yomama")

        # nav to friend req page
        driver.get(self.baseUrl)
        time.sleep(2)

        # accept request
        acceptButton = driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]')
        acceptButton.click()
        time.sleep(5)

        # checks for pending requests (just for this test it will work)
        self.assertIn("No pending friend requests", driver.page_source)

    def login(self, driver, email, password):
        """
        just a function to log in because you log in a lot here
        """

        driver.get(self.baseUrl + "login/")

        # email , password
        driver.find_element(By.XPATH, '//label[contains(text(), "Email:")]/input').send_keys(email)
        driver.find_element(By.XPATH, '//label[contains(text(), "Password:")]/input').send_keys(password)

        driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        time.sleep(3)  

        
        self.assertIn("/", driver.current_url.lower(), "Login did not redirect to the home page.")
        self.assertTrue(
            "Welcome to the Hobbies App" in driver.page_source,
            "Home page content not found after login."
        )

    def tearDown(self):
        self.driver.quit()


#run the test if the file is run directly, not imported
#this is the main method that runs the test
#unittest.main() will run all the tests that are defined as unittest.TestCase
if __name__ == '__main__':
    
    unittest.main()

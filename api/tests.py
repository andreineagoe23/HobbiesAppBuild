from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import FriendRequest

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        data = {'name': 'updated Name'}
        response = self.client.put('/api/profile/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated name')

class FriendRequestTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='pass1')
        self.user2 = get_user_model().objects.create_user(username='user2', password='pass2')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_friend_request_send(self):
        response = self.client.post('/api/friend-requests/', {'to_user_id': self.user2.id})
        self.assertEqual(response.status_code, 201)

    def test_friend_request_accept(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/api/friend-requests/', {'request_id': friend_request.id, 'action': 'accept'})
        self.assertEqual(response.status_code, 200)

#-------------------Selenium Tests-------------------

#need to import the necessary selenium modules and just uncomment the above code
#once you have installed selenium as well on your envrionment. 
#you can install it using pip install selenium



# class SeleniumTests(TestCase):
class TestUserAgeFilter(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()#opens the browser
        self.driver.get("http://localhost:5173/")#specific url where front end is running, change this if it is different later

    #test to check if the user age filter is working
    def test_user_age_filter(self):
        driver = self.driver

        #I can remove the comments, for now i have kept them because
        #I was working with selenium tests for the first time so was trying to understand everything
        #Find min age and max age input fields 
        #driver.find.element finds element that matches the given xpath
        #xpath is query language for selecting nodes from an XML document - HTML rn so it will navigate through the entire HTML to find the element
        #finds element in this case with placeholder "Enter minimum age" and "Enter maximum age" and filter button
        min_age_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter minimum age"]')
        max_age_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter maximum age"]')
        filter_button = driver.find_element(By.XPATH, '//button[@class="filter-button"]')

        min_age_input.send_keys("15")#in the min age input field, we are sending the value 15
        max_age_input.send_keys("20")
        filter_button.click()#checks the filter button
        #end of front end interaction checks

        #find all elements with class user-item (basically gets all users from the database)
        users = driver.find_elements(By.XPATH, '//li[contains(@class, "user-item")]')

        #loop through all the users and check if the age is within the range of 20-30
        for user in users:
            #looks for a p tag with text "Age:" and gets the entire text - so likely "Age:15 years old"
            age_text = user.find_element(By.XPATH, './/p[contains(text(), "Age:")]').text 

            #extracts the age from the text - so it will get the 15 from "Age:15 years old"
            age = int(age_text.split(" ")[1]) # mainly to extract the age from the text -getting int value of age
            

            #the actual test - checks if the age is within the range of 15-20, if it is not true, then the text after comma is printed
            self.assertTrue(15 <= age <= 20, f"Age {age} is not within the filter range.")


            #check if the pagination buttons are present, wasnt sure what else to check, so just simply checking if the buttons are present
            pagination_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "pagination-button")]')
            
            #checks if the length of the pagination buttons is greater than 0, if it is not, then the text after comma is printed
            #how many pagination buttons are there, if there are none, then the test will fail
            self.assertGreater(len(pagination_buttons), 0, "Pagination buttons are missing.")

#special method for unit testing to clean up the environment after the test is done
#reset function 
    def tearDown(self):
        self.driver.quit()#closes the browser

#run the test if the file is run directly, not imported
#this is the main method that runs the test
#unittest.main() will run all the tests that are defined as unittest.TestCase
if __name__ == '__main__':
    unittest.main()


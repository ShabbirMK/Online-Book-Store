from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string
import os

letters = string.ascii_lowercase

# Getting the drivers in case it is not installed
browser = webdriver.Chrome(ChromeDriverManager().install())

# Getting the dummy covers and pdfs
coverFiles = []
for root, _, files in os.walk(os.path.join(os.path.join(os.getcwd(), "media"), "covers")):
    for filename in files:
        coverFiles.append(os.path.join(root, filename))

bookFiles = []
for root, _, files in os.walk(os.path.join(os.path.join(os.getcwd(), "media"), "pdf")):
    for filename in files:
        bookFiles.append(os.path.join(root, filename))


# Registering into the system
count = int(input("Enter the number of cycles of Register-Book upload: "))

for _ in range(count):
    browser.get("http://localhost:5000/signup")

    name = browser.find_element_by_name('inputName')
    email = browser.find_element_by_name('inputEmail')
    password1 = browser.find_element_by_name('inputPassword')
    password2 = browser.find_element_by_name('inputRetypedPassword')

    name.send_keys(''.join(random.choice(letters) for i in range(15)))
    email.send_keys(''.join(random.choice(letters)
                            for i in range(15)) + "@gmail.com")

    password = ''.join(random.choice(letters) for i in range(15))
    password1.send_keys(password)
    password2.send_keys(password)
    time.sleep(5)

    browser.find_element_by_tag_name("button").click()
    time.sleep(2)

    # Moving from the home page to the upload page
    browser.find_element_by_tag_name(
        "nav").find_elements_by_tag_name("a")[1].click()
    time.sleep(2)

    for _ in range(random.randint(1, 5)):
        browser.find_element_by_name("uploadBook").click()
        time.sleep(5)

        # Inputting the upload Book page
        title = browser.find_element_by_name("title")
        author = browser.find_element_by_name("authorname")
        summary = browser.find_element_by_name("summary")

        title.send_keys(''.join(random.choice(letters) for i in range(15)))
        author.send_keys(''.join(random.choice(letters) for i in range(15)))
        summary.send_keys(''.join(random.choice(letters + " ") for i in range(3000)))

        # Selecting the Primary and Secondary Genres
        i = random.randint(0, 4)
        primary = Select(browser.find_element_by_name("primarygenre"))
        primary.select_by_index(i)

        secondary = Select(browser.find_element_by_name("secondarygenre"))
        secondary.select_by_index((i + 1) % 5)

        # Selecting the files
        cover = browser.find_element_by_name(
            "cover").send_keys(random.choice(coverFiles))

        book = browser.find_element_by_name(
            "book").send_keys(random.choice(bookFiles))
        time.sleep(2)

        upload = browser.find_element_by_id("uploadBookButton")
        upload.send_keys(Keys.ENTER)
        time.sleep(2)

    browser.find_element_by_name("logoutFromSystem").click()
    time.sleep(2)

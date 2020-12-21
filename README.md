# Online-Book-Store

This is my implementation of an Online Book Store. The main focus of the project was:
1. Implement and make use of my knowledge about Flask and Flask SQL Alchemey
2. Make a project around basic CRUD operations
3. Explore Bootstrap and learn some basic HTML/CSS

There are routes implemented are:
1. Home Page:
  -> GET: The page loads
2. Sign in Page:
  -> GET: The page loads
	-> POST: The user is registered and a session is created
3. Log in Page:
	-> GET: The page loads
	-> POST: The user logs into the system and a session is created
4. Log out:
	-> GET: The session is terminated and redirected to home page
5. View All:
	-> GET: Check for authentication, and show all books with disabled features if unauthenticated
6. View One:
	-> GET: Check for authentication, and show details of the selected book
7. Upload Book:
	-> GET: Check for authentication, and fill the details in the form regarding the book
	-> POST: Enter the details in the database and save the cover, pdfs
8. Update Book:
	-> GET: Check for authentication, and fill the details in the form with previous data and correct them
	-> POST: Update the entry in the database with the new one
9. Delete Book:
	-> GET: Deletes the entry from the database, the cover and pdf, and redirects to home page
10. Filtered View:
	-> POST: Depending on the genre and the input string, search results are provided.
11. About Me:
	-> GET: A general About Me page

For the project, the modules needed would be:
	1. Flask
	2. Flask SQLAlchemey
	3. Selenium (Optional)
	4. Webdriver Manager (Optional)

To run the web app, use: python app.py

To populate the database with some dummy data using the data from the media folder use: python populate.py
	-> It requires Selenium and Webdrive Manager
	-> The input is the number of users registering, each uploading between 1 to 5 books.

# iMessages Project Project

This is my (first!) personal Python project for a gift to my partner for our second anniversary in mid-2019 - a quick website to host a random iMessage text from the past two years. She loved it! :)

Here were my steps for this project:

1. Using [these](http://aaron-hoffman.blogspot.com/2017/02/iphone-text-message-sqlite-sql-query.html) detailed steps from an Aaron Hoffman, find the ".db" file with all your iMessage data from your iPhone device iTunes backup.
2. Continuing with Hoffman's steps, modify [this SQL code](https://gist.github.com/aaronhoffman/cc7ee127f00b6b5462fa7fc742c23d4f) as needed and run it to view the texts. I uploaded mine as *'imessages_download.sql'*. I saved the data as a JSON file to sort in Python.
3. Make an account with [PythonAnywhere](www.pythonanywhere.com). Although the website no longer exists, I hosted it for free using [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/).
4. See *imessages_website.py* for the processing of the iMessage JSON file. I also only selected texts with positive content. Then route the random text result to the HTML site using Flask!

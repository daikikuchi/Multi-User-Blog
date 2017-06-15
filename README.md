# Multi User Blog
https://multiuserblogudacity.appspot.com/

The main technologies used in this project are Google App Engine, Jinja and Python.

## You can view it live here: https://multiuserblogudacity.appspot.com/

Requirements for local deployment
- Google App Engine SDK
- Python 2.7

To run it locally:
- Clone or download this repository 
- Install Google App Engine SDK https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
- Sign Up for a Google App Engine Account https://console.cloud.google.com/appengine
- Create a new project in Google’s Developer Console using a unique name.
- Follow the App Engine Quickstart to get a sample app up and running.
- cd to project folder and run dev_appserver.py . 
- Access it at http://localhost:8080/

## Project description

This is a blog project. User is directed to login, logout, and signup pages as appropriate. E.g., login page has a link to signup page and vice-versa; logout page is only available to logged in user. Links to edit blog pages are available to users. Users editing a page can click on a link to cancel the edit and go back to viewing that page. Blog pages render properly. Templates are used to unify the site.

Users are able to create accounts, login, and logout correctly.Existing users can revisit the site and log back in without having to recreate their accounts each time. Usernames are unique. Attempting to create a duplicate user results in an error message.Stored passwords are hashed. Passwords are appropriately checked during login. User cookie is set securely.

Logged out users are redirected to the login page when attempting to create, edit, delete, or like a blog post.Logged in users can create, edit, or delete blog posts they themselves have created. Users should only be able to like posts once and should not be able to like their own post.Only signed in users can post comments.
Users can only edit and delete comments they themselves have made.

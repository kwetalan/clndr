# Sowing Calendar

## Description

Sowing Calendar is a website that provides information about gardening based on astrological calculations. Registered users can communicate on the site by posting articles and leaving comments. The site is accompanied by instructions on how to use the calendar, the main page of which contains a calendar for the current month and a list of recommendations for each day of the month.
## Technical features

The project is written in Python, implemented using the Django framework. Class representations are used. A custom mixin has been implemented to simplify the insertion of data into the context. The calendar is calculated in the API and displayed on the page using API requests. API is implemented using Django Rest Framework. The main page of the blog contains a list of posts that can be sorted by date of addition and by views. For each post, the number of views is calculated when visiting the detailed page of the post and is displayed there. An account system has been implemented with the ability to register, log in and log out of an account. Registered users have a profile where you can view a personal data specified in the settings. It is possible to view other users profiles. Access to the page for creating articles is restricted for unregistered users. The form for sending comments is not visible to unregistered users.
The project consists of four applications for the account system, API, blog and main pages, and has three models for articles, comments and user profiles. There are forms for creating articles, comments and searching for articles.
## Issues and expected updates

The user data update form is not working correctly. Also, this form lacks a field for entering geodata, which should be taken into account when calculating the calendar. Recommendations will be selected based on the types of plants grown.

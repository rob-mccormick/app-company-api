# Ideal Role API app

This REST API app was built to provide company details to a recruitment chatbot. The API also collected analytics and information users entered while using the chatbot.

## Background
The idea for the chatbot started when I was speaking to people about applying for jobs. Often they had questions but no way of getting answers. So they didn’t apply.

While the questions people had were varied, they tended to fall into common categories. Which meant a chatbot could answer most of them in a couple of minutes, 24/7. The chatbot’s goal was to guide people to the right job and help them to apply. Getting more candidates for the companies using it.

The chatbot had three parts: 
1. The chatbot ([repo](https://github.com/rob-mccormick/gloria-master))
	2. The web chat window
	3. A REST API to access specific company details and save analytics data (this repo).

## What it’s built with
- Django REST Framework
- PostgreSQL

When it was running, the app was hosted on Heroku.

You can learn more about the chatbot on [my portfolio site](https://robmc.dev/portfolio/chatbot).

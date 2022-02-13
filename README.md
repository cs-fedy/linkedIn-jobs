# scrape linkedin jobs pages:

I'm scraping jobs pages from linkedIn, and i want to store them in a database(postgresql maybe).


## installation:

1. clone the repo `git clone https://github.com/cs-fedy/linkedIn-jobs`
2. change your current directory to the repo dir: `cd linkedIn-jobs`
3. install virtualenv using pip: `sudo pip install virtualenv`
4. create a new virtualenv:  `virtualenv venv`
5. activate the virtualenv: `source venv/bin/activate` if you are using linux
6. activate the virtualenv: `venv/Scripts/activate` if you are using windows
7. install requirements: `pip install -r requirements.txt`
8. change the email, password and url variables with your data
9. run the script and enjoy: `python main.py`

## used tools:

1. [selenium](https://www.selenium.dev/): Primarily it is for automating web applications for testing purposes, but is certainly not limited to just that. Boring web-based administration tasks can (and should) also be automated as well.
2. [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

## Author:
**created at 🌙 with 💻 and ❤ by f0ody**
* **Fedi abdouli** - **linkedIn jobs scraper** - [fedi abdouli](https://github.com/cs-fedy)
* my twitter account [FediAbdouli](https://www.twitter.com/FediAbdouli)
* my instagram account [f0odyy](https://www.instagram.com/f0odyy) 

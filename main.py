from selenium import webdriver
import bs4 as BeautifulSoup
import time
import os
import json


def create_browser() -> webdriver.Chrome:
    return webdriver.Chrome()

def load_full_page(browser, page_url):
    browser.get(page_url)
    time.sleep(10)
    print(f"@@@ {page_url} is loaded @@@")
    return browser, browser.page_source


class Login:
    def __init__(self, email, password) -> None:
        self.__browser: webdriver.Chrome = create_browser()
        self.__url: str = 'https://www.linkedin.com/login'
        self.__email: str = email
        self.__password: str = password
    
    def login(self) -> webdriver.Chrome:
        self.__browser, _ = load_full_page(self.__browser, self.__url)
        username_field = self.__browser.find_element_by_id('username')
        username_field.send_keys(self.__email)
        time.sleep(2)

        password_field = self.__browser.find_element_by_id('password')
        password_field.send_keys(self.__password)
        time.sleep(2)

        submit_btn = self.__browser.find_element_by_css_selector('button[type="submit"]')
        submit_btn.click()
        time.sleep(15)
        
        return self.__browser


class DB:
    def __init__(self, file_name: str) -> None:
        self.__file_name: str = file_name

    def save_data(self, data):
        if not os.path.exists(self.__file_name):
            with open(self.__file_name, 'w+') as file:
                json.dump([data], file)
        else:
            with open(self.__file_name, 'r') as file:
                loaded_data = json.load(file)

            loaded_data.append(data)
            with open(self.__file_name, 'w') as file:
                json.dump(loaded_data, file)

class EmployeeScraper:
    def __init__(self, browser, employee_url: str, company_title: str) -> None:
        self.__browser: webdriver.Chrome = browser
        self.__employee_url: str = employee_url
        self.__company_title: str = company_title

    def __get_name(self, soup: BeautifulSoup.BeautifulSoup, selector: str) -> str:
        return soup.select_one(selector).get_text().strip()

    def __get_bio(self, soup: BeautifulSoup.BeautifulSoup, selector: str) -> str:
        return soup.select_one(selector).get_text().strip()

    def __get_picture(self, soup: BeautifulSoup.BeautifulSoup, selector: str) -> str:
        return soup.select_one(selector)['src']

    def __get_job(self, soup: BeautifulSoup.BeautifulSoup, selector: str) -> str:
        jobs = soup.select_one(selector).findChildren()
        for job in jobs:
            if self.__company_title in job.get_text():
                
                return f'{self.__company_title} - job.select_one("span").get_text()'.strip()
        return ''

    def scrape_employee_data(self):
        self.__browser, content = load_full_page(self.__browser, self.__employee_url)
        soup = BeautifulSoup.BeautifulSoup(content, 'html.parser')
        return {
            'link': self.__employee_url,
            'name': self.__get_name(soup, 'h1'),
            'bio': self.__get_bio(soup, '.pv-text-details__left-panel .text-body-medium.break-words'),
            'picture': self.__get_picture(soup, 'img.pv-top-card-profile-picture__image.pv-top-card-profile-picture__image--show ember-view'),
            'job': self.__get_job(soup, '#ember1121 .pvs-list__outer-container .pvs-list'),
        }

class PageScraper:
    def __init__(self, browser, page) -> None:
        self.__browser: webdriver.Chrome = browser
        self.__page: str = f'{page}about'

    def __get_page_title(self, soup: BeautifulSoup.BeautifulSoup, selector: str) -> str:
        return soup.select_one(selector).get_text().strip()

    def __get_indexed_element_by_selector(self, soup: BeautifulSoup.BeautifulSoup, selector: str, index: int) -> str:
        try:
            return soup.select(selector)[index].get_text().strip()
        except:
            return ''

    def __get_company_size(self, soup: BeautifulSoup.BeautifulSoup) -> str:
        dd_elements = soup.select('main dl dd')
        employees, on_linkedIn = '', ''
        for element in dd_elements:
            if "employees" in element.get_text(): employees = element.get_text()
            if "on LinkedIn" in element.get_text(): on_linkedIn = element.get_text()
        
        return f'{employees} - {on_linkedIn}'.strip()

    def __get_next_element_content(self, soup: BeautifulSoup.BeautifulSoup, text: str) -> int:
        elements = soup.select_one('main dl').findChildren()
        for index, element in enumerate(elements):
            if text in element.get_text():
                return elements[index+1].get_text().strip()


    def __get_page_details(self, content: str):
        soup = BeautifulSoup.BeautifulSoup(content, 'html.parser')
        return {
            'title': self.__get_page_title(soup, 'h1'),
            'followers_count': self.__get_indexed_element_by_selector(soup, '.org-top-card-summary-info-list__info-item', -1),
            'description': self.__get_indexed_element_by_selector(soup, 'main p', 1),
            'website': self.__get_indexed_element_by_selector(soup, 'main a span', 2),
            'company_size': self.__get_company_size(soup),
            'founded': int(self.__get_next_element_content(soup, "Founded")),
            'specialties': self.__get_next_element_content(soup, "Specialties"),
            'location': self.__get_indexed_element_by_selector(soup, 'main p', -1)
        }

    def __get_page_urls(self, content) -> set[str]:
        soup = BeautifulSoup.BeautifulSoup(content, 'html.parser')
        return {element['href'] for element in soup.select('.entity-result__title-line a')}

    def __get_employees_urls(self, content):
        soup = BeautifulSoup.BeautifulSoup(content, 'html.parser')
        urls_page = soup.select_one('main .mt1 a')['href']
        self.__browser, content = load_full_page(self.__browser, f'https://www.linkedin.com{urls_page}')

        urls = set()
        next_btn_selector = 'artdeco-pagination__button--next'
        time.sleep(10)
        while not self.__browser.find_element_by_class_name(next_btn_selector).get_property('disabled'):
            urls += self.__get_page_urls(self.__browser.page_source)
            self.__browser.find_element_by_class_name(next_btn_selector).click()
        time.sleep(20)
        return list(urls)

    def scrape_page_data(self) -> None:
        self.__browser, content = load_full_page(self.__browser, self.__page)
        page_details = self.__get_page_details(content)
        DB('pages.json').save_data(page_details)

        employees_db = DB('employees.json')
        employees_urls: list[str] = self.__get_employees_urls(content)
        print(employees_urls)
        for url in employees_urls:
            employee_scraper = EmployeeScraper(self.__browser, url, page_details['title'])
            employee_data = employee_scraper.scrape_employee_data()
            employees_db.save_data(employee_data)



if __name__ == '__main__':
    email, password = 'your email here', 'your password here'
    login_model = Login(email, password)
    browser = login_model.login()

    url = 'your url'
    page_scraper = PageScraper(browser, url)
    page_scraper.scrape_page_data()
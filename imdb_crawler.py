from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

page = 'https://www.imdb.com/'
movie = 'Interstellar'
recent_reviews = [] 

def main():
    driver = webdriver.Chrome()
    driver.get(page)
    search_form = driver.find_element(By.ID, "suggestion-search")
    search_form.send_keys(movie)
    search_button = driver.find_element(By.ID, "suggestion-search-button")
    search_button.click()
    time.sleep(5)
    movie_link = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")[0]
    movie_link.click()
    time.sleep(5)
    reviews_link = driver.find_element(By.LINK_TEXT, "User reviews")
    reviews_link.click()
    time.sleep(5)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "lister-sort-by"))
    dropdown.select_by_index(1)
    time.sleep(5)
    reviews = driver.find_elements(By.CSS_SELECTOR, "div[class^='text show-more__control']")
    reviews_text = [review.text for review in reviews]
    recent_reviews = reviews_text[:20]
    return recent_reviews

main()
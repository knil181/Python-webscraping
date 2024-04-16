import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Prompt the user to enter the team link
team_link = input("Enter the link to the team in Transfermarkt: ")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window

# Set path to your chromedriver executable
chrome_driver_path = "/chromedriver"

# Create a new Chrome browser instance
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Load the website and wait for 5 seconds
driver.get(team_link)
time.sleep(5)

iframe_xpath = '//*[@id="sp_message_iframe_764226"]'
WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath))
)

# Find and click the "Accept all" button
container_xpath = '/html/body/div'
div1_xpath = '/html/body/div/div[1]'
div3_xpath = '//*[@id="notice"]/div[3]'
div2_xpath = '//*[@id="notice"]/div[3]/div[2]'
button_xpath = '//*[@id="notice"]/div[3]/div[2]/button'

container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, container_xpath))
)

div1 = container.find_element(By.XPATH, div1_xpath)
div3 = div1.find_element(By.XPATH, div3_xpath)

div2 = div3.find_element(By.XPATH, div2_xpath)

accept_all_button = WebDriverWait(div2, 1).until(
    EC.element_to_be_clickable((By.XPATH, button_xpath))
)
accept_all_button.click()
time.sleep(2)

driver.execute_script("window.scrollBy(0, 800)")#scrolls the page by little

# Go to "Transfers & Rumors" and then "Current Season Transfers"
transfer_rumours_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="transfers-amp-rumours"]/a'))
)
transfer_rumours_link.click()

current_season_transfer_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="transfers-amp-rumours"]/div/div/div[1]/ul/li[1]/a'))
)
current_season_transfer_link.click()

time.sleep(10)

# Find and open tabs for each departed player
driver.execute_script("window.scrollBy(0, 800)")  # Adjust the scroll amount as needed

time.sleep(2)  # Add a short delay to allow the page to scroll

# Click on the "Departed Players" link
container_xpath = '//*[@id="main"]/main/div[2]/div[1]/div[3]'
container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, container_xpath))
)

# Find all the player elements within the container
player_elements = container.find_elements(By.XPATH, './/a[contains(@href, "profil")]')

# Determine the range of players to open links for
num_players = min(len(player_elements), 18)  # Limit to 18 players or the total number of players if less

# Open links of departed players in new tabs starting from the end
for i in range(len(player_elements) - 1, len(player_elements) - num_players - 1, -1):
    player_element = player_elements[i]
    link = player_element.get_attribute('href')
    driver.execute_script("window.open(arguments[0]);", link)

# Get the handles of all the currently open tabs
current_handles = driver.window_handles

# Switch to the newly opened tabs
for handle in current_handles[len(current_handles)-num_players:]:
    driver.switch_to.window(handle)
    
    # Scroll down the page
    driver.execute_script("window.scrollBy(0, 500)")  # Adjust the scroll amount as needed
    
    # Click on the "Stats" link
    stats_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="stats"]/a'))
    )
    stats_link.click()

    # Click on the "All Season" link
    all_season_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="stats"]/div/div/div[1]/ul/li[2]/a'))
    )
    all_season_link.click()

# Keep the browser window open for inspection
input("Press Enter to close the browser window...")

# Quit the browser
driver.quit()

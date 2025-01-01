from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json

# WebDriver setup
driver = webdriver.Chrome()

# YouTube open karna
driver.get("https://www.youtube.com")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search_query")))  # Wait for the search bar

# Search bar locate karna aur query dalna
search_box = driver.find_element(By.NAME, "search_query")  # Search bar locate karein
search_box.send_keys("code with harry")  # Query type karein
search_box.send_keys(Keys.RETURN)  # Enter key press karein
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.channel-link[href*='/@CodeWithHarry']")))  # Wait for results
time.sleep(2)  # Let results load

# "CodeWithHarry" channel ke link ko locate karna aur usko open karna
try:
    channel_link = driver.find_element(By.CSS_SELECTOR, "a.channel-link[href*='/@CodeWithHarry']")
    channel_url = channel_link.get_attribute("href")  # href attribute retrieve karein

    print(f"Channel URL: {channel_url}")
    if channel_url:
        driver.get(channel_url)  # Channel link open karein
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//yt-tab-shape[@tab-title='Videos']")))  # Wait for the "Videos" tab
        print("Channel opened successfully!")
    else:
        print("Channel URL not found!")

    videos_tab = driver.find_element(By.XPATH, "//yt-tab-shape[@tab-title='Videos']")
    videos_tab.click()  # Click on the "Videos" tab
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents ytd-rich-item-renderer a#thumbnail")))
    time.sleep(2)  # Let the videos load
    print("Videos tab clicked successfully!")

    # Scroll until the end of the page
    previous_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
        time.sleep(3)  # Wait for new content to load

        # Wait for new content to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#contents ytd-rich-item-renderer"))
        )
        
        # Get the new page height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            print("Reached the end of the page.")
            break
        previous_height = new_height

    # Videos ke links ko collect karna
    video_links = []
    video_elements = driver.find_elements(By.CSS_SELECTOR, "#contents ytd-rich-item-renderer a#thumbnail")
    for video in video_elements:
        href = video.get_attribute("href")
        if href:
            video_url = f"https://www.youtube.com{href}"
            video_links.append(video_url)

    # Save links to CSV
    with open("video_links.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Video URL"])
        for link in video_links:
            writer.writerow([link])

    print("Video links have been saved to CSV file.")

    # Save links to JSON
    with open("video_links.json", mode="w") as json_file:
        json.dump(video_links, json_file, indent=4)

    print("Video links have been saved to JSON file.")

except Exception as e:
    print(f"Error occurred: {e}")

# Browser close karna
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# WebDriver setup
driver = webdriver.Chrome()

try:
    # Read all links from the CSV file
    links = []
    with open("cleaned_video_links.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        links = [row[0] for row in reader]  # Collect all video links

    if not links:
        print("No video links found in the CSV file.")
    else:
        for index, link in enumerate(links, start=1):
            print(f"Opening video {index}: {link}")
            driver.get(link)  # Open the video URL
            
            try:
                # Wait for the video title to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title")))
                print(f"Video {index} opened successfully!")

                # Locate the play button and click it
                try:
                    play_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-play-button"))
                    )
                    play_button.click()  # Play the video
                    print(f"Video {index} started playing!")
                except Exception as e:
                    print(f"Error while trying to play video {index}: {e}")

                # Monitor the video until it ends
                while True:
                    try:
                        # Check for the "Skip Ad" button
                        skip_ad_button = driver.find_elements(By.CSS_SELECTOR, ".ytp-skip-ad-button")
                        if skip_ad_button:
                            skip_ad_button[0].click()
                            print("Ad skipped!")

                        # Check if the video has ended
                        is_ended = driver.execute_script("return document.querySelector('video').ended")
                        if is_ended:
                            print(f"Video {index} has ended.")
                            break

                        # Wait a bit before checking again
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error during playback monitoring for video {index}: {e}")
                        break

            except Exception as e:
                print(f"Error occurred while opening video {index}: {e}")

except Exception as e:
    print(f"Error occurred during execution: {e}")

finally:
    # Close the browser
    driver.quit()

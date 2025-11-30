from selenium import webdriver
from startup_info import StartupInfo

import re
import time
import selenium

startups = []

while True:

    startup = StartupInfo()

    url = input("URL (or q to end):")
    if url == "q":
        break

    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(0.1)
        html = driver.page_source
        #print(html)

        match = re.search(r'<span class="soft-black">(.*?)</span>', html, re.DOTALL)
        startup.money_taken_local = match.group(1)

        match = re.findall(r'<span class="money">(.*?)</span>', html, re.DOTALL)
        startup.money_taken_USD = match[-2]
        startup.planned_money_local = match[-3]
        startup.planned_money_USD = match[-1]

        match = re.search(r'<div class="ml5 ml0-lg mb4-lg"><div class="block type-16 type-28-md bold dark-grey-500"><span>(.*?)</span>', html, re.DOTALL)
        startup.backers = match.group(1)

        match = re.search(r'Updates\n<span class="count">(.*?)</span>', html, re.DOTALL)
        startup.updates = match.group(1)

        match = re.search(r'Comments\n<span class="count">(.*?)</data></span>', html, re.DOTALL)
        comments_str = match.group(1)
        match = re.search(r'data-value="(.*?)"', comments_str, re.DOTALL)
        startup.comments = int(match.group(1))

        if '<button aria-label="Play video"' in html:
            startup.has_video = True


        print(startup)
        startups.append(startup)
        driver.quit()

    except(selenium.common.exceptions.InvalidArgumentException):
        print("Bad URL")
        driver.quit()
        continue

timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = f"startup_data_{timestamp}.txt"
with open(output_file, "w") as f:

    f.write("header TODO\n")
    for startup in startups:
        f.write(str(startup))
        f.write("\n")

"""
    author_created_number = ""
    author_backed_number = ""
    author_registration_date = ""
    rewards_num = 0
    lowest_reward = 0
    highest_reward = 0
"""
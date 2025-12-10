from selenium import webdriver
from startup_info import StartupInfo

import re
import time
import selenium
import sys

startups = []
input_file = ""
urls = []

input_file = sys.argv[1]

with open(input_file, "r") as f:
    urls = f.readlines()

timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = f"startup_data_{timestamp}.txt"
with open(output_file, "w") as f:
    f.write("money_taken_local;money_taken_USD;planned_money_local;planned_money_USD;backers;updates;comments;has_video;author_created_number;author_backed_number;author_registration_date;rewards_num;lowest_reward;highest_reward\n")

for url in urls:

    startup = StartupInfo()

    if "?" in url:
        url = url.split("?")[0]

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

        match = re.search(r'<div class="text-left mb3">(.*?) created<span class="divider">&nbsp;•&nbsp;</span>(.*?) backed</div>', html, re.DOTALL)
        startup.author_created_number = match.group(1)
        startup.author_backed_number = match.group(2)

        driver.quit()

        driver = webdriver.Firefox()
        driver.get(f"{url}/creator")
        time.sleep(0.1)
        html = driver.page_source

        match = re.search(r'<span class="kds-type kds-type-heading-sm">account created</span><span class="kds-type kds-type-heading-lg">(.*?)</span>', html, re.DOTALL)
        try:
            startup.author_registration_date = match.group(1)
        except(AttributeError):
            startup.author_registration_date = ""

        driver.quit()

        driver = webdriver.Firefox()
        driver.get(f"{url}/rewards")
        time.sleep(0.1)
        html = driver.page_source

        reward_list = re.findall(r'<span class="type-12 support-500"><span class="semibold">(.*?)</span><span class="ml1">', html, re.DOTALL)

        startup.rewards_num = len(reward_list)

        if startup.rewards_num > 0:
            min_reward = 999999
            max_reward = 0

            for reward in reward_list:
                reward_int = int("".join(c for c in reward if c.isdigit()))
                if reward_int < min_reward:
                    min_reward = reward_int
                if reward_int > max_reward:
                    max_reward = reward_int

            startup.lowest_reward = min_reward
            startup.highest_reward = max_reward

        print(startup)
        startups.append(startup)

        with open(output_file, "a") as f:
            f.write(str(startup))
            f.write("\n")

        driver.quit()

    except(selenium.common.exceptions.InvalidArgumentException):
        print("Bad URL")
        driver.quit()
        continue

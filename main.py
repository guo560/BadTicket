import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def check_and_click(xpath) -> bool:
    text = browser.find_element_by_xpath(xpath).text[-3:]
    if text == "可预约":
        browser.find_element_by_xpath(xpath).click()
        return True
    return False


def switch_to(day: str = "周日"):
    today = browser.find_element_by_class_name("today2").text
    while today != day:
        browser.find_element_by_class_name("next_day").click()
        today = browser.find_element_by_class_name("today2").text


def choose_time(index):
    s = Select(browser.find_element_by_id("starttime"))
    s.select_by_index(index=index)


def main(day, time_index):
    browser.find_elements_by_class_name("myyuyue")[-1].click()  # -1表示西体
    switch_to(day)  # 切换到周？
    choose_time(time_index)  # 0-6：早8点到晚8点
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/table/tbody/tr[4]/td/input").click()  # 选择同伴
    browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]").click()  # 选择第一位同伴
    time.sleep(1)
    # 西体各个场地对应的xpath
    xpath_dict = {1: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[6]/td[4]",
                  2: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[6]/td[5]",
                  3: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[6]/td[6]",
                  4: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[5]/td[6]",
                  5: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[5]/td[5]",
                  6: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[5]/td[4]",
                  7: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[5]/td[3]",
                  8: "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/tr[6]/td[3]"}
    # 优先选择场地
    priority = [6, 5, 2, 1, 7, 4, 8, 3]
    for i in priority:
        if check_and_click(xpath_dict[i]):
            browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div[3]/input[3]").click()  # 点击预约按钮
            break


if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    with webdriver.Chrome(options=options) as browser:
        while True:
            now = datetime.datetime.now()
            # 8点开抢
            if now.hour == 16:
                main("周六", 1)
                break
            time.sleep(1)

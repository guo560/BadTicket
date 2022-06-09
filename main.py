import time
import datetime

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from cmd import run


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


def get_xpath(stadium: int) -> dict:
    xpath_dict = {}
    root_xpath = "/html/body/div[2]/div[2]/div[2]/form/div[1]/table/tbody/"
    xpath_tail = {
        -1: ["tr[6]/td[4]", "tr[6]/td[5]", "tr[6]/td[6]", "tr[5]/td[6]",
             "tr[5]/td[5]", "tr[5]/td[4]", "tr[5]/td[3]", "tr[6]/td[3]"],
        0: ["tr[3]/td[2]", "tr[3]/td[3]", "tr[3]/td[4]", "tr[3]/td[5]", "tr[3]/td[6]",
            "tr[4]/td[2]", "tr[4]/td[3]", "tr[4]/td[4]", "tr[4]/td[5]", "tr[4]/td[6]",
            "tr[5]/td[2]", "tr[5]/td[5]", "tr[5]/td[4]", "tr[5]/td[5]", "tr[5]/td[6]",
            "tr[6]/td[2]", "tr[6]/td[3]", "tr[6]/td[6]", "tr[6]/td[5]", "tr[6]/td[6]",
            "tr[3]/td[7]", "tr[5]/td[7]"]
    }
    for idx, xpath in enumerate(xpath_tail[stadium]):
        xpath_dict[idx + 1] = root_xpath + xpath
    return xpath_dict


def ticket_grabbing(stadium: int, day, time_index_list: list):
    browser.find_elements_by_class_name("myyuyue")[stadium].click()  # 选择预约体育馆
    try:
        time.sleep(0.1)
        browser.find_element_by_xpath('//*[@id="dialog_0"]/div[2]/div/div/div[2]/div').click()
    except:
        switch_to(day)  # 选择预约星期几
        # 获取体育馆各个场地对应的 xpath
        xpath_dict = get_xpath(stadium)
        # 优先选择场地
        priority = {
            0: [1, 6, 11, 16, 5, 10, 15, 20, 21, 22, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19],
            -1: [6, 5, 2, 1, 7, 4, 8, 3]
        }
        for index in time_index_list:
            choose_time(index)  # 选择预约时间段
            browser.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div[2]/form/table/tbody/tr[4]/td/input").click()  # 选择同伴
            browser.find_element_by_xpath(
                "/html/body/div[3]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]").click()  # 选择第一位同伴
            time.sleep(0.2)
            for i in priority[stadium]:
                if check_and_click(xpath_dict[i]):
                    browser.find_element_by_xpath(
                        "/html/body/div[2]/div[2]/div[2]/form/div[3]/input[3]").click()  # 点击预约按钮
                    return


def main():
    # 相关参数设置
    # 0: "光谷体育馆", -1: "西边体育馆"
    stadium = -1  # TODO: 记得选择场馆！！！
    # 0: "周一",  1: "周二",   2: "周三",  3: "周四",
    # 4: "周五",  5: "周六",   6: "周日"
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # 0: 08:00 - 10:00,   1: 10:00 - 12:00
    # 2: 12:00 - 14:00,   3: 14:00 - 16:00
    # 4: 16:00 - 18:00,   5: 18:00 - 20:00
    # 6: 20:00 - 22:00
    time_index_list = [4, 5, 6, 3, 1, 2]  # TODO: 记得选择时段优先级！！！

    while True:
        # 08:00 - 22:00 可抢时段
        try:
            ticket_grabbing(stadium, weekday[7 - 1], time_index_list)  # TODO: 记得选择星期几！！！
        except:
            break
        time.sleep(0.1)


if __name__ == '__main__':
    path = "C:/Program Files/Google/Chrome/Application"  # chrome.exe所在文件夹
    port = 9527
    run(path, port)

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    with webdriver.Chrome(options=options) as browser:
        browser.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/ul/li[1]/a/img").click()  # 点击校内人员登陆
        browser.close()

    with webdriver.Chrome(options=options) as browser:
        while browser.title != "华中科技大学体育场馆管理系统":
            pass
        browser.find_element_by_xpath('//*[@id="main"]/ul/li[2]/a').click()  # 点击场馆预约
        main()

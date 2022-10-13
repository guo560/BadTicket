import requests


def find_user_rank_by_user_name(name: str, week_number: int, page=1):
    while True:
        url = "https://leetcode.cn/contest/api/ranking/weekly-contest-" + str(week_number) + "/?pagination=" + str(
            page) + "&region=local"
        resp = requests.get(url)
        if resp.status_code == 200:
            js = resp.json()
            users = [users for users in js['total_rank']]
            for user in users:
                if name == user['real_name']:
                    print("user found in page " + str(page) + ". user's rank is " + str(user['rank_v2']))
                    return
        else:
            print("error in getting page " + str(page))
        page += 1


if __name__ == '__main__':
    find_user_rank_by_user_name("yqhp", 310)
    find_user_rank_by_user_name("时光放逐", 310)

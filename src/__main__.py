from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from src.dao.HitResultDao import HitResultDao


def get_game_result(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    game_result_url = "https://sports.news.naver.com" + url
    p = re.compile("[^0-9]")
    teaminfo = "".join(p.findall(game_result_url[game_result_url.rfind("=") + 1:].replace("[0-9]", "")))
    awayteam = teaminfo[0:2]
    hometeam = teaminfo[2:]
    gamedate = game_result_url[game_result_url.rfind("=") + 1: game_result_url.rfind("=") + 9]
    print(game_result_url)
    driver = webdriver.Chrome("D:/Dev/selenium_drivers/chromedriver", options=options)
    driver.get(game_result_url)
    game_result_html = driver.page_source
    game_result_bs_object = BeautifulSoup(game_result_html, "html.parser")

    game_result_items = game_result_bs_object.find_all("div", {"class": {"ico"}})

    for item in game_result_items:
        item_styles = item.attrs["style"].replace(" ", "").split(";")
        left = item_styles[0][5:len(item_styles[0]) - 2]
        top = item_styles[1][4:len(item_styles[1]) - 2]
        detail_infos = item.find_all(lambda tag: tag.name == "em" or tag.name == "strong")
        inning = detail_infos[1].get_text(strip=True)
        batter = detail_infos[2].get_text(strip=True).split(" ")[0]
        result_text = item.contents[1].get_text(strip=True)

        pitcher = result_text[result_text.find("상대투수"):].replace("상대투수-", "")
        result = '아웃'
        if "hit" in item.attrs["class"]:
            result = '안타'
        elif "run" in item.attrs["class"]:
            result = '홈런'
        elif "out" in item.attrs["class"]:
            print("아웃" + left + top)

        __hitresultDao = HitResultDao()
        __hitresultDao.setResult(batter, pitcher, result, left, top, inning, hometeam, awayteam, gamedate)


baseball_url_prefix = "https://sports.news.naver.com/kbaseball/schedule/index.nhn?month="
game_years = range(2008, 2019)

for game_year in game_years:
    baseball_url_postfix = "&year=" + "%02d" % game_year + "&teamCode="
    game_months = range(3, 12)

    for game_month in game_months:
        html = urlopen(baseball_url_prefix + "%02d" % game_month + baseball_url_postfix)
        bs_object = BeautifulSoup(html, "html.parser")

        divs = bs_object.find_all("div", {"class": {"sch_tb", "sch_tb2"}})

        for div in divs:
            if "nogame" not in div.attrs["class"]:
                game_links = div.find_all("span", {"class": "td_btn"})
                for game_link in game_links:
                    if game_link is not None:
                        href = game_link.find("a")["href"]

                        p = re.compile("[^0-9]")
                        teaminfo = "".join(p.findall(href[href.rfind("=") + 1:].replace("[0-9]", "")))
                        awayteam = teaminfo[0:2]
                        hometeam = teaminfo[2:]
                        gamedate = href[href.rfind("=") + 1: href.rfind("=") + 9]
                        __hitresultDao = HitResultDao()
                        if (__hitresultDao.isExistResult(gamedate, hometeam, awayteam) == False):
                            get_game_result(href)

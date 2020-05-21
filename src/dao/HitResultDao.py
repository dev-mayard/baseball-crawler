from src.db.DbHelper import DbHelper


class HitResultDao:
    __db = None;

    def __init__(self):
        self.__db = DbHelper()

    def setResult(self, batter, pitcher, result, left, top, inning, hometeam, awayteam, gamedate):
        self.__db.query("INSERT INTO hit_result(hitter_name, pitcher_name, hit_result, axis_left, axis_top, inning, hometeam, awayteam, gamedate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (batter, pitcher, result, left, top, inning, hometeam, awayteam, gamedate))

    def isExistResult(self, gamedate, hometeam, awayteam):
        result = self.__db.query("SELECT count(*) FROM hit_result WHERE gamedate = %s AND hometeam = %s AND awayteam = %s", (gamedate, hometeam, awayteam)).fetchall();
        if result[0]['count(*)'] > 0:
            return True
        else:
            return False

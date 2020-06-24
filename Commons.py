TIME_LIMIT = 3000
TIME_INTERVAL = 10
OVERVIEW_TEXT = ("Witaj! Gra polega na poprawnym wybraniu jak największej liczby pól szachowych"
                 " w ciągu 30 sekund. Za każde poprawnie wybrane pole zdobywasz o 1 punkt więcej."
                 " Prawdopodobnie zauważyłeś, że szachownica jest ustawiona z punktu widzenia białych."
                 " Współrzędne kolejnych pól będą wyświetlane w prawym dolnym rogu ekranu. Zacznij grę klikając 'Start'"
                 ". Rozgrywka trwa do momentu upłynięcia czasu lub wybrania przycisku 'Stop', który zakończy grę. "
                 "Powodzenia!")


def getY(number):
    return number % 8


def getX(number):
    return number // 8

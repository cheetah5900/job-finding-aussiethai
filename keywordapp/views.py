
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect

from datetime import date,timedelta,datetime

# require login to enter function
# import model
from keywordapp.models import *

# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# To setting mobile device broswer


# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================



def Work(request):
    context = {}
    headerList = []
    dateList = []
    contentList = []
    linkList = []

    # sort by last 7 days
    currentDate = date.today()
    lastSevenDays = currentDate-timedelta(days=7)
    data = ListOfWorkModel.objects.filter(date__range=[lastSevenDays,currentDate]).order_by('-date','-id')


    for item in data:
        headerList.append(item.header)
        contentList.append(item.content)
        linkList.append(item.link)

        day = item.date.strftime("%d")
        month = item.date.strftime("%b")
        year = item.date.strftime("%Y")
        dateReFormat = "{} {} {}".format(day, month, year)
        dateList.append(dateReFormat)


    dataForLoop = zip(headerList,dateList,contentList,linkList)

    context['dataForLoop'] = dataForLoop

    return render(request, 'keywordapp/work.html', context)


def House(request):
    context = {}
    headerList = []
    dateList = []
    contentList = []
    linkList = []

    # sort by last 7 days
    currentDate = date.today()
    lastSevenDays = currentDate-timedelta(days=7)
    data = ListOfHouseModel.objects.filter(date__range=[lastSevenDays,currentDate]).order_by('-date','-id')

    for item in data:
        headerList.append(item.header)
        contentList.append(item.content)
        linkList.append(item.link)

        day = item.date.strftime("%d")
        month = item.date.strftime("%b")
        year = item.date.strftime("%Y")
        dateReFormat = "{} {} {}".format(day, month, year)
        dateList.append(dateReFormat)


    dataForLoop = zip(headerList,dateList,contentList,linkList)

    context['dataForLoop'] = dataForLoop
    return render(request, 'keywordapp/house.html', context)


# =============================== REFRESH CHECK ===============================
# =============================== REFRESH CHECK ===============================
# =============================== REFRESH CHECK ===============================
def RefreshConditionCheck(request):

    RefreshWork()
    RefreshHouse()
    return 'done'

# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshWork():

    # Delete temp link before start anything
    TempLinkOfWorkModel.objects.all().delete()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    driver.get('https://sydneythai.info/jobs.php')

    # if cannot find searchBoxHomePage will re-open browser
    checkElement = True
    while checkElement == True:
        try:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.find_element(By.CLASS_NAME, 'feature-box'))
            checkElement = False
        except:
            print("Cannot find feature-box")
            driver.quit()
            checkElement = False
    link = driver.find_elements(By.CSS_SELECTOR, 'div.feature-box-info > h4.shorter > a')

    # Call link of work to check extist links
    LinkOfWork = LinkOfWorkModel.objects.all()
    countLinkOfWork = LinkOfWork.count()

    newWork = 0
    for x in link:
        tempLink = x.get_attribute('href')
        if countLinkOfWork == 0:
                # permanent link
                newLinkOfWork = LinkOfWorkModel()
                newLinkOfWork.link = tempLink
                newLinkOfWork.save()
                # temp link
                newLinkOfWork = TempLinkOfWorkModel()
                newLinkOfWork.link = tempLink
                newLinkOfWork.save()
        else:
            duplicatedCheck = 0
            for item in LinkOfWork:
                if tempLink == item.link:
                    duplicatedCheck = 1
            # if it is not duplicate it can add to db
            if duplicatedCheck == 0:
                # permanent link
                newLinkOfWork = LinkOfWorkModel()
                newLinkOfWork.link = tempLink
                newLinkOfWork.save()
                # temp link
                newLinkOfWork = TempLinkOfWorkModel()
                newLinkOfWork.link = tempLink
                newLinkOfWork.save()
                newWork += 1

    driver.quit()

    CollectWorkFromDB()

    # Delete temp link after finish everything
    TempLinkOfWorkModel.objects.all().delete()

    return 'done'

def CollectWorkFromDB():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    # Call all data for looping
    tempLinkOfWork = TempLinkOfWorkModel.objects.all()
    for x in tempLinkOfWork:
        tempLink = x.link
        driver.get(tempLink)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        dateText = date.text
        dateOnly = dateText[0:2]

        #Convert text to number to check
        dateToInt = int(dateOnly)

        if dateToInt <= 9:
            monthOnly = dateText[2:5]
            yearOnly = dateText[6:10]
        else:
            monthOnly = dateText[3:6]
            yearOnly = dateText[7:11]

        #Convert text to number
        yearToInt = int(yearOnly)
        monthToInt = ConvertMonthToNumber(monthOnly)

        # If header is "หางาน" Remove it
        headerText = header.text
        checkHeader = RemoveUnwantedHeader(headerText)

        if checkHeader == 'pass':
            # Add data
            newListOfWork = ListOfWorkModel()
            newListOfWork.link = tempLink
            newListOfWork.header = header.text
            newListOfWork.date = "{}-{}-{}".format(yearToInt,monthToInt,dateToInt)
            newListOfWork.content = content.text
            newListOfWork.save()
        else:
            pass

    driver.quit()
    return 'done'



# =============================== HOUSE ===============================
# =============================== HOUSE ===============================
# =============================== HOUSE ===============================

def RefreshHouse():

    # Delete temp link before start anything
    TempLinkOfHouseModel.objects.all().delete()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    driver.get('https://sydneythai.info/house.php')

    # if cannot find searchBoxHomePage will re-open browser
    checkElement = True
    while checkElement == True:
        try:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.find_element(By.CLASS_NAME, 'feature-box'))
            checkElement = False
        except:
            print("Cannot find feature-box")
            driver.quit()
            checkElement = False
    link = driver.find_elements(By.CSS_SELECTOR, 'div.feature-box-info > h4.shorter > a')

    # Call all data for checking
    LinkOfHouse = LinkOfHouseModel.objects.all()
    countLinkOfHouse = LinkOfHouse.count()

    newHouse = 0
    for x in link:
        tempLink = x.get_attribute('href')
        if countLinkOfHouse == 0:
                # permanent link
                newLinkOfHouse = LinkOfHouseModel()
                newLinkOfHouse.link = tempLink
                newLinkOfHouse.save()
                # temp link
                newLinkOfHouse = TempLinkOfHouseModel()
                newLinkOfHouse.link = tempLink
                newLinkOfHouse.save()
        else:
            duplicatedCheck = 0
            for item in LinkOfHouse:
                if tempLink == item.link:
                    duplicatedCheck = 1
            # if it is not duplicate it can add to db
            if duplicatedCheck == 0:
                # permanent link
                newLinkOfHouse = LinkOfHouseModel()
                newLinkOfHouse.link = tempLink
                newLinkOfHouse.save()
                # temp link
                newLinkOfHouse = TempLinkOfHouseModel()
                newLinkOfHouse.link = tempLink
                newLinkOfHouse.save()
                newHouse += 1

    driver.quit()

    CollectHouseFromDB()
    # Delete temp link before start anything
    TempLinkOfHouseModel.objects.all().delete()

    return 'done'

def CollectHouseFromDB():

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    # Call all data for looping

    tempLinkOfHouse = TempLinkOfHouseModel.objects.all()
    for x in tempLinkOfHouse:
        tempLink = x.link

        driver.get(tempLink)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        dateText = date.text
        dateOnly = dateText[0:2]

        #Convert text to number to check
        dateToInt = int(dateOnly)

        if dateToInt <= 9:
            monthOnly = dateText[2:5]
            yearOnly = dateText[6:10]
        else:
            monthOnly = dateText[3:6]
            yearOnly = dateText[7:11]

        #Convert text to number
        yearToInt = int(yearOnly)
        monthToInt = ConvertMonthToNumber(monthOnly)

        # If header is "หางาน" Remove it
        headerText = header.text
        checkHeader = RemoveUnwantedHeader(headerText)
        if checkHeader == 'pass':
            # Add data
            newListOfHouse = ListOfHouseModel()
            newListOfHouse.link = tempLink
            newListOfHouse.header = header.text
            newListOfHouse.date = "{}-{}-{}".format(yearToInt,monthToInt,dateToInt)
            newListOfHouse.content = content.text
            newListOfHouse.save()

    driver.quit()

    return 'done'

def ConvertMonthToNumber(monthOnly):
    if monthOnly == 'Jan':
        result = 1
    elif monthOnly == 'Feb':
        result = 2
    elif monthOnly == 'Mar':
        result = 3
    elif monthOnly == 'Apr':
        result = 4
    elif monthOnly == 'May':
        result = 5
    elif monthOnly == 'Jun':
        result = 6
    elif monthOnly == 'Jul':
        result = 7
    elif monthOnly == 'Aug':
        result = 8
    elif monthOnly == 'Sep' or monthOnly == 'Sept':
        result = 9
    elif monthOnly == 'Oct':
        result = 10
    elif monthOnly == 'Nov':
        result = 11
    elif monthOnly == 'Dec':
        result = 12
    else:
        result = 99
    return result

def RemoveUnwantedHeader(headerText):
    listTextUnwanted = [
                                        'หางาน',
                                        'หาห้อง',
                                        'หาบ้าน',
                                        'การบ้าน',
                                        'รับยื่น ABN',
                                        'แก้ไขฟรี',
                                        'homework',
                                        'Homework',
                                        'essay',
                                        'สล็อต',
                                        'บาคาร่า',
                                        'รับนวด',
                                        'assignment',
                                        'assingment',
                                        '❤️ Assignment',
                                        'Assignment',
                                        'Assingment',
                                        'resume',
                                        'Resume',
                                        'วิธีดูงาน',
                                        'เรซูเม่',
                                        'รับทำ',
                                        'รับยื่น',
                                        'รับงาน',
                                        'IELTS',
                                        'รับ inspect',
                                        ]
    checkUnwanted = 'pass'
    for unwantedText in listTextUnwanted:
        if unwantedText in headerText:
            checkUnwanted = 'not pass'
    return checkUnwanted

# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect

from datetime import date,timedelta,datetime

# require login to enter function
# import model
from keywordapp.models import *
import re

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
    return render(request, 'keywordapp/plain.html')

# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshWork():
    for loopToCheck in range(1,6):
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

# def CollectWorkFromDB(request):
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
            WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')

        # หลังจากได้ header มาเอามาทำเช็ค คำต้องห้าม และเป็นบ้านหรือไม่ก่อนเลย ก่อนที่จะไปเก็บข้อมูลอย่างอื่น
        headerText = header.text
        headerTextToAllLower = headerText.lower()

        checkHeader = RemoveUnwantedHeader(headerTextToAllLower)
        if checkHeader == 'pass':
            checkHouseType = CheckHouseType(headerTextToAllLower)
            if checkHouseType == 'other':
                content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')
                contentText = content.text
                contentTextToAllLower = contentText.lower()
                checkContent = RemoveUnwantedContent(contentTextToAllLower)
                if checkContent == 'pass':
                    date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')

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
                    # If Year = 1970, don't put into database
                    if yearOnly != "1970":
                        # Convert text to number
                        yearToInt = int(yearOnly)
                        monthToInt = ConvertMonthToNumber(monthOnly)


                        # check if in content has a phone number change it to non-number format
                        contentText = content.text
                        lowerContentText = contentText.lower()

                        checkWorkType = CheckWorkType(headerTextToAllLower)

                        # modifiedString = extractSpecificElements(lowerContentText)
                        # Add data
                        newListOfWork = ListOfWorkModel()
                        newListOfWork.link = tempLink
                        newListOfWork.header = header.text
                        newListOfWork.date = "{}-{}-{}".format(yearToInt,monthToInt,dateToInt)
                        newListOfWork.content = lowerContentText
                        newListOfWork.type = checkWorkType
                        newListOfWork.save()
        else:
            print("headerText : ",headerText)

    driver.quit()
    return 'done'
    # return render(request, 'keywordapp/plain.html')


def RefreshHouse():

    for loopToCheck in range(1,6):
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

        # หลังจากได้ header มาเอามาทำเช็ค คำต้องห้าม และเป็นบ้านหรือไม่ก่อนเลย ก่อนที่จะไปเก็บข้อมูลอย่างอื่น
        headerText = header.text
        headerTextToAllLower = headerText.lower()

        checkHeader = RemoveUnwantedHeader(headerTextToAllLower)
        if checkHeader == 'pass':
            checkWorkType = CheckWorkType(headerTextToAllLower)
            if checkWorkType == 'other':
                content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')
                contentText = content.text
                contentTextToAllLower = contentText.lower()
                checkContent = RemoveUnwantedContent(contentTextToAllLower)
                if checkContent == 'pass':
                    date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')

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
                    # If Year = 1970, don't put into database
                    if yearOnly != "1970":
                        #Convert text to number
                        yearToInt = int(yearOnly)
                        monthToInt = ConvertMonthToNumber(monthOnly)

                        # check if in content has a phone number change it to non-number format
                        contentText = content.text
                        lowerContentText = contentText.lower()

                        checkHouseType = CheckHouseType(headerTextToAllLower)

                        # modifiedString = extractSpecificElements(lowerContentText)
                        # Add data
                        newListOfHouse = ListOfHouseModel()
                        newListOfHouse.link = tempLink
                        newListOfHouse.header = header.text
                        newListOfHouse.date = "{}-{}-{}".format(yearToInt,monthToInt,dateToInt)
                        newListOfHouse.content = lowerContentText
                        newListOfHouse.type = checkHouseType
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


# def extractSpecificElements(main_string):
#     # Step 0: List of unwanted elements
#     listOfUnwanted = r'/|:|@|com|am|pm|40|41|42|43|44|45|46|47|48|49|-|\.'
#     # Step 1: Identify numbers and substrings to extract
#     extracted_substrings = re.findall(listOfUnwanted, main_string)

#     # Step 2: Replace numbers and substrings with placeholders
#     placeholder_substring = '&substr;'
#     replaced_string = re.sub(listOfUnwanted, placeholder_substring, main_string)
#     # Step 3: Perform operations on extracted numbers and substrings
#     modified_substrings = [' &zwj;' + substring for substring in extracted_substrings]

#     # Step 4: Re-insert modified numbers and substrings into the main string
#     for modified_substring in modified_substrings:
#         replaced_string = replaced_string.replace(placeholder_substring, modified_substring, 1)

#     return replaced_string


def KeywordManager(request):

    context = {}
    objectKeywordList = KeywordList.objects.all()
    context['objectKeywordList'] = objectKeywordList

    if request.method == 'POST':
        data = request.POST.copy()
        keyword = data.get('keyword')
        type = data.get('type')
        newKeyword = KeywordList()
        newKeyword.text = keyword
        newKeyword.type = type
        newKeyword.save()
    return render (request, 'keywordapp/keyword-manager.html',context)


def PostManager(request):

    context = {}
    objectWorkList = ListOfWorkModel.objects.all()
    objectHouseList = ListOfHouseModel.objects.all()
    context['objectWorkList'] = objectWorkList
    context['objectHouseList'] = objectHouseList

    return render (request, 'keywordapp/post-manager.html',context)

def AutoPromote(request):
    options = webdriver.ChromeOptions()

    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)
    
    driver.get('https://sydneythai.info/login.php')
    try:
        WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.CSS_SELECTOR, '#email'))
    except:
        print("cannot find #email")

    email = driver.find_element(By.CSS_SELECTOR, '#email')
    password = driver.find_element(By.CSS_SELECTOR, '#password')
    submit = driver.find_element(By.CSS_SELECTOR, '#submit')

    email.send_keys('cheetah5900@windowslive.com')
    password.send_keys('0853166969')
    submit.click()

    topic = driver.find_element(By.CSS_SELECTOR, '#topic')
    body = driver.find_element(By.CSS_SELECTOR, '#body')
    submit = driver.find_element(By.CSS_SELECTOR, '#submit')

    topic.send_keys('วิธีดูงาน/บ้านในแอพ SydneyThai แบบเรียงตามวันที่')
    body.send_keys('ให้เข้าไปที่เว็บ https://aussiethai.net ในเว็บจะเรียงวันที่ล่าสุดขึ้นมาก่อน และจะตัดโพสต์ที่ไม่สำคัญออก')
    submit.click()

    return render (request, 'keywordapp/plain.html')

def DeleteKeyword(request,pk):
    objectKeywordList = KeywordList.objects.get(id=pk)
    objectKeywordList.delete()
    return redirect('keyword-manager')

def DeletePostWork(request,pk):
    objectWorkList = ListOfWorkModel.objects.get(id=pk)
    objectWorkList.delete()
    return redirect('post-manager')

def DeletePostHouse(request,pk):
    objectHouseList = ListOfHouseModel.objects.get(id=pk)
    objectHouseList.delete()
    return redirect('post-manager')

def RemoveUnwantedHeader(headerText):
    listTextUnwanted = []
    # Extract KeywordList from db
    objectKeywordList = KeywordList.objects.filter(type="unwanted")
    for instance in objectKeywordList:
        # Perform actions on each instance
        textUnwanted = instance.text

        # Example: Append specific fields to a list
        listTextUnwanted.append(textUnwanted)

    checkUnwanted = 'pass'
    for unwantedText in listTextUnwanted:
        if unwantedText in headerText:
            checkUnwanted = 'not pass'
    return checkUnwanted


def RemoveUnwantedContent(contentText):
    listTextUnwanted = []
    # Extract KeywordList from db
    objectKeywordList = KeywordList.objects.filter(type="unwanted_content")
    for instance in objectKeywordList:
        # Perform actions on each instance
        textUnwanted = instance.text

        # Example: Append specific fields to a list
        listTextUnwanted.append(textUnwanted)

    checkUnwanted = 'pass'
    for unwantedText in listTextUnwanted:
        if unwantedText in contentText:
            checkUnwanted = 'not pass'
    return checkUnwanted

def CheckWorkType(headerText):
    typeOfWork = 'other'

    #? Massage
    listKeywordMassage = []
    # Extract KeywordMassageList from db
    objectKeywordMassageList = KeywordList.objects.filter(type="massage")
    for instance in objectKeywordMassageList:
        # Perform actions on each instance
        keywordMassage = instance.text
        # Example: Append specific fields to a list
        listKeywordMassage.append(keywordMassage)

    #? Kitchen
    listKeywordKitchen = []
    # Extract KeywordKitchenList from db
    objectKeywordKitchenList = KeywordList.objects.filter(type="kitchen")
    for instance in objectKeywordKitchenList:
        # Perform actions on each instance
        keywordKitchen = instance.text
        # Example: Append specific fields to a list
        listKeywordKitchen.append(keywordKitchen)

    #? Barista
    listKeywordBarista = []
    # Extract KeywordBaristaList from db
    objectKeywordBaristaList = KeywordList.objects.filter(type="barista")
    for instance in objectKeywordBaristaList:
        # Perform actions on each instance
        keywordBarista = instance.text
        # Example: Append specific fields to a list
        listKeywordBarista.append(keywordBarista)

    #? Waiter
    listKeywordWaiter = []
    # Extract KeywordWaiterList from db
    objectKeywordWaiterList = KeywordList.objects.filter(type="waiter")
    for instance in objectKeywordWaiterList:
        # Perform actions on each instance
        keywordWaiter = instance.text
        # Example: Append specific fields to a list
        listKeywordWaiter.append(keywordWaiter)

    #? Clean
    listKeywordClean = []
    # Extract KeywordCleanList from db
    objectKeywordCleanList = KeywordList.objects.filter(type="clean")
    for instance in objectKeywordCleanList:
        # Perform actions on each instance
        keywordClean = instance.text
        # Example: Append specific fields to a list
        listKeywordClean.append(keywordClean)


    # Massage type
    for item in listKeywordMassage:
        if item in headerText:
            typeOfWork = 'massage'

    # Kitchen type
    for item in listKeywordKitchen:
        if item in headerText:
            typeOfWork = 'kitchen'

    # Barista type
    for item in listKeywordBarista:
        if item in headerText:
            typeOfWork = 'barista'

    # Waiter type
    for item in listKeywordWaiter:
        if item in headerText:
            typeOfWork = 'waiter'

    # Clean type
    for item in listKeywordClean:
        if item in headerText:
            typeOfWork = 'clean'
    
    return typeOfWork


def CheckHouseType(headerText):
    typeOfHouse = 'other'

    #? Master
    listKeywordMaster = []
    # Extract KeywordMasterList from db
    objectKeywordMasterList = KeywordList.objects.filter(type="master")
    for instance in objectKeywordMasterList:
        # Perform actions on each instance
        keywordMaster = instance.text
        # Example: Append specific fields to a list
        listKeywordMaster.append(keywordMaster)

    #? Second
    listKeywordSecond = []
    # Extract KeywordSecondList from db
    objectKeywordSecondList = KeywordList.objects.filter(type="second")
    for instance in objectKeywordSecondList:
        # Perform actions on each instance
        keywordSecond = instance.text
        # Example: Append specific fields to a list
        listKeywordSecond.append(keywordSecond)

    #? LivSunStu
    listKeywordLivSunStu = []
    # Extract KeywordLivSunStuList from db
    objectKeywordLivSunStuList = KeywordList.objects.filter(type="livsunstu")
    for instance in objectKeywordLivSunStuList:
        # Perform actions on each instance
        keywordLivSunStu = instance.text
        # Example: Append specific fields to a list
        listKeywordLivSunStu.append(keywordLivSunStu)

    # Master type
    for item in listKeywordMaster:
        if item in headerText:
            typeOfHouse = 'master'

    # Second type
    for item in listKeywordSecond:
        if item in headerText:
            typeOfHouse = 'second'

    # LivSun type
    for item in listKeywordLivSunStu:
        if item in headerText:
            typeOfHouse = 'livsunstu'
    
    return typeOfHouse
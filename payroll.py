import sys
import csv as cs
from datetime import datetime, date

def getCoinDenomination(amount):
    """getCoinDenomination: This functions determines the coin denomination of the
                            the given amount
                   mSalary: Amount to find coin denomination
                    return: Coin denomination
    """
    coinList = [100,20,10,5,1,0.25,0.10,0.05,0.01]
    coinDenoD = dict()

    i = cnt = 0 
    while amount > 0:
        if amount >= coinList[i]:
            amount = round(amount - coinList[i],2)
            cnt += 1  
            coinDenoD[coinList[i]] = cnt
        else:
            cnt = 0
            i += 1
    return coinDenoD


def getMontlyPay(age):
    """getMontlyPay: This function calculates the monthly pay based on age and 
                     distributes the montly pay into charity(10%), retirement(40%)
                     and candy(50%) 
                age: Age
             return: monthlyPay - monthly pay
                     mPayDistribution - pay distribution
    """

    mPayDistribution = dict()
    #Calulating monthly salary
    monthlyPay = round((age * 52)/12)
    
    #Distribution of salary[10% to charity, 40% to retirement, 50% to candy]
    mPayDistribution['charity'] = round(monthlyPay * 0.10,2)
    mPayDistribution['retirement'] = round(monthlyPay * 0.40,2)
    mPayDistribution['candy'] = round(monthlyPay * 0.50,2)
    return monthlyPay, mPayDistribution


def getAge(dateOfBirth, notTodayDate=None):
    """getAge: Function to find the age
       dateOfBirth: Date of birth
       notTodayDate: Age calculated based on this day
            return: Age
    """

    birthYear, BirthMonth, birthDay = dateOfBirth.split('-')
    if len(birthDay) == 1:
        birthDay = '0' + birthDay        
    birthMD = BirthMonth + birthDay
  
    #Use notTodayDate to calulate age. If not passed as cmdline parameter use today's date
    if notTodayDate != None:
        currentYear, currentMonth, currentDay = notTodayDate.split('-')
        #Validating correct month and days else return false
        if (int(currentMonth) < 1 or int(currentMonth) > 12 or int(currentDay)< 1 or int(currentDay) > 31):
            return False
    else: 
    	today = str(date.today())
    	currentYear, currentMonth, currentDay = today.split('-')

    #Since we are not considering days and months in age calulation.
    #if given/current month + given/current Date >= birth month + birth day. Return int(currentYear) - int(birthYear)
    #else Return int(currentYear) - int(birthYear) - 1     
    if len(currentDay) == 1:
        currentDay = '0' + currentDay
    currMD = currentMonth + currentDay
    
    if (int(currMD)-int(birthMD)) >= 0:
        return int(currentYear) - int(birthYear)
    else:
        return int(currentYear) - int(birthYear) - 1


def getPayroll(fileName, notTodayDate=None):
    """getPayroll: Function to load the file (format csv), create dictionary (key: Name of elve, value: date of birth),
                   get the age, monthly pay, pay distribution, coin denomination and display the result
         fileName: File containng the name and date of birth of elve.
      noTodayDate: If this date is not passed as commandline paramter then today's date is used by default for calucalation of
                   monthly pay.
    """
    colTitle = colName = 0
    colDOB = 1
    elfDict = dict()
    coinDeno = dict()
    try:
        #Opening csv file
        with open(fileName,'r') as csvFile:
            reader = cs.reader(csvFile,delimiter=',')
            for row in reader:
                #If the csv file contains column title then ignore it.
                if row[colTitle] == 'Name':
                    continue
                else:
                    #If the date of birth coloumn is not empty then adding (key: name of elve, value: date of birth) to dict.
                    if row[colDOB] != '':
                        elfDict[row[colName]] = row[colDOB]
                    else:
                        print ("\nError: date of birth empty for elve:",row[colName])
    except OSError as e:
        print ("Error:",e)

    for name, dob in elfDict.items():
        try: 
            age = getAge(dob, notTodayDate)
            #check for age less or equal to 0
            if age <= 0:
                print ("\nElve [",name ,"]: age cannot be  0 or less or incorrect month or days")
                continue
            else:
                mPay, mSalDistribution = getMontlyPay(age)
                #Get the coin denomination
                for key in sorted(mSalDistribution.keys()):
                    coinDeno[key] = getCoinDenomination(mSalDistribution[key])
                #To display result
                print ("\nName:",name, ", DOB:",dob, ", Age:",age, ", Monthly Pay: $",mPay)
                print ("Pay Distribution:", mSalDistribution)
                print ("Coin Denomination:")
                for ckey, cval in coinDeno.items():
                    print (ckey,":")
                    for coKey, coVal in sorted(cval.items(), reverse=True):
                        print ("coin value:",coKey, "coin count:",coVal)
        except ValueError as e:
            print ("\nError: Age format not correct for elve:[", name,"] correct format <YYYY-MM-DD>") 


def payroll():
    try:
        argLen = len(sys.argv[1:])
        fileName = sys.argv[1]
        if argLen > 1:
            action = sys.argv[2]
            if action == '-d':
                if sys.argv[3] == '':
                    raise IndexError
                notTodayDate = sys.argv[3]
        else:
            action = None
            notTodayDate = None
      
        getPayroll(fileName, notTodayDate)
    except IndexError as e:
       print ("Command options:")
       print ("cmd: ./",sys.argv[0],"<filename>")
       print ("cmd: ./",sys.argv[0],"<filename> -d <YYYY-MM-DD>")
       sys.exit(0)


#Program entry point
payroll()

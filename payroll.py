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
    colTitle = colName = 0
    colDOB = 1
    elfDict = dict()
    coinDeno = dict()
    try:
        with open(fileName,'r') as csvFile:
            reader = cs.reader(csvFile,delimiter=',')
            for row in reader:
                #If the csv file contains column title then ignore it.
                if row[colTitle] == 'Name':
                    continue
                else:
                    if row[colDOB] != '':
                        elfDict[row[colName]] = row[colDOB]
                    else:
                        print ("Error: date of birth empty for elve:",row[colName],"\n")
    except OSError as e:
        print ("Error:",e)

    for name, dob in elfDict.items():
        try: 
            age  = getAge(dob, notTodayDate)
            if age <= 0:
                print ("Elve [",name ,"]: age cannot be  0 or less\n")
                continue
            else:
                mPay, mSalDistribution = getMontlyPay(age)
                for key in sorted(mSalDistribution.keys()):
                    coinDeno[key] = getCoinDenomination(mSalDistribution[key])
                print ("\nName:",name, ", DOB:",dob, ", Age:",age, ", Monthly Pay: $",mPay)
                print ("Pay Distribution:", mSalDistribution)
                print ("Coin Denomination:")
                for ckey, cval in coinDeno.items():
                    print (ckey,":")
                    for coKey, coVal in sorted(cval.items(), reverse=True):
                        print ("coin value:",coKey, "coin count:",coVal)
        except ValueError as e:
            print ("\nError: Age format not correct for elve:[", name,"] correct format <YYYY-MM-DD>\n") 


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

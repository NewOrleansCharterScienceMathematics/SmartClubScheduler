__author__ = 'Wade'

import pymysql.cursors
import pymysql.connections
import random

connection = pymysql.connect(host="localhost",user="root",password=
                            "zeuswade",charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor, database="students")
def update_student_table(c,smart,aorb,studentname):
    query = "UPDATE students SET %s=\"%s\" WHERE Student=\"%s\"" % (aorb,smart,studentname)

    c.execute(query)
    connection.commit()
    return


def getSmartDatabase(c,smartdatabase):
    query = "SELECT * FROM %s" % (smartdatabase)
    c.execute(query)
    result =  c.fetchall()
    return result

def pick_smart(smartprefrences,smarts,smartdatabase,c,bigsmarts):
    smartprefs = []
    bigsmartnames = []
    for n in bigsmarts:
        bigsmartnames.append(n["Smart"])
    for i in smartprefrences:
        smartprefs.append(i.strip(" "))
    smartchoice = set(smartprefs) & set(smarts)
    for j in bigsmartnames:
        if j in smartchoice:
            smartchoice = set(smartprefs) & set(smarts) & set(bigsmartnames)
        if j in smartprefs:
            smartchoice = set(smartprefs) & set(bigsmartnames)

    for y in smartchoice:
            if isFull(c,y,smartdatabase) is False:
                return y
    for x in smarts:
        if isFull(c,x,smartdatabase) is False:
            return x
    return bigsmartnames[random.randint(0,len(bigsmarts)-1)]

def isFull(c,x,smartdatabase):
    sql = "SELECT * FROM %s WHERE Smart=\"%s\"" % (smartdatabase,x)
    c.execute(sql)
    result = c.fetchone()

    try:
        result["NumStudents"]+=1
        result = update_students_in_smart(smartdatabase,"NumStudents",result["NumStudents"],result["Smart"],c)
        if result['NumStudents'] >= result['MaxStudents']:

            return True

    except KeyError:
        result['StudentsInSmart'] += 1
        result = update_students_in_smart(smartdatabase,"StudentsInSmart",result["StudentsInSmart"],result["Smart"],c)
        if result['StudentsInSmart'] >= result['MaxStudents']:

            return True

    return False


def update_students_in_smart(Smartdatabase,numstudenttstr, numofstudents,smart,c):
    sql = "UPDATE %s SET %s=%s WHERE Smart=\"%s\" " % (Smartdatabase,numstudenttstr,numofstudents,smart)
    c.execute(sql)
    query = "SELECT * FROM %s WHERE Smart=\"%s\"" % (Smartdatabase, smart)
    c.execute(query)
    result = c.fetchone()

    return result



def assign_a_smarts(studentdatabase,c,smart10,smart11,SmartAorB,database10,database11):
    bigasmarts10 = []
    bigasmarts11 = []
    smartdatabasea10 = getSmartDatabase(c,database10)
    smartdatabasea11 = getSmartDatabase(c,database11)


    for y in smartdatabasea10:

        if y["MaxStudents"] > 15:

            if y["Smart"] in smart10:
                smart10.remove(y["Smart"])
            bigasmarts10.append(y)
    for j in smartdatabasea11:
        if j["MaxStudents"] > 15:
            if j["Smart"] in smart11:
                smart11.remove(j["Smart"])
            bigasmarts11.append(j)

    for x in studentdatabase:
        smartwants = x[SmartAorB]

        if smartwants is None:
            smartprefs = ""
        else:
            smartprefs = smartwants.split(",")

        smartprefrences = []

        for i in smartprefs:
            smartprefrences.append(i.split("(")[0])

        if x["Gradelevel"] is "9":
            database = database10
            #print(x["Student"]+" is in "+x["Gradelevel"]+" and is assigned "+str(pick_smart(smartprefrences,smart10,database,c,bigasmarts10))+" as "+SmartAorB)
            smart = pick_smart(smartprefrences,smart10,database,c,bigasmarts10)
            update_student_table(c,smart,SmartAorB,x["Student"])
        if int(x["Gradelevel"]) == 10:
            database = database11
            #print(x["Student"]+" is in "+x["Gradelevel"]+" and is assigned "+str(pick_smart(smartprefrences,smart11,database,c,bigasmarts11))+" as "+SmartAorB)
            smart = pick_smart(smartprefrences,smart11,database,c,bigasmarts11)
            update_student_table(c,smart,SmartAorB,x["Student"])
        if int(x["Gradelevel"]) == 11:
            database = database11
            #print(x["Student"]+" is in "+x["Gradelevel"]+" and is assigned "+str(pick_smart(smartprefrences,smart11,database,c,bigasmarts11))+" as "+SmartAorB)
            smart = pick_smart(smartprefrences,smart11,database,c,bigasmarts11)
            update_student_table(c,smart,SmartAorB,x["Student"])
    return





def fetch_me(c, query):
    c.execute(query)
    dict = c.fetchall()
    list = []
    for x in dict:
        list.append(x["Smart"])
    return list

try:
    with connection.cursor() as cursor:
        a10thquery = "SELECT Smart FROM smarta10th"
        b10thquery = "SELECT Smart FROM smartb10th"
        a11thQuery = "SELECT Smart FROM smarta11th12th"
        b11thQuery = "SELECT Smart FROM smartb11th12th"

        a10smarts = fetch_me(cursor, a10thquery)
        b10smarts = fetch_me(cursor, b10thquery)
        a11smarts = fetch_me(cursor, a11thQuery)
        b11smarts = fetch_me(cursor, b11thQuery)

        studentQuery = "SELECT * FROM smarttable"
        cursor.execute(studentQuery)
        studentdatabase = cursor.fetchall()


        assign_a_smarts(studentdatabase,cursor,a10smarts,a11smarts,"SmartA","smarta10th","smarta11th12th")
        assign_a_smarts(studentdatabase,cursor,b10smarts,b11smarts,"SmartB","smartb10th","smartb11th12th")


finally:
    print("CLOSED")
    connection.close()


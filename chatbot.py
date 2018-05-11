#!/usr/bin/python3
import os
import aiml
import string

def controlStatementsChapter():
    count=0
    topics=["if else","switch","for loop","while loop","do while loop","break","continue","comments"]
    while count<8:
        print("\n ########## Chapter : "+str(count+1)+" ==> "+topics[count]+" ########")
        response=kernel.respond(topics[count])
        newResponse=response.split('-,');
        print(" \n ".join(newResponse))

        review=input("type [done] to move to next topic \n type [repeat] to repeat same topic \n type [exit] to exit from chapter >")
        if (review=="exit"):
            return
        elif(review=="done"):
            count+=1

    pass
def f(x):
    lesson1=["OBJECT","CLASS","CONSTRUCTOR","STATIC","THIS","EXAMPLE"]
    lesson2=["if else","switch","for loop","while loop","do while loop","break","continue","comments"]
    lesson4=["POLYMORPHISM","METHOD OVERLOADING","SUPER","FINAL","FUNTIME POLYMORPHISM","BINDING","EXAMPLE"]
    return {
        ' 1':lesson1,
        ' 2':lesson2,
        ' 4': lesson4
    }.get(x, lesson2)
def getLesson(number):
    count=0
    topics=f(number)
    final=len(topics)
    while count<final:
        print("\n ########## Chapter : "+str(count+1)+" ==> "+topics[count]+" ########")
        response=kernel.respond(topics[count])
        newResponse=response.split('-,');
        print(" \n ".join(newResponse))

        review=input("type [done] to move to next topic \n type [repeat] to repeat same topic \n type [exit] to exit from chapter >")
        if (review=="exit"):
            return
        elif(review=="done"):
            count+=1
    # print(f(number))

BRAIN_FILE="brain.dump"

k = aiml.Kernel()

# To increase the startup speed of the bot it is
# possible to save the parsed aiml files as a
# dump. This code checks if a dump exists and
# otherwise loads the aiml from the xml files
# and saves the brain dump.
kernel = aiml.Kernel()
if os.path.isfile('Resources/bot_brain.brn'):
    kernel.bootstrap(brainFile='Resources/bot_brain.brn')
else:
    kernel.learn('std-startup.xml')
    kernel.respond("programming")
    kernel.saveBrain('Resources/bot_brain.brn')
    # print("Saving brain file: " + BRAIN_FILE)
    # k.saveBrain(BRAIN_FILE)

# Endless loop which passes the input to the bot and prints
# its response
while True:
    input_text = input("> ")
    if (input_text=="learn"):
        print("1. JAVA Basics")
        print("2. Control Statements")
        chapter_number=int(input("enter your choice (in numbers)"))
        if (chapter_number==2):
            controlStatementsChapter()
        continue
    elif (input_text.startswith("select lesson")):
        lesson_no=string.replace(input_text,'select lesson','')
        print(lesson_no)
        getLesson(lesson_no)

    response = kernel.respond(input_text)
    # newResponse=['adf','adffd']
    


    if response:
        newResponse=response.split('-,');
        print(" \n ".join(newResponse))
    else:
        print ("\n no data found")




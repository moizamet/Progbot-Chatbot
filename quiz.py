import sqlite3

db=sqlite3.connect("bot.db")
count=1
score=0
quizid=1001
questions=db.execute('SELECT * FROM questions where quizid='+str(quizid))

for question in questions:
	print ("q"+str(count)+" "+question[1]+"\n")
	print("1 "+question[2])
	print("2 "+question[3])
	print("3 "+question[4])
	print("4 "+question[5]+"\n")
	choice=int(input("enter your choice : "))
	if (choice==question[6]):
		score+=1
		print ("Correct Answer !!")
	else:
		print ("Sorry wrong Choice ")

db.execute("update score set score="+str(score)+" where uid='moiz' and quizid=1001")
if (db.total_changes==0):
	db.execute("insert into score (uid,quizid,score) values ('moiz',1001,"+str(score)+" )")
	db.commit()
print("\n Your Score : "+str(score))

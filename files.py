sc = 1
f = open('score.txt', 'r')
highScore = int(f.read) 
f.close()
if b:
    f = open('score.txt','w')
    f.write(str(sc))
    f.close()
    print('yes')
else:
    print('no')
import os
import MySQLdb
import random
import numpy as np

project = 'car'
objects = ["car"]

conn = MySQLdb.connect("localhost","root","123","images" )
cursor = conn.cursor()

wd = os.getcwd()
if not os.path.exists(project):
    os.mkdir(project)


tmp = ['object="{}"'.format(obj) for obj in objects]
sql = 'SELECT * FROM t1 WHERE ({});'.format(' OR '.join(tmp))
infos = cursor.fetchmany(cursor.execute(sql))

i=0
images = []
while i<len(infos)-1:
    imgId=infos[i][0]
    j=i+1
    while j<len(infos) and infos[j][0]==imgId:
        j+=1
    
    tmp = [ '{} {} {} {} {}\n'.format(objects.index(obj),x,y,w,h)
            for (_,obj,x,y,w,h) in infos[i:j] ]
    txt=''.join(tmp)

    print 'imgId:', imgId
    # ln -s
    fin  = '{}/data/jpg/{}.jpg'.format(wd,imgId)
    fout = '{}/{}/{}.jpg'.format(wd,project,imgId)
    os.symlink(fin,fout)
    # print txt
    f=open('{}/{}.txt'.format(project,imgId),'w')
    f.write(txt)
    f.close()
    
    images.append(imgId)
    i=j

cursor.close()
#conn.commit()
conn.close()

N = len(images)

print "\n\nnumber of pics:", N

imagesTest = random.sample(images,int(N*0.1))
imagesTest.sort()

imagesTrain = list( set(images)-set(imagesTest) )
imagesTrain.sort()

ftest  = open('{}.test'.format(project),'w')
for i in imagesTest:
    ftest.write('{}/{}/{}.jpg\n'.format(wd,project,i))
ftest.close()

ftrain = open('{}.train'.format(project),'w')
for i in imagesTrain:
    ftrain.write('{}/{}/{}.jpg\n'.format(wd,project,i))
ftrain.close()


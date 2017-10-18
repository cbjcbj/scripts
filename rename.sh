ori=/home/cbj/desktop/1
tar=/home/cbj/docs/scripts/test
mkdir $d

((j=1))
for i in $ori/*
do
    echo $i $j
    cp $i $tar/$j.jpg
    #jj=`printf "%08d" $i`
    #cp $i $tar/$jj.jpg
    ((j++))
done

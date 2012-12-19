cd /home1/c/cis530/final_project/TopicWords-v1/
for i in {9..49}
do
        echo Processing File $i
        java -Xmx1000m TopicSignatures /home1/j/jmow/school/cis530/project/configs/config$i.example
        echo Finished processing file $i
done

exit 0

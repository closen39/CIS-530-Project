for i in {0..49}
do
        echo Processing File $i
        java -Xmx1000m /home1/c/cis530/final_project/TopicWords-v1/TopicSignatures configs/config$i.example
        echo Finished processing file $i
done

exit 0

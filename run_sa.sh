hadoop fs -rm -r /output0
python3 search_assist.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///res1.txt --output-dir hdfs:///output0 --no-output
hadoop fs -text /output0/part* | less
hadoop fs -rm -r /ii_output
python3 DAT500/inverted_index.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///processed_data.txt --output-dir hdfs:///ii_output --no-output
hadoop fs -text /ii_output/part* | less
hadoop fs -rm -r /output2
# python3 DAT500/profanityrank.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///crawl-data/warc/testfilemrjob.txt --output-dir hdfs:///output2 --no-output
# python3 DAT500/profanityrank.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///crawl-data/warc/processed_data_new.txt --output-dir hdfs:///output2 --no-output
# python3 DAT500/profanityrank.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///processed_data_134MB.txt --output-dir hdfs:///output2 --no-output
# python3 DAT500/profanityrank.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///crawl-data/warc/doubled.txt --output-dir hdfs:///output2 --no-output
python3 DAT500/profanityrank.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.0.jar -r hadoop hdfs:///crawl-data/warc/quadrupled.txt --output-dir hdfs:///output2 --no-output
# hadoop fs -text /output2/part* | less
# python3 DAT500/preprocessing.py
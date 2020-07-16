import yfinance as yf
import subprocess
from subprocess import PIPE
import os

# Change directory to run stanford sentiment analysis model
wd = os.getcwd()
os.chdir("./stanford-corenlp-4.0.0/")

call = subprocess.Popen(["java -cp "*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -stdin"], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')
call.stdin.write("I hate obama")
print(call.stderr, call.stdout)  # Hello from the other side
call.stdin.close()
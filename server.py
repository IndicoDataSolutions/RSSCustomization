from flask import Flask, render_template
import feedparser
from indicoio import text_tags

app = Flask(__name__)
app.debug = True

DEFAULT = "http://www.reddit.com/.rss"

@app.route('/')
def main():
	entries = feedparser.parse(DEFAULT)['entries']
	parsed = [(entry['title'], entry['link'], text_tags(entry['title']))
	          for entry in entries]
	return render_template('main.html')

if __name__ == '__main__':
    app.run()
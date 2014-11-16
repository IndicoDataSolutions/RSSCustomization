from multiprocessing.pool import ThreadPool

from flask import Flask, render_template
import feedparser
from indicoio import text_tags

app = Flask(__name__)
app.debug = True

DEFAULT = "http://www.reddit.com/.rss"

def thresholded(tags, minimum):
	return dict((category, prob) for category, prob in tags.items()
	        	if prob > minimum)

def likely_category(tags, minimum=0.1):
	trimmed = thresholded(tags, minimum) or {'none': 0}
	return max(trimmed, key=lambda key: trimmed[key])

def parsed(entry):
	return {
		'title': entry['title'],
		'link': entry['link'],
		'tag': likely_category(text_tags(entry['title']))
	}

@app.route('/')
def main():
	pool = ThreadPool(16)
	entries = pool.map(parsed, feedparser.parse(DEFAULT)['entries'])
	return render_template('main.html', entries=entries)

if __name__ == '__main__':
    app.run()
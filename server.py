from multiprocessing.pool import ThreadPool

from flask import Flask, render_template
import feedparser
from indicoio import text_tags

app = Flask(__name__)
app.debug = True

feed = "http://www.reddit.com/.rss"

def thresholded(tags, minimum):
	""" 
	Remove all tags with probability less than `minimum` 
	"""
	return dict((category, prob) for category, prob in tags.items()
	        	if prob > minimum)

def likely_tag(tags, minimum=0.1):
	""" 
	Threshold tags, then get the tag with the highest probability.
	If no tag probability exceeds the minimum, return the string 'none'
	"""
	trimmed = thresholded(tags, minimum) or {'none': 0}
	return max(trimmed, key=lambda key: trimmed[key])

def parsed(entry):
	"""
	Strip unnecessary content from the return of feedparser, 
	and augment with the output of indico's `text_tags` API
	"""
	return {
		'title': entry['title'],
		'link': entry['link'],
		'tag': likely_tag(text_tags(entry['title']))
	}

@app.route('/')
def main():
	# simple threading to prevent network calls from blocking
	pool = ThreadPool(16)
	entries = feedparser.parse(feed)['entries']
	entries = pool.map(parsed, entries)

	# render template with additional jinja2 data
	return render_template('main.html', entries=entries)

if __name__ == '__main__':
    app.run()
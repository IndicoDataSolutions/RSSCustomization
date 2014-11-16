from flask import Flask, render_template
import feedparser

app = Flask(__name__)
app.debug = True

DEFAULT = "http://www.reddit.com/subreddits/new.rss"

@app.route('/')
def main():
	entries = feedparser.parse(DEFAULT)['entries']
	entries = [(entry['title'], entry['link']) for entry in entries]
	return render_template('main.html')

if __name__ == '__main__':
    app.run()
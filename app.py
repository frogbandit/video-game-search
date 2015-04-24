from flask import Flask, request, render_template
import requests, feedparser

app = Flask(__name__)

app.config['DEBUG'] = True 

#use feedparser to read the RSS url
rss_url = "http://newyork.craigslist.org/search/vga?format=rss"
feed = feedparser.parse(rss_url)

#Use inverted indexing to create a dictionary with keys as potential keywords, and values as a list of entries
search_dict = {}
for item in feed.entries:
	#get each word from the description from the entry, without capitalization
	original_entry = item["summary"]
	entry = original_entry.strip().lower()
	entry_list = entry.split()
	#get rid of duplicates and make sure the dollar signs look good!
	woduplicates = set(entry_list)
	item["title"] = item["title"].replace("&#x0024;", "$")
	#print item["title"]
	for word in woduplicates:
		#if the word is already in the dictionary, just append it to the existing list of entries
		if word in search_dict: 
			search_dict[word].append([item["title"], item["summary"]])
		#otherwise, create a new list of entries as the value under that key
		else:
			search_dict[word] = [[item["title"], item["summary"]]]

@app.route("/", methods=["GET", "POST"])
def search():
	if request.method == "POST": #when user clicks the search button

		keyword = request.form["user_search"]

		if keyword in search_dict:
			#print search_dict[keyword]
			return render_template("results.html", api_data=search_dict[keyword])
		else:
			#print "Failure!"
			search_dict[keyword] = [["Your query did not return any results. Please try again."]]

		return render_template("results.html", api_data=search_dict[keyword])

	else: # request.method == "GET"
		return render_template("search.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0')

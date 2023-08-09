from flask import Flask, render_template, request, redirect, url_for
from requests_html import HTMLSession
import time

app = Flask(__name__)


@app.api_route("/", methods=["GET", "POST"])
def index():
    data_dict = {}
    if request.method=="POST":
        query = request.form["query"]
        query = query.strip()
        return redirect(url_for("get_news", query = query))
    else:
        return render_template("index.html", data=data_dict)

@app.api_route("/<string:query>")
def get_news(query):
    t1 = time.time()
    dict1 = {}
    url = f"https://www.google.com/search?q={query}"
    session = HTMLSession()
    r = session.get(url)
    div_tag = r.html.find("div.kno-rdesc", first=True)
    if div_tag:
        dict1["summary"]=div_tag.find("span")[0].text
    else:
        pass
    dict1["query"] = query
    
    links = r.html.absolute_links
    new_links = links.copy()
    google_domains = ('https://search.google.',
                      'https://www.google.',
                      'https://www.amazon.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.',
                      'http://en.wikipedia.',
                      'https://en.wikipedia.',
                      'https://twitter.com',
                      'https://posts.google.',
                      'http://britannica.',
                      'https://www.britannica.com/',
                      'https://www.facebook.',
                      'https://www.tiktok.',
                      'https://www.instagram.')
    for i in new_links:
        if i.startswith(google_domains):
            links.remove(i)
    new_links = sorted(list(links)[:8])
    virtual_links = new_links.copy()
    title_list = []
    for i in new_links:
        r = session.get(i)
        val = r.html.find("title", first=True)
        try:
            title = val.text
            if "{" in title:
                raise Exception
            elif i.startswith("https://open.spotify."):
                title = f"On Spotify | {query}"
                title_list.append(title)
            else:
                title_list.append(title)
        except Exception:
            virtual_links.remove(i)
    title_and_link = {i:j for i,j in zip(title_list, virtual_links)}
    dict1["title_and_link"] = title_and_link
    t2 = time.time()
    print((t2-t1))
    print("New Change")
    return render_template("sample.html", data=dict1)

if __name__ == "__main__":
    app.run(debug=True)

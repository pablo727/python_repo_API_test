# Suppress InsecureRequestWarning
import warnings
import urllib3

warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)


from operator import itemgetter
import requests
import plotly.express as px


# Make an API call and check the response.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url, verify=False)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:5]:
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url, verify=False)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                           reverse=True)

# Process repository information
article_links, article_comments = [], []
for submission_dict in submission_dicts:
    try:
        # Turn article names into active links.
        article_name = submission_dict['title']
        article_url = submission_dict.get('url', submission_dict['hn_link'])
        article_link = f"<a href='{article_url}'>{article_name}</a>"
        article_links.append(article_link)
        article_comments.append(submission_dict['comments'])
    except ValueError as e:
        continue

# Make visualization.
title = "Most Active Discussions on Hacker News"
labels = {'x': 'Article', 'y': 'Comments'}
fig = px.bar(x=article_links, y=article_comments, title=title,
             labels=labels)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
                  yaxis_title_font_size=20)

fig.update_traces(marker_color='orangered', marker_opacity=0.7)

fig.show()





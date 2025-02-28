from operator import itemgetter
import requests
import plotly.express as px

# Make an API call, and check the response.
url = 'https://hacker-news.firebaseio.com/v0/newstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:10]:
    # Make a new API call for each submission.
    url = (
      f'https://hacker-news.firebaseio.com/v0/item/{submission_id}.json')
    r = requests.get(url)
    # print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # print(response_dict)

    # Build a dictionary for each article.
    submission_dict = {
        # Always use .get() with defaults for API data you don't control
        'title': response_dict.get('title', 'No Title Available'),
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'score': response_dict.get('score', 0),  # Default 0 if missing
        'type': response_dict.get('type', 0),  # Default 0 if missing
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('score'),
                              reverse=True)
    
# for submission_dict in submission_dicts:
#     print(f"\nTitle: {submission_dict['title']}")
#     print(f"Discussion link: {submission_dict['hn_link']}")
#     print(f"Scores: {submission_dict['score']}")


news_links, scores, hover_texts = [], [], []
for news_dict in submission_dicts:
    # Turn news titles into active links.
    news_title = news_dict['title']
    truncate_title = ((news_title[:25] + '...')
                       if len(news_title) > 28 else news_title) 
    news_url = news_dict['hn_link']
    news_link = f"<a href='{news_url}'>{truncate_title}</a>"
    news_links.append(news_link)

    scores.append(news_dict['score'])

    # Build hover text
    hover_text = f"{news_title}<br /> {news_dict.get('type', 0)}"
    hover_texts.append(hover_text)

# Make visualization
title = "Most Recent News in Hacker News"
labels = {'x': 'News', 'y': 'Score'}
fig = px.bar(x=news_links, y=scores, title=title, labels=labels,
             hover_name=hover_texts)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
                  xaxis_tickangle=-45, margin=dict(b=50),
                  yaxis_title_font_size=20)

fig.update_traces(marker_color=scores, marker_colorscale='viridis',
                   marker_opacity=0.7)

fig.show()













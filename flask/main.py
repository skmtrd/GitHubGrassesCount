from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
import os

name_list = ["o-ren-zi", "Fukushou1911", "shiro-1107", "riku546", "sakura1020", "ramy370612", "yui162205", "rinitsuha419","1F10230292", "hibikinggg", "suisus", "tsukushi-wakige", "Noarhl" ,"skmtrd" ]
GITHUB_API_URL = "https://api.github.com/graphql"


def generate_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        date_range = []
        current_date = start
        while current_date <= end:
            date_range.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
        
        return date_range
    except ValueError:
        return "Invalid date format. Please provide dates in the format 'YYYY-MM-DD'."
    

def get_grass_count(name, start_day, end_day):
    GITHUB_TOKEN = "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"
    print("get_grass_count")
    day_range = generate_date_range(start_day, end_day)
    print(day_range)
    query = """
    query($name: String!) {
      user(login: $name) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    variables = {
        "name": name
    }
    response = requests.post(GITHUB_API_URL, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('user') and data['data']['user'].get('contributionsCollection'):
            weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
            contribution_days_list = []
            for week in weeks:
                for day in week['contributionDays']:
                    if day['contributionCount'] > 0 and day['date'] in day_range:
                        contribution_days_list.append(day['date'])
            return len(contribution_days_list)
        else:
            return None
    else:
        return None

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/form-post', methods=['POST'])
def form_post():
    start_day = request.form['start_day']
    end_day = request.form['end_day']
    dict = {}
    count = get_grass_count("skmtrd", start_day, end_day)
    for name in name_list:
        count = get_grass_count(name, start_day, end_day)
        dict[name] = count
    result = """"""
    result += f"<h1>{start_day}~{end_day}</h1><br>"
    for key, value in dict.items():
        result += f"<p><strong>{key}: {value}</strong></p>"
    return result

if __name__ == '__main__':
    app.debug = True
    app.run()
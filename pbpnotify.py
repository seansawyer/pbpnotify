import os
import requests
import smtplib
import ssl

SUB_NAME = 'pbpmooo'
SUB_NEW_URL_FORMAT = 'https://oauth.reddit.com/r/{sub}/new.json'
USER_AGENT = 'pbpmooo-notify/0.1 by ikvind'
TOKEN_VAR = 'REDDIT_TOKEN'

def run():
    token = os.getenv('REDDIT_TOKEN')
    new_url = SUB_NEW_URL_FORMAT.format(sub=SUB_NAME)
    headers = {
        'Authorization': f'bearer {token}',
        'User-Agent': USER_AGENT,
    }
    response = requests.get(new_url, headers=headers)
    if not response.status_code == requests.codes.ok:
        print(f'Request failed with {response.status_code}')
        print(response.text)
        return
    data = response.json()
    posts = [child['data'] for child in data['data']['children']]
    send_email(posts)

def send_email(posts):
    user = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_PASSWORD')
    port = 465  # For SSL
    lines = []
    for post in posts:
        lines.append(post['title'])
        permalink = post['permalink']
        permalink_url = f'https://www.reddit.com{permalink}'
        lines.append(permalink_url)
        lines.append('')
    body = '\n'.join(lines)
    message = f'Subject: New post(s) in pbpmooo\n{body}'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(user, password)
        to_addrs = [
            'mikezackles@gmail.com',
            'seancsawyer@gmail.com',
        ]
        server.sendmail(user, to_addrs, message)


if __name__ == '__main__':
    run()

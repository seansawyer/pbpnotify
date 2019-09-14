import argparse
import os
import requests
import smtplib
import ssl
import sys

from typing import Any, Dict, List

USER_AGENT = 'pbpmooo-notify/0.1 by ikvind'
TOKEN_VAR = 'REDDIT_TOKEN'

def run(args: argparse.Namespace):
    if args.email is None:
        print('No emails to notify. Please supply --email at least once.')
        sys.exit(1)
    sub = args.subreddit
    to_addrs = args.email
    token = os.getenv('REDDIT_TOKEN')
    new_url = f'https://oauth.reddit.com/r/{sub}/new.json'
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
    send_email(to_addrs, posts)

def send_email(to_addrs: List[str], posts: List[Dict[str, Any]]):
    """
    Send a summary of posts to the supplied email addresses.
    """
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
        server.sendmail(user, to_addrs, message)

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Send notifications of new posts to a private subreddit.')
    parser.add_argument('subreddit', metavar='SUB', help='the subreddit name')
    parser.add_argument('--email', action='append')
    return parser


if __name__ == '__main__':
    parser = build_arg_parser()
    args = parser.parse_args()
    run(args)

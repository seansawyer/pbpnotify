#!/bin/bash

# You must set the following environment variables before running this script:
#
# $REDDIT_USER - your Reddit username
# $REDDIT_PASSWORD - your Reddit password
# $REDDIT_APP_KEY - the key of a Reddit script app owned by your user
# $REDDIT_SECRET_KEY - the secret key of a Reddit script app owned by your user

curl \
    -X POST \
    -d "grant_type=password&username=$REDDIT_USER&password=$REDDIT_PASSWORD" \
    --user "$REDDIT_APP_KEY:$REDDIT_SECRET_KEY" \
    -H 'User-Agent: pbpmooo-notify 0.1' \
    https://www.reddit.com/api/v1/access_token

Create a virtual environment.

```bash
pyenv virtualenv 3.7.2 pbpnotify-3.7.2
pyenv activate 'pbpnotify-3.7.2'
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Set up the environment variables you'll need to get a token.

```bash
export REDDIT_USER="username"
export REDDIT_PASSWORD="password"
export REDDIT_APP_KEY="redditappkey"
export REDDIT_SECRET_KEY="redditsecretkey"
```

Get a token.

```bash
./get_token.sh
```

Take the token and set it in an environment variable, too.

```bash
export REDDIT_TOKEN="123456789012-abcdefghijklmnopqrstuvwxyz"
```

Right now this thing only supports temporary tokens. Permanent token support via refresh will be added soon.

Now set your GMail credentials in environment variables as well.

```bash
export GMAIL_USER='youraddress@gmail.com'
export GMAIL_PASSWORD='hunter2'
```

You will need the "less secure apps" setting enabled for your GMail account. For this reason, I highly recommend using a throwaway account.

Now you can run the script:

```bash
python pbpnotify.py subname --email recipient1@domain1.com --email recipient2@domain2.com
```

Deactivate the virtual environment when you are done.

```bash
pyenv deactivate
```

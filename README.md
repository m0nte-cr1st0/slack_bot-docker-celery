# Slack API
1. Create a [Slack App](https://api.slack.com/apps).
2. Install Slack App to Team
3. Copy `Bot User OAuth Access Token` from `OAuth & Permissions` page and create `environment varible` - `export SLACK_API_TOKEN = <Bot User OAuth Access Token>`
4. On the `Events Subscriptions` page enter link of your website + `/events/`, pick next events:
`im_created`, `im_history_changed`, `message.channels`, `message.groups`, `message.im` to `Workspace Events` and `im_created`, `message.channels`, `message.im` to `Bot Events`.
5. On the `OAuth & Permissions` page to a `Scopes` add `files.read`
6. On the `Incoming Webhooks` page create `Add New Webhook to Workspace`

# Run application

1. `mkdir -p /tmp/slack_bot/mysqld && sudo chmod -R 777 /tmp/slack_bot/mysqld`
2. `sudo docker-compose up -d --no-deps --build --force-recreat`
3. `sudo docker-compose run web python3 manage.py migrate`
4. create a `superuser` (admin) - `sudo docker-compose run web python manage.py createsuperuser`
4. `sudo docker-compose up`

Site included at http://0.0.0.0:9001 (f.e. http://0.0.0.0:9001/admin/)

## Run tests

```bash
./manage.py tests
```

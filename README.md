# Generic Cron Server

This server sends requests to other servers on a pre-defined schedule. Those requests can be optionally authenticated.

This sends slack notifications to a configurable channel when cron requests get a not-okay response.

## API

### Registering a new schedule

**POST /api/schedules**

Requires KBase auth token with the `CRON_EDITOR` role.

_Request JSON body object_

Similar to a crontab, you can specify values for minute, hour, weekday, day, and month.

* `minute` - optional - integer (0-60) - minute to run on
* `hour` - optional - integer (0-23) - hour to run on
* `week_day` - optional - integer (1-7) - day of the week to run on
* `month_day` - optional - integer (1-31) - day of the month to run on
* `month` - optional - integer (1-12) - month of the year to run on
* `scheduled_request` - required - object
  * `url` - required - string (url) - url you want to make a request to on schedule
  * `method` - optional (default is GET) - string - http method you want to use
  * `body` - optional - string - request body text you want to send
  * `headers` - optional - array of strings - headers to send

This uses the following rules:

* If only minute is specified, then the request is run hourly on that minute
* If both minute and hour are specified, or just hour, then the request is run daily
* If minute, hour, and week_day are specified (or just week_day), then the request is run weekly
* If minute, hour, week_day, and month_day are specified (or just month_day) then the request is run monthly
* If minute, hour, week_day, month_day, and month are specified (or just month), then the request is run yearly

_Response JSON_

On success

* id: unique ID of the scheduled request (use this for editing and removing)

On failure

* error: error message describing the failure

### Editing an existing schedule

**PUT /api/schedules/{id}**

Edit an existing scheduled request. You can use the same JSON body format as in the creation endpoint.

Requires `CRON_EDITOR` if you are owner, or `CRON_ADMIN` if you are not owner.

### Removing a schedule

**DELETE /api/schedules/{id}**

Delete an existing scheduled request. No query params or body.

Requires `CRON_EDITOR` if you are owner, or `CRON_ADMIN` if you are not owner.

### Viewing registered schedules

**GET /api/schedules**

View existing schedules. Returns a JSON object where each key is a schedule ID, and each value is some schedule info.
 
If you are a `CRON_EDITOR` , then only shows schedules you've created. If you're a `CRON_ADMIN`, then it shows all schedules.

No query params.

### Other administration stuff

Server configuration allows you to:
* set the slack API token and channel for failure notifications

**GET /api/config**

View the current configuration (requires `CRON_ADMIN` role).

**PUT /api/config**

Update current configuration with these optional JSON properties in the body:

* slack_api_token - string - slack API token
* slack_channel - string - slack channel to send failure notifications to

Requires `CRON_ADMIN` role.

## Development

Run `docker-compose up` to start the dev server, and `make test` to run tests against the server.

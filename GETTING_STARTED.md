# Getting Started

## To get up and running for development...

- In the project root, create a Python environment:
```
$ python3 -m venv ENV
```

- In the environment's `activate` script, at `ENV/bin/activate`, create an environment variable that points to your local database for storing dungeonbot's information. An example: `export DB_URL='postgresql://localhost:5432/dungeonbot_db'`
- Activate your virtual environment
```
$ source ENV/bin/activate
```

- `pip` install all of Dungeonbot's dependencies
```
(ENV) $ pip install -r pipreqs.txt
```

- Apply Dungeonbot's migrations to your database with the following shell command, runing from the project root:
```
(ENV) $ python src/manage.py db upgrade
```

**Note: if there are conflicts between migrations, try looking at the `migrations/versions` directory.
Apply the latest migration by getting the hash of the latest migration and running the upgrade command: `python src/manage.py db upgrade <the hash>`**

- Now you're ready to start developing with Dungeonbot! Run the bot with `python src/manage.py runserver`, where you'll get something like the following output to the console:
```
 * Running on http://0.0.0.0:5006/ (Press CTRL+C to quit)
```

- In a second terminal, you can send a sample request to the bot to check what the output. An example of the type of request that can be sent to the bot can be found in `src/auxiliaries/send_dummy_event.sh`. Run that shell script in the second terminal to get your output from the bot, and you're good to go!

Dungeonbot runs based on events from the Slack application.
These events are specified in the "text" field in the "event" key of the incoming JSON.
Dungeonbot will recognize and attempt to handle any event text starting with `!`, so try to start there!

At this point, you're ready to contribute, so head over to the [contribution guide](CONTRIBUTING.md) and get started on improving the bot!


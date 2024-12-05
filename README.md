# Cerbos Flask Authorization

This repo contains a sample blog application that supports users, posts, and comments. The routes are authorized and protected by Cerbos Policy Decision Point (PDP). Essentially, this means there are yaml files at cerbos/policies that define the rules on how users can carry out actions in this application.

NB: This README assumes you are using a UNIX system. If you are on Windows, consider using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

## Setting up

To set up and run this app, you need:

1. [Cerbos binary](https://docs.cerbos.dev/cerbos/latest/installation/binary.html) or [Docker](https://docs.cerbos.dev/cerbos/latest/installation/container.html) for starting the PDP server
2. Python3

Follow the steps below for set up instructions

### Cloning the repo

```sh
git clone https://github.com/vicradon/cerbos-flask-authorization.git
cd cerbos-flask-authorization
```

### Setting up the virtual environment and installing dependencies

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Cerbos PDP Server

```sh
cd cerbos
cerbos server
```

Or by using Docker

```sh
cd cerbos
bash docker-start.sh
```

### Running the app

```sh
flask --app app run --debug --port 4600
```

The app will be available on http://localhost:4600

## Testing the API routes using Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/11429418-e7d7eeb1-cc53-440f-ac39-c7bd78f28fc0?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D11429418-e7d7eeb1-cc53-440f-ac39-c7bd78f28fc0%26entityType%3Dcollection%26workspaceId%3Da855b671-a075-4e89-91d6-043ecda366fd)

Download [this public Postman collection](https://www.postman.com/osinachi1/workspace/cerbos-flask-authorization/collection/11429418-e7d7eeb1-cc53-440f-ac39-c7bd78f28fc0?action=share&creator=11429418), explore its routes, and test them. You can

1. Register users /auth/register
2. Create posts /posts
3. Fetch comments for a post /posts/:postid/comments

And many more!

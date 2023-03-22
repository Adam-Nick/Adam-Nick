import os
import random
import numpy as np
import datetime
from github import Github
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
g = Github(username, password)

# Repository name to update
repo_name = "<Adam-Nick>/<Adam-Nick>"

# Create snake
canvas = np.zeros((7, 52))
snake = [(0, 0)]
canvas[0, 0] = 1

# Iterate over days
today = datetime.datetime.now().strftime("%Y-%m-%d")
for i in range(365):
    date = (datetime.datetime.now() - datetime.timedelta(i)).strftime("%Y-%m-%d")
    count = random.randint(1, 5)
    for j in range(count):
        x, y = random.randint(0, 6), random.randint(0, 51)
        if (x, y) not in snake:
            snake.append((x, y))
            canvas[x, y] = 1

    # Push snake to GitHub
    commit_message = f"Snake ate {count} things on {date}"
    g.get_user().get_repo(repo_name).create_git_ref(ref=f"refs/heads/snake/{date}", sha="main")
    contents = g.get_user().get_repo(repo_name).get_contents("README.md")
    g.get_user().get_repo(repo_name).update_file(contents.path, commit_message, canvas.tostring().decode("utf-8"), contents.sha, branch=f"snake/{date}")

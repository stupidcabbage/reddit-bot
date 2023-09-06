class PostExists(Exception):
    def __str__(self):
        return "Post is already exists."


class SubredditsExists(Exception):
    def __str__(self):
        return "Subreddits are missing in the database"

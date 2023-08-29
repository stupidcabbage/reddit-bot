class PostExists(Exception):
    def __str__(self):
        return "Post is already exists."

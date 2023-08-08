from reddit.api import get_new_posts_from_subreddit as gs
import pprint

pprint.pprint(gs(sreddit="FORTnITE", limit=5))

from flask import Flask, request
import pytumblr
from flask import render_template
import json
import settings

app = Flask(__name__)





@app.route("/tag", methods=["GET",])
def get_tag():
    user = request.args.get("user").strip()
    tag = request.args.get("tag")
    client = pytumblr.TumblrRestClient(
        settings.TUMBLR_CONSUMER_KEY,
        settings.TUMBLR_CONSUMER_SECRET,
        settings.TUMBLR_OAUTH_TOKEN,
        settings.TUMBLR_OAUTH_SECRET
    )

    tagged_posts = client.posts("{}.tumblr.com".format(user),"photo", tag=tag.strip() )
    post_group = {
        "tag":tag.strip(),
        "posts": tagged_posts
    }
    return json.dumps(post_group)



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    user = request.args.get("user").strip()
    tags = request.args.get("tags")
    tags_list = request.args.get("tags", "").split(",")
    posts = None
    if user and bool(len(tags_list)):

        client = pytumblr.TumblrRestClient(
            settings.TUMBLR_CONSUMER_KEY,
            settings.TUMBLR_CONSUMER_SECRET,
            settings.TUMBLR_OAUTH_TOKEN,
            settings.TUMBLR_OAUTH_SECRET
        )

        info = client.blog_info(user)
        posts = []
        tags_list.append(user)
        for tag in tags_list:
            tagged_posts = client.posts("{}.tumblr.com".format(user),"photo", tag=tag.strip() )
            if bool(tagged_posts['total_posts']):
                post_group = {
                    "tag":tag.strip(),
                    "posts": tagged_posts
                }
                posts.append(post_group)



    return render_template("index.html", user=user, tags=tags, tags_list=tags_list, posts=posts, info=info)

if __name__ == '__main__':
    app.run(debug=True)

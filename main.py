import os
import csv
import datetime
from openai import OpenAI
from typing import List
from bs4 import BeautifulSoup

OpenAI.api_key_path = "/home/mat/Documents/ProgramExperiments/openAIapiKey"
client = OpenAI()
BLOG_DIR = "/home/mat/Documents/blog/blog/"

###### CSV CREATION SECTION: LINKS NOT WORKING SO NOT BEING USED #########

### Create csv files if they don't exist ###
# # check if nodes.csv exists, if not create it with fields title,id,type:primary,tag:<name>,meta:<name>,time:begin,content,thumbnail,reference
# if not os.path.exists("./data/nodes.csv"):
#     with open("./data/nodes.csv", "w") as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["title", "id", "type:primary", "tag:<name>", "meta:<name>", "time:begin", "content", "thumbnail", "reference"])

# # check if links.csv exists, if not create it with fields id,source,target,label
# if not os.path.exists("./data/links.csv"):
#     with open("./data/links.csv", "w") as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(["id", "source", "target", "label"])


# get all blog posts from /home/mat/Documents/blog/blog/ and put them into a list
blog_list = os.listdir(BLOG_DIR)

def create_yaml(blog_name, model_res):

    content = f"""---
title: {blog_name}.md
types:
- undefined
---

{model_res}

Link to the original post: https://enjoy.monster/blog/{blog_name}.html
"""

    with open(f"./data/{blog_name}.md", "w") as md_file:
        md_file.write(content)    
    return

    

for post in blog_list:
    raw_blog = open(BLOG_DIR + post, "r").read()
    print(f"working on {post}")

    parsed_blog = BeautifulSoup(raw_blog, 'html.parser').get_text()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": f"""you are the world's greatest assistant go you chat :) 
        Please take the following blog post and construct a three to four sentence summary of the content and topics of the post.
        Write this as if you were the author of the post and quite excited about the post's contents taking the tone of a random presenter, a cowboy, Shakespeare, a robot, anything! Anything you want to do to make it fun and interesting.
        Emojis are HIGHLY encouraged! And please make sure to put links to other websites in the summary if they are referenced in the post. 
        Make sure to say "I" and "me" as opposed to "the author" or "the writer", have this be your voice.
        If a post references a another post of the following: {blog_list} then please link to it in the summary in the format [[name-of-linked-post.md]] (note the replacing of '_' with '-')
        """
        },
        {
        "role": "user",
        "content": f"{parsed_blog}"
        }
    ])

    base_name = post.split("/")[-1].split(".")[0].replace("_", "-")

    create_yaml(base_name, response.choices[0].message.content)
    # raw_blog.close()

    #### WRITE TO CSV: NOT USED UNTIL LINKS ARE WORKED OUT ####
    # # write the response to a csv file
    # with open("./data/nodes.csv", "a") as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow([post.split("/")[-1], post.split("/")[-1], "", "", "", "", response.choices[0].message.content, "", ""])

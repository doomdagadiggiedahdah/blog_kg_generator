import os
import csv
import datetime
from openai import OpenAI
# import instructor
# import subprocess
from typing import List
from bs4 import BeautifulSoup
# from pydantic import BaseModel, Field

OpenAI.api_key_path = "/home/mat/Documents/ProgramExperiments/openAIapiKey"
client = OpenAI()

# instructor.patch(openai)
# nodes.csv and links.csv

BLOG_DIR = "/home/mat/Documents/blog/blog/"


### Create csv files if they don't exist ###
# TODO: (not sure if this sentence makes sense) if the file exists ask if they want to overwrite it, if not then append to it
# check if nodes.csv exists, if not create it with fields title,id,type:primary,tag:<name>,meta:<name>,time:begin,content,thumbnail,reference
if not os.path.exists("./data/nodes.csv"):
    with open("./data/nodes.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["title", "id", "type:primary", "tag:<name>", "meta:<name>", "time:begin", "content", "thumbnail", "reference"])

# check if links.csv exists, if not create it with fields id,source,target,label
if not os.path.exists("./data/links.csv"):
    with open("./data/links.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["id", "source", "target", "label"])


# get all blog posts from /home/mat/Documents/blog/blog/ and put them into a list
blog_list = os.listdir(BLOG_DIR)

for post in blog_list:
    raw_blog = open(BLOG_DIR + post, "r").read()

    parsed_blog = BeautifulSoup(raw_blog, 'html.parser').get_text()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": f"""you are the world's greatest assistant go you chat :) 
        Please take the following blog post and construct a three to four sentence summary of the content and topics of the post.
        Write this as if you were the author of the post, saying "I" and "me" and "my" as opposed to "the author" or "the writer".
        If a post references a another post of the following: {blog_list} then please link to it in the summary in the format [[name_of_linked_post]]
        """
        },
        {
        "role": "user",
        "content": f"{parsed_blog}"
        }
    ])

    # time of creation as id of node
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # write the response to a csv file
    with open("./data/nodes.csv", "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([post.split("/")[-1], post.split("/")[-1], "", "", "", "", response.choices[0].message.content, "", ""])
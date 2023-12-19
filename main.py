import os
import openai
import instructor
import subprocess
from typing import List
from pydantic import BaseModel, Field

openai.api_key_path= "/home/mat/Documents/ProgramExperiments/openAIapiKey"

instructor.patch(openai)

# note to self: the csv file names need to be assigned so that they can be written to the config file
# nodes.csv and links.csv


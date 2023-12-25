#!/bin/bash

cd /home/mat/Documents/ProgramExperiments/kg2online/
source ~/Documents/ProgramExperiments/.ftp_creds
 

# TODO: check if this overwrites
# doesn't seem like this overwrites, just returns an error (file exists)
mkdir ./data/ ./export/ # will this overwrite if already exists? TODO check that and then handle if so

# (maybe) create config
if ! [[ -f "./config.yml" ]]; then
    cosma config
fi

## configure the configuration: CSV STYLE
# sed -i 's|directory|csv|' ./config.yml # using "|" because I've got directory strucutes going on.
# sed -i 's|nodes_origin: ""|nodes_origin: "./data/nodes.csv"|' ./config.yml
# sed -i 's|links_origin: ""|links_origin: "./data/links.csv"|' ./config.yml
# sed -i 's|history: true|history: false|' ./config.yml
# sed -i 's|export_target: ""|export_target: "./export/"|' ./config.yml

## configure the configuration: MARKDOWN STYLE
sed -i 's|files_origin: ""|files_origin: "./data/"|' ./config.yml
sed -i 's|export_target: ""|export_target: "./export/"|' ./config.yml
sed -i 's|history: true|history: false|' ./config.yml
sed -i 's|generate_id: always|generate_id: never|' ./config.yml # not sure if this is needed or not.


echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!$1"

# call python for summary / node generation
source venv/bin/activate
python3 main.py $1
deactivate

cosma modelize
# firefox export/cosmoscope.html

cd ./export/
ftp -n -p $FTP_SERVER <<END_SCRIPT
user $FTP_USERNAME $FTP_PASSWORD
cd about
put cosmoscope.html
ls
bye
END_SCRIPT

sleep 5
firefox enjoy.monster/about/cosmoscope.html

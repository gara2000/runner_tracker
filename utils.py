import streamlit as st
import json
import datetime
from PIL import Image
import qrcode
import os

#######################################################################
#General utilities
#######################################################################

def get_data():
    with open("data.json") as f:
        return json.load(f)

def set_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

def click_func(state):
    data = get_data()
    data["state"] = state
    set_data(data)

#######################################################################
#Race utilities
#######################################################################

def get_id(word, prefix):
    return int(word[len(prefix):])

def create_race(name, length, timestamp, num_ckpt, state):
    data = get_data()
    data["state"] = state

    race = {"id":len(data["races"]), "name":name, "length":length, "timestamp":timestamp.isoformat(), "runners":[], "num_ckpt":num_ckpt}

    data["races"].append(race)
    set_data(data)

def delete_race(idx):
    pass

#######################################################################
#Runner utilities
#######################################################################

def gen_qr(idx, qr_path):
    img = qrcode.make(idx)
    img.save(qr_path)

def add_runner(raceid, name, gender, up_file, state):
    data = get_data()
    data["state"]="view"

    race = data["races"][raceid]
    num_ckpt = race["num_ckpt"]

    directory = f"images/race_{raceid}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    runnerid = len(data["races"][raceid]["runners"])

    im_path = f"{directory}/runner_{runnerid}.png"
    qr_path = f"{directory}/qr_{runnerid}.png"

    runner = {"id":runnerid, "name":name, "gender":gender, "im_path":im_path, "qr_path":qr_path}
    ckpts = {f"ckpt_{i}":"DNF" for i in range(num_ckpt)}
    runner.update(ckpts)
    runner.update({"next_ckpt":1})

    if up_file is not None:
        image = Image.open(up_file)
        image.save(im_path)

    gen_qr(runnerid, qr_path)
    
    data["races"][raceid]["runners"].append(runner)
    set_data(data)

#######################################################################
#Leaderboard utilities
#######################################################################

def get_data_frame(runners):
    pass

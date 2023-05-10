import streamlit as st
import json
import datetime
from PIL import Image
import qrcode
import os
import pandas as pd
from detect import init_ckpt_data

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

def get_new_race_id(data):
    idd = data["next_race_id"]
    data["next_race_id"]+=1
    return idd

def create_race(name, length, timestamp, num_ckpt, state):
    data = get_data()
    data["state"] = state
    race_id = get_new_race_id(data)
    race_dir = f"races_info/race_{race_id}"
    if not os.path.exists(race_dir):
        os.makedirs(race_dir)

    for ckpt_id in range(num_ckpt):
        ckpt_data = init_ckpt_data(race_id, ckpt_id)
        with open(race_dir+f"/ckpt_{ckpt_id}.json", "w") as f:
            json.dump(ckpt_data, f)

    race = {"id":race_id, "name":name, "length":length, "timestamp":timestamp.isoformat(), "runners":[], "num_ckpt":num_ckpt, "race_dir": race_dir}

    data["races"].append(race)
    set_data(data)

def delete_race(idx):
    data = get_data()
    del data["races"][idx]

    set_data(data)

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
    idx = race["id"]
    num_ckpt = race["num_ckpt"]

    directory = race["race_dir"]+"/images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    runnerid = len(data["races"][raceid]["runners"])

    im_path = f"{directory}/runner_{runnerid}.png"
    qr_path = f"{directory}/qr_{runnerid}.png"

    runner = {"id":runnerid, "name":name, "gender":gender, "im_path":im_path, "qr_path":qr_path}
    ckpts = {f"ckpt_{i}":"DNF" for i in range(num_ckpt)}
    runner.update(ckpts)
    runner.update({"next_ckpt":0, "time":"DNF", "verdict":"DNF"})

    if up_file is not None:
        image = Image.open(up_file)
        image.save(im_path)

    gen_qr(runnerid, qr_path)
    
    data["races"][raceid]["runners"].append(runner)
    set_data(data)

#######################################################################
#Leaderboard utilities
#######################################################################

def get_data_frame(race):
    runners = race["runners"]
    num_ckpt = race["num_ckpt"]

    df = {"Runner":[runner["name"] for runner in runners]}
    df.update({f"Checkpoint {i}":[runner[f"ckpt_{i}"] for runner in runners] for i in range(num_ckpt)})
    df.update({"Fina Time":[runner["time"] for runner in runners], "Verdict":[runner["verdict"] for runner in runners]})

    # Sort the dictionary before making the data frame
    #
    #
    #


    df = pd.DataFrame(df)

    return df

def time_format(time_diff):
    return "{:02d}:{:02d}:{:02d}".format(time_diff.seconds // 3600, (time_diff.seconds % 3600) // 60, time_diff.seconds % 60)

def get_time(race):
    race_start = datetime.datetime.fromisoformat(race["timestamp"])
    now = datetime.datetime.now()
    
    if now > race_start:
        time_diff = now - race_start
        time_diff_str = "Racing time: {:02d}:{:02d}:{:02d}".format(time_diff.seconds // 3600, (time_diff.seconds % 3600) // 60, time_diff.seconds % 60)
    else:
        time_diff = race_start - now
        time_diff_str = "Race starts in: {} days, {:02d} hours, {:02d} minutes, {:02d} seconds".format(time_diff.days, time_diff.seconds // 3600, (time_diff.seconds % 3600) // 60, time_diff.seconds % 60)

    return time_diff_str

def get_race_by_id(data, race_id):
    for race in data["races"]:
        if race["id"]==race_id:
            return race

def update_data(race):
    race_id = race["id"]

    data = get_data()
    race = get_race_by_id(data, race_id)
    num_ckpt = race["num_ckpt"]
    runners = race["runners"]


    for ckpt in range(num_ckpt):
        path = race["race_dir"]+f"/ckpt_{ckpt}.json"
        with open(path) as f:
            ckpt_data = json.load(f)
            for i, time in ckpt_data["ids"].items():
                try:
                    runner = runners[int(i)]
                    next_ckpt = runner["next_ckpt"]
                    if next_ckpt==ckpt:
                        race_start = datetime.datetime.fromisoformat(race["timestamp"])
                        target = datetime.datetime.fromisoformat(time)
                        time_diff = target - race_start

                        runner[f"ckpt_{ckpt}"] = time_format(time_diff)
                        next_ckpt+=1
                    elif runner[f"ckpt_{ckpt}"]=="DNF":
                        runner[f"ckpt_{ckpt}"]=="DNA"
                    runners[int(i)]["next_ckpt"] = next_ckpt
                except:
                    print("Undefined QR data!")
                        
        set_data(data)

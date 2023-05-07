import streamlit as st
import json
from utils import *

#######################################################################
#Description of the states
#######################################################################
#The application has different states where each state refers to a page:
#1."main"               : The home page
#2."create"             : Creating a race
#3."view"               : Viewing the created races
#4."runner_{race_id}"   : Creating a runner for the race
#5."runners"            : Viewing the runners of a race
#6."leaderboard"        : Viewing the leaderboard of the race

#######################################################################
#loading the data from the json file
#######################################################################

with open("data.json") as f:
    data = json.load(f)

state = data["state"]
#######################################################################
#The main page
#######################################################################
if state=="main":
    st.header(":man-running: Welcome to Runner Tracker :woman-running:")
    st.subheader("Here are the options provided by this application:")
    st.write('''
        1. Click on the button "Create a new race" below to start a new race
        2. Visit previously created races
        3. Add runners to the created races
        4. Visit the runners' information for each race
        5. Visit the leaderboard for each race
        6. Additionally you can ask for help by calling the numbers provided in the help section
        7. Enjoy!!!
        ''')
           
    col1, col2  = st.columns(2)
    with col1:
        st.button("Create a new race", on_click=click_func, args=["create"])
    with col2:
        st.button("View existing races", on_click=click_func, args=["view"])
    
#######################################################################
#Creating a new race
#######################################################################

if state=="create":
    name = st.text_input("Race name", "name")
    length = st.number_input("Race length in meters", value=5000, min_value=25, max_value=50000)
    num_ckpt = st.number_input("Number of checkpoints", value=5, min_value=1, max_value=51)
    date = st.date_input("Race date", value=datetime.date.today())
    time = st.time_input("Race time", value=datetime.time(9, 0))
    timestamp = datetime.datetime.combine(date, time)
    
    col1, col2  = st.columns(2)
    with col1:
        st.button("Create race", on_click=create_race, args=[name, length, timestamp, num_ckpt, "view"])
    with col2:
        st.button("Cancel", on_click=click_func, args=["main"])
    
#######################################################################
#Viewing existing races
#######################################################################

if state=="view":
    #use tabs
    races = data["races"]
    tabs = st.tabs([race["name"] for race in races])

    for i, tab in enumerate(tabs):
        with tab:
            st.write(races[i])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("Leaderboard", on_click=click_func, args=[f"leaderboard_{i}"], key=str(i)+"leaderboard")
            with col2:
                st.button("Add runner", on_click=click_func, args=[f"runner_{i}"], key=str(i)+"add")
            with col3:
                st.button("View runners", on_click=click_func, args=[f"runners_{i}"], key=str(i)+"view")
            with col4:
                st.button("Delete race", on_click=delete_race, args=[i], key=str(i)+"delete")

    col1, col2  = st.columns(2)
    with col1:
        st.button("Create a new race", on_click=click_func, args=["create"])
    with col2:
        st.button("Back to home page", on_click=click_func, args=["main"])
    
#######################################################################
#Adding runners
#######################################################################

if state.startswith("runner_"):
    raceid = get_id(state, "runner_")

    name = st.text_input("Runner name", "name")
    gender = st.selectbox("Gender", ("Male", "Female", "Other"))
    up_file = st.file_uploader("Image")

    col1, col2  = st.columns(2)
    with col1:
        st.button("Submit", on_click=add_runner, args=[raceid, name, gender, up_file, "view"])
    with col2:
        st.button("Cancel", on_click=click_func, args=["view"])
    
#######################################################################
#Viewing runners
#######################################################################

if state.startswith("runners_"):
    raceid = get_id(state, "runners_")

    race = data["races"][raceid]
    runners = race["runners"]
    st.header(race["name"])
    st.subheader("List of Runners")
    st.markdown("---")
    for runner in runners:
        st.write(runner)
        st.markdown("---")

    st.button("Back to viewing races", on_click=click_func, args=["view"])

#######################################################################
#Leaderboard
#######################################################################

if state.startswith("leaderboard_"):
    raceid = get_id(state, "leaderboard_")

    race = data["races"][raceid]
    runners = race["runners"]

    #create the data frame
    df = get_data_frame(runners)

    st.button("Back to viewing races", on_click=click_func, args=["view"])


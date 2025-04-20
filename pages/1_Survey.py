# Accessible via /survey
import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

st.set_page_config(page_title="Roominate Survey", layout="wide")

# loads secrets needed
load_dotenv()
MONGO_URI, type = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI"), "Deployed" if st.secrets.get("MONGO_URI") else "Locally"
print(f"Currently using: {type}")
client = MongoClient(MONGO_URI)
db = client["roominate"]
collection = db["responses"] # where to store responses

if "responses" not in st.session_state:
    st.session_state.responses = {} # create empty responses for first ever submission

st.title("📝 Roominate Questionairre")

# top-level tabs
tab1, tab2 = st.tabs(["👤 About You", "🤝 Roommate Preferences"])

with tab1:
    st.header("👤 About You")
    email = st.text_input("Your Cornell Email")
    year = st.selectbox(
        "What year are you?", ["Freshman", "Sophomore", "Junior", "Senior", "Other"]
    )
    gender = st.selectbox(
        "Your gender?", ["Male", "Female", "Nonbinary", "Prefer not to say"]
    )
    clean_self = st.slider(
        "How clean do you keep your room? (1 = Messy, 10 = Spotless)", 1, 10, 5
    )
    wake_time = st.time_input("On average, what time do you wake up?")
    sleep_time = st.time_input("On average, what time do you go to bed?")

    st.subheader("Your substance use")
    use_responses = {}
    for substance in ["Alcohol", "Marijuana", "Nicotine", "Harder Drugs"]:
        use_responses[substance] = st.radio(
            f"{substance} usage:",
            ["Never", "Sometimes", "Often", "Daily"],
            horizontal=True,
        )

    personality = st.selectbox("I am an...", ["Introvert", "Extrovert", "Ambivert"])
    relationship = st.selectbox(
        "What kind of relationship do you hope to have with your roommate?",
        ["Best friends", "Friendly", "Just coexisting"],
    )
    snore = st.selectbox("Do you snore?", ["Yes", "No", "Not sure"])
    sleep_depth = st.slider("How deep of a sleeper are you?", 1, 10, 5)
    room_social = st.slider(
        "My room is a social space (1 = not at all, 10 = very social)", 1, 10, 5
    )
    room_private = st.slider(
        "My room is a private space (1 = not at all, 10 = very private)", 1, 10, 5
    )
    room_study = st.slider(
        "My room is a study space (1 = not at all, 10 = very academic)", 1, 10, 5
    )
    guests = st.selectbox(
        "What are your guest hosting habits?",
        ["Rarely", "Occasionally", "Often", "Very Often"],
    )
    notify_guests = st.selectbox(
        "Do you inform your roommate before guests?", ["Yes", "No", "Depends"]
    )
    conflict = st.selectbox(
        "When conflict arises, what is your first instinct for addressing it?",
        ["Talk it out", "Avoid it", "Write a message", "Get a third party"],
    )
    study_place = st.selectbox(
        "Where do you usually study?", ["Library", "My room", "Café", "Other"]
    )
    shower_freq = st.selectbox(
        "How often do you shower?", ["Daily", "Every other day", "Few times a week"]
    )

with tab2:
    st.header("🤝 Roommate Preferences")
    preferred_gender = st.selectbox(
        "Preferred roommate gender?", ["Any", "Male", "Female", "Nonbinary"]
    )
    roommate_clean = st.slider("How clean do you want your roommate to be?", 1, 10, 5)
    sleep_importance = st.slider(
        "How important is it that your roommate has a similar sleep schedule?", 1, 10, 5
    )

    st.subheader("Substance use tolerance for your roommate")
    tolerance_responses = {}
    for substance in ["Alcohol", "Marijuana", "Nicotine", "Harder Drugs"]:
        tolerance_responses[substance] = st.radio(
            f"{substance} (OK for roommate):",
            ["None", "Sometimes", "Often", "Daily"],
            horizontal=True,
        )

    roommate_personality = st.selectbox(
        "I'd prefer if my roommate was an...",
        ["Introvert", "Extrovert", "Ambivert", "No preference"],
    )
    cares_snore = st.selectbox("Do you care if your roommate snores?", ["Yes", "No"])
    roommate_guests = st.selectbox(
        "How often would you prefer your roommate to have guests over?",
        ["Rarely", "Occasionally", "Often", "Very Often"],
    )
    guest_notify = st.selectbox(
        "How would you prefer your roommate inform you about guests coming over?",
        ["Always", "Sometimes", "Not necessary"],
    )
    conflict_pref = st.selectbox(
        "What do you prefer your roommate do when there's conflict?",
        ["Talk it out", "Avoid it", "Message me", "Get a third party"],
    )
    study_pref = st.selectbox(
        "Where would you prefer your roommate studies?",
        ["Library", "Room", "Café", "Anywhere is fine"],
    )
    shower_expectation = st.selectbox(
        "Minimum shower frequency for your roommate?",
        ["Daily", "Every other day", "Few times a week"],
    )

# Final submission button
if st.button("📩 Submit My Survey"):
    required = [email, year, gender]
    if any(x.strip() == "" for x in required):
        st.warning("Please fill in all required fields.")
    else:
        all_data = {
            "Email": email,
            "What year are you?": year,
            "Your gender?": gender,
            "How clean do you keep your room?": clean_self,
            "Wake Time": str(wake_time),
            "Bed Time": str(sleep_time),
            "I am an...": personality,
            "Roommate relationship goal": relationship,
            "Do you snore?": snore,
            "How deep of a sleeper are you?": sleep_depth,
            "Room as social": room_social,
            "Room as private": room_private,
            "Room as study": room_study,
            "Guest habits": guests,
            "Notify guests?": notify_guests,
            "Conflict approach": conflict,
            "Study location": study_place,
            "Shower frequency": shower_freq,
            "Preferred roommate gender?": preferred_gender,
            "How clean do you want your roommate to keep the room?": roommate_clean,
            "Importance of sleep match": sleep_importance,
            "I'd prefer if my roommate was an...": roommate_personality,
            "Care if roommate snores": cares_snore,
            "Guest frequency (preferred)": roommate_guests,
            "How roommate should notify about guests": guest_notify,
            "Preferred conflict response": conflict_pref,
            "Roommate study location preference": study_pref,
            "Roommate shower minimum": shower_expectation,
        }

        for substance, val in use_responses.items():
            all_data[f"{substance} (use)"] = val

        for substance, val in tolerance_responses.items():
            all_data[f"{substance} (ok with)"] = val

        st.session_state.responses.update(all_data)

        # write to MongoDB collection (i.e. the "responses" one)
        collection.insert_one(st.session_state.responses)

        st.success("🎉 Your full survey has been submitted to the database! Thank you!")

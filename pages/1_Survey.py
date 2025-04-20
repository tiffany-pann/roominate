import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

st.set_page_config(page_title="Roominate Survey", 
                   layout="wide",
                   page_icon="📝")

# load secrets
load_dotenv()
MONGO_URI = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["roominate"]
collection = db["responses"]

if "responses" not in st.session_state:
    st.session_state.responses = {} # create empty dictionary to store responses
if "survey_page" not in st.session_state:
    st.session_state.survey_page = "about_you"

st.title("Roominate — Questionnaire")
st.markdown("Please answer these questions to the best of your abilities, as they allow us to match you with your most compatible potential roommates!")

st.markdown("All responses will be kept confidential and only used for the purposes of Roominate.")

# Page 1: Your Preferences 
if st.session_state.survey_page == "about_you":
    st.header("👤 About You")
    st.subheader("Questions about yourself")
    
    email = st.text_input("Your Cornell Email")
    year = st.selectbox("What year are you?", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])
    gender = st.selectbox("Your gender?", ["Male", "Female", "Nonbinary", "Prefer not to say"])
    
    clean_self = st.slider("How clean do you keep your room? (1 = Messy, 10 = Spotless)", 1, 10, 5)
    
    # 3am -> 3pm in 1 hr intervals
    wake_time = st.selectbox("On average, what time do you wake up?", 
                             [f"{hour}:00 AM" for hour in range(3, 12)] + 
                             ["12:00 PM"] +
                             [f"{hour}:00 PM" for hour in range(1, 4)])
    # 6pm to 6am in 1 hr intervals
    sleep_time = st.selectbox("On average, what time do you go to bed?", 
                              [f"{hour}:00 PM" for hour in range(6, 12)] + ["12:00 AM"] +
                              [f"{hour}:00 AM" for hour in range(1, 7)])

    st.markdown("How often do you use the following substances?")
    use_responses = {}
    for substance in ["Alcohol", "Marijuana", "Nicotine", "Harder Drugs"]:
        use_responses[substance] = st.radio(
            f"{substance}:", ["Never", "Rarely", "Monthly", "Weekly", "Daily"], horizontal=True
        )

    personality = st.selectbox("I am an...", ["Introvert", "Extrovert"])
    
    relationship = st.selectbox("What kind of relationship do you hope to have with your roommate?", ["Be friends", "Just cohabitate"])
    
    snore = st.selectbox("Do you snore? (Be honest)", ["Yes", "No"])
    sleep_depth = st.slider("How deep of a sleeper are you?", 1, 10, 7)
    
    room_social = st.slider("My room is a social space (1 = not at all, 10 = very social)", 1, 10, 5)
    room_private = st.slider("My room is a private space (1 = not at all, 10 = very private)", 1, 10, 5)
    room_study = st.slider("My room is a study space (1 = not at all, 10 = very academic)", 1, 10, 5)
    
    guests = st.selectbox("What are your guest hosting habits?", 
                          ["I never have guests over", 
                           "I have guests over 1-2 times a week", 
                           "I have guests over 4-5 times a week", 
                           "I have guests over more than 5 times a week"]
                        )
    
    notify_guests = st.selectbox("When having guests over, do you typically inform your roommate beforehand?", 
                                 ["I never have guests over", 
                                  "Only if it's a big gathering", 
                                  "No I don't ask, I assume it's fine because it's my room",
                                  "Yes - I always check first, even if it's just one person"])
    
    conflict = st.selectbox("When conflict arises, what is your first instinct for addressing it?", 
                            ["Address it immediately and directly with the person", 
                             "Wait and see if resolves itself", 
                             "Avoid it unless addressing it is absolutely necessary"])
    
    study_place = st.selectbox("Where do you usually study?", ["In my room", "In the library or anywhere else"])
    shower_freq = st.selectbox("How often do you shower?", ["At least once a day", "Every other day", "A few times a week"]) 
    
    if st.button("Next →"):
        required = [email, year, gender]
        if any(x.strip() == "" for x in required):
            st.warning("Please fill in all required fields.")
        else:
            personal_data = {
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
                "Shower frequency": shower_freq
            }
            for substance, val in use_responses.items():
                personal_data[f"{substance} (use)"] = val

            # temp save responses and move onto the next section
            st.session_state.responses.update(personal_data)
            st.session_state.survey_page = "preferences"

# Page 2: Their Roommate Preferences
if st.session_state.survey_page == "preferences":
    st.header("🤝 Roommate Preferences")
    st.subheader("Questions about what you prefer in a roommate")
    
    preferred_gender = st.selectbox("Preferred roommate gender?", ["Male", "Female", "Nonbinary", "I don't care"])
    
    roommate_clean = st.slider("How clean do you want your roommate to keep the room?", 1, 10, 5)
    
    sleep_importance = st.slider("How important is it to you that your roommate has similar bedtime and wakeup times to you?", 1, 10, 5)

    st.markdown("#### What is the maximum you are okay with in terms of your roommate's usage of the follow substances?")
    st.markdown("##### In other words, more than this amount of usage would be a dealbreaker. \nFor example, if you don't care about your roommate's usage, select 'Daily' for every option.")
    tolerance_responses = {}
    for substance in ["Alcohol", "Marijuana", "Nicotine", "Harder Drugs"]:
        tolerance_responses[substance] = st.radio(
            f"{substance}", ["Never", "Rarely", "Monthly", "Weekly", "Daily"], horizontal=True
        )

    roommate_personality = st.selectbox("I'd prefer if my roommate was an...", ["Introvert", "Extrovert", "No preference"])
    
    cares_snore = st.selectbox("Do you care if your roommate snores? (Be honest)", ["Yes, I care", "No, I don't care"])
    
    roommate_guests = st.selectbox("How often would you prefer your roommate to have guests over?", 
                                   ["I'd prefer if they never had guests over", 
                                    "I'd prefer if they had guests over 1-2 times a week", 
                                    "I'd be okay if they had guests over 4-5 times a week", 
                                    "I'd be okay if they had guests over more than 5 times a week"])
    
    guest_notify = st.selectbox("How would you prefer your roommate inform you about guests coming over?", 
                                ["I'd prefer if they don't have guests over", 
                                 "Only if it's a big gathering", 
                                 "They should inform me even if it's just one person"])
    
    conflict_pref = st.selectbox("What do you prefer your roommate do when there is a conflict?", 
                                 ["Bring it up with you immediately and directly address the issue", 
                                  "Let it settle before discussing", 
                                  "Avoid it completely unless absolutely necessary"])
    
    study_pref = st.selectbox("Where would you prefer your roommate studies?", ["It's okay if they study in the room", "I'd prefer if they studied elsewhere"])
    
    shower_expectation = st.selectbox("How often would you prefer your roommate showered, at the very minimum?", 
                                      ["I don't care how often they shower", "At least once a day", "Every other day", "A few times a week"]) 

    if st.button("Submit My Responses!"):
        roommate_data = {
            "Preferred roommate gender?": preferred_gender,
            "How clean do you want your roommate to keep the room?": roommate_clean,
            "Importance of sleep match": sleep_importance,
            "I'd prefer if my roommate was an...": roommate_personality,
            "Care if roommate snores": cares_snore,
            "Guest frequency (preferred)": roommate_guests,
            "How roommate should notify about guests": guest_notify,
            "Preferred conflict response": conflict_pref,
            "Roommate study location preference": study_pref,
            "Roommate shower minimum": shower_expectation
        }
        for substance, val in tolerance_responses.items():
            roommate_data[f"{substance} (ok with)"] = val

        st.session_state.responses.update(roommate_data)
        collection.insert_one(st.session_state.responses)
        st.success("🎉 Your full survey has been submitted to the database.\n\nYou can now close this tab or return to the home page. Thank you! \n\nBe on the lookout for our matchings (via email)! :)")
        st.session_state.survey_page = "done"
import sqlite3
import pandas as pd
from os import name, path
import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from PIL import Image
import json
import requests  # pip install requests
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    """Simple Login App"""

    st.set_page_config(page_title='Data Analyzer')

    lottie_anime = load_lottieurl(
        "https://assets6.lottiefiles.com/packages/lf20_su8vw1n6.json")

    st_lottie(
        lottie_anime,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        renderer="svg",  # canvas
        height=None,
        width=None,
        key=None,
    )

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                st.header('Hello Synchron\'s Wanna Check your metrics!')
                # Hide the Menu(i.e, Hamburger)
                st.markdown(""" <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """, unsafe_allow_html=True)

                uploaded_file = st.sidebar.file_uploader(
                    label='Upload your Excel File!',
                    type='xlsx')

                if uploaded_file is not None:
                    print("File uploaded Sucessfully!")

                    try:
                        # --- LOAD DATAFRAME

                        df = pd.read_excel(uploaded_file)

                    except Exception as e:
                        print(e)

                try:

                    try:
                        type(df.shape)

                    except Exception as e:
                        print(e)
                        st.write("Please upload your file!")

                    if df['Scheme'][0].split()[0] == 'PMKVY':
                        # Fill nan Values
                        df['Certified'] = df['Certified'].fillna('No')
                        df['Candidate Placed'] = df['Candidate Placed'].fillna(
                            'No')
                        df['Education Level'] = df['Education Level'].fillna(
                            'Uneducated')
                        df.dropna(axis=1, inplace=True)

                        # TO update values accordingly
                        # Updates Duplicated States
                        df.replace(to_replace='ANDHRA PRADESH',
                                   value='Andhra Pradesh', inplace=True)
                        df.replace(to_replace='TELANGANA',
                                   value='Telangana', inplace=True)
                        # Update Similar Education levels
                        df.replace(to_replace=['9th to 10th', 'SSC'],
                                   value='10th Class', inplace=True)
                        df.replace(to_replace=['ITI', '10th Class/I.T.I',
                                               '12th Class/I.T.I'], value='I.T.I', inplace=True)
                        df.replace(to_replace=['Un Educated', 'Other', 'Not Applicable',
                                               'Certificate'], value='Uneducated', inplace=True)
                        df.replace(to_replace=['11th to 12th', '12th Class/Diploma',
                                               'Inter'], value='12th Class', inplace=True)
                        df.replace(to_replace=['B.E./B.Tech', 'B.Tech', 'B.E.', 'B.Pharma',
                                               'B.Sc', 'B.Com'], value='Under Graduate', inplace=True)
                        df.replace(to_replace=['6th Class', '5th Class', '7th Class',
                                               '8th Class'], value='5th to 8th', inplace=True)
                        # Update Similar Gender Duplicates
                        df.replace(to_replace='M', value='Male', inplace=True)
                        df.replace(to_replace='F',
                                   value='Female', inplace=True)
                        # Update Certified Column
                        df.replace(to_replace=['FAIL', 'Not Appeared',
                                               'Dropout'], value='No', inplace=True)
                        df.replace(to_replace=['PASS'],
                                   value='Yes', inplace=True)

                        # Streamlit Selection
                        gender = df['Gender'].unique().tolist()
                        Education = df['Education Level'].unique().tolist()
                        states = df['Centre State'].unique().tolist()
                        center_name = df['Centre Name'].unique().tolist()
                        job_role = df['Job Role'].unique().tolist()
                        scheme = df['Scheme'].unique().tolist()

                        c1, c2 = st.columns(2)
                        # Multiple Gender Selection
                        gender_selection = c1.multiselect('GENDER :',
                                                          gender)  # Set default=gener(if by default all values r needed!)
                        # Multiple Schemes Selection
                        m1 = (df['Gender'].isin(gender_selection))
                        filter_scheme = df[m1]['Scheme'].unique().tolist()
                        # Scheme Selection
                        scheme_selection = c2.multiselect('SCHEME :',
                                                          filter_scheme)

                        c3, c4 = st.columns(2)
                        # Multiple Education Qualifications Selection
                        m2 = (df['Gender'].isin(gender_selection)) & (
                            df['Scheme'].isin(scheme_selection))
                        filter_education = df[m2]['Education Level'].unique(
                        ).tolist()
                        # Education Selection
                        education_selection = c3.multiselect('EDUCATION :',
                                                             filter_education)

                        # Multiple States Selection
                        m3 = (df['Gender'].isin(gender_selection)) & (df['Scheme'].isin(
                            scheme_selection)) & (df['Education Level'].isin(education_selection))
                        states_filter = df[m3]['Centre State'].unique(
                        ).tolist()
                        # States selection
                        states_selection = c4.multiselect('STATE :',
                                                          states_filter)  # Set default=states(if by default all values r needed!)
                        # c5, c6 = st.columns(2)
                        # Multiple Centres Selection
                        m4 = (df['Gender'].isin(gender_selection)) & (df['Scheme'].isin(scheme_selection)) & (
                            df['Education Level'].isin(education_selection)) & (df['Centre State'].isin(states_selection))
                        centre_filter = df[m4]['Centre Name'].unique().tolist()
                        center_name_selection = st.multiselect('CENTER :',  # Use " & (df['Centre Name'].isin(center_name_selection)) " when uncommented
                                                               centre_filter)

                        # Multiple Job roles Selection
                        # job_role_selection = c6.multiselect('JOB ROLE :',         ##  Use " & (df['job Role'].isin(job_role_selection)) " when uncommented
                        # job_role)  # Set default=gener(if by default all values r needed!)

                        # Filter Data Based on User Selection
                        mask = (df['Gender'].isin(gender_selection)) & (df['Education Level'].isin(education_selection)) & (
                            df['Centre State'].isin(states_selection)) & (df['Scheme'].isin(scheme_selection)) & (df['Centre Name'].isin(center_name_selection))

                        number_of_results = df[mask].shape[0]
                        st.markdown(
                            f'*Available Results :{number_of_results}*')

                        # Converting Categorical to Numerical Data
                        # A new column to know How many have enrolled!
                        df['Enrolled'] = 1
                        df.loc[df['Certified'] == "Yes", 'Certified'] = 1
                        df.loc[df['Certified'] == "No", 'Certified'] = 0
                        df.loc[df['Candidate Placed'] ==
                               "Yes", 'Candidate Placed'] = 1
                        df.loc[df['Candidate Placed'] ==
                               "No", 'Candidate Placed'] = 0
                        # Sunburst
                        st.markdown("<h2 style='text-align: left;'> Visualization </h2>",
                                    unsafe_allow_html=True)

                        sun_burst_enrolled = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                         'Centre Name', 'Job Role'], values='Enrolled',
                                                         width=600, height=600)
                        sun_burst_enrolled.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))
                        # sun_burst_enrolled.update_layout(uniformtext=dict(minsize=10,mode='hide'))

                        sun_burst_certified = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                          'Centre Name', 'Job Role'], values='Certified', width=600, height=600)
                        sun_burst_certified.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))
                        sun_burst_certified.update_traces(
                            insidetextorientation='auto')
                        # Get count of no. of people Certified
                        certified = (df[mask]['Certified'] == 1).sum()

                        sun_burst_placed = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                       'Centre Name', 'Job Role'], values='Candidate Placed',  width=600, height=600)
                        sun_burst_placed.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))
                        sun_burst_placed.update_traces(
                            insidetextorientation='auto')
                        # Get count of no. of people Placed
                        placed = (df[mask]['Candidate Placed'] == 1).sum()

                        st.plotly_chart(sun_burst_enrolled)
                        st.markdown(
                            f'*Number of Candidates Enrolled :{number_of_results}*')

                        st.plotly_chart(sun_burst_certified)
                        st.markdown(
                            f'*Number of Candidates Certified :{certified}*')

                        st.plotly_chart(sun_burst_placed)
                        st.markdown(f'*Number of Candidates Placed :{placed}*')

                    else:
                        # Replace Duplicates in GENDER
                        df.replace(to_replace=['F', 'Female '],
                                   value='Female', inplace=True)
                        df.replace(to_replace='M', value='Male', inplace=True)

                        # CLeaning the data by Replacing the Duplicates EDUCATION
                        df.replace(to_replace=['S.S.C Pass', '10th class', 'SSC PASS',
                                               'Intermediate Fail', 'SSC', 'Ssc'], value='10th Class', inplace=True)
                        df.replace(to_replace=['Intermediate Pass', 'Intermediate', 'INTER', 'MPC', 'BIPC', 'Inter', 'H.E.C', 'Inter pass',
                                               'INTER PASS', 'VOCATIONAL', 'OCATIONAL', 'CEC', 'HEC', 'CCP', 'D.El.Ed', 'Ttc', 'CGA', ], value='12th Class', inplace=True)
                        df.replace(to_replace=['Degree', 'BE/B.Tech Pass', 'B.tech', 'Degree Pass', 'B.sc', 'B.SC', 'BSC', 'BiPC', 'B.Tech', 'B.tech Civil', 'B.Sc', 'B.tech EEE', 'BA',
                                               'BCOM', 'B.PHARMACY', 'B.COM', 'B.A', 'B.A.', 'CIVIL ENGG', 'CIVIL', 'AGRICULTURE', 'BZC', 'EEE', 'Degreepass', 'DEGREE'], value='Under Graduate', inplace=True)
                        df.replace(to_replace=['I.T.I', 'Iti'],
                                   value='I.T.I', inplace=True)
                        df.replace(to_replace=['Diploma Civil', 'Diploma'],
                                   value='Diploma', inplace=True)
                        df.replace(to_replace=['PG'], value='Post Graduate')
                        df['Education Level'] = df['Education Level'].fillna(
                            'Uneducated')
                        df.replace(to_replace=['Mba'],
                                   value='Masters', inplace=True)

                        # Cleaning data by replacing the duplicate values in it SCHEME
                        df.replace(to_replace=['DDUGKY 1', 'DDUGKY 2',
                                               'DDUGKY-3'], value='DDUGKY', inplace=True)
                        df['Scheme'] = df['Scheme'].fillna('DDUGKY')

                        # Replacing Duplicates with desired ones! ASSESSED
                        df.replace(
                            to_replace=['Completed', 'YES'], value='Yes', inplace=True)
                        df.replace(to_replace=['Absent', 'NO', 'Pending'],
                                   value='No', inplace=True)
                        df['Assessed'] = df['Assessed'].fillna('No')

                        # Duplicates & Null values CERTIFIED
                    # Duplicates & Null values CERTIFIED
                        df.replace(to_replace=['Passed', 'Pass', 'Not Declared',
                                               'PASS', 'Pending'], value='Yes', inplace=True)
                        df.replace(to_replace=['Failed', 'No', 'Fail', 'ABSENT',
                                               'FAIL', 'Absent'], value='No', inplace=True)
                        df['Certified'] = df['Certified'].fillna('No')

                        # Duplicates & Null values PLACED
                        df.replace(to_replace=['P'], value='Yes', inplace=True)
                        df.replace(to_replace=['NP', 'Drop out', 'NO'],
                                   value='No', inplace=True)
                        df['Candidate Placed'] = df['Candidate Placed'].fillna(
                            'No')

                        # Converting Categorical to Numerical Data to get the values count while plotting the data
                        # A new column to know How many have enrolled!
                        df['Enrolled'] = 1
                        df.loc[df['Assessed'] == "Yes", 'Assessed'] = 1
                        df.loc[df['Assessed'] == "No", 'Assessed'] = 0
                        df.loc[df['Certified'] == "Yes", 'Certified'] = 1
                        df.loc[df['Certified'] == "No", 'Certified'] = 0
                        df.loc[df['Candidate Placed'] ==
                               "Yes", 'Candidate Placed'] = 1
                        df.loc[df['Candidate Placed'] ==
                               "No", 'Candidate Placed'] = 0

                        # For P1, P2 & P3 ,to know have they stayed for 1, 2 or 3 months
                        df.loc[df['P1'] == "Yes", 'P1'] = 1
                        df.loc[df['P1'] == "No", 'P1'] = 0
                        df.loc[df['P2'] == "Yes", 'P2'] = 1
                        df.loc[df['P2'] == "No", 'P2'] = 0
                        df.loc[df['P3'] == "Yes", 'P3'] = 1
                        df.loc[df['P3'] == "No", 'P3'] = 0

                        # Converting String values to Numeric for analysis

                        df.replace(to_replace=['6500 + food and accommodation',
                                               '7000/-'], value=7000, inplace=True)
                        df.replace(to_replace=['7000 + food and accommodation', '7500/-', '7000.00 + ACCOMMODATION AND FOOD',
                                               '7000 + FOOD AND ACCOMMODATION', '-'], value=7500, inplace=True)
                        df.replace(to_replace=['9500 + food and accommodation', '10000/-',
                                               '9229 + Food and Accomodation', '₹ 9,831', '₹ 9,223', '₹ 10,520'], value=10000, inplace=True)
                        df.replace(to_replace='7770/-',
                                   value=7700, inplace=True)
                        df.replace(to_replace='6000/- + Incentives',
                                   value=6500, inplace=True)
                        df.replace(to_replace='10979/-',
                                   value=10979, inplace=True)
                        df.replace(to_replace='8270/-',
                                   value=8270, inplace=True)
                        df.replace(to_replace=['8000/-', '7500.00 + ACCOMMODATION AND FOOD', '7000.00 + INCENTIVES and ACCOMMODATION AND FOOD',
                                               '7500 + FOOD AND ACCOMMODATION', '7900/-', '7992/-', '₹ 8,167'], value=8000, inplace=True)
                        df.replace(to_replace='10500/-',
                                   value=10500, inplace=True)
                        df.replace(to_replace=['8500/- + Incentives', '8500.00 + ACCOMMODATION AND FOOD', '9194/-',
                                               '9000/-', '8900/-', '9060/-', '9229/-', '₹ 8,752', 9170.8], value=9000, inplace=True)
                        df.replace(to_replace='8241/- + Incentives',
                                   value=8800, inplace=True)
                        df.replace(
                            to_replace=['9500/-', '9362/-'], value=9500, inplace=True)
                        df.replace(to_replace='6000/-',
                                   value=6000, inplace=True)
                        df.replace(to_replace='7721/-',
                                   value=7721, inplace=True)
                        df.replace(to_replace=[
                            '12000/-', 'Rs 11268.00 and ACCOMMODATION', '11490/-'], value=12000, inplace=True)
                        df.replace(to_replace='13000/-',
                                   value=13000, inplace=True)
                        df.replace(to_replace=['Rs 8000.00 and Food & Accomodation', '8000.00 + Incentives', 'Rs. 8000.00 + FOOD AND ACCOMMODATION',
                                               '8500/-', '₹ 8,459', '8000.00 + FOOD AND ACCOMMODATION'], value=8500, inplace=True)
                        df.replace(to_replace='Rs 11,000.00 and Food & Accomodation',
                                   value=11500, inplace=True)
                        df.replace(to_replace='Rs 8500.00 and Food & Accomodation',
                                   value=9000, inplace=True)
                        df.replace(to_replace=['11000/-', '11067/-', '₹ 10,400',
                                               '₹ 11,059', '₹ 10,589', '₹ 10,730'], value=11000, inplace=True)
                        df.replace(to_replace='15000/-',
                                   value=15000, inplace=True)
                        df.replace(to_replace='16000/-',
                                   value=16000, inplace=True)
                        df.replace(to_replace='19000/-',
                                   value=19000, inplace=True)
                        df.replace(to_replace=['₹ 4,791', '₹ 5,157',
                                               '₹ 5,192'], value=5000, inplace=True)
                        df.replace(
                            to_replace=['₹ 1,696', '₹ 2,634'], value=2000, inplace=True)

                        # Fill null values with mean of salary
                        df['Salary'] = (df['Salary'].fillna(
                            df['Salary'].mean()).round(0))

                        # Fill all the rest null values in P1,P2 & P3 with 0(as NO)
                        df.fillna(0, inplace=True)

                        # STREAMLIT USAGE
                        gender = df['Gender'].unique().tolist()
                        Education = df['Education Level'].unique().tolist()
                        states = df['Centre State'].unique().tolist()
                        center_name = df['Centre Name'].unique().tolist()
                        job_role = df['Job Role'].unique().tolist()
                        scheme = df['Scheme'].unique().tolist()

                        c1, c2 = st.columns(2)
                        # Multiple Gender Selection
                        gender_selection = c1.multiselect('GENDER :',
                                                          gender)  # Set default=gener(if by default all values r needed!)
                        # Multiple Schemes Selection
                        m1 = (df['Gender'].isin(gender_selection))
                        filter_scheme = df[m1]['Scheme'].unique().tolist()
                        # Scheme Selection
                        scheme_selection = c2.multiselect('SCHEME :',
                                                          filter_scheme)

                        c3, c4 = st.columns(2)
                        # Multiple Education Qualifications Selection
                        m2 = (df['Gender'].isin(gender_selection)) & (
                            df['Scheme'].isin(scheme_selection))
                        filter_education = df[m2]['Education Level'].unique(
                        ).tolist()
                        # Education Selection
                        education_selection = c3.multiselect('EDUCATION :',
                                                             filter_education)

                        # Multiple States Selection
                        m3 = (df['Gender'].isin(gender_selection)) & (df['Scheme'].isin(
                            scheme_selection)) & (df['Education Level'].isin(education_selection))
                        states_filter = df[m3]['Centre State'].unique(
                        ).tolist()
                        # States selection
                        states_selection = c4.multiselect('STATE :',
                                                          states_filter)  # Set default=states(if by default all values r needed!)
                        # c5, c6 = st.columns(2)
                        # Multiple Centres Selection
                        m4 = (df['Gender'].isin(gender_selection)) & (df['Scheme'].isin(scheme_selection)) & (
                            df['Education Level'].isin(education_selection)) & (df['Centre State'].isin(states_selection))
                        centre_filter = df[m4]['Centre Name'].unique().tolist()
                        center_name_selection = st.multiselect('CENTER :',  # Use " & (df['Centre Name'].isin(center_name_selection)) " when uncommented
                                                               centre_filter)

                        # Filter Data Based on User Selection
                        mask = (df['Gender'].isin(gender_selection)) & (df['Education Level'].isin(education_selection)) & (
                            df['Centre State'].isin(states_selection)) & (df['Scheme'].isin(scheme_selection)) & (df['Centre Name'].isin(center_name_selection))

                        number_of_results = df[mask].shape[0]
                        st.markdown(
                            f'*Available Results :{number_of_results}*')
                        st.markdown("<h2 style='text-align: left;'> Visualization </h2>",
                                    unsafe_allow_html=True)

                        sun_burst_enrolled = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                         'Centre Name', 'Job Role'], values='Enrolled',
                                                         width=600, height=600)
                        sun_burst_enrolled.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))
                        # sun_burst_enrolled.update_layout(uniformtext=dict(minsize=10,mode='hide'))

                        sun_burst_certified = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                          'Centre Name', 'Job Role'], values='Certified', width=600, height=600)
                        sun_burst_certified.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))

                        # Get count of no. of people Certified
                        certified = (df[mask]['Certified'] == 1).sum()

                        sun_burst_placed = px.sunburst(df[mask], path=['Gender', 'Education Level', 'Centre State',
                                                                       'Centre Name', 'Job Role'], values='Candidate Placed',  width=600, height=600)
                        sun_burst_placed.update_layout(margin=dict(
                            t=0, b=0, l=0, r=0))

                        # Get count of no. of people Placed
                        placed = (df[mask]['Candidate Placed'] == 1).sum()

                        # Get highest salaries in P1,p2 & p3
                        p1 = (df[mask].loc[df['P1'] == 1, 'Salary'])
                        p2 = (df[mask].loc[df['P2'] == 1, 'Salary'])
                        p3 = (df[mask].loc[df['P3'] == 1, 'Salary'])

                        st.plotly_chart(sun_burst_enrolled)
                        st.markdown(
                            f'*Number of Candidates Enrolled :{number_of_results}*')

                        st.plotly_chart(sun_burst_certified)
                        st.markdown(
                            f'*Number of Candidates Certified :{certified}*')

                        st.plotly_chart(sun_burst_placed)
                        st.markdown(f'*Number of Candidates Placed :{placed}*')
                        st.markdown(
                            f'*Highest Salary in 1st Month :{max(p1)}*')
                        st.markdown(
                            f'*Highest Salary in 2nd Month :{max(p2)}*')
                        st.markdown(
                            f'*Highest Salary in 3rd Month :{max(p3)}*')
                        st.markdown(
                            f'*Average Salary in 1st Month :{round(p1.mean(),0)}*')
                        st.markdown(
                            f'*Average Salary in 2nd Month :{round(p2.mean(),0)}*')
                        st.markdown(
                            f'*Average Salary in 3rd Month :{round(p3.mean(),0)}*')

                except Exception as e:
                    print(e)

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()

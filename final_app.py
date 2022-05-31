import sqlite3
import pandas as pd
from os import name, path
import os
import datetime
import random
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

    st.set_page_config(page_title='Data Analyzer', layout='wide')

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

                        # Fill nan Values
                    df['Certified'] = df['Certified'].fillna('No')
                    df['Candidate Placed'] = df['Candidate Placed'].fillna(
                        'No')

                    # TO update values accordingly

                    # Duplicates & Null values CERTIFIED
                    df.replace(to_replace=['Passed', 'Pass', 'Not Declared',
                                           'PASS', 'Pending'], value='Yes', inplace=True)
                    df.replace(to_replace=['Failed', 'No', 'Fail', 'ABSENT',
                                           'FAIL', 'Absent'], value='No', inplace=True)
                    #Yes_No_vars = ['Yes', 'No']
                    df['Certified'] = df['Certified'].fillna('Yes')

                    # Duplicates & Null values PLACED
                    df.replace(to_replace=['P', 'YES'],
                               value='Yes', inplace=True)
                    df.replace(to_replace=['NP', 'Drop out', 'NO', 'ONGOING'],
                               value='No', inplace=True)
                    df['Candidate Placed'] = df['Candidate Placed'].fillna(
                        'No')

                    # Cleaning data by replacing the duplicate values in it SCHEME
                    df.replace(to_replace=['DDUGKY 1', 'DDUGKY 2',
                                           'DDUGKY-3'], value='DDUGKY', inplace=True)
                    df['Scheme'] = df['Scheme'].fillna('DDUGKY')

                    # Updating States column
                    df.replace(to_replace='ANDHRA PRADESH',
                               value='Andhra Pradesh', inplace=True)
                    df.replace(to_replace='TELANGANA',
                               value='Telangana', inplace=True)

                    # Updating Certified Column
                    df.replace(to_replace=['FAIL', 'Not Appeared',
                                           'Dropout'], value='No', inplace=True)
                    df.replace(to_replace=['PASS'],
                               value='Yes', inplace=True)

                    # Updating Year Column
                    df_arr = []
                    for val in df['Year']:
                        if type(val) == str:
                            if val[4] == '-':
                                df_arr.append(int(val.split('-')[0]))
                            elif val[2] == '/':
                                df_arr.append(int(val.split('/')[2]))

                        elif type(val) == datetime.datetime:
                            df_arr.append(val.timetuple().tm_year)

                    df['Year'] = df_arr

                    # Get Salaries, Tp1,.. based on if placed, as its dummy data
                    df['Salary'] = df['Candidate Placed']
                    df['TP1'] = df['Candidate Placed']
                    df['TP2'] = df['Candidate Placed']
                    df['TP3'] = df['Candidate Placed']

                    df['Salary'].replace(
                        to_replace='Yes', value=8000, inplace=True)

                    # Get True/ False values at P1, P2& P3 based on If salary was given!
                    df['TP1'][df['Centre State'] ==
                              'Andhra Pradesh'] = df['Salary'].notna()
                    df['TP2'][df['Centre State'] ==
                              'Andhra Pradesh'] = df['Salary'].notna()
                    df['TP3'][df['Centre State'] ==
                              'Andhra Pradesh'] = df['Salary'].notna()

                    # Fill null values
                    df['TP1'] = df['TP1'].fillna('No')
                    df['TP2'] = df['TP2'].fillna('No')
                    df['TP3'] = df['TP3'].fillna('No')

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

                    # Converting Categorical to Numerical Data to get the values count while plotting the data
                    # A new column to know How many have enrolled!
                    df['Enrolled'] = 1
                    df.loc[df['Certified'] == "Yes", 'Certified'] = 1
                    df.loc[df['Certified'] == "No", 'Certified'] = 0
                    df.loc[df['Candidate Placed'] ==
                           "Yes", 'Candidate Placed'] = 1
                    df.loc[df['Candidate Placed'] ==
                           "No", 'Candidate Placed'] = 0

                    # For P1, P2 & P3 ,to know have they stayed for 1, 2 or 3 months
                    df.loc[df['TP1'] == "Yes", 'TP1'] = 1
                    df.loc[df['TP1'] == "No", 'TP1'] = 0
                    df.loc[df['TP2'] == "Yes", 'TP2'] = 1
                    df.loc[df['TP2'] == "No", 'TP2'] = 0
                    df.loc[df['TP3'] == "Yes", 'TP3'] = 1
                    df.loc[df['TP3'] == "No", 'TP3'] = 0

                    # Similarly, if true, then salary was given!
                    df.loc[df['TP1'] == True, 'TP1'] = 1
                    df.loc[df['TP1'] == False, 'TP1'] = 0
                    df.loc[df['TP2'] == True, 'TP2'] = 1
                    df.loc[df['TP2'] == False, 'TP2'] = 0
                    df.loc[df['TP3'] == True, 'TP3'] = 1
                    df.loc[df['TP3'] == False, 'TP3'] = 0

                    # Streamlit Selection
                    states = df['Centre State'].unique().tolist()
                    center_name = df['Centre Name'].unique().tolist()
                    job_role = df['Job Role'].unique().tolist()
                    scheme = df['Scheme'].unique().tolist()
                    year = df['Year'].unique().tolist()

                    # Year slider
                    year_selection = st.slider('YEAR:',
                                               min_value=min(year),
                                               max_value=max(year),
                                               value=(min(year), max(year)))
                    c1, c2 = st.columns(2)
                    scheme_selection = c1.multiselect(
                        'SCHEME :', scheme, default=scheme)

                    # Multiple States Selection
                    m1 = (df['Scheme'].isin(scheme_selection)) & (
                        df['Year'].isin(year_selection))
                    states_filter = df[m1]['Centre State'].unique(
                    ).tolist()
                    # States selection
                    states_selection = c2.multiselect('STATE :',
                                                      states_filter)  # Set default=states(if by default all values r needed!)
                    # c5, c6 = st.columns(2)
                    # Multiple Centres Selection
                    m2 = (df['Scheme'].isin(scheme_selection)) & (df['Year'].isin(year_selection)) & (
                        df['Centre State'].isin(states_selection))
                    centre_filter = df[m2]['Centre Name'].unique().tolist()
                    center_name_selection = st.multiselect('CENTER :',  # Use " & (df['Centre Name'].isin(center_name_selection)) " when uncommented
                                                           centre_filter)

                    # Filter Data Based on User Selection
                    mask = (df['Scheme'].isin(scheme_selection)) & (df['Year'].isin(year_selection)) & (df['Centre State'].isin(
                        states_selection)) & (df['Centre Name'].isin(center_name_selection))

                    # Filter Data Based on User Selection
                    mask = (df['Scheme'].isin(scheme_selection)) & (df['Year'].isin(year_selection)) & (df['Centre State'].isin(
                        states_selection)) & (df['Centre Name'].isin(center_name_selection))

                    number_of_results = df[mask].shape[0]
                    st.markdown(
                        f'*Available Results :{number_of_results}*')
                    st.markdown("<h1 style='text-align: center; '> Visualization </h1>",
                                unsafe_allow_html=True)

                    sun_burst_enrolled = px.sunburst(df[mask], path=['Centre State',
                                                                     'Centre Name', 'Job Role'], values='Enrolled', color_discrete_sequence=px.colors.qualitative.Set3, width=500, height=500)
                    sun_burst_enrolled.update_layout(margin=dict(
                        t=0, b=0, l=0, r=0))
                    # sun_burst_enrolled.update_layout(uniformtext=dict(minsize=10,mode='hide'))

                    sun_burst_certified = px.sunburst(df[mask], path=['Centre State',
                                                                      'Centre Name', 'Job Role'], values='Certified', color_discrete_sequence=px.colors.qualitative.Set2, width=500, height=500)
                    sun_burst_certified.update_layout(margin=dict(
                        t=0, b=0, l=0, r=0))

                    line_colors = [
                        "#7CEA9C", '#50B2C0', "rgb(114, 78, 145)", "hsv(348, 66%, 90%)", "hsl(45, 93%, 58%)"]
                    # Get count of no. of people Certified
                    certified = (df[mask]['Certified'] == 1).sum()

                    sun_burst_placed = px.sunburst(df[mask], path=['Centre State',
                                                                   'Centre Name', 'Job Role'], values='Candidate Placed', color_discrete_sequence=line_colors, width=500, height=500)
                    sun_burst_placed.update_layout(margin=dict(
                        t=20, b=0, l=0, r=0))

                    # Get count of no. of people Placed
                    placed = (df[mask]['Candidate Placed'] == 1).sum()

                    # Get corresponding salaries in P1,p2 & p3
                    p1 = (df[mask].loc[df['TP1'] == 1, 'Salary'])
                    p2 = (df[mask].loc[df['TP2'] == 1, 'Salary'])
                    p3 = (df[mask].loc[df['TP3'] == 1, 'Salary'])

                    c11, c12 = st.columns(2)

                    c11.plotly_chart(sun_burst_enrolled,
                                     use_container_width=True)
                    c11.markdown(
                        f'*Number of Candidates Enrolled :{number_of_results}*')

                    c12.plotly_chart(sun_burst_certified,
                                     use_container_width=True)
                    c12.markdown(
                        f'*Number of Candidates Certified :{certified}*')

                    s11, s12 = st.columns(2)
                    s11.plotly_chart(sun_burst_placed,
                                     use_container_width=True)
                    s11.markdown(
                        f'*Number of Candidates Placed :{placed}*')

                    fig = go.Figure()
                    Months = ['TP1', 'TP2', 'TP3']
                    # To drop null values while plotting salaries plot
                    df1 = df[mask].dropna()
                    df1 = df[mask].drop(
                        df.loc[df['Salary'] == 'No'].index)
                    for month in Months:
                        fig.add_trace(go.Violin(y=df1.loc[df1[month] == 1, 'Salary'],
                                                name=month,
                                                box_visible=True,
                                                meanline_visible=True))
                        fig.update_layout(
                            yaxis_title="Salaries")
                        fig.update_layout(margin=dict(
                            t=20, b=0, l=0, r=0))

                    s12.markdown("<h4 style='text-align: center;'> 3 MONTHS SALARIES VISUALIZATION </h4>",
                                 unsafe_allow_html=True)
                    s12.plotly_chart(fig, use_container_width=True)

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

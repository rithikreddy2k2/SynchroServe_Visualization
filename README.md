# SynchroServe_Visualization
### A visualization App, when uploaded chunks of data (i.e., datasets), shows the metrics (such as enrolled, placed & certified), based on the parameters chosen (such as centres, states & schemes), so that comparision can be made among centres to know how good they are performing.
### Firstly, Data-Analytics has been done (for 2 schemes available (i.e., PMKVY & DDUGKY)) to find the trends in the data & make neccesary changes (say handling null values, removing duplicacies & converting categorical data to target data (0's & 1's)) using Python & a dataset (i.e., FINAL_DATA.xlsx) has been made out of it, after all neccesary changes have been made.
### Finally, deployed the app using streamlit & added user-authentication with sqlite3 database!
### Here are some of the snapshots of how it works!
## Login-Page:
![image](https://user-images.githubusercontent.com/66252916/179464723-61789984-caea-4bf1-b440-f33d6c1925f9.png)
## After Uploading Data-set:
![image](https://user-images.githubusercontent.com/66252916/179465686-a7ccaa12-e425-4a96-bd4f-e6ac223f9767.png)
## After choosing the required (say year-range, states, schemes & centres):
![image](https://user-images.githubusercontent.com/66252916/179466892-37720577-bb2f-492b-8234-d0e9f9ea861a.png)
## Visualization:
![image](https://user-images.githubusercontent.com/66252916/179466614-ab55cb85-3635-4aea-9fbc-8a8343fa4319.png)
![image](https://user-images.githubusercontent.com/66252916/179466781-404ee74a-2c52-4cf0-91ad-7a8b1d8c526d.png)
## In-depth (To know indepth details about a centre or state, we can either hover to see data or click on it to see in more specifically (say Job roles)):
### Click (When clicked on Andhra-Pradesh, all info about its centres & its corresponding Job-Roles are shown):
![image](https://user-images.githubusercontent.com/66252916/179467747-c2c2f2b7-2d31-4465-b76b-b2c617df2f64.png)
### Hover (when hovered on Hand-Embroidery Job-Role, all required Details (say, placed & its parent) are being shown):
![image](https://user-images.githubusercontent.com/66252916/179467888-26956258-81bd-4a46-87d5-21d18b533eb1.png)



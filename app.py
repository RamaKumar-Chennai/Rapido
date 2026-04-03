import streamlit as st
import pandas as pd
from eda import eda_ride_vol_by_hour
from eda import eda_ride_vol_by_weeekday
from eda import eda_ride_vol_by_city
from eda import cancellation_heatmap
from eda import  distance_fare_corr
from eda import rating_distbn
from eda import traffic_weather_cancellation
from models import fare_pred_model


st.title("🚖 Rapido: Intelligent Mobility Insights ")

@st.cache_data
def load_data1():
  bookings_df=pd.read_csv(r"D:\VS_CODE\Rapido\drive-download-20260323T152350Z-3-001\cleaned_csv_files\bookings.csv")
  return bookings_df
bookings_df=load_data1()

@st.cache_data
def load_data2():
  location_demand_df=pd.read_csv(r"D:\VS_CODE\Rapido\drive-download-20260323T152350Z-3-001\cleaned_csv_files\location_demand.csv")
  return location_demand_df
location_demand_df=load_data2()

@st.cache_data
def load_data3():
  customers_df=pd.read_csv(r"D:\VS_CODE\Rapido\drive-download-20260323T152350Z-3-001\cleaned_csv_files\customers.csv")
  return customers_df
customers_df=load_data3()

@st.cache_data
def load_data4():
  drivers_df=pd.read_csv(r"D:\VS_CODE\Rapido\drive-download-20260323T152350Z-3-001\cleaned_csv_files\drivers.csv")
  return drivers_df
drivers_df=load_data4()



main_menu_choice=st.sidebar.radio("Enter your choice here",["Home","Exploratory Data Analysis","Prediction Models"],index=None)
if main_menu_choice=="Home":               

  st.markdown("""

### 📊 Ride Patterns • ❌ Cancellations • 💰 Fare Forecasting  

---

### 🔍 Overview  
Gain actionable insights into urban mobility trends by analyzing ride data, cancellation behavior, and fare dynamics.  

### 🚀 Key Focus Areas  
- 🛣️ **Ride Patterns**: Track demand hotspots and peak hours  
- ❌ **Cancellations**: Identify risk factors and reduce drop-offs  
- 💰 **Fare Forecasting**: Predict pricing trends for better decision-making  

---

### 📈 Why It Matters  
Efficient mobility insights empower smarter operations, improve customer satisfaction, and optimize revenue streams.
""")
  

  
elif main_menu_choice=="Exploratory Data Analysis":
  eda_choice=st.sidebar.radio("Enter your choice here",["Ride volume by hour, weekday, city","Cancellation heatmap across cities","Distance vs Fare correlation","Rating distribution-Customer vs Driver behaviour comparison","Traffic/Weather vs Cancellation"],index=None)
  if eda_choice=="Ride volume by hour, weekday, city":
    ride_vol_choice=st.radio("Enter your choice here",["Ride volume by hour","Ride volume by Weekday","Ride volume by City"],index=None)
    if ride_vol_choice=="Ride volume by hour":
      fig,df=eda_ride_vol_by_hour(bookings_df)
      st.success("Ride Volume by Hour of the Day")
      st.write(df)
      st.pyplot(fig)
    elif ride_vol_choice=="Ride volume by Weekday":
       fig,df=eda_ride_vol_by_weeekday(bookings_df)
       st.success("Ride Volume by Day of the Week")
       st.write(df)
       st.pyplot(fig)

    elif ride_vol_choice=="Ride volume by City":
        fig,df=eda_ride_vol_by_city(bookings_df)
        st.success("Ride Volume by City")
        st.write(df)
        st.pyplot(fig)

  if eda_choice=="Cancellation heatmap across cities":
    fig=cancellation_heatmap(location_demand_df)
    st.plotly_chart(fig)
  
  if eda_choice=="Distance vs Fare correlation":
    fig=distance_fare_corr(bookings_df)
    st.pyplot(fig)
    st.info(""" 
For short trips: fare is almost proportional to distance, very predictable.

For long trips: fare depends on distance plus other conditions (traffic, demand, booking category, etc.), so the model needs to account for those""")
  if eda_choice=="Rating distribution-Customer vs Driver behaviour comparison":
    fig1,fig2=rating_distbn(customers_df,drivers_df)
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.info("Statistical summary of Customer Rating")
    st.write(customers_df['avg_customer_rating'].describe())
    st.info("Statistical summary of Driver Rating")
    st.write(drivers_df['avg_driver_rating'].describe())

  if eda_choice=="Traffic/Weather vs Cancellation":

    fig=traffic_weather_cancellation(bookings_df)
    st.pyplot(fig)

if main_menu_choice=="Prediction Models":
  pred_choice=st.sidebar.radio("Enter your choice here",["Ride Outcome Prediction (Multi-Class Classification)","Fare Prediction Model (Regression)","Customer Cancellation Risk Model (Binary Classification)","Driver Delay Prediction Model (Binary Classification)"],index=None)
  if pred_choice=="Ride Outcome Prediction (Multi-Class Classification)":
    pass
  elif pred_choice=="Fare Prediction Model (Regression)":
    st.info("Enter the following details")
    pred_val=fare_pred_model(bookings_df)
    
    if pred_val:
     st.success(f"The predicted booking value for the above booking details in INR :{pred_val}")
  elif pred_choice=="Customer Cancellation Risk Model (Binary Classification)":
    pass
  elif pred_choice=="Driver Delay Prediction Model (Binary Classification)":
    pass
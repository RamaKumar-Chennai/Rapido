import streamlit as st
import pandas as pd
import datetime
import pickle
def fare_pred_model(bookings_df):
    
   ride_dt= st.date_input("Enter the date here")
   ride_time=st.time_input("Enter the time here")
   
   unique_pickup_loc=bookings_df['pickup_location'].unique()
   pickup_loc=st.selectbox("Enter your pickup location here",unique_pickup_loc,index=None)

   unique_drop_loc=bookings_df['drop_location'].unique()
   drop_loc=st.selectbox("Enter your drop location here",unique_drop_loc,index=None)

   ride_distance=st.text_input("Enter the ride distance in km here")
   estimated_ride_time=st.text_input("Enter the estimated ride time in mins here")
    
   unique_traffic_level=bookings_df['traffic_level'].unique()
   traffic_level=st.selectbox("Enter the traffic level here",unique_traffic_level,index=None)
   base_fare=st.text_input("Enter the base fare here")
   surge_multiplier=st.text_input("Enter the surge multiplier here")

   unique_city=bookings_df['city'].unique()
   city=st.selectbox("Enter your city here",unique_city,index=None)

   unique_vehicle_type=bookings_df['vehicle_type'].unique()
   vehicle_type=st.selectbox("Enter your vehicle_type here",unique_vehicle_type,index=None)

   unique_weather=bookings_df['weather_condition'].unique()
   weather=st.selectbox("Enter the weather condition here",unique_weather,index=None)


   fare_per_km=st.text_input("Enter the fare per km here")
   fare_per_min=st.text_input("Enter the fare per min here")

   click_button=st.button("Click this button to see your ride fare and book your ride")

   if click_button:
    ride_dt_time=datetime.datetime.combine(ride_dt,ride_time)
    ride_dt_time=pd.to_datetime(ride_dt_time)
   
    
    ride_day_name=ride_dt_time.day_name()
    ride_day_name=ride_day_name.lower()
    map={'sunday':0,'monday':1,'tuesday':2,'wednesday':3,'thursday':4,'friday':5,'saturday':6}
    ride_day_number=map[ride_day_name]
    ride_time=ride_dt_time.hour
    print("day number is ",ride_day_number)
    print("week day name is ",ride_day_name)
    is_weekend_flag=1.0 if ride_day_name in ["saturday","sunday"] else 0.0
    
    ride_time=float(ride_time)
    print("hour of the day is ",ride_time)
    print("is weekend",is_weekend_flag)
    if base_fare:
      base_fare=float(base_fare)
    if surge_multiplier:
      surge_multiplier=float(surge_multiplier)
    if fare_per_km:
      fare_per_km=float(fare_per_km)
    if fare_per_min:
      fare_per_min=float(fare_per_min)
    if estimated_ride_time:
      estimated_ride_time=float(estimated_ride_time)


    if (ride_time >=8.0) & (ride_time<=10.0) | (ride_time >=17.0) & (ride_time<=20.0) :

      rush_hour_flag=1.0
    else:
      rush_hour_flag=0.0

    if ride_distance:
      ride_distance=float(ride_distance)
      if ride_distance>15:
        long_distance_flag=1.0
      else:
        long_distance_flag=0.0
    if estimated_ride_time:
      estimated_ride_time=float(estimated_ride_time)
    
    if city:
     if city=="Bangalore":
      city_Bangalore=1.0
      city_Chennai=0.0
      city_Delhi=0.0
      city_Hyderabad=0.0
      city_Mumbai=0.0
     elif city=="Chennai":
      city_Bangalore=0.0
      city_Chennai=1.0
      city_Delhi=0.0
      city_Hyderabad=0.0
      city_Mumbai=0.0
     elif city=="Delhi":
      city_Bangalore=0.0
      city_Chennai=0.0
      city_Delhi=1.0
      city_Hyderabad=0.0
      city_Mumbai=0.0
     elif city=="Hyderabad":
      city_Bangalore=0.0
      city_Chennai=0.0
      city_Delhi=0.0
      city_Hyderabad=1.0
      city_Mumbai=0.0
     elif city=="Mumbai":
      city_Bangalore=0.0
      city_Chennai=0.0
      city_Delhi=0.0
      city_Hyderabad=0.0
      city_Mumbai=1.0

    
    if vehicle_type:
      if vehicle_type=="Auto":
        vehicle_type_Auto=1.0
        vehicle_type_Bike=0.0
        vehicle_type_Cab=0.0
      elif vehicle_type=="Bike":
        vehicle_type_Auto=0.0
        vehicle_type_Bike=1.0
        vehicle_type_Cab=0.0
      elif vehicle_type=="Cab":
        vehicle_type_Auto=0.0
        vehicle_type_Bike=0.0
        vehicle_type_Cab=1.0
   
    if weather:
     if weather=="Clear":
       weather_condition_Clear=1.0
       weather_condition_Heavy_Rain=0.0
       weather_condition_Rain=0.0
     elif weather=="Heavy Rain":
       weather_condition_Clear=0.0
       weather_condition_Heavy_Rain=1.0
       weather_condition_Rain=0.0
     elif weather=="Rain":
       weather_condition_Clear=0.0
       weather_condition_Heavy_Rain=0.0
       weather_condition_Rain=1.0


    if pickup_loc:
       pickup_loc=str(pickup_loc).replace("Loc_","")
       pickup_loc=float(pickup_loc)
    if drop_loc:
       drop_loc=str(drop_loc).replace("Loc_","")
       drop_loc=float(drop_loc)
    if traffic_level:
      if traffic_level=="Low":
        traffic_level=0.0
      elif traffic_level=="Medium":
        traffic_level=1.0
      elif traffic_level=="High":
        traffic_level=2.0

    input_features= [[ride_day_number,is_weekend_flag,ride_time,pickup_loc,drop_loc,ride_distance,estimated_ride_time,traffic_level,base_fare,surge_multiplier,fare_per_km,fare_per_min,rush_hour_flag,long_distance_flag,city_Bangalore, city_Chennai, city_Delhi, city_Hyderabad,
       city_Mumbai, vehicle_type_Auto, vehicle_type_Bike,
       vehicle_type_Cab, weather_condition_Clear,
       weather_condition_Heavy_Rain, weather_condition_Rain]]
    print("the input features are /n",input_features)
    
    filename = "RF_model.pkl"

    # Load the model
    with open(filename, "rb") as file:
       rf_model = pickle.load(file)

    # check the type to confirm
    print("the type of rf model is /n")
    print(type(rf_model))

    # Now you can use it for predictions
    y_pred = rf_model.predict(input_features)
    y_pred=round(y_pred[0],2)
    print("Predictions:", y_pred)  
    return y_pred



     
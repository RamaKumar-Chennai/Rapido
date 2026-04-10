
import pandas as pd
import mysql
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np


#create SQL connection object
def create_connection():
 from mysql.connector import Error
 
 try:
   connection=mysql.connector.connect(host="localhost",username="root",password="root",database="rapido")
   if connection.is_connected():
    print("Successfully connected to MYSQL")
    return connection
 except Error as err:
    print(f"Error code in connecting with MYSQL server :{err} ")
    return None
  
#FETCH THE RECORDS FOR THE QUERY
def res_fn(connection,query):
     #This function is to fetch the results from the query
     import pandas as pd
     cursor=connection.cursor()
     # Execute a SELECT statement

     cursor.execute(query)
     # Fetch all results from the executed query
     results=cursor.fetchall()
     
     #COPY THE RESULTS TO A DATAFRAME

     df=pd.DataFrame(results,columns=[i[0] for i in cursor.description])        
     cursor.close()
     return df

def res_scalar_fn(connection,query):
    #This function is to fetch the results from the query
     import pandas as pd
     cursor=connection.cursor()
     # Execute a SELECT statement

     cursor.execute(query)
     # Fetch all results from the executed query
     results=cursor.fetchall()
     
          
     cursor.close()
     return results


def eda_ride_vol_by_hour(bookings_df):
    connection=create_connection()
    query="""select hour_of_day,count(hour_of_day) as ride_volume_by_hour from rapido.bookings_df_cleaned 
             group by hour_of_day
             order by count(hour_of_day) desc """
    df=res_fn(connection,query)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=df,
        x="hour_of_day",
        y="ride_volume_by_hour",
        color="blue"
        
    )
    ax.set_title("Ride Volume  By Hour of Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Ride Volume")
    ax.set_ylim(df["ride_volume_by_hour"].min() * 0.95,df["ride_volume_by_hour"].max() * 1.05)

    
    return fig,df


def  eda_ride_vol_by_weeekday(bookings_df):
    connection=create_connection()
    query="""select day_of_week,count(day_of_week) as ride_volume_by_day from rapido.bookings_df_cleaned 
             group by day_of_week
             order by count(day_of_week) desc """
    df=res_fn(connection,query)
    day_order_lst=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    ordered_df=df.set_index("day_of_week").loc[day_order_lst].reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=ordered_df,
        x="day_of_week",
        y="ride_volume_by_day",
        color="blue"
        
    )
    ax.set_title("Ride Volume  By Day of Week")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Ride Volume")
    ax.set_ylim(df["ride_volume_by_day"].min() * 0.95,df["ride_volume_by_day"].max() * 1.05)

    
    return fig,df


def  eda_ride_vol_by_city(bookings_df):
    connection=create_connection()
    query="""select city,count(city) as ride_volume_by_city from rapido.bookings_df_cleaned 
             group by city
             order by count(city) desc """
    df=res_fn(connection,query)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=df,
        x="city",
        y="ride_volume_by_city",
        color="blue"
        
    )
    ax.set_title("Ride Volume  By City")
    ax.set_xlabel("City")
    ax.set_ylabel("Ride Volume")
    ax.set_ylim(df["ride_volume_by_city"].min() * 0.95,df["ride_volume_by_city"].max() * 1.05)

    
    return fig,df

def cancellation_heatmap(location_demand_df):
  heatmap_df=location_demand_df.groupby('city').agg(Total_count=('city','size'),Cancelled_Rides_count=('cancelled_rides','sum'))
  heatmap_df['Cancellation_rate']=round(heatmap_df['Cancelled_Rides_count'] /heatmap_df['Total_count'],3)

  city_coords={
     "Bangalore": (12.9716, 77.5946),
     'Delhi': (28.7041, 77.1025),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867)
        }
  heatmap_df['Latitude']=heatmap_df.index.map(lambda x: city_coords[x][0])
  heatmap_df['Longitude']=heatmap_df.index.map(lambda x: city_coords[x][1])
  heatmap_df = heatmap_df.reset_index()

  print("heat map df is /n",heatmap_df)

  fig = px.scatter_mapbox(
    heatmap_df,
    lat="Latitude",
    lon="Longitude",
    color="Cancellation_rate",
    size="Cancellation_rate",
    size_max=30,
    hover_name="city",   # use column, not index
    mapbox_style="carto-positron",
    title="Cancellation Heatmap Across Cities",
    zoom=4

)
  
  fig.update_layout(
    width=3500,   # increase width
    height=1000    # increase height
)
 
  return fig


def distance_fare_corr(bookings_df):
   corr_df=bookings_df[['ride_distance_km','booking_value']]
   corr_df['ride_distance_km']=pd.to_numeric(corr_df['ride_distance_km'],errors="coerce") 
   corr_df['booking_value']=pd.to_numeric(corr_df['booking_value'],errors="coerce") 

   # Drop rows with NaN to avoid regplot failing silently
   corr_df = corr_df.dropna(subset=['ride_distance_km','booking_value'])

   fig,ax=plt.subplots(figsize=(8,6))
   sns.regplot(data=corr_df,x='ride_distance_km',y='booking_value',scatter_kws={'alpha':0.4}, line_kws={'color':'red','linewidth':2})
   plt.title("Distance vs Fare correlation")
   plt.xlabel("Distance")
   plt.ylabel("Booking Value")
   
   return fig

def rating_distbn(customers_df_cleaned,drivers_df_cleaned):
   
   fig1,ax=plt.subplots(1,2,figsize=(8,6))
   sns.histplot(data=customers_df_cleaned,x='avg_customer_rating',ax=ax[0],bins=12,kde=True)
   ax[0].set_title("Customer Rating Distribution")
   sns.histplot(data=drivers_df_cleaned,x='avg_driver_rating',ax=ax[1],bins=10,kde=True)
   ax[1].set_title("Driver Rating Distribution")
   fig1.suptitle("Rating Distribution of Customers and Drivers")
   plt.tight_layout()

   fig2,ax=plt.subplots(figsize=(8,6))
   sns.boxplot(data=[customers_df_cleaned['avg_customer_rating'],drivers_df_cleaned['avg_driver_rating']])
   plt.xticks([0,1],["Customers","Drivers"])
   plt.title("Customer vs Driver Rating Behaviour")
   
   return fig1,fig2

def traffic_weather_cancellation(bookings_df):
   
   # Filter only cancelled bookings
   cancelled_df = bookings_df[bookings_df['booking_status'] == 'Cancelled']
   
   cancel_counts = cancelled_df.groupby(['weather_condition', 'traffic_level']).size().unstack(fill_value=0)
   print("cancel_counts is \n ",cancel_counts)
   fig,ax=plt.subplots(figsize=(10,6))
   sns.heatmap(cancel_counts, annot=True, fmt='d', cmap='Reds', linewidths=0.5)
   plt.title("Cancellation Counts by Traffic and Weather")
   plt.xlabel("Traffic Level")
   plt.ylabel("Weather Condition")
   
   return fig


def peak_cancellation_windows(bookings_df):
   bookings_cancel_df=bookings_df[bookings_df['booking_status']=='Cancelled']
   bookings_cancel_df_unstack=bookings_cancel_df.groupby(['day_of_week','hour_of_day']).size().unstack(fill_value=0)
   print(bookings_cancel_df_unstack)
  

   #  Define proper weekday order
   weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

   #  Reindex rows to match this order
   bookings_cancel_df_unstack = bookings_cancel_df_unstack.reindex(weekday_order)

   # Plot heatmap
   fig,ax=plt.subplots(figsize=(20,12))
   sns.heatmap(bookings_cancel_df_unstack, cmap="Reds", annot=True, fmt="d")
   plt.title("Rapido Ride Cancellations by Hour and Day of Week")
   plt.ylabel("Day of Week")
   plt.xlabel("Hour of Day")
   return fig

def high_risk_rides(bookings_df):

 # --- STEP 0: Create binary cancelled flag ---
 bookings_df['cancelled_flag'] = bookings_df['booking_status'].apply(
    lambda x: 1 if str(x).lower() == 'cancelled' else 0
)

 # --- STEP 1: Customer & Driver cancellation rates ---
 cust_stats = bookings_df.groupby('customer_id')['cancelled_flag'].agg(['sum','count']).reset_index()
 cust_stats['cust_cancel_rate'] = cust_stats['sum'] / cust_stats['count']
 cust_stats = cust_stats[['customer_id','cust_cancel_rate']]

 driver_stats = bookings_df.groupby('driver_id')['cancelled_flag'].agg(['sum','count']).reset_index()
 driver_stats['driver_cancel_rate'] = driver_stats['sum'] / driver_stats['count']
 driver_stats = driver_stats[['driver_id','driver_cancel_rate']]

 bookings_df = bookings_df.merge(cust_stats, on='customer_id', how='left')
 bookings_df = bookings_df.merge(driver_stats, on='driver_id', how='left')

 # --- STEP 2: Time-based clustering ---
 # Convert booking_time strings to datetime and extract hour
 bookings_df['booking_time_dt'] = pd.to_datetime(bookings_df['booking_time'], errors='coerce')
 bookings_df['hour'] = bookings_df['booking_time_dt'].dt.hour

 def time_risk(hour):
    if pd.isna(hour):
        return 0.0
    if 7 <= hour <= 9 or 17 <= hour <= 20:   # rush hours
        return 0.4
    elif hour >= 22 or hour <= 5:            # late night
        return 0.5
    else:
        return 0.1

 bookings_df['time_risk'] = bookings_df['hour'].apply(time_risk)

 # --- STEP 3: Location-based risk factors (pickup_location instead of pickup_zone) ---
 zone_stats = bookings_df.groupby('pickup_location')['cancelled_flag'].agg(['sum','count']).reset_index()
 zone_stats['cancel_rate'] = zone_stats['sum'] / zone_stats['count']
 zone_stats = zone_stats[['pickup_location','cancel_rate']]

 hotspots = zone_stats.loc[zone_stats['cancel_rate'] > 0.3, 'pickup_location']
 bookings_df = bookings_df.merge(zone_stats, on='pickup_location', how='left')

 bookings_df['location_risk'] = bookings_df['pickup_location'].apply(
    lambda z: 0.5 if z in hotspots.values else 0.1
)

 # --- STEP 4: Composite Risk Score ---
 alpha, beta, gamma, delta = 0.4, 0.4, 0.1, 0.1

 bookings_df['risk_score'] = (
    alpha * bookings_df['cust_cancel_rate'] +
    beta * bookings_df['driver_cancel_rate'] +
    gamma * bookings_df['time_risk'] +
    delta * bookings_df['location_risk']
)

 # --- STEP 5: Flag high-risk bookings ---
 bookings_df['risk_flag'] = np.where(bookings_df['risk_score'] > 0.5, 'High', 'Low')

 print(bookings_df[['booking_id','cust_cancel_rate','driver_cancel_rate',
                   'time_risk','location_risk','risk_score','risk_flag']].head())

 res_df = bookings_df[['booking_id','cust_cancel_rate','driver_cancel_rate',
                      'time_risk','location_risk','risk_score','risk_flag']]
 res_df=res_df[res_df['risk_flag'] =='High']
 res_df=res_df.reset_index(drop=True)
 return res_df

def driver_allocation_strategy(drivers_df):
  return drivers_df[drivers_df['reliability_score']>0.78]

def pickup_drop_city_heatmaps(bookings_df):

 # Create a pickup vs drop matrix
 matrix = bookings_df.groupby(['pickup_location','drop_location']).size().unstack(fill_value=0)

 fig,ax=plt.subplots(figsize=(12,8))
 sns.heatmap(matrix, cmap="Reds", linewidths=0.5)
 plt.title("Pickup vs Drop Location Heatmap")
 return fig





def cancellations_by_hour(bookings_df):
    # Filter cancelled rides
    cancel_df = bookings_df[bookings_df['booking_status'] == 'Cancelled']
    
    # Group by hour_of_day and count
    res_df = cancel_df.groupby('hour_of_day').size().reset_index(name='Cancellation_count').sort_values('Cancellation_count',ascending=False)
    
    # Rename the grouping column
    res_df.rename(columns={'hour_of_day': 'Hour_of_Day'}, inplace=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=res_df,
        x="Hour_of_Day",
        y='Cancellation_count',
        color="blue"
        
    )
    ax.set_title("Cancellation Hours")
    ax.set_xlabel("Hour_of_Day")
    ax.set_ylabel("Cancellation_count")
    #ax.set_ylim(df["ride_volume_by_city"].min() * 0.95,df["ride_volume_by_city"].max() * 1.05)

    
    return fig,res_df

def surge_behaviour(bookings_df):
  booking_hour_df= bookings_df.groupby('hour_of_day')['booking_id'].count().reset_index()
  booking_hour_df.columns=["Hour_of_Day","Booking_count"]

  base_line=booking_hour_df["Booking_count"].mean()

  # Add as a new column with a descriptive name
  booking_hour_df['Average_hourly_bookings'] = base_line

  # Flag surge hours
  
  booking_hour_df['Surge_Flag'] = np.where(
     booking_hour_df['Booking_count'] > base_line, 'Surge', 'Normal'
)

  print(booking_hour_df.head())
  surge_df=booking_hour_df[booking_hour_df['Surge_Flag']=='Surge']


  fig, ax = plt.subplots(figsize=(8, 6))
  sns.barplot(
        data=surge_df,
        x="Hour_of_Day",
        y='Booking_count',
        color="blue"
        
    )
  ax.set_title("Surge Hours")
  ax.set_xlabel("Hour_of_Day")
  ax.set_ylabel("Booking_count")
  ax.set_ylim(surge_df["Booking_count"].min() * 0.95,surge_df["Booking_count"].max() * 1.05)
  

  return fig,booking_hour_df

def cancellation_reasons(bookings_df):
   reasons_df=bookings_df.groupby('incomplete_ride_reason').size().reset_index()
   reasons_df.columns=["Incomplete_ride_reason","Count"]
   reasons_df.sort_values("Count",ascending=False,inplace=True)
   return reasons_df

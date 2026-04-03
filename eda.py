
import pandas as pd
import mysql
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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


def  eda_ride_vol_by_hour(bookings_df):
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

   fig,ax=plt.subplots(figsize=(8,6))
   sns.regplot(data=corr_df,x='ride_distance_km',y='booking_value',scatter_kws={'alpha':0.4}, line_kws={'color':'red','linewidth':2})
   plt.title("Distance vs Fare correlation")
   plt.xlabel("Distance")
   plt.ylabel("Booking Value")
   
   return fig

def rating_distbn(customers_df_cleaned,drivers_df_cleaned):
   #rating_df=
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


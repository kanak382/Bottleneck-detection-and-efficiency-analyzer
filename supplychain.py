import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st   

st.title("Supply Chain Bottleneck & Efficiency Analyzer")

df = pd.read_csv("Supply_chain_dataset.csv")

# Show raw data 
st.subheader("SUPPLY CHAIN DATA")
st.dataframe(df)

st.sidebar.header("Select Visualizations")
delivery_time = st.sidebar.checkbox("delivery_time",value=True )
deliverydelay_trend = st.sidebar.checkbox("deliverydelay_trend", value=True )
demand_seasonality = st.sidebar.checkbox("demand_seasonality" , value=True )
heatmap_delayed_routes = st.sidebar.checkbox("heatmap_delayed_routes" ,value=True)
bottleneck_trend_pattern = st.sidebar.checkbox("bottleneck_trend_pattern" , value=True )


# Delivery Delay Bars
if delivery_time :
 st.subheader("Delivery Time")
 plt.figure(figsize=(8,5))
 sns.histplot(df['delivery_time_days'], bins=10)
 plt.title("Delivery Time Distribution")
 plt.xlabel("Delivery Time (Days)")
 plt.ylabel("Number of Orders")
 st.pyplot(plt)

# Supply Chain Delay Trend Line
if deliverydelay_trend :
 st.subheader("Delivery delay Trend (Monthly)")
 monthly_delay = df.groupby('temporal_month')['delivery_time_days'].mean()
 plt.figure(figsize=(9,5))
 plt.plot(monthly_delay.index, monthly_delay.values, marker='o')
 plt.title("Average Delivery Time Trend (Monthly)")
 plt.xlabel("Month")
 plt.ylabel("Avg Delivery Time (Days)")
 st.pyplot(plt)

# Delivery Delay Percentage

df['delay_percentage'] = (1 - df['on_time_delivery_rate']) * 100

st.metric(label="Average Delivery Delay Percentage",value=f"{round(df['delay_percentage'].mean(), 2)} %" )

# Demand Seasonality Graph
if demand_seasonality :
 st.subheader("Demand Seasonality Pattern")
 seasonality = df.groupby('temporal_month')['seasonality_index'].mean()
 plt.figure(figsize=(9,5))
 plt.plot(seasonality.index, seasonality.values, marker='o')
 plt.title("Demand Seasonality Pattern")
 plt.xlabel("Month")
 plt.ylabel("Seasonality Index")
 st.pyplot(plt)

# Heatmap for Delayed Routes
if heatmap_delayed_routes :
 st.subheader("Heatmap for delayed routes")
 route_delay = ( df.groupby('delivery_mode')['delivery_time_days'].mean())
 st.write(route_delay)   
 route_delay = route_delay.to_frame()
 plt.figure(figsize=(7,4))
 sns.heatmap(route_delay, cmap="Reds")
 plt.title("Average Delivery Time by Delivery Mode")
 st.pyplot(plt)

# Bottleneck Detection

st.subheader("Potential Bottleneck Delivery Modes")
bottlenecks = df.groupby('delivery_mode')['lead_time_variance'].mean()
bottlenecks = bottlenecks.sort_values(ascending=False)
st.write(bottlenecks)


# Bottleneck Trend Pattern
if bottleneck_trend_pattern :
 st.subheader("Bottleneck Trend Using Lead Time Variance")
 bottleneck_trend = df.groupby('temporal_month')['lead_time_variance'].mean()
 plt.figure(figsize=(9,5))
 plt.plot(bottleneck_trend.index, bottleneck_trend.values, marker='o')
 plt.title("Bottleneck Trend Using Lead Time Variance")
 plt.xlabel("Month")
 plt.ylabel("Avg Lead Time Variance")
 st.pyplot(plt)


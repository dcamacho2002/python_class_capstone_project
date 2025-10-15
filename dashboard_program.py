import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect("baseball_history.db")

eventsdf = pd.read_sql_query("SELECT * FROM Events", conn)
statsdf = pd.read_sql_query("SELECT * FROM Stats", conn)

data = pd.merge(eventsdf, statsdf, on="Year")

st.title("MLB Historical Stats (1901 - 1905)")
st.write("Explore player statistics and events in MLB history")

st.sidebar.header("Filter Options")
selectYear = st.sidebar.selectbox("Select Year", sorted(data["Year"].unique()))
selectEvent = st.sidebar.selectbox("Select Event", sorted(data["Event"].unique()))

filtered = data[(data["Year"] == selectYear) & (data["Event"] == selectEvent)]

st.subheader(f"Statistics for {selectEvent} in {selectYear}")
st.dataframe(filtered)

st.subheader("Number of Events per Year")
count = eventsdf.groupby("Year").count()["Event"].reset_index()

first = px.bar(count, x = "Year", y = "Event", labels = {"Event": "Number of Events"}, title = "Events per Year")
st.plotly_chart(first)

st.subheader("Top 10 Most Frequent Statistics")
top = statsdf["Statistic"].value_counts().head(10).reset_index()
top.columns = ["Statistic", "Count"]

second = px.bar(top, x = "Count", y = "Statistic", orientation = "h", title = "Top 10 Statistics", text = "Count")
st.plotly_chart(second)

st.subheader("Statistics Count Over Years")
range = st.slider("Select Year Range", int(data["Year"].min()), int(data["Year"].max()), (1901, 1903))
rangeData = data[(data["Year"] >= range[0]) & (data["Year"] <= range[1])]
counts = rangeData.groupby("Year")["Statistic"].count().reset_index()

fig3 = px.line(counts, x="Year", y="Statistic", markers=True,
               title="Number of Statistics by Year")
st.plotly_chart(fig3)
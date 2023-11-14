import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
from typing import Iterable
import matplotlib.pyplot as plt

# @st.cache_data
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")

st.title("Netflix Data Dashboard")
st.write(
    "Explorator Data Analysis on the netflix dataset. Showing important information about latest movies on Netflix"
)
df = pd.read_csv("./netflix_movies.csv")


def untangleData(data: Iterable):
    counted_data: dict[str, int] = {}
    for row in data:
        if type(row) == str:
            split_data = row.split(",")
            split_data = map(lambda x: x.strip(), split_data)
            for datum in split_data:
                if datum in counted_data:
                    counted_data[datum] += 1
                else:
                    counted_data[datum] = 1
    return counted_data


def word_clouder():
    st.header("Word Cloud of Data")
    wc_column = st.selectbox(
        "Choose column for world cloud", ["title", "description"], 0
    )
    # Your text data
    text = " ".join(df[wc_column])
    bc = "#0e1117"
    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color=bc).generate(
        text
    )
    # Display the generated word cloud using matplotlib
    fig, ax = plt.subplots()
    # fig.set_size_inches()
    ax.axis("off")
    ax.imshow(wordcloud, interpolation="bilinear")
    fig.set_facecolor(bc)
    st.pyplot(fig)


def filter_by_countries():
    st.header("Filter by Countries")
    untangled_country = untangleData(df["country"])
    unique_countries = untangled_country.keys()
    countries = st.multiselect(
        "Choose countries",
        list(unique_countries),
        ["India", "United States"],
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.dropna()[
            df["country"].dropna().str.contains("|".join(countries), case=False)
        ]
        st.write("### Netflix data based on countries", data.sort_index())
        diplay_data = filter(
            lambda x: True if x[0] in countries else False, untangled_country.items()
        )
        chart = (
            alt.Chart(pd.DataFrame(diplay_data, columns=["country", "count"]))
            .mark_bar(opacity=0.3)
            .encode(x="country", y=alt.Y("count:Q", stack=None), color="country:N")
        ).properties(
            title="Chart of Movies done the following countries "
            + ", ".join(countries),
            height=600,
        )
        st.altair_chart(chart, use_container_width=True)


def filter_by_genre():
    st.header("Filter by Genre")
    untangled_genre = untangleData(df["listed_in"])
    unique_genre = untangled_genre.keys()
    genre = st.multiselect(
        "Choose Genre",
        list(unique_genre),
        ["Comedies", "Action & Adventure"],
    )
    if not genre:
        st.error("Please select at least one Genre.")
    else:
        data = df.dropna()[
            df["listed_in"].dropna().str.contains("|".join(genre), case=False)
        ]
        st.write("### Netflix data based on genre", data.sort_index())
        diplay_data = filter(
            lambda x: True if x[0] in genre else False, untangled_genre.items()
        )
        chart = (
            alt.Chart(pd.DataFrame(diplay_data, columns=["genre", "count"]))
            .mark_bar(opacity=0.3)
            .encode(x="genre", y=alt.Y("count:Q", stack=None), color="genre:N")
        ).properties(
            title="Chart of Movies by genre " + ", ".join(genre),
            height=600,
        )
        st.altair_chart(chart, use_container_width=True)


word_clouder()
filter_by_countries()
filter_by_genre()

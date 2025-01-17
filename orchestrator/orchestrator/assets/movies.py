from dagster_snowflake import SnowflakeResource
from dagster import asset, AssetExecutionContext
from ..partitions import monthly_partition

import os
import pandas as pd
import matplotlib.pyplot as plt


@asset(
        deps=['dlt_mongodb_comments', 'dlt_mongodb_embedded_movies']
)
def user_engagement(snowflake: SnowflakeResource) -> None:
    query = """
    select 
        movies.title, 
        movies.year as year_released,
        count(*) as number_of_comments
    from comments comments
    join embedded_movies movies on comments.movie_id = movies._id
    group by movies.title, movies.year
    order by number_of_comments desc
    """
    with snowflake.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        eng_df = cursor.fetch_pandas_all()

    eng_df.to_csv("data/movies_engagement.csv", index=False)

@asset(
        deps=['dlt_mongodb_embedded_movies'],
        partitions_def=monthly_partition
)
def top_movies_by_month(context: AssetExecutionContext, snowflake: SnowflakeResource) -> None:
    partition_date = context.partition_key
    query = f"""
    select 
        movies.title,
        movies.released,
        movies.imdb__rating,
        movies.imdb__votes,
        genres.value as genres
    from EMBEDDED_MOVIES movies
    join EMBEDDED_MOVIES__GENRES genres on movies._dlt_id = genres._dlt_parent_id
    where released >= '{partition_date}'::date
    and released < '{partition_date}'::date + interval '1 month'
    """
    with snowflake.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        movies_df = cursor.fetch_pandas_all()
    
    movies_df = movies_df.loc[movies_df.groupby('GENRES')['IMDB__RATING'].idxmax().dropna()]

    movies_df['partition_date'] = partition_date

    try:
        exist = pd.read_csv("data/top_movies_by_month.csv")
        exist = exist.loc[exist['partition_date'] != partition_date]
        exist = pd.concat([exist, movies_df]).sort_values(by="partition_date")
        exist.to_csv("data/top_movies_by_month.csv", index=False)
    except FileNotFoundError:
        movies_df.to_csv("data/top_movies_by_month.csv", index=False)

@asset(
        deps=['user_engagement']
)
def top_movies_by_engagement(snowflake: SnowflakeResource) -> None:
    movie_engagement = pd.read_csv("data/movies_engagement.csv")
    top_10_movies = movie_engagement.sort_values(by='NUMBER_OF_COMMENTS', ascending=False).head(10)

    plt.figure(figsize=(10, 8))

    bars = plt.barh(top_10_movies['TITLE'], top_10_movies['NUMBER_OF_COMMENTS'], color='blue')

    for bar, year in zip(bars, top_10_movies['YEAR_RELEASED'].astype(int)):
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f"{year}",
                 va='center', ha='left', color='black')
        
    plt.xlabel('Number of Comments')
    plt.ylabel('Movie Title')
    plt.title('Top 10 Movies by Comments')
    plt.gca().invert_yaxis()
    plt.savefig("data/top_movies_by_engagement.png")
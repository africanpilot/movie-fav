-- schema.sql

-- CREATE DATABASE dev_secure_postgresql_movie;
\c dev_secure_postgresql_movie;

CREATE TABLE IF NOT EXISTS movie_imdb_info(
    movie_imdb_info_id SERIAL PRIMARY KEY,
    movie_imdb_info_imdb_id VARCHAR(100),
    movie_imdb_info_title VARCHAR(500),
    movie_imdb_info_cast JSON[],
    movie_imdb_info_year INTEGER,
    movie_imdb_info_directors TEXT[],
    movie_imdb_info_genres TEXT[],
    movie_imdb_info_countries TEXT[],
    movie_imdb_info_plot TEXT,
    movie_imdb_info_cover TEXT,
    movie_imdb_info_episode_start INTEGER,
    movie_imdb_info_episode_end INTEGER,
    movie_imdb_info_rating_imdb Float,
    movie_imdb_info_type VARCHAR(50),
    movie_imdb_info_popular_id INTEGER
);
CREATE SEQUENCE IF NOT EXISTS movie_imdb_info_sequence start 1 increment 1;

CREATE TABLE IF NOT EXISTS movie_fav_info(
    movie_fav_info_id SERIAL PRIMARY KEY,
    movie_fav_info_imdb_info_id int references movie_imdb_info(movie_imdb_info_id),
	movie_fav_info_user_id int,
    movie_fav_info_imdb_id VARCHAR(100),
    movie_fav_info_status VARCHAR(50),
    movie_fav_info_episode_current VARCHAR(50),
    movie_fav_info_rating_user Float
);
CREATE SEQUENCE IF NOT EXISTS movie_fav_info_sequence start 1 increment 1;

CREATE TABLE IF NOT EXISTS movie_archive(
    movie_fav_info_id int,
    movie_fav_info_imdb_info_id int,
	movie_fav_info_user_id int,
    movie_fav_info_imdb_id VARCHAR(100),
    movie_fav_info_status VARCHAR(50),
    movie_fav_info_episode_current VARCHAR(50),
    movie_fav_info_rating_user Float
);
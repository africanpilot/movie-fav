-- 001: Redis branch migrations
ALTER TABLE movie_imdb_info ADD COLUMN IF NOT EXISTS "movie_imdb_info_popular_id" INTEGER DEFAULT NULL;

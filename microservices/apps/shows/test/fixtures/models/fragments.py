from link_test.fixtures import GENERAL_RESPONSE_FRAGMENT, PAGE_INFO_FRAGMENT
from ariadne import gql


SHOWS_EPISODE_FRAGMENT = gql("""
  fragment ShowsEpisode on ShowsEpisode {
    id
    shows_info_id
    shows_season_id
    imdb_id
    title
    rating
    votes
    release_date
    plot
    year
    season
    episode
  }
""")

SHOWS_SEASON_FRAGMENT = gql("""
  fragment ShowsSeason on ShowsSeason {
    id
    shows_info_id
    season
    total_episodes
    release_date
    shows_episode{...ShowsEpisode}
  }
""" + SHOWS_EPISODE_FRAGMENT)

SHOWS_INFO_FRAGMENT = gql("""
  fragment ShowsInfo on ShowsInfo {
    id
    imdb_id
    title
    cast
    year
    directors
    genres
    countries
    plot
    cover
    rating
    votes
    run_times
    series_years
    creators
    full_cover
    popular_id
    release_date
    trailer_link
    added_count
    provider
    total_seasons
    total_episodes
    shows_season{...ShowsSeason}
  }
""" + SHOWS_SEASON_FRAGMENT)


SHOWS_EPISODE_RESPONSE_FRAGMENT = gql("""
  fragment ShowsEpisodeResponse on ShowsEpisodeResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...ShowsEpisode}
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT + SHOWS_EPISODE_FRAGMENT)


SHOWS_RESPONSE_FRAGMENT = gql("""
  fragment ShowsInfoResponse on ShowsInfoResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...ShowsInfo}
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT + SHOWS_INFO_FRAGMENT)


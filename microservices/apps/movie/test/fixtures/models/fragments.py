from link_test.fixtures import GENERAL_RESPONSE_FRAGMENT, PAGE_INFO_FRAGMENT
from ariadne import gql


MOVIE_INFO_FRAGMENT = gql("""
  fragment MovieInfo on MovieInfo {
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
    creators
    full_cover
    popular_id
    release_date
    trailer_link
    added_count
  }
""")


MOVIE_INFO_RESPONSE_FRAGMENT = gql("""
  fragment MovieInfoResponse on MovieInfoResponse {
    response{...GeneralResponse}
    pageInfo{...PageInfo}
    result{...MovieInfo}
  }
""" + GENERAL_RESPONSE_FRAGMENT + PAGE_INFO_FRAGMENT + MOVIE_INFO_FRAGMENT)

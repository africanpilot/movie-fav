import { gql } from "@apollo/client";

export const  ACCOUNT_CREATE_MUTATION = gql`
    mutation accountCreate(
        $login: String!
        $password: String!
        $reTypePassword: String!
    ){
        accountCreate(
            accountCreateInput: { 
                login: $login, 
                password: $password,
                reTypePassword: $reTypePassword
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                account_info_id
                account_info_email
            }
        }
    }
`;

export const ACCOUNT_RESEND_CONFIRM_MUTATION = gql`
    mutation accountResendConfirm(
        $login: String!
    ){
        accountResendConfirm(
            accountLogin: $login
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                account_info_id
                account_info_email
            }
        }
    }
`;

export const ACCOUNT_CONFIRM_EMAIL_MUTATION = gql`
    mutation accountConfirmEmail{
        accountConfirmEmail{
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                account_info_id
                account_info_email
            }
        }
    }
`;

export const ACCOUNT_AUTHENTICATION_LOGIN_MUTATION = gql`
    mutation accountAuthenticationLogin(
        $login: String!
        $password: String!
    ){
        accountAuthenticationLogin(
            accountLoginInput: { 
                login: $login, 
                password: $password,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                authenticationToken
                authenticationTokenType
                registrationStatus
                accountInfo{
                    account_info_id
                    account_info_email
                }
            }
        }
    }
`;

export const ACCOUNT_FORGOT_PASSWORD_MUTATION = gql`
    mutation accountForgotPassword(
        $login: String!
    ){
        accountForgotPassword(
            accountLogin: $login, 
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                authenticationToken
                authenticationTokenType
                registrationStatus
                accountInfo{
                    account_info_id
                    account_info_email
                }
            }
        }
    }
`;

export const ACCOUNT_FORGOT_PASSWORD_CONFIRM_EMAIL_MUTATION = gql`
    mutation accountForgotPasswordConfirmEmail{
        accountForgotPasswordConfirmEmail{
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                authenticationToken
                authenticationTokenType
                registrationStatus
                accountInfo{
                    account_info_id
                    account_info_email
                }
            }
        }
    }
`;

export const  ACCOUNT_MODIFY_PASSWORD_MUTATION = gql`
    mutation accountModify(
        $password: String
        $passwordRetype: String
    ){
        accountModify(
            accountModifyInput: { 
                account_info_password: $password,
                account_info_password_retype: $passwordRetype,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                account_info_id
                account_info_email
            }
        }
    }
`;

export const  MOVIE_POPULAR_QUERY = gql`
    query moviePopular(
        $first: Int
    ){
        moviePopular(
            pageInfo: { 
                first: $first,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_imdb_info_imdb_id
                movie_imdb_info_title
                movie_imdb_info_cast{
                    name
                    image
                }
                movie_imdb_info_genres
                movie_imdb_info_plot
                movie_imdb_info_cover
                movie_imdb_info_user_added
            }
        }
    }
`;

export const  MOVIE_CREATE_QUICK_ADD_MUTATION = gql`
    mutation movieCreate(
        $imdbId: String!
    ){
        movieCreate(
            movieInput: { 
                movie_fav_info_imdb_id: $imdbId,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_fav_info_id
            }
        }
    }
`;

export const  MOVIE_CREATE_MUTATION = gql`
    mutation movieCreate(
        $movie_fav_info_imdb_id: String!
        $movie_fav_info_episode_current: String
        $movie_fav_info_status: MovieStatusEnum
        $movie_fav_info_rating_user: Float
    ){
        movieCreate(
            movieInput: { 
                movie_fav_info_imdb_id: $movie_fav_info_imdb_id,
                movie_fav_info_episode_current: $movie_fav_info_episode_current,
                movie_fav_info_status: $movie_fav_info_status,
                movie_fav_info_rating_user: $movie_fav_info_rating_user,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_fav_info_id
                movie_fav_info_imdb_id
                movie_fav_info_status
                movie_fav_info_episode_current
                movie_fav_info_rating_user
            }
        }
    }
`;

export const  MOVIE_FAV_QUERY = gql`
    query movieFav(
        $first: Int
    ){
        movieFav(
            pageInfo: { 
                first: $first,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_fav_info_id
                movie_fav_info_imdb_id
                movie_fav_info_status
                movie_fav_info_episode_current
                movie_fav_info_rating_user
                movie_search_info{
                    movie_imdb_info_imdb_id
                    movie_imdb_info_title
                    movie_imdb_info_cast{
                        name
                        image
                    }
                    movie_imdb_info_genres
                    movie_imdb_info_plot
                    movie_imdb_info_cover
                }
            }
        }
    }
`;

export const  MOVIE_MODIFY_MUTATION = gql`
    mutation movieModify(
        $infoId: ID!
        $episode: String
        $movieStatus: MovieStatusEnum
        $rating: Float
    ){
        movieModify(
            movieInput: { 
                movie_fav_info_id: $infoId,
                movie_fav_info_episode_current: $episode,
                movie_fav_info_status: $movieStatus,
                movie_fav_info_rating_user: $rating
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_fav_info_id
                movie_fav_info_imdb_id
                movie_fav_info_status
                movie_fav_info_episode_current
                movie_fav_info_rating_user
            }
        }
    }
`;

export const  MOVIE_SEARCH_DETAIL_QUERY = gql`
    query movieSearch(
        $search_type: MovieSearchTypeEnum!
        $search_value: String!
    ){
        movieSearch(
            filterInput: { 
                search_type: $search_type,
                search_value: $search_value,
            }
        ){
            response{
                success
                code
                message
                version
            }
            pageInfo{
                page_info_count
            }
            result{
                movie_imdb_info_imdb_id
                movie_imdb_info_title
                movie_imdb_info_cast{
                    name
                    image
                }
                movie_imdb_info_genres
                movie_imdb_info_plot
                movie_imdb_info_cover
                movie_imdb_info_user_added
                movie_fav_info {
                    movie_fav_info_id
                    movie_fav_info_imdb_id
                    movie_fav_info_status
                    movie_fav_info_episode_current
                    movie_fav_info_rating_user
                }
            }
        }
    }
`;
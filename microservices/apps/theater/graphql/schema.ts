import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
const defaultOptions = {} as const;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type AccountAuthentication = {
  __typename?: 'AccountAuthentication';
  account_info?: Maybe<Array<Maybe<AccountInfo>>>;
  authenticationToken?: Maybe<Scalars['String']>;
  authenticationTokenType?: Maybe<AuthenticationTokenTypeEnum>;
  registrationStatus?: Maybe<AccountRegistrationEnum>;
};

export type AccountAuthenticationResponse = {
  __typename?: 'AccountAuthenticationResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<AccountAuthentication>;
};

export enum AccountBusinessTypeEnum {
  Corporation = 'CORPORATION',
  Llc = 'LLC',
  NonProfit = 'NON_PROFIT',
  PartnershipsLpAndLlp = 'PARTNERSHIPS_LP_AND_LLP',
  PubliclyTradedCorporation = 'PUBLICLY_TRADED_CORPORATION',
  SoleProprietary = 'SOLE_PROPRIETARY',
  Trust = 'TRUST',
  UnincorporatedAssociation = 'UNINCORPORATED_ASSOCIATION'
}

export enum AccountClassificationEnum {
  NonProfit = 'NON_PROFIT',
  Other = 'OTHER',
  Retail = 'RETAIL'
}

export type AccountCompany = {
  __typename?: 'AccountCompany';
  account_store?: Maybe<Array<Maybe<AccountStore>>>;
  address?: Maybe<Scalars['String']>;
  business_type?: Maybe<AccountBusinessTypeEnum>;
  city?: Maybe<Scalars['String']>;
  classification?: Maybe<AccountClassificationEnum>;
  cover_image?: Maybe<Scalars['String']>;
  dba?: Maybe<Scalars['String']>;
  ein?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  logo?: Maybe<Scalars['String']>;
  name?: Maybe<Scalars['String']>;
  phone_number?: Maybe<Scalars['String']>;
  product_description?: Maybe<Scalars['String']>;
  profile_thumbnail?: Maybe<Scalars['String']>;
  registration_date?: Maybe<Scalars['String']>;
  sole_address?: Maybe<Scalars['String']>;
  sole_birthday?: Maybe<Scalars['String']>;
  sole_city?: Maybe<Scalars['String']>;
  sole_email?: Maybe<Scalars['String']>;
  sole_first_name?: Maybe<Scalars['String']>;
  sole_job_title?: Maybe<Scalars['String']>;
  sole_last_name?: Maybe<Scalars['String']>;
  sole_phone_number?: Maybe<Scalars['String']>;
  sole_ssn?: Maybe<Scalars['String']>;
  sole_state?: Maybe<Scalars['String']>;
  sole_zip_code?: Maybe<Scalars['Int']>;
  state?: Maybe<Scalars['String']>;
  status?: Maybe<AccountStatusEnum>;
  website?: Maybe<Scalars['String']>;
  zip_code?: Maybe<Scalars['Int']>;
};

export type AccountCompanyCreateInput = {
  account_store?: InputMaybe<AccountStoreCreateInput>;
  address?: InputMaybe<Scalars['String']>;
  business_type?: InputMaybe<AccountBusinessTypeEnum>;
  city?: InputMaybe<Scalars['String']>;
  classification?: InputMaybe<AccountClassificationEnum>;
  cover_image?: InputMaybe<Scalars['String']>;
  dba?: InputMaybe<Scalars['String']>;
  ein?: InputMaybe<Scalars['String']>;
  logo?: InputMaybe<Scalars['String']>;
  name: Scalars['String'];
  phone_number?: InputMaybe<Scalars['String']>;
  product_description?: InputMaybe<Scalars['String']>;
  profile_thumbnail?: InputMaybe<Scalars['String']>;
  sole_address?: InputMaybe<Scalars['String']>;
  sole_birthday?: InputMaybe<Scalars['String']>;
  sole_city?: InputMaybe<Scalars['String']>;
  sole_email: Scalars['String'];
  sole_first_name?: InputMaybe<Scalars['String']>;
  sole_job_title?: InputMaybe<Scalars['String']>;
  sole_last_name?: InputMaybe<Scalars['String']>;
  sole_phone_number?: InputMaybe<Scalars['String']>;
  sole_ssn?: InputMaybe<Scalars['String']>;
  sole_state?: InputMaybe<Scalars['String']>;
  sole_zip_code?: InputMaybe<Scalars['Int']>;
  state?: InputMaybe<Scalars['String']>;
  status?: InputMaybe<AccountStatusEnum>;
  website: Scalars['String'];
  zip_code?: InputMaybe<Scalars['Int']>;
};

export type AccountCompanyFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  name?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

export type AccountCompanyPageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<AccountCompanySortByEnum>>>;
};

export type AccountCompanyResponse = {
  __typename?: 'AccountCompanyResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<AccountCompany>>>;
};

export enum AccountCompanySortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type AccountCompanyUpdateInput = {
  account_store?: InputMaybe<AccountStoreUpdateInput>;
  address?: InputMaybe<Scalars['String']>;
  business_type?: InputMaybe<AccountBusinessTypeEnum>;
  city?: InputMaybe<Scalars['String']>;
  classification?: InputMaybe<AccountClassificationEnum>;
  cover_image?: InputMaybe<Scalars['String']>;
  dba?: InputMaybe<Scalars['String']>;
  ein?: InputMaybe<Scalars['String']>;
  logo?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  phone_number?: InputMaybe<Scalars['String']>;
  product_description?: InputMaybe<Scalars['String']>;
  profile_thumbnail?: InputMaybe<Scalars['String']>;
  sole_address?: InputMaybe<Scalars['String']>;
  sole_birthday?: InputMaybe<Scalars['String']>;
  sole_city?: InputMaybe<Scalars['String']>;
  sole_email?: InputMaybe<Scalars['String']>;
  sole_first_name?: InputMaybe<Scalars['String']>;
  sole_job_title?: InputMaybe<Scalars['String']>;
  sole_last_name?: InputMaybe<Scalars['String']>;
  sole_phone_number?: InputMaybe<Scalars['String']>;
  sole_ssn?: InputMaybe<Scalars['String']>;
  sole_state?: InputMaybe<Scalars['String']>;
  sole_zip_code?: InputMaybe<Scalars['Int']>;
  state?: InputMaybe<Scalars['String']>;
  status?: InputMaybe<AccountStatusEnum>;
  website?: InputMaybe<Scalars['String']>;
  zip_code?: InputMaybe<Scalars['Int']>;
};

export type AccountInfo = {
  __typename?: 'AccountInfo';
  address?: Maybe<Scalars['String']>;
  birthday?: Maybe<Scalars['String']>;
  city?: Maybe<Scalars['String']>;
  email?: Maybe<Scalars['String']>;
  first_name?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  last_login_date?: Maybe<Scalars['String']>;
  last_logout_date?: Maybe<Scalars['String']>;
  last_name?: Maybe<Scalars['String']>;
  maiden_name?: Maybe<Scalars['String']>;
  middle_name?: Maybe<Scalars['String']>;
  preferred_name?: Maybe<Scalars['String']>;
  profile_image?: Maybe<Scalars['String']>;
  profile_thumbnail?: Maybe<Scalars['String']>;
  registration_date?: Maybe<Scalars['String']>;
  registration_status?: Maybe<AccountRegistrationEnum>;
  state?: Maybe<Scalars['String']>;
  status?: Maybe<AccountStatusEnum>;
  title?: Maybe<Scalars['String']>;
  verified_email?: Maybe<Scalars['Boolean']>;
  zip_code?: Maybe<Scalars['Int']>;
};

export type AccountInfoCreateInput = {
  account_company?: InputMaybe<AccountCompanyCreateInput>;
  address?: InputMaybe<Scalars['String']>;
  birthday?: InputMaybe<Scalars['String']>;
  city?: InputMaybe<Scalars['String']>;
  email: Scalars['String'];
  first_name?: InputMaybe<Scalars['String']>;
  last_name?: InputMaybe<Scalars['String']>;
  maiden_name?: InputMaybe<Scalars['String']>;
  middle_name?: InputMaybe<Scalars['String']>;
  password: Scalars['String'];
  preferred_name?: InputMaybe<Scalars['String']>;
  profile_image?: InputMaybe<Scalars['String']>;
  profile_thumbnail?: InputMaybe<Scalars['String']>;
  reTypePassword: Scalars['String'];
  state?: InputMaybe<Scalars['String']>;
  title?: InputMaybe<Scalars['String']>;
  zip_code?: InputMaybe<Scalars['Int']>;
};

export type AccountInfoResponse = {
  __typename?: 'AccountInfoResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<AccountInfo>>>;
};

export enum AccountInfoSortByEnum {
  Id = 'ID'
}

export type AccountInfoUpdateInput = {
  address?: InputMaybe<Scalars['String']>;
  birthday?: InputMaybe<Scalars['String']>;
  city?: InputMaybe<Scalars['String']>;
  first_name?: InputMaybe<Scalars['String']>;
  last_name?: InputMaybe<Scalars['String']>;
  maiden_name?: InputMaybe<Scalars['String']>;
  middle_name?: InputMaybe<Scalars['String']>;
  preferred_name?: InputMaybe<Scalars['String']>;
  profile_image?: InputMaybe<Scalars['String']>;
  profile_thumbnail?: InputMaybe<Scalars['String']>;
  state?: InputMaybe<Scalars['String']>;
  title?: InputMaybe<Scalars['String']>;
  zip_code?: InputMaybe<Scalars['Int']>;
};

export type AccountInfoUpdatePasswordInput = {
  password: Scalars['String'];
  password_retype: Scalars['String'];
};

export type AccountLoginInput = {
  login: Scalars['String'];
  password: Scalars['String'];
};

export enum AccountRegistrationEnum {
  Approved = 'APPROVED',
  Complete = 'COMPLETE',
  NotComplete = 'NOT_COMPLETE',
  Waiting = 'WAITING'
}

export enum AccountRoleEnum {
  Admin = 'ADMIN',
  Company = 'COMPANY',
  Customer = 'CUSTOMER',
  Employee = 'EMPLOYEE',
  Guest = 'GUEST',
  Manager = 'MANAGER'
}

export enum AccountStatusEnum {
  Active = 'ACTIVE',
  Deactivated = 'DEACTIVATED',
  Deleted = 'DELETED'
}

export type AccountStore = {
  __typename?: 'AccountStore';
  account_company_id?: Maybe<Scalars['Int']>;
  account_store_employee?: Maybe<Array<Maybe<AccountStoreEmployee>>>;
  address?: Maybe<Scalars['String']>;
  city?: Maybe<Scalars['String']>;
  ein?: Maybe<Scalars['String']>;
  fax_number?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  image?: Maybe<Scalars['String']>;
  images?: Maybe<Array<Maybe<Scalars['String']>>>;
  is_closed?: Maybe<Scalars['Boolean']>;
  latitude?: Maybe<Scalars['Float']>;
  logo?: Maybe<Scalars['String']>;
  logo_thumbnail?: Maybe<Scalars['String']>;
  longitude?: Maybe<Scalars['Float']>;
  name?: Maybe<Scalars['String']>;
  phone_number?: Maybe<Scalars['String']>;
  return_policy?: Maybe<Scalars['String']>;
  state?: Maybe<Scalars['String']>;
  tax_rate_applied?: Maybe<Scalars['Float']>;
  thumb_nail?: Maybe<Scalars['String']>;
  website?: Maybe<Scalars['String']>;
  zip_code?: Maybe<Scalars['Int']>;
};

export type AccountStoreCreateInput = {
  account_store_employee?: InputMaybe<Array<InputMaybe<AccountStoreEmployeeCreateInput>>>;
  address?: InputMaybe<Scalars['String']>;
  city?: InputMaybe<Scalars['String']>;
  ein: Scalars['String'];
  fax_number?: InputMaybe<Scalars['String']>;
  image?: InputMaybe<Scalars['String']>;
  images?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
  is_closed?: InputMaybe<Scalars['Boolean']>;
  latitude?: InputMaybe<Scalars['Float']>;
  logo?: InputMaybe<Scalars['String']>;
  logo_thumbnail?: InputMaybe<Scalars['String']>;
  longitude?: InputMaybe<Scalars['Float']>;
  name: Scalars['String'];
  phone_number?: InputMaybe<Scalars['String']>;
  return_policy?: InputMaybe<Scalars['String']>;
  state?: InputMaybe<Scalars['String']>;
  tax_rate_applied: Scalars['Float'];
  thumb_nail?: InputMaybe<Scalars['String']>;
  website: Scalars['String'];
  zip_code?: InputMaybe<Scalars['Int']>;
};

export type AccountStoreEmployee = {
  __typename?: 'AccountStoreEmployee';
  account_company_id?: Maybe<Scalars['Int']>;
  account_info_id?: Maybe<Scalars['Int']>;
  account_store_id?: Maybe<Scalars['Int']>;
  id?: Maybe<Scalars['Int']>;
  user_role?: Maybe<AccountRoleEnum>;
};

export type AccountStoreEmployeeCreateInput = {
  email: Scalars['String'];
  user_role: AccountRoleEnum;
};

export type AccountStoreEmployeeFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

export type AccountStoreEmployeePageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<AccountStoreEmployeeSortByEnum>>>;
};

export type AccountStoreEmployeeResponse = {
  __typename?: 'AccountStoreEmployeeResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<AccountStoreEmployee>>>;
};

export enum AccountStoreEmployeeSortByEnum {
  Id = 'ID'
}

export type AccountStoreEmployeeUpdateInput = {
  account_store_employee_id: Scalars['Int'];
  user_role: AccountRoleEnum;
};

export type AccountStoreFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  name?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

export type AccountStorePageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<AccountStoreSortByEnum>>>;
};

export type AccountStoreResponse = {
  __typename?: 'AccountStoreResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<AccountStore>>>;
};

export enum AccountStoreSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type AccountStoreUpdateInput = {
  account_store_employee?: InputMaybe<Array<InputMaybe<AccountStoreEmployeeUpdateInput>>>;
  account_store_id: Scalars['Int'];
  address?: InputMaybe<Scalars['String']>;
  city?: InputMaybe<Scalars['String']>;
  ein?: InputMaybe<Scalars['String']>;
  fax_number?: InputMaybe<Scalars['String']>;
  image?: InputMaybe<Scalars['String']>;
  images?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
  is_closed?: InputMaybe<Scalars['Boolean']>;
  latitude?: InputMaybe<Scalars['Float']>;
  logo?: InputMaybe<Scalars['String']>;
  logo_thumbnail?: InputMaybe<Scalars['String']>;
  longitude?: InputMaybe<Scalars['Float']>;
  name?: InputMaybe<Scalars['String']>;
  phone_number?: InputMaybe<Scalars['String']>;
  return_policy?: InputMaybe<Scalars['String']>;
  state?: InputMaybe<Scalars['String']>;
  tax_rate_applied?: InputMaybe<Scalars['Float']>;
  thumb_nail?: InputMaybe<Scalars['String']>;
  website?: InputMaybe<Scalars['String']>;
  zip_code?: InputMaybe<Scalars['Int']>;
};

export enum AuthenticationTokenTypeEnum {
  AccessToken = 'ACCESS_TOKEN',
  CsrfToken = 'CSRF_TOKEN',
  Other = 'OTHER',
  RefreshToken = 'REFRESH_TOKEN'
}

export type CartEvent = {
  __typename?: 'CartEvent';
  id?: Maybe<Scalars['Int']>;
};

export enum CartEventSortByEnum {
  Id = 'ID'
}

export type CartProduct = {
  __typename?: 'CartProduct';
  id?: Maybe<Scalars['Int']>;
};

export enum CartProductSortByEnum {
  Id = 'ID'
}

export type CartWishlist = {
  __typename?: 'CartWishlist';
  id?: Maybe<Scalars['Int']>;
};

export enum CartWishlistSortByEnum {
  Id = 'ID'
}

export type CollectionInfo = {
  __typename?: 'CollectionInfo';
  id?: Maybe<Scalars['Int']>;
};

export enum CollectionInfoSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export enum DownloadLocationEnum {
  Database = 'DATABASE',
  Imdb = 'IMDB',
  ImdbAll = 'IMDB_ALL',
  Redis = 'REDIS'
}

export enum DownloadTypeEnum {
  Download_480p = 'DOWNLOAD_480p',
  Download_720p = 'DOWNLOAD_720p',
  Download_1080p = 'DOWNLOAD_1080p'
}

export type EventInfo = {
  __typename?: 'EventInfo';
  id?: Maybe<Scalars['Int']>;
};

export enum EventInfoSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type EventSchedule = {
  __typename?: 'EventSchedule';
  id?: Maybe<Scalars['Int']>;
};

export enum EventScheduleSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type EventTicket = {
  __typename?: 'EventTicket';
  id?: Maybe<Scalars['Int']>;
};

export enum EventTicketSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type GeneralResponse = {
  __typename?: 'GeneralResponse';
  code: Scalars['Int'];
  message?: Maybe<Scalars['String']>;
  success?: Maybe<Scalars['Boolean']>;
  version?: Maybe<Scalars['String']>;
};

export type MovieInfo = {
  __typename?: 'MovieInfo';
  added_count?: Maybe<Scalars['Int']>;
  cast?: Maybe<Array<Maybe<Scalars['String']>>>;
  casts?: Maybe<Array<Maybe<PersonInfo>>>;
  countries?: Maybe<Array<Maybe<Scalars['String']>>>;
  cover?: Maybe<Scalars['String']>;
  creators?: Maybe<Array<Maybe<Scalars['String']>>>;
  directors?: Maybe<Array<Maybe<Scalars['String']>>>;
  download_480p_url?: Maybe<Scalars['String']>;
  download_720p_url?: Maybe<Scalars['String']>;
  download_1080p_url?: Maybe<Scalars['String']>;
  full_cover?: Maybe<Scalars['String']>;
  genres?: Maybe<Array<Maybe<Scalars['String']>>>;
  id?: Maybe<Scalars['Int']>;
  imdb_id?: Maybe<Scalars['String']>;
  person_cast?: Maybe<Array<Maybe<Scalars['String']>>>;
  plot?: Maybe<Scalars['String']>;
  popular_id?: Maybe<Scalars['Int']>;
  rating?: Maybe<Scalars['Float']>;
  release_date?: Maybe<Scalars['String']>;
  run_times?: Maybe<Array<Maybe<Scalars['String']>>>;
  title?: Maybe<Scalars['String']>;
  trailer_link?: Maybe<Scalars['String']>;
  videos?: Maybe<Array<Maybe<Scalars['String']>>>;
  votes?: Maybe<Scalars['Int']>;
  year?: Maybe<Scalars['Int']>;
};

export type MovieInfoDownloadInput = {
  download_type: DownloadTypeEnum;
  imdb_id: Scalars['String'];
};

export type MovieInfoFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  title?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
  year?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

export type MovieInfoPageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<MovieInfoSortByEnum>>>;
};

export type MovieInfoResponse = {
  __typename?: 'MovieInfoResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<MovieInfo>>>;
};

export enum MovieInfoSortByEnum {
  Id = 'ID',
  ImdbId = 'IMDB_ID',
  PopularId = 'POPULAR_ID',
  Title = 'TITLE'
}

export enum MovieStatusEnum {
  Completed = 'COMPLETED',
  NotCompleted = 'NOT_COMPLETED'
}

export type Mutation = {
  __typename?: 'Mutation';
  accountAuthenticationAuthZeroLogin?: Maybe<AccountAuthenticationResponse>;
  accountAuthenticationLogin?: Maybe<AccountAuthenticationResponse>;
  accountAuthenticationLogout?: Maybe<AccountAuthenticationResponse>;
  accountCompanyCreate?: Maybe<AccountCompanyResponse>;
  accountCompanyDelete?: Maybe<AccountCompanyResponse>;
  accountCompanyUpdate?: Maybe<AccountCompanyResponse>;
  accountConfirmEmail?: Maybe<AccountInfoResponse>;
  accountCreate?: Maybe<AccountInfoResponse>;
  accountDelete?: Maybe<AccountInfoResponse>;
  accountForgotPassword?: Maybe<AccountInfoResponse>;
  accountForgotPasswordConfirmEmail?: Maybe<AccountInfoResponse>;
  accountGuestLogin?: Maybe<AccountAuthenticationResponse>;
  accountResendConfirm?: Maybe<AccountInfoResponse>;
  accountStoreCreate?: Maybe<AccountStoreResponse>;
  accountStoreDelete?: Maybe<AccountStoreResponse>;
  accountStoreEmployeeCreate?: Maybe<AccountStoreEmployeeResponse>;
  accountStoreEmployeeDelete?: Maybe<AccountStoreEmployeeResponse>;
  accountStoreEmployeeUpdate?: Maybe<AccountStoreEmployeeResponse>;
  accountStoreUpdate?: Maybe<AccountStoreResponse>;
  accountUpdate?: Maybe<AccountInfoResponse>;
  accountUpdatePassword?: Maybe<AccountInfoResponse>;
  debug?: Maybe<Scalars['String']>;
  movieDownload?: Maybe<MovieInfoResponse>;
  movieUpdate?: Maybe<MovieInfoResponse>;
  showsDownload?: Maybe<ShowsInfoResponse>;
  showsEpisodeUpdate?: Maybe<ShowsEpisodeResponse>;
  trackerMovieCreate?: Maybe<TrackerMovieResponse>;
  trackerMovieUpdate?: Maybe<TrackerMovieResponse>;
  trackerShowsCreate?: Maybe<TrackerShowsInfoResponse>;
  trackerShowsEpisodeCreate?: Maybe<TrackerShowsInfoResponse>;
  trackerShowsEpisodeUpdate?: Maybe<TrackerShowsInfoResponse>;
  trackerShowsSeasonCreate?: Maybe<TrackerShowsInfoResponse>;
  trackerShowsSeasonUpdate?: Maybe<TrackerShowsInfoResponse>;
  trackerShowsUpdate?: Maybe<TrackerShowsInfoResponse>;
};


export type MutationAccountAuthenticationLoginArgs = {
  accountLoginInput: AccountLoginInput;
};


export type MutationAccountCompanyCreateArgs = {
  createInput: AccountCompanyCreateInput;
  filterInput?: InputMaybe<AccountCompanyFilterInput>;
  pageInfo?: InputMaybe<AccountCompanyPageInfoInput>;
};


export type MutationAccountCompanyDeleteArgs = {
  deleteInput: Array<InputMaybe<Scalars['Int']>>;
  filterInput?: InputMaybe<AccountCompanyFilterInput>;
  pageInfo?: InputMaybe<AccountCompanyPageInfoInput>;
};


export type MutationAccountCompanyUpdateArgs = {
  filterInput?: InputMaybe<AccountCompanyFilterInput>;
  pageInfo?: InputMaybe<AccountCompanyPageInfoInput>;
  updateInput: AccountCompanyUpdateInput;
};


export type MutationAccountCreateArgs = {
  createInput: AccountInfoCreateInput;
};


export type MutationAccountForgotPasswordArgs = {
  accountLogin: Scalars['String'];
};


export type MutationAccountResendConfirmArgs = {
  accountLogin: Scalars['String'];
};


export type MutationAccountStoreCreateArgs = {
  createInput: AccountStoreCreateInput;
  filterInput?: InputMaybe<AccountStoreFilterInput>;
  pageInfo?: InputMaybe<AccountStorePageInfoInput>;
};


export type MutationAccountStoreDeleteArgs = {
  deleteInput: Array<InputMaybe<Scalars['Int']>>;
  filterInput?: InputMaybe<AccountStoreFilterInput>;
  pageInfo?: InputMaybe<AccountStorePageInfoInput>;
};


export type MutationAccountStoreEmployeeCreateArgs = {
  createInput: Array<InputMaybe<AccountStoreEmployeeCreateInput>>;
  filterInput?: InputMaybe<AccountStoreEmployeeFilterInput>;
  pageInfo?: InputMaybe<AccountStoreEmployeePageInfoInput>;
};


export type MutationAccountStoreEmployeeDeleteArgs = {
  deleteInput: Array<InputMaybe<Scalars['Int']>>;
  filterInput?: InputMaybe<AccountStoreEmployeeFilterInput>;
  pageInfo?: InputMaybe<AccountStoreEmployeePageInfoInput>;
};


export type MutationAccountStoreEmployeeUpdateArgs = {
  filterInput?: InputMaybe<AccountStoreEmployeeFilterInput>;
  pageInfo?: InputMaybe<AccountStoreEmployeePageInfoInput>;
  updateInput: Array<InputMaybe<AccountStoreEmployeeUpdateInput>>;
};


export type MutationAccountStoreUpdateArgs = {
  filterInput?: InputMaybe<AccountStoreFilterInput>;
  pageInfo?: InputMaybe<AccountStorePageInfoInput>;
  updateInput: AccountStoreUpdateInput;
};


export type MutationAccountUpdateArgs = {
  updateInput: AccountInfoUpdateInput;
};


export type MutationAccountUpdatePasswordArgs = {
  updateInput: AccountInfoUpdatePasswordInput;
};


export type MutationMovieDownloadArgs = {
  searchInput?: InputMaybe<Array<InputMaybe<MovieInfoDownloadInput>>>;
};


export type MutationMovieUpdateArgs = {
  movie_info_id: Scalars['Int'];
};


export type MutationShowsDownloadArgs = {
  searchInput?: InputMaybe<Array<InputMaybe<ShowsDownloadInput>>>;
};


export type MutationShowsEpisodeUpdateArgs = {
  shows_episode_id: Scalars['Int'];
};


export type MutationTrackerMovieCreateArgs = {
  trackerMovieCreateInput: TrackerMovieCreateInput;
};


export type MutationTrackerMovieUpdateArgs = {
  trackerMovieUpdateInput: TrackerMovieUpdateInput;
};


export type MutationTrackerShowsCreateArgs = {
  createInput: TrackerShowsCreateInput;
};


export type MutationTrackerShowsEpisodeCreateArgs = {
  createInput: TrackerShowsEpisodeCreateInput;
};


export type MutationTrackerShowsEpisodeUpdateArgs = {
  updateInput: TrackerShowsEpisodeUpdateInput;
};


export type MutationTrackerShowsSeasonCreateArgs = {
  createInput: TrackerShowsSeasonCreateInput;
};


export type MutationTrackerShowsSeasonUpdateArgs = {
  updateInput: TrackerShowsSeasonUpdateInput;
};


export type MutationTrackerShowsUpdateArgs = {
  updateInput: TrackerShowsUpdateInput;
};

export type NotificationsSagaState = {
  __typename?: 'NotificationsSagaState';
  id?: Maybe<Scalars['Int']>;
};

export enum NotificationsSagaStateSortByEnum {
  Id = 'ID'
}

export enum NotifyStatusEnum {
  Closed = 'CLOSED',
  Open = 'OPEN'
}

export enum NotifyTemplateEnum {
  AllNationContact = 'ALL_NATION_CONTACT',
  LabelleAppointment = 'LABELLE_APPOINTMENT',
  LabelleContact = 'LABELLE_CONTACT',
  LabelleRsvp = 'LABELLE_RSVP',
  PromedexpressContact = 'PROMEDEXPRESS_CONTACT',
  PromedexpressRequestTransport = 'PROMEDEXPRESS_REQUEST_TRANSPORT',
  SumexusContact = 'SUMEXUS_CONTACT',
  SumexusRequestTransport = 'SUMEXUS_REQUEST_TRANSPORT'
}

export enum OrderByEnum {
  Asc = 'ASC',
  Desc = 'DESC'
}

export type OrdersInfo = {
  __typename?: 'OrdersInfo';
  id?: Maybe<Scalars['Int']>;
};

export enum OrdersInfoSortByEnum {
  Id = 'ID'
}

export enum OrdersInfoStatusEnum {
  Canceled = 'CANCELED',
  Error = 'ERROR',
  Pending = 'PENDING',
  Success = 'SUCCESS'
}

export enum OrdersTypeEnum {
  Event = 'EVENT',
  Product = 'PRODUCT'
}

export type PageInfo = {
  __typename?: 'PageInfo';
  page_info_count?: Maybe<Scalars['Int']>;
};

export type PageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  refresh?: InputMaybe<Scalars['Boolean']>;
};

export type PersonInfo = {
  __typename?: 'PersonInfo';
  akas?: Maybe<Array<Maybe<Scalars['String']>>>;
  birth_date?: Maybe<Scalars['String']>;
  birth_place?: Maybe<Scalars['String']>;
  filmography?: Maybe<Array<Maybe<Scalars['String']>>>;
  head_shot?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  imdb_id?: Maybe<Scalars['String']>;
  mini_biography?: Maybe<Scalars['String']>;
  name?: Maybe<Scalars['String']>;
  titles_refs?: Maybe<Array<Maybe<Scalars['String']>>>;
};

export type PersonInfoFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  name?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

export type PersonInfoPageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<PersonInfoSortByEnum>>>;
};

export type PersonInfoResponse = {
  __typename?: 'PersonInfoResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<PersonInfo>>>;
};

export enum PersonInfoSortByEnum {
  Id = 'ID'
}

export enum ProductBrandEnum {
  AdriannaPapell = 'ADRIANNA_PAPELL',
  AmeliaCouture = 'AMELIA_COUTURE',
  AshleyLauren = 'ASHLEY_LAUREN',
  Clarisse = 'CLARISSE',
  ColorsDress = 'COLORS_DRESS',
  EllieWild = 'ELLIE_WILD',
  JaszCouture = 'JASZ_COUTURE',
  JessicaAngel = 'JESSICA_ANGEL',
  Jovani = 'JOVANI',
  LaDivine = 'LA_DIVINE',
  MnmCouture = 'MNM_COUTURE',
  NoxAnabel = 'NOX_ANABEL',
  Other = 'OTHER',
  PortiaAndScarlett = 'PORTIA_AND_SCARLETT',
  PrimaveraCouture = 'PRIMAVERA_COUTURE',
  Scala = 'SCALA',
  SherriHill = 'SHERRI_HILL',
  SophiaThomas = 'SOPHIA_THOMAS',
  StellaCouture = 'STELLA_COUTURE',
  SydneysCloset = 'SYDNEYS_CLOSET',
  Walmart = 'WALMART'
}

export type ProductCategory = {
  __typename?: 'ProductCategory';
  id?: Maybe<Scalars['Int']>;
};

export enum ProductCategorySortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type ProductColor = {
  __typename?: 'ProductColor';
  id?: Maybe<Scalars['Int']>;
};

export enum ProductColorSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export type ProductInfo = {
  __typename?: 'ProductInfo';
  id?: Maybe<Scalars['Int']>;
};

export enum ProductInfoSortByEnum {
  Id = 'ID',
  MsrpPrice = 'MSRP_PRICE',
  Name = 'NAME'
}

export enum ProductIngestEnum {
  AdriannaPapell = 'ADRIANNA_PAPELL',
  AmeliaCouture = 'AMELIA_COUTURE',
  AshleyLauren = 'ASHLEY_LAUREN',
  Clarisse = 'CLARISSE',
  ColorsDress = 'COLORS_DRESS',
  EllieWild = 'ELLIE_WILD',
  JaszCouture = 'JASZ_COUTURE',
  JessicaAngel = 'JESSICA_ANGEL',
  Jovani = 'JOVANI',
  LaDivine = 'LA_DIVINE',
  Manual = 'MANUAL',
  MnmCouture = 'MNM_COUTURE',
  NoxAnabel = 'NOX_ANABEL',
  PortiaAndScarlett = 'PORTIA_AND_SCARLETT',
  PrimaveraCouture = 'PRIMAVERA_COUTURE',
  Scala = 'SCALA',
  SherriHill = 'SHERRI_HILL',
  SophiaThomas = 'SOPHIA_THOMAS',
  StellaCouture = 'STELLA_COUTURE',
  SydneysCloset = 'SYDNEYS_CLOSET'
}

export type ProductVariant = {
  __typename?: 'ProductVariant';
  id?: Maybe<Scalars['Int']>;
};

export enum ProductVariantSortByEnum {
  Id = 'ID',
  Name = 'NAME'
}

export enum ProviderTypeEnum {
  Amazon = 'AMAZON',
  Appletv = 'APPLETV',
  Disney = 'DISNEY',
  Hulu = 'HULU',
  Netflix = 'NETFLIX'
}

export type Query = {
  __typename?: 'Query';
  accountCompany?: Maybe<AccountCompanyResponse>;
  accountMe?: Maybe<AccountInfoResponse>;
  accountStore?: Maybe<AccountStoreResponse>;
  accountStoreEmployee?: Maybe<AccountStoreEmployeeResponse>;
  debug?: Maybe<Scalars['String']>;
  movieInfo?: Maybe<MovieInfoResponse>;
  personInfo?: Maybe<PersonInfoResponse>;
  showsEpisode?: Maybe<ShowsEpisodeResponse>;
  showsInfo?: Maybe<ShowsInfoResponse>;
  trackerMovieMe?: Maybe<TrackerMovieResponse>;
  trackerShowsMe?: Maybe<TrackerShowsInfoResponse>;
};


export type QueryAccountCompanyArgs = {
  filterInput?: InputMaybe<AccountCompanyFilterInput>;
  pageInfo?: InputMaybe<AccountCompanyPageInfoInput>;
};


export type QueryAccountStoreArgs = {
  filterInput?: InputMaybe<AccountStoreFilterInput>;
  pageInfo?: InputMaybe<AccountStorePageInfoInput>;
};


export type QueryAccountStoreEmployeeArgs = {
  filterInput?: InputMaybe<AccountStoreEmployeeFilterInput>;
  pageInfo?: InputMaybe<AccountStoreEmployeePageInfoInput>;
};


export type QueryMovieInfoArgs = {
  filterInput?: InputMaybe<MovieInfoFilterInput>;
  pageInfo?: InputMaybe<MovieInfoPageInfoInput>;
};


export type QueryPersonInfoArgs = {
  filterInput?: InputMaybe<PersonInfoFilterInput>;
  pageInfo?: InputMaybe<PersonInfoPageInfoInput>;
};


export type QueryShowsEpisodeArgs = {
  filterInput?: InputMaybe<ShowsEpisodeFilterInput>;
  pageInfo?: InputMaybe<ShowsEpisodePageInfoInput>;
};


export type QueryShowsInfoArgs = {
  filterInput?: InputMaybe<ShowsInfoFilterInput>;
  pageInfo?: InputMaybe<ShowsInfoPageInfoInput>;
};


export type QueryTrackerMovieMeArgs = {
  filterInput?: InputMaybe<TrackerMovieFilterInput>;
  pageInfo?: InputMaybe<TrackerMoviePageInfoInput>;
};


export type QueryTrackerShowsMeArgs = {
  filterInput?: InputMaybe<TrackerShowsFilterInput>;
  pageInfo?: InputMaybe<TrackerShowsPageInfoInput>;
};

export enum ReactionEmojiEnum {
  Amused = 'AMUSED',
  Bored = 'BORED',
  Confused = 'CONFUSED',
  Frustrated = 'FRUSTRATED',
  Reflective = 'REFLECTIVE',
  Sad = 'SAD',
  Scared = 'SCARED',
  Shocked = 'SHOCKED',
  Tense = 'TENSE',
  Thrilled = 'THRILLED',
  Touched = 'TOUCHED',
  Understood = 'UNDERSTOOD'
}

export enum RedisDatabaseEnum {
  Account = 'ACCOUNT',
  Cart = 'CART',
  Collection = 'COLLECTION',
  Default = 'DEFAULT',
  Event = 'EVENT',
  Movie = 'MOVIE',
  Notifications = 'NOTIFICATIONS',
  Orders = 'ORDERS',
  Person = 'PERSON',
  Product = 'PRODUCT',
  Shows = 'SHOWS',
  Trackstar = 'TRACKSTAR'
}

export type ShowsDownloadInput = {
  download_type: DownloadTypeEnum;
  episode: Scalars['Int'];
  imdb_id: Scalars['String'];
  season: Scalars['Int'];
  shows_imdb_id: Scalars['String'];
};

export type ShowsEpisode = {
  __typename?: 'ShowsEpisode';
  cover?: Maybe<Scalars['String']>;
  download_480p_url?: Maybe<Scalars['String']>;
  download_720p_url?: Maybe<Scalars['String']>;
  download_1080p_url?: Maybe<Scalars['String']>;
  episode?: Maybe<Scalars['Int']>;
  full_cover?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  imdb_id?: Maybe<Scalars['String']>;
  plot?: Maybe<Scalars['String']>;
  rating?: Maybe<Scalars['Float']>;
  release_date?: Maybe<Scalars['String']>;
  run_times?: Maybe<Array<Maybe<Scalars['String']>>>;
  season?: Maybe<Scalars['Int']>;
  shows_imdb_id?: Maybe<Scalars['String']>;
  shows_info_id?: Maybe<Scalars['Int']>;
  shows_season_id?: Maybe<Scalars['Int']>;
  title?: Maybe<Scalars['String']>;
  votes?: Maybe<Scalars['Int']>;
  year?: Maybe<Scalars['Int']>;
};

export type ShowsEpisodeFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  title?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
  year?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

export type ShowsEpisodePageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<ShowsEpisodeSortByEnum>>>;
};

export type ShowsEpisodeResponse = {
  __typename?: 'ShowsEpisodeResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<ShowsEpisode>>>;
};

export enum ShowsEpisodeSortByEnum {
  Id = 'ID'
}

export type ShowsInfo = {
  __typename?: 'ShowsInfo';
  added_count?: Maybe<Scalars['Int']>;
  cast?: Maybe<Array<Maybe<Scalars['String']>>>;
  casts?: Maybe<Array<Maybe<PersonInfo>>>;
  countries?: Maybe<Array<Maybe<Scalars['String']>>>;
  cover?: Maybe<Scalars['String']>;
  creators?: Maybe<Array<Maybe<Scalars['String']>>>;
  directors?: Maybe<Array<Maybe<Scalars['String']>>>;
  full_cover?: Maybe<Scalars['String']>;
  genres?: Maybe<Array<Maybe<Scalars['String']>>>;
  id?: Maybe<Scalars['Int']>;
  imdb_id?: Maybe<Scalars['String']>;
  plot?: Maybe<Scalars['String']>;
  popular_id?: Maybe<Scalars['Int']>;
  provider?: Maybe<ProviderTypeEnum>;
  rating?: Maybe<Scalars['Float']>;
  release_date?: Maybe<Scalars['String']>;
  run_times?: Maybe<Array<Maybe<Scalars['String']>>>;
  series_years?: Maybe<Scalars['String']>;
  shows_cast?: Maybe<Array<Maybe<Scalars['String']>>>;
  shows_season?: Maybe<Array<Maybe<ShowsSeason>>>;
  title?: Maybe<Scalars['String']>;
  total_episodes?: Maybe<Scalars['Int']>;
  total_seasons?: Maybe<Scalars['Int']>;
  trailer_link?: Maybe<Scalars['String']>;
  videos?: Maybe<Array<Maybe<Scalars['String']>>>;
  votes?: Maybe<Scalars['Int']>;
  year?: Maybe<Scalars['Int']>;
};

export type ShowsInfoFilterInput = {
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  title?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
  year?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

export type ShowsInfoPageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<ShowsInfoSortByEnum>>>;
};

export type ShowsInfoResponse = {
  __typename?: 'ShowsInfoResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<ShowsInfo>>>;
};

export enum ShowsInfoSortByEnum {
  Id = 'ID',
  ImdbId = 'IMDB_ID',
  PopularId = 'POPULAR_ID',
  Title = 'TITLE'
}

export type ShowsSeason = {
  __typename?: 'ShowsSeason';
  id?: Maybe<Scalars['Int']>;
  release_date?: Maybe<Scalars['String']>;
  season?: Maybe<Scalars['Int']>;
  shows_episode?: Maybe<Array<Maybe<ShowsEpisode>>>;
  shows_info_id?: Maybe<Scalars['Int']>;
  total_episodes?: Maybe<Scalars['Int']>;
};

export enum ShowsSeasonSortByEnum {
  Id = 'ID'
}

export enum SubscriptionGroupsEnum {
  Developer = 'DEVELOPER',
  Executive = 'EXECUTIVE',
  General = 'GENERAL',
  Youth = 'YOUTH'
}

export enum SubscriptionStatusEnum {
  Active = 'ACTIVE',
  Canceled = 'CANCELED',
  Suspended = 'SUSPENDED'
}

export enum SubscriptionTypeEnum {
  Free = 'FREE',
  MacausMember = 'MACAUS_MEMBER'
}

export type Subscriptions = {
  __typename?: 'Subscriptions';
  id?: Maybe<Scalars['Int']>;
};

export type TrackerMovie = {
  __typename?: 'TrackerMovie';
  account_info_id?: Maybe<Scalars['Int']>;
  completed?: Maybe<Scalars['Boolean']>;
  completed_date?: Maybe<Scalars['String']>;
  favorite?: Maybe<Scalars['Boolean']>;
  id?: Maybe<Scalars['Int']>;
  movie_info?: Maybe<MovieInfo>;
  movie_info_id?: Maybe<Scalars['Int']>;
  rating?: Maybe<Scalars['Float']>;
  reaction_emoji?: Maybe<Array<Maybe<ReactionEmojiEnum>>>;
  watch_location?: Maybe<WatchLocationEnum>;
};

export type TrackerMovieCreateInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  movie_info_id: Scalars['Int'];
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  watch_location?: InputMaybe<WatchLocationEnum>;
};

export type TrackerMovieFilterInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

export type TrackerMoviePageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<TrackerMovieSortByEnum>>>;
};

export type TrackerMovieResponse = {
  __typename?: 'TrackerMovieResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<TrackerMovie>>>;
};

export enum TrackerMovieSortByEnum {
  Completed = 'COMPLETED',
  Id = 'ID',
  Rating = 'RATING'
}

export type TrackerMovieUpdateInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id: Scalars['Int'];
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  watch_location?: InputMaybe<WatchLocationEnum>;
};

export type TrackerShows = {
  __typename?: 'TrackerShows';
  account_info_id?: Maybe<Scalars['Int']>;
  completed?: Maybe<Scalars['Boolean']>;
  completed_date?: Maybe<Scalars['String']>;
  favorite?: Maybe<Scalars['Boolean']>;
  id?: Maybe<Scalars['Int']>;
  rating?: Maybe<Scalars['Float']>;
  reaction_emoji?: Maybe<Array<Maybe<ReactionEmojiEnum>>>;
  shows_info?: Maybe<ShowsInfo>;
  shows_info_id?: Maybe<Scalars['Int']>;
  status?: Maybe<TrackerShowsStatusEnum>;
  tracker_shows_season?: Maybe<Array<Maybe<TrackerShowsSeason>>>;
  watch_location?: Maybe<WatchLocationEnum>;
};

export type TrackerShowsCreateInput = {
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  shows_info_id: Scalars['Int'];
  status?: InputMaybe<TrackerShowsStatusEnum>;
  watch_location?: InputMaybe<WatchLocationEnum>;
};

export type TrackerShowsEpisode = {
  __typename?: 'TrackerShowsEpisode';
  account_info_id?: Maybe<Scalars['Int']>;
  completed?: Maybe<Scalars['Boolean']>;
  completed_date?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  rating?: Maybe<Scalars['Float']>;
  reaction_emoji?: Maybe<Array<Maybe<ReactionEmojiEnum>>>;
  shows_episode_id?: Maybe<Scalars['Int']>;
  shows_info_id?: Maybe<Scalars['Int']>;
  shows_season_id?: Maybe<Scalars['Int']>;
  tracker_shows_id?: Maybe<Scalars['Int']>;
  tracker_shows_season_id?: Maybe<Scalars['Int']>;
};

export type TrackerShowsEpisodeCreateInput = {
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  shows_episode_id: Scalars['Int'];
  shows_info_id: Scalars['Int'];
  shows_season_id: Scalars['Int'];
};

export enum TrackerShowsEpisodeSortByEnum {
  Id = 'ID'
}

export type TrackerShowsEpisodeUpdateInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id: Scalars['Int'];
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  up_to_date?: InputMaybe<Scalars['Boolean']>;
};

export type TrackerShowsFilterInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
  rating?: InputMaybe<Array<InputMaybe<Scalars['Float']>>>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  status?: InputMaybe<Array<InputMaybe<TrackerShowsStatusEnum>>>;
  watch_location?: InputMaybe<Array<InputMaybe<WatchLocationEnum>>>;
};

export type TrackerShowsInfoResponse = {
  __typename?: 'TrackerShowsInfoResponse';
  pageInfo?: Maybe<PageInfo>;
  response: GeneralResponse;
  result?: Maybe<Array<Maybe<TrackerShows>>>;
};

export type TrackerShowsPageInfoInput = {
  first?: InputMaybe<Scalars['Int']>;
  maxId?: InputMaybe<Scalars['Int']>;
  minId?: InputMaybe<Scalars['Int']>;
  orderBy?: InputMaybe<OrderByEnum>;
  pageNumber?: InputMaybe<Scalars['Int']>;
  sortBy?: InputMaybe<Array<InputMaybe<TrackerShowsSortByEnum>>>;
};

export type TrackerShowsSeason = {
  __typename?: 'TrackerShowsSeason';
  account_info_id?: Maybe<Scalars['Int']>;
  completed?: Maybe<Scalars['Boolean']>;
  completed_date?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['Int']>;
  rating?: Maybe<Scalars['Float']>;
  reaction_emoji?: Maybe<Array<Maybe<ReactionEmojiEnum>>>;
  shows_info_id?: Maybe<Scalars['Int']>;
  shows_season_id?: Maybe<Scalars['Int']>;
  tracker_shows_episode?: Maybe<Array<Maybe<TrackerShowsEpisode>>>;
  tracker_shows_id?: Maybe<Scalars['Int']>;
};

export type TrackerShowsSeasonCreateInput = {
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  shows_info_id: Scalars['Int'];
  shows_season_id: Scalars['Int'];
};

export enum TrackerShowsSeasonSortByEnum {
  Id = 'ID'
}

export type TrackerShowsSeasonUpdateInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id: Scalars['Int'];
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  up_to_date?: InputMaybe<Scalars['Boolean']>;
};

export enum TrackerShowsSortByEnum {
  Id = 'ID'
}

export enum TrackerShowsStatusEnum {
  Completed = 'COMPLETED',
  Removed = 'REMOVED',
  StopWatching = 'STOP_WATCHING',
  UpToDate = 'UP_TO_DATE',
  Watching = 'WATCHING',
  WatchLater = 'WATCH_LATER'
}

export type TrackerShowsUpdateInput = {
  completed?: InputMaybe<Scalars['Boolean']>;
  id: Scalars['Int'];
  rating?: InputMaybe<Scalars['Float']>;
  reaction_emoji?: InputMaybe<Array<InputMaybe<ReactionEmojiEnum>>>;
  status?: InputMaybe<TrackerShowsStatusEnum>;
  watch_location?: InputMaybe<WatchLocationEnum>;
};

export enum TrackerTypeEnum {
  Movie = 'MOVIE',
  Show = 'SHOW'
}

export enum WatchLocationEnum {
  Computer = 'COMPUTER',
  Other = 'OTHER',
  Phone = 'PHONE',
  Tablet = 'TABLET',
  Television = 'TELEVISION',
  Theater = 'THEATER',
  Unofficial = 'UNOFFICIAL'
}

export type AccountAuthenticationAuthZeroLoginMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountAuthenticationAuthZeroLoginMutation = { __typename?: 'Mutation', accountAuthenticationAuthZeroLogin?: { __typename?: 'AccountAuthenticationResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: { __typename?: 'AccountAuthentication', authenticationToken?: string | null, authenticationTokenType?: AuthenticationTokenTypeEnum | null, registrationStatus?: AccountRegistrationEnum | null, account_info?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, status?: AccountStatusEnum | null, registration_status?: AccountRegistrationEnum | null, profile_image?: string | null } | null> | null } | null } | null };

export type AccountAuthenticationLoginMutationVariables = Exact<{
  accountLoginInput: AccountLoginInput;
}>;


export type AccountAuthenticationLoginMutation = { __typename?: 'Mutation', accountAuthenticationLogin?: { __typename?: 'AccountAuthenticationResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: { __typename?: 'AccountAuthentication', authenticationToken?: string | null, authenticationTokenType?: AuthenticationTokenTypeEnum | null, registrationStatus?: AccountRegistrationEnum | null, account_info?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, status?: AccountStatusEnum | null, registration_status?: AccountRegistrationEnum | null, profile_image?: string | null } | null> | null } | null } | null };

export type AccountAuthenticationLogoutMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountAuthenticationLogoutMutation = { __typename?: 'Mutation', accountAuthenticationLogout?: { __typename?: 'AccountAuthenticationResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type AccountConfirmEmailMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountConfirmEmailMutation = { __typename?: 'Mutation', accountConfirmEmail?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type AccountCreateMutationVariables = Exact<{
  createInput: AccountInfoCreateInput;
}>;


export type AccountCreateMutation = { __typename?: 'Mutation', accountCreate?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, status?: AccountStatusEnum | null, registration_status?: AccountRegistrationEnum | null, profile_image?: string | null } | null> | null } | null };

export type AccountDeleteMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountDeleteMutation = { __typename?: 'Mutation', accountDelete?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type AccountForgotPasswordMutationVariables = Exact<{
  accountLogin: Scalars['String'];
}>;


export type AccountForgotPasswordMutation = { __typename?: 'Mutation', accountForgotPassword?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type AccountForgotPasswordConfirmEmailMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountForgotPasswordConfirmEmailMutation = { __typename?: 'Mutation', accountForgotPasswordConfirmEmail?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type AccountGuestLoginMutationVariables = Exact<{ [key: string]: never; }>;


export type AccountGuestLoginMutation = { __typename?: 'Mutation', accountGuestLogin?: { __typename?: 'AccountAuthenticationResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: { __typename?: 'AccountAuthentication', authenticationToken?: string | null, authenticationTokenType?: AuthenticationTokenTypeEnum | null, registrationStatus?: AccountRegistrationEnum | null } | null } | null };

export type AccountMeQueryVariables = Exact<{ [key: string]: never; }>;


export type AccountMeQuery = { __typename?: 'Query', accountMe?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, registration_date?: string | null, registration_status?: AccountRegistrationEnum | null, verified_email?: boolean | null, last_login_date?: string | null, last_logout_date?: string | null, profile_image?: string | null, profile_thumbnail?: string | null, status?: AccountStatusEnum | null, first_name?: string | null, last_name?: string | null } | null> | null } | null };

export type AccountResendConfirmMutationVariables = Exact<{
  accountLogin: Scalars['String'];
}>;


export type AccountResendConfirmMutation = { __typename?: 'Mutation', accountResendConfirm?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, status?: AccountStatusEnum | null, registration_status?: AccountRegistrationEnum | null, profile_image?: string | null } | null> | null } | null };

export type AccountUpdateMutationVariables = Exact<{
  updateInput: AccountInfoUpdateInput;
}>;


export type AccountUpdateMutation = { __typename?: 'Mutation', accountUpdate?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'AccountInfo', id?: number | null, email?: string | null, registration_date?: string | null, registration_status?: AccountRegistrationEnum | null, verified_email?: boolean | null, last_login_date?: string | null, last_logout_date?: string | null, profile_image?: string | null, profile_thumbnail?: string | null, status?: AccountStatusEnum | null, first_name?: string | null, last_name?: string | null, middle_name?: string | null, maiden_name?: string | null, title?: string | null, preferred_name?: string | null, birthday?: string | null, address?: string | null, city?: string | null, state?: string | null, zip_code?: number | null } | null> | null } | null };

export type AccountUpdatePasswordMutationVariables = Exact<{
  updateInput: AccountInfoUpdatePasswordInput;
}>;


export type AccountUpdatePasswordMutation = { __typename?: 'Mutation', accountUpdatePassword?: { __typename?: 'AccountInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null } | null };

export type MovieDetailsQueryVariables = Exact<{
  filterInput?: InputMaybe<MovieInfoFilterInput>;
}>;


export type MovieDetailsQuery = { __typename?: 'Query', movieInfo?: { __typename?: 'MovieInfoResponse', response: { __typename?: 'GeneralResponse', code: number, message?: string | null, success?: boolean | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'MovieInfo', id?: number | null, imdb_id?: string | null, title?: string | null, popular_id?: number | null, genres?: Array<string | null> | null, cast?: Array<string | null> | null, plot?: string | null, rating?: number | null, release_date?: string | null, run_times?: Array<string | null> | null, trailer_link?: string | null, full_cover?: string | null, cover?: string | null, votes?: number | null, year?: number | null, download_1080p_url?: string | null, download_720p_url?: string | null, download_480p_url?: string | null, videos?: Array<string | null> | null, casts?: Array<{ __typename?: 'PersonInfo', id?: number | null, head_shot?: string | null, name?: string | null, imdb_id?: string | null } | null> | null } | null> | null } | null };

export type MovieDownloadMutationVariables = Exact<{
  searchInput?: InputMaybe<Array<InputMaybe<MovieInfoDownloadInput>> | InputMaybe<MovieInfoDownloadInput>>;
}>;


export type MovieDownloadMutation = { __typename?: 'Mutation', movieDownload?: { __typename?: 'MovieInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null } } | null };

export type MoviePopularQueryVariables = Exact<{
  pageInfo?: InputMaybe<MovieInfoPageInfoInput>;
}>;


export type MoviePopularQuery = { __typename?: 'Query', movieInfo?: { __typename?: 'MovieInfoResponse', response: { __typename?: 'GeneralResponse', code: number, message?: string | null, success?: boolean | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'MovieInfo', id?: number | null, imdb_id?: string | null, title?: string | null, popular_id?: number | null, full_cover?: string | null, cover?: string | null, trailer_link?: string | null, download_1080p_url?: string | null, download_720p_url?: string | null, download_480p_url?: string | null, plot?: string | null } | null> | null } | null };

export type MovieUpdateMutationVariables = Exact<{
  movieInfoId: Scalars['Int'];
}>;


export type MovieUpdateMutation = { __typename?: 'Mutation', movieUpdate?: { __typename?: 'MovieInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null } } | null };

export type ShowsDetailsQueryVariables = Exact<{
  filterInput?: InputMaybe<ShowsInfoFilterInput>;
}>;


export type ShowsDetailsQuery = { __typename?: 'Query', showsInfo?: { __typename?: 'ShowsInfoResponse', response: { __typename?: 'GeneralResponse', code: number, message?: string | null, success?: boolean | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'ShowsInfo', id?: number | null, imdb_id?: string | null, title?: string | null, popular_id?: number | null, full_cover?: string | null, cover?: string | null, genres?: Array<string | null> | null, plot?: string | null, cast?: Array<string | null> | null, trailer_link?: string | null, release_date?: string | null, total_seasons?: number | null, total_episodes?: number | null, videos?: Array<string | null> | null, casts?: Array<{ __typename?: 'PersonInfo', id?: number | null, head_shot?: string | null, name?: string | null, imdb_id?: string | null } | null> | null, shows_season?: Array<{ __typename?: 'ShowsSeason', id?: number | null, season?: number | null, shows_episode?: Array<{ __typename?: 'ShowsEpisode', id?: number | null, season?: number | null, episode?: number | null, shows_info_id?: number | null, shows_season_id?: number | null, download_1080p_url?: string | null, download_720p_url?: string | null, download_480p_url?: string | null, cover?: string | null, full_cover?: string | null } | null> | null } | null> | null } | null> | null } | null };

export type ShowsDownloadMutationVariables = Exact<{
  searchInput?: InputMaybe<Array<InputMaybe<ShowsDownloadInput>> | InputMaybe<ShowsDownloadInput>>;
}>;


export type ShowsDownloadMutation = { __typename?: 'Mutation', showsDownload?: { __typename?: 'ShowsInfoResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null } } | null };

export type ShowsEpisodeDetailsQueryVariables = Exact<{
  filterInput?: InputMaybe<ShowsEpisodeFilterInput>;
}>;


export type ShowsEpisodeDetailsQuery = { __typename?: 'Query', showsEpisode?: { __typename?: 'ShowsEpisodeResponse', response: { __typename?: 'GeneralResponse', code: number, message?: string | null, success?: boolean | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'ShowsEpisode', id?: number | null, imdb_id?: string | null, shows_imdb_id?: string | null, shows_info_id?: number | null, shows_season_id?: number | null, title?: string | null, season?: number | null, episode?: number | null, rating?: number | null, plot?: string | null, release_date?: string | null, download_1080p_url?: string | null, download_720p_url?: string | null, download_480p_url?: string | null, cover?: string | null, full_cover?: string | null, run_times?: Array<string | null> | null } | null> | null } | null };

export type ShowsEpisodeUpdateMutationVariables = Exact<{
  showsEpisodeId: Scalars['Int'];
}>;


export type ShowsEpisodeUpdateMutation = { __typename?: 'Mutation', showsEpisodeUpdate?: { __typename?: 'ShowsEpisodeResponse', response: { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null } } | null };

export type ShowsPopularQueryVariables = Exact<{
  pageInfo?: InputMaybe<ShowsInfoPageInfoInput>;
}>;


export type ShowsPopularQuery = { __typename?: 'Query', showsInfo?: { __typename?: 'ShowsInfoResponse', response: { __typename?: 'GeneralResponse', code: number, message?: string | null, success?: boolean | null, version?: string | null }, pageInfo?: { __typename?: 'PageInfo', page_info_count?: number | null } | null, result?: Array<{ __typename?: 'ShowsInfo', id?: number | null, imdb_id?: string | null, title?: string | null, popular_id?: number | null, full_cover?: string | null, cover?: string | null, trailer_link?: string | null, shows_season?: Array<{ __typename?: 'ShowsSeason', id?: number | null, shows_episode?: Array<{ __typename?: 'ShowsEpisode', id?: number | null, shows_info_id?: number | null, shows_season_id?: number | null, download_1080p_url?: string | null, download_720p_url?: string | null, download_480p_url?: string | null } | null> | null } | null> | null } | null> | null } | null };

export type PageInfoFragment = { __typename?: 'PageInfo', page_info_count?: number | null };

export type GeneralResponseFragment = { __typename?: 'GeneralResponse', code: number, success?: boolean | null, message?: string | null, version?: string | null };

export const PageInfoFragmentDoc = gql`
    fragment PageInfo on PageInfo {
  page_info_count
}
    `;
export const GeneralResponseFragmentDoc = gql`
    fragment GeneralResponse on GeneralResponse {
  code
  success
  message
  version
}
    `;
export const AccountAuthenticationAuthZeroLoginDocument = gql`
    mutation AccountAuthenticationAuthZeroLogin {
  accountAuthenticationAuthZeroLogin {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
    result {
      authenticationToken
      authenticationTokenType
      registrationStatus
      account_info {
        id
        email
        status
        registration_status
        profile_image
      }
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountAuthenticationAuthZeroLoginMutationFn = Apollo.MutationFunction<AccountAuthenticationAuthZeroLoginMutation, AccountAuthenticationAuthZeroLoginMutationVariables>;

/**
 * __useAccountAuthenticationAuthZeroLoginMutation__
 *
 * To run a mutation, you first call `useAccountAuthenticationAuthZeroLoginMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountAuthenticationAuthZeroLoginMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountAuthenticationAuthZeroLoginMutation, { data, loading, error }] = useAccountAuthenticationAuthZeroLoginMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountAuthenticationAuthZeroLoginMutation(baseOptions?: Apollo.MutationHookOptions<AccountAuthenticationAuthZeroLoginMutation, AccountAuthenticationAuthZeroLoginMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountAuthenticationAuthZeroLoginMutation, AccountAuthenticationAuthZeroLoginMutationVariables>(AccountAuthenticationAuthZeroLoginDocument, options);
      }
export type AccountAuthenticationAuthZeroLoginMutationHookResult = ReturnType<typeof useAccountAuthenticationAuthZeroLoginMutation>;
export type AccountAuthenticationAuthZeroLoginMutationResult = Apollo.MutationResult<AccountAuthenticationAuthZeroLoginMutation>;
export type AccountAuthenticationAuthZeroLoginMutationOptions = Apollo.BaseMutationOptions<AccountAuthenticationAuthZeroLoginMutation, AccountAuthenticationAuthZeroLoginMutationVariables>;
export const AccountAuthenticationLoginDocument = gql`
    mutation AccountAuthenticationLogin($accountLoginInput: AccountLoginInput!) {
  accountAuthenticationLogin(accountLoginInput: $accountLoginInput) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
    result {
      authenticationToken
      authenticationTokenType
      registrationStatus
      account_info {
        id
        email
        status
        registration_status
        profile_image
      }
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountAuthenticationLoginMutationFn = Apollo.MutationFunction<AccountAuthenticationLoginMutation, AccountAuthenticationLoginMutationVariables>;

/**
 * __useAccountAuthenticationLoginMutation__
 *
 * To run a mutation, you first call `useAccountAuthenticationLoginMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountAuthenticationLoginMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountAuthenticationLoginMutation, { data, loading, error }] = useAccountAuthenticationLoginMutation({
 *   variables: {
 *      accountLoginInput: // value for 'accountLoginInput'
 *   },
 * });
 */
export function useAccountAuthenticationLoginMutation(baseOptions?: Apollo.MutationHookOptions<AccountAuthenticationLoginMutation, AccountAuthenticationLoginMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountAuthenticationLoginMutation, AccountAuthenticationLoginMutationVariables>(AccountAuthenticationLoginDocument, options);
      }
export type AccountAuthenticationLoginMutationHookResult = ReturnType<typeof useAccountAuthenticationLoginMutation>;
export type AccountAuthenticationLoginMutationResult = Apollo.MutationResult<AccountAuthenticationLoginMutation>;
export type AccountAuthenticationLoginMutationOptions = Apollo.BaseMutationOptions<AccountAuthenticationLoginMutation, AccountAuthenticationLoginMutationVariables>;
export const AccountAuthenticationLogoutDocument = gql`
    mutation AccountAuthenticationLogout {
  accountAuthenticationLogout {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
  }
}
    `;
export type AccountAuthenticationLogoutMutationFn = Apollo.MutationFunction<AccountAuthenticationLogoutMutation, AccountAuthenticationLogoutMutationVariables>;

/**
 * __useAccountAuthenticationLogoutMutation__
 *
 * To run a mutation, you first call `useAccountAuthenticationLogoutMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountAuthenticationLogoutMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountAuthenticationLogoutMutation, { data, loading, error }] = useAccountAuthenticationLogoutMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountAuthenticationLogoutMutation(baseOptions?: Apollo.MutationHookOptions<AccountAuthenticationLogoutMutation, AccountAuthenticationLogoutMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountAuthenticationLogoutMutation, AccountAuthenticationLogoutMutationVariables>(AccountAuthenticationLogoutDocument, options);
      }
export type AccountAuthenticationLogoutMutationHookResult = ReturnType<typeof useAccountAuthenticationLogoutMutation>;
export type AccountAuthenticationLogoutMutationResult = Apollo.MutationResult<AccountAuthenticationLogoutMutation>;
export type AccountAuthenticationLogoutMutationOptions = Apollo.BaseMutationOptions<AccountAuthenticationLogoutMutation, AccountAuthenticationLogoutMutationVariables>;
export const AccountConfirmEmailDocument = gql`
    mutation AccountConfirmEmail {
  accountConfirmEmail {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountConfirmEmailMutationFn = Apollo.MutationFunction<AccountConfirmEmailMutation, AccountConfirmEmailMutationVariables>;

/**
 * __useAccountConfirmEmailMutation__
 *
 * To run a mutation, you first call `useAccountConfirmEmailMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountConfirmEmailMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountConfirmEmailMutation, { data, loading, error }] = useAccountConfirmEmailMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountConfirmEmailMutation(baseOptions?: Apollo.MutationHookOptions<AccountConfirmEmailMutation, AccountConfirmEmailMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountConfirmEmailMutation, AccountConfirmEmailMutationVariables>(AccountConfirmEmailDocument, options);
      }
export type AccountConfirmEmailMutationHookResult = ReturnType<typeof useAccountConfirmEmailMutation>;
export type AccountConfirmEmailMutationResult = Apollo.MutationResult<AccountConfirmEmailMutation>;
export type AccountConfirmEmailMutationOptions = Apollo.BaseMutationOptions<AccountConfirmEmailMutation, AccountConfirmEmailMutationVariables>;
export const AccountCreateDocument = gql`
    mutation AccountCreate($createInput: AccountInfoCreateInput!) {
  accountCreate(createInput: $createInput) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
    result {
      id
      email
      status
      registration_status
      profile_image
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountCreateMutationFn = Apollo.MutationFunction<AccountCreateMutation, AccountCreateMutationVariables>;

/**
 * __useAccountCreateMutation__
 *
 * To run a mutation, you first call `useAccountCreateMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountCreateMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountCreateMutation, { data, loading, error }] = useAccountCreateMutation({
 *   variables: {
 *      createInput: // value for 'createInput'
 *   },
 * });
 */
export function useAccountCreateMutation(baseOptions?: Apollo.MutationHookOptions<AccountCreateMutation, AccountCreateMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountCreateMutation, AccountCreateMutationVariables>(AccountCreateDocument, options);
      }
export type AccountCreateMutationHookResult = ReturnType<typeof useAccountCreateMutation>;
export type AccountCreateMutationResult = Apollo.MutationResult<AccountCreateMutation>;
export type AccountCreateMutationOptions = Apollo.BaseMutationOptions<AccountCreateMutation, AccountCreateMutationVariables>;
export const AccountDeleteDocument = gql`
    mutation AccountDelete {
  accountDelete {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
  }
}
    `;
export type AccountDeleteMutationFn = Apollo.MutationFunction<AccountDeleteMutation, AccountDeleteMutationVariables>;

/**
 * __useAccountDeleteMutation__
 *
 * To run a mutation, you first call `useAccountDeleteMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountDeleteMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountDeleteMutation, { data, loading, error }] = useAccountDeleteMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountDeleteMutation(baseOptions?: Apollo.MutationHookOptions<AccountDeleteMutation, AccountDeleteMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountDeleteMutation, AccountDeleteMutationVariables>(AccountDeleteDocument, options);
      }
export type AccountDeleteMutationHookResult = ReturnType<typeof useAccountDeleteMutation>;
export type AccountDeleteMutationResult = Apollo.MutationResult<AccountDeleteMutation>;
export type AccountDeleteMutationOptions = Apollo.BaseMutationOptions<AccountDeleteMutation, AccountDeleteMutationVariables>;
export const AccountForgotPasswordDocument = gql`
    mutation AccountForgotPassword($accountLogin: String!) {
  accountForgotPassword(accountLogin: $accountLogin) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
  }
}
    `;
export type AccountForgotPasswordMutationFn = Apollo.MutationFunction<AccountForgotPasswordMutation, AccountForgotPasswordMutationVariables>;

/**
 * __useAccountForgotPasswordMutation__
 *
 * To run a mutation, you first call `useAccountForgotPasswordMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountForgotPasswordMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountForgotPasswordMutation, { data, loading, error }] = useAccountForgotPasswordMutation({
 *   variables: {
 *      accountLogin: // value for 'accountLogin'
 *   },
 * });
 */
export function useAccountForgotPasswordMutation(baseOptions?: Apollo.MutationHookOptions<AccountForgotPasswordMutation, AccountForgotPasswordMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountForgotPasswordMutation, AccountForgotPasswordMutationVariables>(AccountForgotPasswordDocument, options);
      }
export type AccountForgotPasswordMutationHookResult = ReturnType<typeof useAccountForgotPasswordMutation>;
export type AccountForgotPasswordMutationResult = Apollo.MutationResult<AccountForgotPasswordMutation>;
export type AccountForgotPasswordMutationOptions = Apollo.BaseMutationOptions<AccountForgotPasswordMutation, AccountForgotPasswordMutationVariables>;
export const AccountForgotPasswordConfirmEmailDocument = gql`
    mutation AccountForgotPasswordConfirmEmail {
  accountForgotPasswordConfirmEmail {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
  }
}
    `;
export type AccountForgotPasswordConfirmEmailMutationFn = Apollo.MutationFunction<AccountForgotPasswordConfirmEmailMutation, AccountForgotPasswordConfirmEmailMutationVariables>;

/**
 * __useAccountForgotPasswordConfirmEmailMutation__
 *
 * To run a mutation, you first call `useAccountForgotPasswordConfirmEmailMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountForgotPasswordConfirmEmailMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountForgotPasswordConfirmEmailMutation, { data, loading, error }] = useAccountForgotPasswordConfirmEmailMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountForgotPasswordConfirmEmailMutation(baseOptions?: Apollo.MutationHookOptions<AccountForgotPasswordConfirmEmailMutation, AccountForgotPasswordConfirmEmailMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountForgotPasswordConfirmEmailMutation, AccountForgotPasswordConfirmEmailMutationVariables>(AccountForgotPasswordConfirmEmailDocument, options);
      }
export type AccountForgotPasswordConfirmEmailMutationHookResult = ReturnType<typeof useAccountForgotPasswordConfirmEmailMutation>;
export type AccountForgotPasswordConfirmEmailMutationResult = Apollo.MutationResult<AccountForgotPasswordConfirmEmailMutation>;
export type AccountForgotPasswordConfirmEmailMutationOptions = Apollo.BaseMutationOptions<AccountForgotPasswordConfirmEmailMutation, AccountForgotPasswordConfirmEmailMutationVariables>;
export const AccountGuestLoginDocument = gql`
    mutation AccountGuestLogin {
  accountGuestLogin {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
    result {
      authenticationToken
      authenticationTokenType
      registrationStatus
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountGuestLoginMutationFn = Apollo.MutationFunction<AccountGuestLoginMutation, AccountGuestLoginMutationVariables>;

/**
 * __useAccountGuestLoginMutation__
 *
 * To run a mutation, you first call `useAccountGuestLoginMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountGuestLoginMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountGuestLoginMutation, { data, loading, error }] = useAccountGuestLoginMutation({
 *   variables: {
 *   },
 * });
 */
export function useAccountGuestLoginMutation(baseOptions?: Apollo.MutationHookOptions<AccountGuestLoginMutation, AccountGuestLoginMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountGuestLoginMutation, AccountGuestLoginMutationVariables>(AccountGuestLoginDocument, options);
      }
export type AccountGuestLoginMutationHookResult = ReturnType<typeof useAccountGuestLoginMutation>;
export type AccountGuestLoginMutationResult = Apollo.MutationResult<AccountGuestLoginMutation>;
export type AccountGuestLoginMutationOptions = Apollo.BaseMutationOptions<AccountGuestLoginMutation, AccountGuestLoginMutationVariables>;
export const AccountMeDocument = gql`
    query AccountMe {
  accountMe {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      email
      registration_date
      registration_status
      verified_email
      last_login_date
      last_logout_date
      profile_image
      profile_thumbnail
      status
      first_name
      last_name
    }
  }
}
    `;

/**
 * __useAccountMeQuery__
 *
 * To run a query within a React component, call `useAccountMeQuery` and pass it any options that fit your needs.
 * When your component renders, `useAccountMeQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useAccountMeQuery({
 *   variables: {
 *   },
 * });
 */
export function useAccountMeQuery(baseOptions?: Apollo.QueryHookOptions<AccountMeQuery, AccountMeQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<AccountMeQuery, AccountMeQueryVariables>(AccountMeDocument, options);
      }
export function useAccountMeLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<AccountMeQuery, AccountMeQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<AccountMeQuery, AccountMeQueryVariables>(AccountMeDocument, options);
        }
export type AccountMeQueryHookResult = ReturnType<typeof useAccountMeQuery>;
export type AccountMeLazyQueryHookResult = ReturnType<typeof useAccountMeLazyQuery>;
export type AccountMeQueryResult = Apollo.QueryResult<AccountMeQuery, AccountMeQueryVariables>;
export const AccountResendConfirmDocument = gql`
    mutation AccountResendConfirm($accountLogin: String!) {
  accountResendConfirm(accountLogin: $accountLogin) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      ...PageInfo
    }
    result {
      id
      email
      status
      registration_status
      profile_image
    }
  }
}
    ${PageInfoFragmentDoc}`;
export type AccountResendConfirmMutationFn = Apollo.MutationFunction<AccountResendConfirmMutation, AccountResendConfirmMutationVariables>;

/**
 * __useAccountResendConfirmMutation__
 *
 * To run a mutation, you first call `useAccountResendConfirmMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountResendConfirmMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountResendConfirmMutation, { data, loading, error }] = useAccountResendConfirmMutation({
 *   variables: {
 *      accountLogin: // value for 'accountLogin'
 *   },
 * });
 */
export function useAccountResendConfirmMutation(baseOptions?: Apollo.MutationHookOptions<AccountResendConfirmMutation, AccountResendConfirmMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountResendConfirmMutation, AccountResendConfirmMutationVariables>(AccountResendConfirmDocument, options);
      }
export type AccountResendConfirmMutationHookResult = ReturnType<typeof useAccountResendConfirmMutation>;
export type AccountResendConfirmMutationResult = Apollo.MutationResult<AccountResendConfirmMutation>;
export type AccountResendConfirmMutationOptions = Apollo.BaseMutationOptions<AccountResendConfirmMutation, AccountResendConfirmMutationVariables>;
export const AccountUpdateDocument = gql`
    mutation AccountUpdate($updateInput: AccountInfoUpdateInput!) {
  accountUpdate(updateInput: $updateInput) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      email
      registration_date
      registration_status
      verified_email
      last_login_date
      last_logout_date
      profile_image
      profile_thumbnail
      status
      first_name
      last_name
      middle_name
      maiden_name
      title
      preferred_name
      birthday
      address
      city
      state
      zip_code
    }
  }
}
    `;
export type AccountUpdateMutationFn = Apollo.MutationFunction<AccountUpdateMutation, AccountUpdateMutationVariables>;

/**
 * __useAccountUpdateMutation__
 *
 * To run a mutation, you first call `useAccountUpdateMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountUpdateMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountUpdateMutation, { data, loading, error }] = useAccountUpdateMutation({
 *   variables: {
 *      updateInput: // value for 'updateInput'
 *   },
 * });
 */
export function useAccountUpdateMutation(baseOptions?: Apollo.MutationHookOptions<AccountUpdateMutation, AccountUpdateMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountUpdateMutation, AccountUpdateMutationVariables>(AccountUpdateDocument, options);
      }
export type AccountUpdateMutationHookResult = ReturnType<typeof useAccountUpdateMutation>;
export type AccountUpdateMutationResult = Apollo.MutationResult<AccountUpdateMutation>;
export type AccountUpdateMutationOptions = Apollo.BaseMutationOptions<AccountUpdateMutation, AccountUpdateMutationVariables>;
export const AccountUpdatePasswordDocument = gql`
    mutation AccountUpdatePassword($updateInput: AccountInfoUpdatePasswordInput!) {
  accountUpdatePassword(updateInput: $updateInput) {
    response {
      code
      success
      message
      version
    }
    pageInfo {
      page_info_count
    }
  }
}
    `;
export type AccountUpdatePasswordMutationFn = Apollo.MutationFunction<AccountUpdatePasswordMutation, AccountUpdatePasswordMutationVariables>;

/**
 * __useAccountUpdatePasswordMutation__
 *
 * To run a mutation, you first call `useAccountUpdatePasswordMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useAccountUpdatePasswordMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [accountUpdatePasswordMutation, { data, loading, error }] = useAccountUpdatePasswordMutation({
 *   variables: {
 *      updateInput: // value for 'updateInput'
 *   },
 * });
 */
export function useAccountUpdatePasswordMutation(baseOptions?: Apollo.MutationHookOptions<AccountUpdatePasswordMutation, AccountUpdatePasswordMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<AccountUpdatePasswordMutation, AccountUpdatePasswordMutationVariables>(AccountUpdatePasswordDocument, options);
      }
export type AccountUpdatePasswordMutationHookResult = ReturnType<typeof useAccountUpdatePasswordMutation>;
export type AccountUpdatePasswordMutationResult = Apollo.MutationResult<AccountUpdatePasswordMutation>;
export type AccountUpdatePasswordMutationOptions = Apollo.BaseMutationOptions<AccountUpdatePasswordMutation, AccountUpdatePasswordMutationVariables>;
export const MovieDetailsDocument = gql`
    query MovieDetails($filterInput: MovieInfoFilterInput) {
  movieInfo(filterInput: $filterInput) {
    response {
      code
      message
      success
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      imdb_id
      title
      popular_id
      genres
      cast
      casts {
        id
        head_shot
        name
        imdb_id
      }
      plot
      rating
      release_date
      run_times
      trailer_link
      full_cover
      cover
      votes
      year
      download_1080p_url
      download_720p_url
      download_480p_url
      videos
    }
  }
}
    `;

/**
 * __useMovieDetailsQuery__
 *
 * To run a query within a React component, call `useMovieDetailsQuery` and pass it any options that fit your needs.
 * When your component renders, `useMovieDetailsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useMovieDetailsQuery({
 *   variables: {
 *      filterInput: // value for 'filterInput'
 *   },
 * });
 */
export function useMovieDetailsQuery(baseOptions?: Apollo.QueryHookOptions<MovieDetailsQuery, MovieDetailsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<MovieDetailsQuery, MovieDetailsQueryVariables>(MovieDetailsDocument, options);
      }
export function useMovieDetailsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<MovieDetailsQuery, MovieDetailsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<MovieDetailsQuery, MovieDetailsQueryVariables>(MovieDetailsDocument, options);
        }
export type MovieDetailsQueryHookResult = ReturnType<typeof useMovieDetailsQuery>;
export type MovieDetailsLazyQueryHookResult = ReturnType<typeof useMovieDetailsLazyQuery>;
export type MovieDetailsQueryResult = Apollo.QueryResult<MovieDetailsQuery, MovieDetailsQueryVariables>;
export const MovieDownloadDocument = gql`
    mutation MovieDownload($searchInput: [MovieInfoDownloadInput]) {
  movieDownload(searchInput: $searchInput) {
    response {
      code
      success
      message
      version
    }
  }
}
    `;
export type MovieDownloadMutationFn = Apollo.MutationFunction<MovieDownloadMutation, MovieDownloadMutationVariables>;

/**
 * __useMovieDownloadMutation__
 *
 * To run a mutation, you first call `useMovieDownloadMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useMovieDownloadMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [movieDownloadMutation, { data, loading, error }] = useMovieDownloadMutation({
 *   variables: {
 *      searchInput: // value for 'searchInput'
 *   },
 * });
 */
export function useMovieDownloadMutation(baseOptions?: Apollo.MutationHookOptions<MovieDownloadMutation, MovieDownloadMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<MovieDownloadMutation, MovieDownloadMutationVariables>(MovieDownloadDocument, options);
      }
export type MovieDownloadMutationHookResult = ReturnType<typeof useMovieDownloadMutation>;
export type MovieDownloadMutationResult = Apollo.MutationResult<MovieDownloadMutation>;
export type MovieDownloadMutationOptions = Apollo.BaseMutationOptions<MovieDownloadMutation, MovieDownloadMutationVariables>;
export const MoviePopularDocument = gql`
    query MoviePopular($pageInfo: MovieInfoPageInfoInput) {
  movieInfo(pageInfo: $pageInfo) {
    response {
      code
      message
      success
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      imdb_id
      title
      popular_id
      full_cover
      cover
      trailer_link
      download_1080p_url
      download_720p_url
      download_480p_url
      plot
    }
  }
}
    `;

/**
 * __useMoviePopularQuery__
 *
 * To run a query within a React component, call `useMoviePopularQuery` and pass it any options that fit your needs.
 * When your component renders, `useMoviePopularQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useMoviePopularQuery({
 *   variables: {
 *      pageInfo: // value for 'pageInfo'
 *   },
 * });
 */
export function useMoviePopularQuery(baseOptions?: Apollo.QueryHookOptions<MoviePopularQuery, MoviePopularQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<MoviePopularQuery, MoviePopularQueryVariables>(MoviePopularDocument, options);
      }
export function useMoviePopularLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<MoviePopularQuery, MoviePopularQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<MoviePopularQuery, MoviePopularQueryVariables>(MoviePopularDocument, options);
        }
export type MoviePopularQueryHookResult = ReturnType<typeof useMoviePopularQuery>;
export type MoviePopularLazyQueryHookResult = ReturnType<typeof useMoviePopularLazyQuery>;
export type MoviePopularQueryResult = Apollo.QueryResult<MoviePopularQuery, MoviePopularQueryVariables>;
export const MovieUpdateDocument = gql`
    mutation MovieUpdate($movieInfoId: Int!) {
  movieUpdate(movie_info_id: $movieInfoId) {
    response {
      code
      success
      message
      version
    }
  }
}
    `;
export type MovieUpdateMutationFn = Apollo.MutationFunction<MovieUpdateMutation, MovieUpdateMutationVariables>;

/**
 * __useMovieUpdateMutation__
 *
 * To run a mutation, you first call `useMovieUpdateMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useMovieUpdateMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [movieUpdateMutation, { data, loading, error }] = useMovieUpdateMutation({
 *   variables: {
 *      movieInfoId: // value for 'movieInfoId'
 *   },
 * });
 */
export function useMovieUpdateMutation(baseOptions?: Apollo.MutationHookOptions<MovieUpdateMutation, MovieUpdateMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<MovieUpdateMutation, MovieUpdateMutationVariables>(MovieUpdateDocument, options);
      }
export type MovieUpdateMutationHookResult = ReturnType<typeof useMovieUpdateMutation>;
export type MovieUpdateMutationResult = Apollo.MutationResult<MovieUpdateMutation>;
export type MovieUpdateMutationOptions = Apollo.BaseMutationOptions<MovieUpdateMutation, MovieUpdateMutationVariables>;
export const ShowsDetailsDocument = gql`
    query ShowsDetails($filterInput: ShowsInfoFilterInput) {
  showsInfo(filterInput: $filterInput) {
    response {
      code
      message
      success
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      imdb_id
      title
      popular_id
      full_cover
      cover
      genres
      plot
      cast
      casts {
        id
        head_shot
        name
        imdb_id
      }
      trailer_link
      release_date
      total_seasons
      total_episodes
      videos
      shows_season {
        id
        season
        shows_episode {
          id
          season
          episode
          shows_info_id
          shows_season_id
          download_1080p_url
          download_720p_url
          download_480p_url
          cover
          full_cover
        }
      }
    }
  }
}
    `;

/**
 * __useShowsDetailsQuery__
 *
 * To run a query within a React component, call `useShowsDetailsQuery` and pass it any options that fit your needs.
 * When your component renders, `useShowsDetailsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useShowsDetailsQuery({
 *   variables: {
 *      filterInput: // value for 'filterInput'
 *   },
 * });
 */
export function useShowsDetailsQuery(baseOptions?: Apollo.QueryHookOptions<ShowsDetailsQuery, ShowsDetailsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<ShowsDetailsQuery, ShowsDetailsQueryVariables>(ShowsDetailsDocument, options);
      }
export function useShowsDetailsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<ShowsDetailsQuery, ShowsDetailsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<ShowsDetailsQuery, ShowsDetailsQueryVariables>(ShowsDetailsDocument, options);
        }
export type ShowsDetailsQueryHookResult = ReturnType<typeof useShowsDetailsQuery>;
export type ShowsDetailsLazyQueryHookResult = ReturnType<typeof useShowsDetailsLazyQuery>;
export type ShowsDetailsQueryResult = Apollo.QueryResult<ShowsDetailsQuery, ShowsDetailsQueryVariables>;
export const ShowsDownloadDocument = gql`
    mutation ShowsDownload($searchInput: [ShowsDownloadInput]) {
  showsDownload(searchInput: $searchInput) {
    response {
      code
      success
      message
      version
    }
  }
}
    `;
export type ShowsDownloadMutationFn = Apollo.MutationFunction<ShowsDownloadMutation, ShowsDownloadMutationVariables>;

/**
 * __useShowsDownloadMutation__
 *
 * To run a mutation, you first call `useShowsDownloadMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useShowsDownloadMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [showsDownloadMutation, { data, loading, error }] = useShowsDownloadMutation({
 *   variables: {
 *      searchInput: // value for 'searchInput'
 *   },
 * });
 */
export function useShowsDownloadMutation(baseOptions?: Apollo.MutationHookOptions<ShowsDownloadMutation, ShowsDownloadMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<ShowsDownloadMutation, ShowsDownloadMutationVariables>(ShowsDownloadDocument, options);
      }
export type ShowsDownloadMutationHookResult = ReturnType<typeof useShowsDownloadMutation>;
export type ShowsDownloadMutationResult = Apollo.MutationResult<ShowsDownloadMutation>;
export type ShowsDownloadMutationOptions = Apollo.BaseMutationOptions<ShowsDownloadMutation, ShowsDownloadMutationVariables>;
export const ShowsEpisodeDetailsDocument = gql`
    query ShowsEpisodeDetails($filterInput: ShowsEpisodeFilterInput) {
  showsEpisode(filterInput: $filterInput) {
    response {
      code
      message
      success
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      imdb_id
      shows_imdb_id
      shows_info_id
      shows_season_id
      title
      season
      episode
      rating
      plot
      release_date
      download_1080p_url
      download_720p_url
      download_480p_url
      cover
      full_cover
      run_times
    }
  }
}
    `;

/**
 * __useShowsEpisodeDetailsQuery__
 *
 * To run a query within a React component, call `useShowsEpisodeDetailsQuery` and pass it any options that fit your needs.
 * When your component renders, `useShowsEpisodeDetailsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useShowsEpisodeDetailsQuery({
 *   variables: {
 *      filterInput: // value for 'filterInput'
 *   },
 * });
 */
export function useShowsEpisodeDetailsQuery(baseOptions?: Apollo.QueryHookOptions<ShowsEpisodeDetailsQuery, ShowsEpisodeDetailsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<ShowsEpisodeDetailsQuery, ShowsEpisodeDetailsQueryVariables>(ShowsEpisodeDetailsDocument, options);
      }
export function useShowsEpisodeDetailsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<ShowsEpisodeDetailsQuery, ShowsEpisodeDetailsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<ShowsEpisodeDetailsQuery, ShowsEpisodeDetailsQueryVariables>(ShowsEpisodeDetailsDocument, options);
        }
export type ShowsEpisodeDetailsQueryHookResult = ReturnType<typeof useShowsEpisodeDetailsQuery>;
export type ShowsEpisodeDetailsLazyQueryHookResult = ReturnType<typeof useShowsEpisodeDetailsLazyQuery>;
export type ShowsEpisodeDetailsQueryResult = Apollo.QueryResult<ShowsEpisodeDetailsQuery, ShowsEpisodeDetailsQueryVariables>;
export const ShowsEpisodeUpdateDocument = gql`
    mutation ShowsEpisodeUpdate($showsEpisodeId: Int!) {
  showsEpisodeUpdate(shows_episode_id: $showsEpisodeId) {
    response {
      code
      success
      message
      version
    }
  }
}
    `;
export type ShowsEpisodeUpdateMutationFn = Apollo.MutationFunction<ShowsEpisodeUpdateMutation, ShowsEpisodeUpdateMutationVariables>;

/**
 * __useShowsEpisodeUpdateMutation__
 *
 * To run a mutation, you first call `useShowsEpisodeUpdateMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useShowsEpisodeUpdateMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [showsEpisodeUpdateMutation, { data, loading, error }] = useShowsEpisodeUpdateMutation({
 *   variables: {
 *      showsEpisodeId: // value for 'showsEpisodeId'
 *   },
 * });
 */
export function useShowsEpisodeUpdateMutation(baseOptions?: Apollo.MutationHookOptions<ShowsEpisodeUpdateMutation, ShowsEpisodeUpdateMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<ShowsEpisodeUpdateMutation, ShowsEpisodeUpdateMutationVariables>(ShowsEpisodeUpdateDocument, options);
      }
export type ShowsEpisodeUpdateMutationHookResult = ReturnType<typeof useShowsEpisodeUpdateMutation>;
export type ShowsEpisodeUpdateMutationResult = Apollo.MutationResult<ShowsEpisodeUpdateMutation>;
export type ShowsEpisodeUpdateMutationOptions = Apollo.BaseMutationOptions<ShowsEpisodeUpdateMutation, ShowsEpisodeUpdateMutationVariables>;
export const ShowsPopularDocument = gql`
    query ShowsPopular($pageInfo: ShowsInfoPageInfoInput) {
  showsInfo(pageInfo: $pageInfo) {
    response {
      code
      message
      success
      version
    }
    pageInfo {
      page_info_count
    }
    result {
      id
      imdb_id
      title
      popular_id
      full_cover
      cover
      trailer_link
      shows_season {
        id
        shows_episode {
          id
          shows_info_id
          shows_season_id
          download_1080p_url
          download_720p_url
          download_480p_url
        }
      }
    }
  }
}
    `;

/**
 * __useShowsPopularQuery__
 *
 * To run a query within a React component, call `useShowsPopularQuery` and pass it any options that fit your needs.
 * When your component renders, `useShowsPopularQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useShowsPopularQuery({
 *   variables: {
 *      pageInfo: // value for 'pageInfo'
 *   },
 * });
 */
export function useShowsPopularQuery(baseOptions?: Apollo.QueryHookOptions<ShowsPopularQuery, ShowsPopularQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<ShowsPopularQuery, ShowsPopularQueryVariables>(ShowsPopularDocument, options);
      }
export function useShowsPopularLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<ShowsPopularQuery, ShowsPopularQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<ShowsPopularQuery, ShowsPopularQueryVariables>(ShowsPopularDocument, options);
        }
export type ShowsPopularQueryHookResult = ReturnType<typeof useShowsPopularQuery>;
export type ShowsPopularLazyQueryHookResult = ReturnType<typeof useShowsPopularLazyQuery>;
export type ShowsPopularQueryResult = Apollo.QueryResult<ShowsPopularQuery, ShowsPopularQueryVariables>;
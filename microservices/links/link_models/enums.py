# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from enum import Enum

# Usage: Set the 'is_gql' property to true to load the enum into graphql. 
#        Enum class must match name defined on the ariadne schema


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

# General Enums
class OrderByEnum(Enum):
    ASC = "asc"
    DESC = "desc"
    
    @property
    def is_gql():
        return True
    
class SortByEnum(Enum):
    First = "1"

class ServiceNameEnum(Enum):
    MOVIEFAV = "moviefav"
    ANIMESTAT = "animestat"
    LABELLE = "labelle"
    UVGRETREATS = "uvgretreats"
    ALLNATION = "allnation"
    PROMEDEXPRESS= "promedexpress"
    SUMEXUS = "sumexus"
    THEATER = "theater"
    MONXT = "monxt"

class SagaStateStatusEnum(Enum):
    NOT_STARTED = "not_started"
    SUCCESS = "success"
    FAILURE = "failure"
    

class SchemaTypeEnum(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    
class ServiceTypeEnum(Enum):
    MICROSERVICE = "microservice"
    MODULE = "module"
    LINKS = "links"
    
class AccountRoleEnum(Enum):
    ADMIN = "ADMIN"
    COMPANY = "COMPANY"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    CUSTOMER = "CUSTOMER"
    GUEST = "GUEST"
    
    @property
    def is_gql():
        return True
    
    @property
    def is_database():
        return True


# Account Enums
class AccountRegistrationEnum(Enum):
    NOT_COMPLETE = "not_complete"
    COMPLETE = "complete"
    WAITING = "waiting"
    APPROVED = "approved"
    
    @property
    def is_gql():
        return True
    
    @property
    def is_database():
        return True

class AccountStatusEnum(Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    DELETED = "deleted"
    
    @property
    def is_gql():
        return True
    
    @property
    def is_database():
        return True

class AccountInfoSortByEnum(Enum):
    ID = "id"
    
    @property
    def is_gql():
        return True
    
class AccountCompanySortByEnum(Enum):
    ID = "id"
    NAME= "name"
    
    @property
    def is_gql():
        return True

class AuthenticationTokenTypeEnum(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    CSRF_TOKEN = "csrf_token"
    OTHER = "other"
    
    @property
    def is_gql():
        return True
    
class AccountBusinessTypeEnum(Enum):
    SOLE_PROPRIETARY = "SOLE_PROPRIETARY"
    UNINCORPORATED_ASSOCIATION = "UNINCORPORATED_ASSOCIATION"
    TRUST = "TRUST"
    CORPORATION = "CORPORATION"
    PUBLICLY_TRADED_CORPORATION = "PUBLICLY_TRADED_CORPORATION"
    NON_PROFIT = "NON_PROFIT"
    LLC = "LLC"
    PARTNERSHIPS_LP_AND_LLP = "PARTNERSHIPS_LP_AND_LLP"

    @property
    def is_gql():
        return True
    
    @property
    def is_database():
        return True

class AccountClassificationEnum(Enum):
    RETAIL = "RETAIL"
    NON_PROFIT = "NON_PROFIT"
    OTHER = "OTHER"
    
    @property
    def is_gql():
        return True
    
    @property
    def is_database():
        return True

class AccountStoreSortByEnum(Enum):
    ID = "id"
    NAME = "name"
    
    @property
    def is_gql():
        return True
    
class AccountStoreEmployeeSortByEnum(Enum):
    ID = "id"
    
    @property
    def is_gql():
        return True


# Movie Enums
class MovieStatusEnum(Enum):
    COMPLETED = "completed"
    NOT_COMPLETED = "not_completed"

    @property
    def is_gql():
        return True


class MovieInfoSortByEnum(Enum):
    ID = "id"
    IMDB_ID = "imdb_id"
    TITLE = "title"
    POPULAR_ID = "popular_id"
    
    @property
    def is_gql():
        return True


class MovieSearchEnum(Enum):
    SEARCH_TITLE = "search_title"
    SEARCH_IMDB_ID = "search_imdb_id"
    
class ProviderTypeEnum(Enum):
    NETFLIX = "netflix"
    DISNEY = "disney"
    HULU = "hulu"
    AMAZON = "amazon"
    APPLETV = "appletv"
    
    @property
    def is_gql():
        return True
    
class ImportProviderTypeEnum(ExtendedEnum):
    NETFLIX = "NF"
    DISNEY = "DSNP"
    HULU = "HULU"
    AMAZON = "AMZN"
    APPLETV = "ATVP"
    HBO_MAX = "HMAX"

class ShowsInfoSortByEnum(Enum):
    ID = "id"
    IMDB_ID = "imdb_id"
    TITLE = "title"
    POPULAR_ID = "popular_id"

    @property
    def is_gql():
        return 
    
class ShowsSeasonSortByEnum(Enum):
    ID = "id"

    @property
    def is_gql():
        return True
    
class ShowsEpisodeSortByEnum(Enum):
    ID = "id"

    @property
    def is_gql():
        return True

class PersonInfoSortByEnum(Enum):
    ID = "id"

    @property
    def is_gql():
        return True


class DownloadLocationEnum(Enum):
    DATABASE = "database"
    REDIS = "redis"
    IMDB = "imdb"
    IMDB_ALL = "imdb_all"

    @property
    def is_gql():
        return True

class StripeMethodEnum(Enum):
    CREATE_CUSTOMER = "create_customer"
    CREATE_EPHEMERAL_KEY = "create_ephemeral_key"
    CREATE_INTENT = "create_intent"
    CONFIRM_INTENT = "confirm_intent"
    CAPTURE_INTENT = "capture_intent"
    RETRIEVE_INTENT = "revert_intent"
    TRANSFER_INTENT = "transfer_intent"
    REFUND_INTENT = "refund_intent"
    PAYOUT = "payout"
    CANCEL_INTENT = "cancel_intent"
    RETRIEVE_ACCOUNT = "retrieve_account"
    UPDATE_INTENT = "update_intent"
    PAYOUT_LIST = "payout_list"
    PAYOUT_TRANSACTION_LIST = "payout_transaction_list"
    VERIFICATION_ID_CHECK = "verification_id_check"

class NotifyTemplateEnum(Enum):
    LABELLE_APPOINTMENT = "labelle_appointment"
    ALL_NATION_CONTACT = "all_nation_contact"
    LABELLE_CONTACT = "labelle_contact"
    LABELLE_RSVP = "labelle_rsvp"
    PROMEDEXPRESS_CONTACT = "promedexpress_contact"
    SUMEXUS_CONTACT = "sumexus_contact"
    PROMEDEXPRESS_REQUEST_TRANSPORT = "promedexpress_request_transport"
    SUMEXUS_REQUEST_TRANSPORT = "sumexus_request_transport"
    
    @property
    def is_gql():
        return True


class RedisDatabaseEnum(Enum):
    ACCOUNT = "account"
    MOVIE = "movie"
    NOTIFICATIONS = "notifications"
    PERSON = "person"
    SHOWS = "shows"
    DEFAULT = "default"
    
    @property
    def is_gql():
        return True

class NotificationsSagaStateSortByEnum(Enum):
    ID = "id"
    
    @property
    def is_gql():
        return True
    
class NotifyStatusEnum(Enum):
    OPEN = "open"
    CLOSED = "closed"
    
    @property
    def is_gql():
        return True

from ariadne import QueryType
from api.account_me_query import AccountMeQuery


class Queries:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    query = QueryType()
    
    @query.field("accountMe")
    def resolve_account_me(_, info: object) -> dict:
        return AccountMeQuery.account_me(_, info)
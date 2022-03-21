from ariadne import QueryType
from api.example_hello_query import ExampleHelloQuery


class Queries:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    query = QueryType()
    
    @query.field("exampleHelloQuery")
    def resolve_example_hello_query(_, info):
        return ExampleHelloQuery.example_hello_query(_, info)
from ariadne import MutationType
from api.example_hello_mutation import ExampleHelloMutation


class Mutations:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    mutation = MutationType()

    @mutation.field("exampleHelloMutation")
    def resolve_example_hello_mutation(_, info):
        return ExampleHelloMutation.example_hello_mutation(_, info)
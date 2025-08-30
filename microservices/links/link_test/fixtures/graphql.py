# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from graphql import FieldNode, GraphQLField, GraphQLObjectType, GraphQLResolveInfo, GraphQLSchema, GraphQLString, OperationDefinitionNode, ResponsePath, execute_sync, parse
from typing import cast
from monxt.src.controller.controller_api import APISchema

# grabbed from https://github.com/graphql-python/graphql-core/blob/a1c15d128fcb6e981ba298419b6e66cf87efc17a/tests/execution/test_executor.py
def create_gql_info(context_value, result_context: str = None):
  resolved_infos = []

  def resolve(_obj, info):
    resolved_infos.append(info)

  test_type = GraphQLObjectType(
    "Test", {"test": GraphQLField(GraphQLString, resolve=resolve)}
  )

  schema = GraphQLSchema(test_type)

  result_context = result_context or "{ result: test }"

  document = parse(f"""query ($var: String) {result_context}""")
  root_value = {"root": "val"}
  variable_values = {"var": "abc"}
  execute_sync(schema, document, root_value, variable_values=variable_values)

  operation = cast(OperationDefinitionNode, document.definitions[0])
  assert operation and operation.kind == "operation_definition"
  field = cast(FieldNode, operation.selection_set.selections)

  return GraphQLResolveInfo(
    field_name="test",
    field_nodes=field,
    return_type=GraphQLString,
    parent_type=cast(GraphQLObjectType, schema.query_type),
    path=ResponsePath(None, "result", "Test"),
    schema=schema,
    fragments={},
    root_value=root_value,
    operation=operation,
    variable_values=variable_values,
    context=context_value,
    is_awaitable=None,
  )

@pytest.fixture
def gql_info():
  return create_gql_info

@pytest.fixture
def private_schema():
  return APISchema.private_schema

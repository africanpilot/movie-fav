# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from link_lib.microservice_request import LinkRequest
from person.src.models.person_info import PersonInfo, PersonInfoCreate, PersonInfoRead, PersonInfoUpdate, PersonInfoResponses
from person.src.models.person_saga_state import PersonSagaState, PersonSagaStateCreate, PersonSagaStateRead, PersonSagaStateUpdate


class PersonModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def person_info(self):
        return PersonInfo()
    
    @cached_property
    def person_info_create(self):
        return PersonInfoCreate()
    
    @cached_property
    def person_info_read(self):
        return PersonInfoRead()

    @cached_property
    def person_info_update(self):
        return PersonInfoUpdate()
    
    @cached_property
    def person_info_response(self):
        return PersonInfoResponses()

    @cached_property
    def person_saga_state(self):
        return PersonSagaState()
    
    @cached_property
    def person_saga_state_create(self):
        return PersonSagaStateCreate()

    @cached_property
    def person_saga_state_read(self):
        return PersonSagaStateRead()
    
    @cached_property
    def person_saga_state_update(self):
        return PersonSagaStateUpdate()

from test.domain.common import FakeCeleryApp
from unittest.mock import MagicMock

from link_lib.saga_framework.async_saga import AsyncSaga, AsyncStep
from link_lib.saga_framework.base_saga import SyncStep


def test_saga_run_success():
    step_1_compensation_mock = MagicMock()

    step_2_action_mock = MagicMock()
    step_2_on_success_mock = MagicMock()
    step_2_on_failure_mock = MagicMock()

    on_saga_success_mock = MagicMock()
    on_saga_failure_mock = MagicMock()

    step_3_action_mock = MagicMock()

    class Saga(AsyncSaga):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.steps = [
                SyncStep(name="step_1", compensation=step_1_compensation_mock),
                AsyncStep(
                    name="step_2",
                    action=step_2_action_mock,
                    queue="some_queue",
                    base_task_name="step_2_task",
                    on_success=step_2_on_success_mock,
                    on_failure=step_2_on_failure_mock,
                ),
                SyncStep(name="step_3", action=step_3_action_mock),
            ]

        on_saga_success = on_saga_success_mock
        on_saga_failure = on_saga_failure_mock

    fake_celery_app = FakeCeleryApp()

    # register 'response' Celery tasks handlers.
    # It's crucial part to make Saga Orchestrator
    #  launch next saga step (or rollback saga) when Saga Handler service
    #  returns result (via Celery task)
    # noinspection PyTypeChecker
    Saga.register_async_step_handlers(fake_celery_app)

    # Preraration ended. Launching a test

    fake_saga_id = 123

    # launch saga
    Saga(fake_celery_app, fake_saga_id).execute()

    # check that first and second steps executed,
    #   but not third one (it will be run after AsyncStep 2 finishes)
    step_2_action_mock.assert_called_once()
    step_3_action_mock.assert_not_called()

    # emulate that Step Handler service successfully handled step 2
    #  and triggered corresponding Celery task on Saga Orchestrator
    celery_task_params = dict(saga_id=fake_saga_id, payload={"ticket_id": "111"})
    fake_celery_app.emulate_celery_task_launch("step_2_task.response.success", **celery_task_params)

    # finally, validate
    step_2_on_success_mock.assert_called_once()
    on_saga_success_mock.assert_called_once()
    step_3_action_mock.assert_called_once()

    step_1_compensation_mock.assert_not_called()
    on_saga_failure_mock.assert_not_called()
    on_saga_failure_mock.assert_not_called()


def test_saga_run_failure():
    step_1_compensation_mock = MagicMock()

    step_2_action_mock = MagicMock()
    step_2_on_success_mock = MagicMock()
    step_2_on_failure_mock = MagicMock()

    on_saga_success_mock = MagicMock()
    on_saga_failure_mock = MagicMock()

    step_3_action_mock = MagicMock()

    class Saga(AsyncSaga):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.steps = [
                SyncStep(name="step_1", compensation=step_1_compensation_mock),
                AsyncStep(
                    name="step_2",
                    action=step_2_action_mock,
                    queue="some_queue",
                    base_task_name="step_2_task",
                    on_success=step_2_on_success_mock,
                    on_failure=step_2_on_failure_mock,
                ),
                SyncStep(name="step_3", action=step_3_action_mock),
            ]

        on_saga_success = on_saga_success_mock
        on_saga_failure = on_saga_failure_mock

    fake_celery_app = FakeCeleryApp()

    # register 'response' Celery tasks handlers.
    # It's crucial part to make Saga Orchestrator
    #  launch next saga step (or rollback saga) when Saga Handler service
    #  returns result (via Celery task)
    # noinspection PyTypeChecker
    Saga.register_async_step_handlers(fake_celery_app)

    # Preraration ended. Launching a test

    fake_saga_id = 123

    # launch saga
    Saga(fake_celery_app, fake_saga_id).execute()

    # validate that step 3 doesn't start until AsyncStep 2 finishes
    step_3_action_mock.assert_not_called()

    # emulate that Step Handler service successfully handled step 2
    #  and triggered corresponding Celery task on Saga Orchestrator
    celery_task_params = dict(saga_id=fake_saga_id, payload={"ticket_id": "111"})
    fake_celery_app.emulate_celery_task_launch("step_2_task.response.failure", **celery_task_params)

    # finally, validate
    step_2_on_failure_mock.assert_called_once()
    step_1_compensation_mock.assert_called_once()
    on_saga_failure_mock.assert_called_once()

    step_2_on_success_mock.assert_not_called()
    step_3_action_mock.assert_not_called()
    on_saga_success_mock.assert_not_called()

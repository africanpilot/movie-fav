# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property

import stripe
from link_config.config import LOGLEVEL, STRIPE_API_KEY
from link_lib.microservice_response import LinkResponse
from link_models.enums import StripeMethodEnum


class LinkStripe(LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def stripe_api(self):
        stripe.api_key = STRIPE_API_KEY
        stripe.log = LOGLEVEL.lower()
        return stripe

    def _stripe_create_customer(self, payment: dict):
        return self.stripe_api.Customer.create(email=payment["email"], description="TrackstarUser")  # must be an email

    def _stripe_ephemeral_key(self, payment: dict):
        return self.stripe_api.EphemeralKey.create(
            customer=payment["customer_id"],
            stripe_version="2020-08-27",
        )

    def _stripe_payment_intent(self, payment: dict):
        return self.stripe_api.PaymentIntent.create(
            amount=int(payment["amount"] * 100),  # charge is in cents
            currency="usd",
            customer=payment.get("customer_id"),
            capture_method="automatic",
            # payment_method_types=['card'], # ex: card
            # payment_method_options={
            #     'card': {
            #     'capture_method': 'automatic',
            #     }
            # },
            # payment_method=payment.get("payment_method"),
            metadata=payment.get("metadata", {}),
        )

    def _stripe_payment_capture_intent(self, payment: dict):
        return self.stripe_api.PaymentIntent.confirm(
            payment["intent_id"],
            payment_method=payment.get("payment_method"),
            return_url=payment.get("return_url"),
        )

    def _stripe_payment_capture(self, payment: dict):
        return self.stripe_api.PaymentIntent.capture(
            payment["intent_id"],
        )

    def _stripe_payment_retrieve(self, payment: dict):
        return self.stripe_api.PaymentIntent.retrieve(
            payment["intent_id"],
        )

    def _stripe_payment_cancel(self, payment: dict):
        """
        Can't be canceled when PaymentIntent can't be canceled while it's actively processing or after it has succeeded
        """
        return self.stripe_api.PaymentIntent.cancel(
            payment["intent_id"],
        )

    def _stripe_transfer_payment(self, payment: dict):
        return self.stripe_api.Transfer.create(
            amount=int(payment["amount"] * 100),  # charge is in cents
            currency="usd",
            destination=payment["destination"],
        )

    def _stripe_payment_refund(self, payment: dict):
        return self.stripe_api.Refund.create(
            payment_intent=payment["intent_id"],
            amount=int(payment["amount"] * 100),  # charge is in cents
        )

    def _stripe_payment_payout(self, payment: dict):
        return self.stripe_api.Payout.create(
            amount=int(payment["amount"] * 100),
            currency="usd",
            stripe_account=payment["stripe_id"],
        )

    def _stripe_account_retrieve(self, payment: dict):
        return self.stripe_api.Account.retrieve(
            payment["account_id"],
        )

    def _stripe_intent_update(self, payment: dict):
        return self.stripe_api.PaymentIntent.modify(payment["intent_id"], amount=payment["amount"])

    def _stripe_payment_payout_list(self, payment: dict):
        return self.stripe_api.Payout.list(
            limit=10,
            stripe_account=payment["stripe_id"],
        )

    def _stripe_payment_balance_transaction_payout_list(self, payment: dict):
        return self.stripe_api.BalanceTransaction.list(
            limit=payment["first"],
            starting_after=(
                payment["startingAfter"] if "startingAfter" in payment and payment["startingAfter"] else None
            ),
            ending_before=payment["endingBefore"] if "endingBefore" in payment and payment["endingBefore"] else None,
            stripe_account=payment["stripe_id"],
            type="payout",
        )

    def _stripe_payment_balance_transaction_payout_transaction_list(self, payment: dict):
        return self.stripe_api.BalanceTransaction.list(
            stripe_account=payment["stripe_id"], payout=payment["payout_id"], type="payment"
        )

    def _stripe_payment_verification_session(self, payment: dict):
        return self.stripe_api.identity.VerificationSession.create(
            type="document",
            stripe_account=payment["stripe_id"],
            options={
                "document": {
                    "allowed_types": ["driving_license", "id_card"],
                    "require_id_number": True,
                    "require_live_capture": True,
                }
            },
        )

    def _get_method_handlers(self):
        """Returns a dictionary mapping StripeMethodEnum values to their handler methods."""
        return {
            StripeMethodEnum.CREATE_CUSTOMER: self._stripe_create_customer,
            StripeMethodEnum.CREATE_EPHEMERAL_KEY: self._stripe_ephemeral_key,
            StripeMethodEnum.CREATE_INTENT: self._stripe_payment_intent,
            StripeMethodEnum.CONFIRM_INTENT: self._stripe_payment_capture_intent,
            StripeMethodEnum.CAPTURE_INTENT: self._stripe_payment_capture,
            StripeMethodEnum.RETRIEVE_INTENT: self._stripe_payment_retrieve,
            StripeMethodEnum.TRANSFER_INTENT: self._stripe_transfer_payment,
            StripeMethodEnum.REFUND_INTENT: self._stripe_payment_refund,
            StripeMethodEnum.PAYOUT: self._stripe_payment_payout,
            StripeMethodEnum.CANCEL_INTENT: self._stripe_payment_cancel,
            StripeMethodEnum.RETRIEVE_ACCOUNT: self._stripe_account_retrieve,
            StripeMethodEnum.UPDATE_INTENT: self._stripe_intent_update,
            StripeMethodEnum.PAYOUT_LIST: self._stripe_payment_balance_transaction_payout_list,
            StripeMethodEnum.PAYOUT_TRANSACTION_LIST: self._stripe_payment_balance_transaction_payout_transaction_list,
            StripeMethodEnum.VERIFICATION_ID_CHECK: self._stripe_payment_verification_session,
        }

    def _handle_stripe_exceptions(self, e):
        """Handle different types of Stripe exceptions."""
        if isinstance(e, self.stripe_api.error.CardError):
            self.http_400_bad_request_response("Stripe Card Error")
        elif isinstance(e, self.stripe_api.error.RateLimitError):
            # Too many requests made to the API too quickly
            self.http_500_internal_server_error("Stripe Rate Limit Error")
        elif isinstance(e, self.stripe_api.error.InvalidRequestError):
            # Invalid parameters were supplied to Stripe's API
            self.http_400_bad_request_response("Stripe Invalid Input Error")
        elif isinstance(e, self.stripe_api.error.AuthenticationError):
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            self.http_401_unauthorized_response("Stripe Authentication Error")
        elif isinstance(e, self.stripe_api.error.APIConnectionError):
            # Network communication with Stripe failed
            self.http_500_internal_server_error("Stripe API Connection Error")
        elif isinstance(e, self.stripe_api.error.StripeError):
            # Display a very generic error to the user, and maybe send
            # yourself an email
            self.http_500_internal_server_error("Stripe Error")
        else:
            self.log.info(f"Stripe unknown Exception: {e}")
            # Something else happened, completely unrelated to Stripe
            self.http_500_internal_server_error("Unknown Error while processing stripe request")

    def stripe_method(self, method: StripeMethodEnum, payment: dict):
        method_handlers = self._get_method_handlers()

        if method not in method_handlers:
            self.http_400_bad_request_response(f"Unsupported stripe method: {method}")
            return None

        try:
            handler = method_handlers[method]
            payment_info = handler(payment)
        except Exception as e:
            self._handle_stripe_exceptions(e)
            return None

        if not payment_info:
            self.http_500_internal_server_error("Stripe did not return payment info")

        return payment_info

    def stripe_connected_account_business(self, data):
        # create Account
        try:
            account_info = self.stripe_api.Account.create(
                type="custom",
                country="US",
                email=data["email"],
                capabilities={
                    "transfers": {"requested": True},
                },
                business_profile={
                    "mcc": data["mcc"],
                    "name": data["dba_name"],
                    "product_description": data["product_description"],
                    "url": data["url"],
                },
                business_type="company",
                tos_acceptance={
                    "date": data["date"],
                    "ip": data["ip"],
                },
                company={
                    "name": data["company_name"],
                    "tax_id": data["tax_id"],
                },
                external_account={
                    "object": "bank_account",
                    "country": "US",
                    "currency": "USD",
                    "account_number": data["account_number"],
                    # "last4": data["last4"], # The last four digits of the bank account number.
                    "account_holder_name": data[
                        "account_holder_name"
                    ],  # The name of the person or business that owns the bank account.
                    "account_holder_type": "company",  # The type of entity that holds the account.
                    # "bank_name": data["bank_name"], # Name of the bank associated with the routing number
                    "routing_number": data["routing_number"],  # The routing transit number for the bank account.
                },
            )
            return {"Success": True, "result": account_info}
        except self.stripe_api.error.CardError:
            return {"Success": False, "result": "Card Error"}
        except self.stripe_api.error.RateLimitError:
            # Too many requests made to the API too quickly
            return {"Success": False, "result": "Rate Limit Error"}
        except self.stripe_api.error.InvalidRequestError:
            # Invalid parameters were supplied to Stripe's API
            return {"Success": False, "result": "Invalid Input Error"}
        except self.stripe_api.error.AuthenticationError:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return {"Success": False, "result": "Authentication Error"}
        except self.stripe_api.error.APIConnectionError:
            # Network communication with Stripe failed
            return {"Success": False, "result": "API Connection Error"}
        except self.stripe_api.error.StripeError:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return {"Success": False, "result": "Stripe Error"}
        except Exception:
            return {"Success": False, "result": "Unknown Error"}

    def stripe_connected_account_mobile_user(self, data):
        # create Account
        try:
            account_info = self.stripe_api.Account.create(
                type="custom",
                country="US",
                email=data["email"],
                capabilities={
                    "transfers": {"requested": True},
                },
                business_profile={
                    "product_description": "Pickup goods from stores as a service",
                },
                business_type="individual",
                tos_acceptance={
                    "date": data["date"],
                    "ip": data["ip"],
                },
                external_account={
                    "object": "bank_account",
                    "country": "US",
                    "currency": "USD",
                    "account_number": data["account_number"],
                    # "last4": data["last4"], # The last four digits of the bank account number.
                    "account_holder_name": data[
                        "account_holder_name"
                    ],  # The name of the person or business that owns the bank account.
                    "account_holder_type": "individual",  # The type of entity that holds the account.
                    # "bank_name": data["bank_name"], # Name of the bank associated with the routing number
                    "routing_number": data["routing_number"],  # The routing transit number for the bank account.
                },
                individual={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "dob": {
                        "day": data["day"],
                        "month": data["month"],
                        "year": data["year"],
                    },
                    "ssn_last_4": data["ssn_last_4"],
                },
            )
            return {"Success": True, "result": account_info}
        except self.stripe_api.error.CardError:
            return {"Success": False, "result": "Card Error"}
        except self.stripe_api.error.RateLimitError:
            # Too many requests made to the API too quickly
            return {"Success": False, "result": "Rate Limit Error"}
        except self.stripe_api.error.InvalidRequestError:
            # Invalid parameters were supplied to Stripe's API
            return {"Success": False, "result": "Invalid Input Error"}
        except self.stripe_api.error.AuthenticationError:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return {"Success": False, "result": "Authentication Error"}
        except self.stripe_api.error.APIConnectionError:
            # Network communication with Stripe failed
            return {"Success": False, "result": "API Connection Error"}
        except self.stripe_api.error.StripeError:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return {"Success": False, "result": "Stripe Error"}
        except Exception:
            return {"Success": False, "result": "Unknown Error"}

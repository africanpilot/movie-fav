# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from link_lib.microservice_response import LinkResponse
from notifications.src.app_lib import config
from twilio.rest import Client, TwilioException


class TwilioHelper(LinkResponse):
    def __init__(self, email: Optional[str], phone: Optional[str], **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.phone = phone
    
    @property
    def twilio_client(self):
        return Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    
    @property
    def twilio_verify_client(self):
        return self.twilio_client.verify.services(config.TWILIO_VERIFY_SERVICE_ID)
    
    @property
    def user_email(self):
        return self.email if config.APP_DEFAULT_ENV == 'prod' else config.APP_DEFAULT_EMAIL
    
    @property
    def user_phone(self):
        return self.phone if config.APP_DEFAULT_ENV == 'prod' else config.APP_DEFAULT_PHONE

    def request_verification_token(self):
        try:
            self.twilio_verify_client.verifications.create(to=self.user_phone, channel='sms')
        except TwilioException:
            self.twilio_verify_client.verifications.create(to=self.user_phone, channel='call')

    def request_verification_token_email(self):
        try:
            self.twilio_verify_client.verifications.create(to=self.user_email, channel='email')
        except TwilioException:
            return False

    def check_verification_token(self, token, phone=None, email=None):
        if phone:
            to_verify = self.user_phone
        
        if email:
            to_verify = self.user_email
        try:
            result = self.twilio_verify_client.verification_checks.create(to=to_verify, code=token)
        except TwilioException:
            return False
        except:
            return False
        return result.status == 'approved'

    def twilio_send_sms(self, msg, templete, resp={}):
        order_id = msg["body"]["order_id"]
        
        try:
            if templete == "NewOrderReceipt":
                body_templete = f"We've received your Noa order #{order_id}"

            if templete == "NewOrderReady":
                store_order_id = msg["body"]["store_order_id"]
                storeName = resp["stores"][0]["storeName"]
                address = resp["stores"][0]["address"]
                body_templete = f"Your Noa order #{store_order_id} from {storeName} is ready for pick-up at {address}."

            if templete in ["OrderModify","OrderRefund"]:
                store_order_id = msg["body"]["store_order_id"]
                storeName = resp["stores"][0]["storeName"]
                body_templete = f"Your Noa order #{store_order_id} from {storeName} has been adjusted."

            self.twilio_client.messages.create(
                from_='+15717079530',
                to=self.user_phone,
                body=body_templete
            )
            self.log.debug(f"Message sent for order #{order_id}")
        except TwilioException:
            self.log.debug(f"Failed to Send Message for order #{order_id}")
            return False

    def twilio_create_binding(self, data):
        # Initialize the client
        binding = self.twilio_client.notify.services(config.TWILIO_NOTIFY_SID).bindings.create(
            identity=data["UserIdentity"],
            binding_type='apn',
            address=data["address"]
        )
        self.log.debug(f"Create Twilio binding: {binding.sid}")

    def twilio_send_push_notification(self, msg, data, resp={}):
        body_templete = "Shop Noa! Earn Labor Coin!"
        # New order Templete
        if data["template"] == "NewOrder":
            order_id = msg["body"]["order_id"]
            body_templete = f"We've received your Noa order #{order_id}"
        
        if data["template"] == "InProgress":
            store_order_id = msg["body"]["store_order_id"]
            storeName = resp["stores"][0]["storeName"]
            body_templete = f"Your Noa store order #{store_order_id} from {storeName} is in progress."

        notification = self.twilio_client.notify.services(config.TWILIO_NOTIFY_SID).notifications.create(
            body=body_templete, 
            identity=[data["user_id"]]
        )
        self.log.debug(f"Create Twilio notification: {notification.sid}")

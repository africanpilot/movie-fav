# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import re
import bcrypt

from link_lib.microservice_response import LinkResponse

class AccountInfoValidate(LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def email_check(self, email: str) -> bool:
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if (re.match(regex, email.lower())) else False

  def hash_password(self, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(int(os.environ["APP_DEFAULT_GEN_SALT_VALUE"])))

  def verify_hash_password(self, password: str, hashed: str) -> None:
    if not bcrypt.checkpw(password, hashed):
      return self.http_401_unauthorized_response(msg="Invalid credentials")

  def password_check(self, password: str) -> bool:
    regex = r"(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?^&])[A-Za-z\d@$!%*^#?&]{8,}$)"
    return True if (re.match(regex, password)) else False

  def validate_email(self, email: str):
    email_valid = self.email_check(email)
    if not email_valid:
      self.http_401_unauthorized_response(msg="Invalid email format")

  def validate_password(self, password: str) -> bool:
    # check password length	
    if len(password) > 64 or len(password) < 8:
      self.http_401_unauthorized_response(msg="Invalid password length")

    # verify password regex
    password_check = self.password_check(password)
    if not password_check:
      self.http_401_unauthorized_response(msg="Failed password criteria")

  def validate_retype_password(self, password, reTypePassword):
    # check reTypePassword Matches password
    if password != reTypePassword:
      self.http_401_unauthorized_response(msg="Invalid password retype")

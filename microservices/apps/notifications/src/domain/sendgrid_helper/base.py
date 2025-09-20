# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
from link_lib.microservice_response import LinkResponse
from notifications.src.app_lib.config import APP_DEFAULT_ENV, APP_SENDGRID_API_KEY, APP_ADDRESS, APP_DEFAULT_EMAIL
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To


class SendgridHelper(LinkResponse):
  def __init__(self, body: dict, template: str, **kwargs):
    super().__init__(**kwargs)
    self.body = body
    self.template = template
    self.message: Mail = None

  @property
  def from_email(self):
    email = APP_DEFAULT_EMAIL
    if APP_DEFAULT_ENV == "prod":
      if self.body.get("service_name") == "theater":
        email = APP_DEFAULT_EMAIL
    return email
  
  @property
  def host(self):
    if APP_DEFAULT_ENV == "prod":
      if self.body.get("service_name") == "theater":
        return "theater.com"
    return "localhost:3000"
  
  @property
  def http_host(self) -> str:
    return "https" if APP_DEFAULT_ENV == "prod" else "http"
  
  @property
  def email_distro(self):
    return [self.body.get("email")]
  
  @property
  def additional_distro(self):
    return []
  
  @property
  def total_email_distro(self):
    return list(set(self.email_distro + self.additional_distro))

  @property
  def send_to_email(self):    
    return [To(em) for em in self.total_email_distro] if APP_DEFAULT_ENV in ["prod"] else [To(APP_DEFAULT_EMAIL)]
    
  def base_message(self):
    self.message = Mail(
      from_email=self.from_email,
      to_emails=self.send_to_email
    )
    
  def verify_email_template(self) -> None:
    token = self.body.get('token')
    email_template = None
    link = f"{self.http_host}://{self.host}/email-confirmation?token={token}"
    self.message.dynamic_template_data = {"tokenLink": link}

    if self.body.get('service_name') == "theater":
      link = f"{self.http_host}://{self.host}/portal/email-confirmation?token={token}"
      email_template = "d-f1f739d6e76c44788a14df0dd059f153"

    self.message.template_id = email_template
    
  def forgot_password_template(self) -> None:
    token = self.body.get('token')
    email_template = None
    link = f"{self.http_host}://{self.host}/change-password?token={token}"
    self.message.dynamic_template_data = {"tokenLink": link}
    
    if self.body.get('service_name') == "theater":
      link = f"{self.http_host}://{self.host}/portal/change-password?token={token}"
      email_template = "d-9ff6287268c44d448cd744cc388cc30b"
      
    self.message.template_id = email_template

  def send_email(self) -> None:
    try:
      sg = SendGridAPIClient(APP_SENDGRID_API_KEY)
      sg.send(self.message)
      self.log.info(f"Sent {self.template} to {self.send_to_email} ")
    except Exception as e:
      self.http_500_internal_server_error(msg=str(e))

  def execute(self) -> bool:
    if APP_DEFAULT_ENV not in ["dev", "prod"]:
      return None
    
    self.base_message()
    
    # Template for Email verification
    if self.template == "VerifyEmail":
      self.verify_email_template()

    # Template for Forgot Password
    if self.template == "ForgotPassword":
      self.forgot_password_template()

    # send email
    if APP_DEFAULT_ENV in ["prod"]:
      self.send_email()

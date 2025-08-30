# Copyright © 2022 by Richard Maku, Inc.
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
      if self.template in ["all_nation_contact"] or self.body.get("service_name") == "allnation":
        email = "info@allnationsbiblechurch.org"
      if self.template in ["sumexus_contact", "sumexus_request_transport"] or self.body.get("service_name") == "sumexus":
        email = "info@sumexus.com"
      if self.template in ["labelle_contact", "labelle_rsvp"] or self.body.get("service_name") == "labelle":
        email = "sales@labellebf.com"
    return email
  
  @property
  def host(self):
    if APP_DEFAULT_ENV == "prod":
      if self.template in ["sumexus_contact", "sumexus_request_transport"] or self.body.get("service_name") == "sumexus":
        return "sumexus.com"
      if self.template in ["all_nation_contact"] or self.body.get("service_name") == "allnation":
        return "allnationsbiblechurch.org"
      if self.template in ["labelle_contact", "labelle_rsvp"] or self.body.get("service_name") == "labelle":
        return "labellebf.com"
    return "localhost:3000"
  
  @property
  def http_host(self) -> str:
    return "https" if APP_DEFAULT_ENV == "prod" else "http"
  
  @property
  def email_distro(self):
    return [self.body.get("email")]
  
  @property
  def additional_distro(self):
    if self.template in ["sumexus_contact", "sumexus_request_transport"]:
      return [self.from_email]
    if self.template in ["all_nation_contact"]:
      return [self.from_email, "okenyitodo87@gmail.com"]
    if self.template in ["labelle_contact", "labelle_rsvp"]:
      return [self.from_email]
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

    if self.body.get('service_name') == "sumexus":
      link = f"{self.http_host}://{self.host}/portal/email-confirmation?token={token}"
      email_template = "d-f1f739d6e76c44788a14df0dd059f153"
      
    if self.body.get('service_name') == "labelle":
      link = f"{self.http_host}://{self.host}/email-confirmation?token={token}"
      email_template = "d-f51b7897018f47ecbf9338cf22c9d741"

    self.message.template_id = email_template
    
  def forgot_password_template(self) -> None:
    token = self.body.get('token')
    email_template = None
    link = f"{self.http_host}://{self.host}/change-password?token={token}"
    self.message.dynamic_template_data = {"tokenLink": link}
    
    if self.body.get('service_name') == "sumexus":
      link = f"{self.http_host}://{self.host}/portal/change-password?token={token}"
      email_template = "d-9ff6287268c44d448cd744cc388cc30b"
      
    if self.body.get('service_name') == "labelle":
      link = f"{self.http_host}://{self.host}/change-password?token={token}"
      email_template = "d-d2d808426be1431783088e8d7334d24e"
      
    self.message.template_id = email_template
    
  def labelle_appointment_template(self) -> None:
    duration = self.body.get("duration", "1")
    self.message.dynamic_template_data = {
      "date": datetime.strptime(self.body.get("date"), '%Y-%m-%dT%H:%M').strftime("%d %B, %Y at %I:%M %p"),
      "duration": f"{duration} hour" if int(duration) == 1 else f"{duration} hours",
      "message": self.body.get("message"),
      "name": self.body.get("name"),
      "subject": self.body.get("subject"),
    }
    self.message.template_id = "d-394bb2a0a2ef4205a15cd81643246bb6"
    
  def all_nation_contact_template(self) -> None:
    self.message.dynamic_template_data = {
      "message": self.body.get("message"),
      "name": self.body.get("name"),
    }
    self.message.template_id = "d-bcc4c1db891f4ce1b327bc1bb9a58784"
    
  def labelle_contact_template(self) -> None:
    self.message.dynamic_template_data = {
      "message": self.body.get("message"),
      "name": self.body.get("name"),
      "subject": self.body.get("subject"),
    }
    self.message.template_id = "d-54da5de124d249ec913d7a7dae979042"
    
  def labelle_rsvp_template(self) -> None:
    self.message.dynamic_template_data = {
      "message": self.body.get("message"),
      "name": self.body.get("name"),
      "subject": self.body.get("subject"),
      "high_school_name": self.body.get("high_school_name"),
      "first_guest": self.body.get("first_guest"),
      "second_guest": self.body.get("second_guest"),
    }
    self.message.template_id = "d-60899e003d2b424cb8f86a070320505c"
    
  def promedexpress_contact_template(self) -> None:
    self.message.dynamic_template_data = {
      "message": self.body.get("message"),
      "name": self.body.get("name"),
    }
    self.message.template_id = "d-c9b83aef8f144601baaf9f72c83d6e93"
    
  def sumexus_contact_template(self) -> None:
    self.message.dynamic_template_data = {
      "message": self.body.get("message"),
      "name": self.body.get("name"),
    }
    self.message.template_id = "d-9c263a934fda4a5e8f57d75d5ace65d1"
    
  def promedexpress_request_transport_template(self) -> None:
    transport_date = datetime.strptime(self.body.get("transport_date"), '%Y-%m-%dT%H:%M').strftime("%d %B, %Y at %I:%M %p")
    self.body.pop("transport_date")
    self.message.dynamic_template_data = {
      **self.body,
      "transport_date": transport_date,
    }
    self.message.template_id = "d-dd27d39502194837aafd21fe85f7b35c"
    
  def sumexus_request_transport_template(self) -> None:
    transport_date = datetime.strptime(self.body.get("transport_date"), '%Y-%m-%dT%H:%M').strftime("%d %B, %Y at %I:%M %p")
    self.body.pop("transport_date")
    self.message.dynamic_template_data = {
      **self.body,
      "transport_date": transport_date,
    }
    self.message.template_id = "d-383f18df13f74899bbe3a7f5bc48b9e8"

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
      
    # Template labelle appointment
    if self.template == "labelle_appointment":
      self.labelle_appointment_template()
      
    if self.template == "labelle_contact":
      self.labelle_contact_template()
      
    if self.template == "labelle_rsvp":
      self.labelle_rsvp_template()

    # Template all nation contact
    if self.template == "all_nation_contact":
      self.all_nation_contact_template()

    # Template promedexpress
    if self.template == "promedexpress_contact":
      self.promedexpress_contact_template()
      
    if self.template == "sumexus_contact":
      self.sumexus_contact_template()
      
    if self.template == "promedexpress_request_transport":
      self.promedexpress_request_transport_template()
      
    if self.template == "sumexus_request_transport":
      self.sumexus_request_transport_template()

    # send email
    if APP_DEFAULT_ENV in ["prod"]:
      self.send_email()

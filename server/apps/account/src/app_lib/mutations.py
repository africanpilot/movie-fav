from ariadne import MutationType
from api.account_authentication_login_mutation import AccountAuthenticationLoginMutation
from api.account_create_mutation import AccountCreateMutation
from api.account_authentication_logout_mutation import AccountAuthenticationLogoutMutation
from api.account_forgot_password_mutation import AccountForgotPasswordMutation
from api.account_confirm_email_mutation import AccountConfirmEmailMutation
from api.account_forgot_password_confirm_email_mutation import AccountForgotPasswordConfirmEmailMutation
from api.account_resend_confirm_mutation import AccountResendConfirmMutation
from api.account_modify_mutation import AccountModifyMutation
from api.account_delete_mutation import AccountDeleteMutation

class Mutations:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    mutation = MutationType()
    
    @mutation.field("accountAuthenticationLogin")
    def resolve_account_authentication_login(_, info: object, accountLoginInput: dict) -> dict:
        return AccountAuthenticationLoginMutation.account_authentication_login(_, info, accountLoginInput)
    
    @mutation.field("accountCreate")
    def resolve_account_create(_, info: object, accountCreateInput: dict) -> dict:
        return AccountCreateMutation.account_create(_, info, accountCreateInput)
    
    @mutation.field("accountAuthenticationLogout")
    def resolve_user_authentication_logout(_, info: object) -> dict:
        return AccountAuthenticationLogoutMutation.account_authentication_logout(_, info)
    
    @mutation.field("accountForgotPassword")
    def resolve_account_forgot_password(_, info: object, accountLogin: str) -> dict:
        return AccountForgotPasswordMutation.account_forgot_password(_, info, accountLogin)
    
    @mutation.field("accountConfirmEmail")
    def resolve_account_confirm_email(_, info: object) -> dict:
        return AccountConfirmEmailMutation.account_confirm_email(_, info)
    
    @mutation.field("accountForgotPasswordConfirmEmail")
    def resolve_account_forgot_password_confirm_email(_, info: object) -> dict:
        return AccountForgotPasswordConfirmEmailMutation.account_forgot_password_confirm_email(_, info)
    
    @mutation.field("accountResendConfirm")
    def resolve_account_resend_confirm(_, info: object, accountLogin: str) -> dict:
        return AccountResendConfirmMutation.account_resend_confirm(_, info, accountLogin)
    
    @mutation.field("accountModify")
    def resolve_account_modify(_, info: object, accountModifyInput: dict) -> dict:
        return AccountModifyMutation.account_modify(_, info, accountModifyInput)
    
    @mutation.field("accountDelete")
    def resolve_account_delete(_, info: object) -> dict:
        return AccountDeleteMutation.account_delete(_, info)
"""create account table

Revision ID: 301b949688c7
Revises: 
Create Date: 2023-05-07 22:55:47.739818

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, AccountBusinessTypeEnum, AccountClassificationEnum


# revision identifiers, used by Alembic.
revision = '301b949688c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.execute("create schema IF NOT EXISTS account")
    
    op.create_table(
        'account_info',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('email', sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column('password', sa.VARCHAR(255), nullable=False),
        sa.Column('registration_date', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('registration_status', sa.Enum(AccountRegistrationEnum), nullable=False, server_default=AccountRegistrationEnum.NOT_COMPLETE.name),
        sa.Column('verified_email', sa.BOOLEAN(), nullable=False, server_default='f'),
        sa.Column('last_login_date', sa.DateTime()),
        sa.Column('last_logout_date', sa.DateTime()),
        sa.Column('profile_image', sa.VARCHAR()),
        sa.Column('profile_thumbnail', sa.VARCHAR()),
        sa.Column('status', sa.Enum(AccountStatusEnum), nullable=False, server_default=AccountStatusEnum.ACTIVE.name),
        sa.Column('forgot_password_expire_date', sa.DateTime()),
        sa.Column('first_name', sa.VARCHAR(100)),
        sa.Column('last_name', sa.VARCHAR(100)),
        sa.Column('middle_name', sa.VARCHAR(100)),
        sa.Column('maiden_name', sa.VARCHAR(100)),
        sa.Column('title', sa.VARCHAR(100)),
        sa.Column('preferred_name', sa.VARCHAR(100)),
        sa.Column('birthday', sa.DateTime()),
        sa.Column('address', sa.VARCHAR()),
        sa.Column('city', sa.VARCHAR(100)),
        sa.Column('state', sa.VARCHAR(100)),
        sa.Column('zip_code', sa.INTEGER()),
        sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema='account'
    )
    
    op.create_table(
        'account_company',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('ein', sa.VARCHAR(50), nullable=False, unique=True),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.Column('registration_date', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('cover_image', sa.VARCHAR()),
        sa.Column('logo', sa.VARCHAR()),
        sa.Column('profile_thumbnail', sa.VARCHAR()),
        sa.Column('status', sa.Enum(AccountStatusEnum), nullable=False, server_default=AccountStatusEnum.ACTIVE.name),
        sa.Column('stripe_connect_account_id', sa.VARCHAR(50)),
        sa.Column('business_type', sa.Enum(AccountBusinessTypeEnum), nullable=False, server_default=AccountBusinessTypeEnum.LLC.name),
        sa.Column('dba', sa.VARCHAR(255)),
        sa.Column('phone_number', sa.VARCHAR(12)),
        sa.Column('classification', sa.Enum(AccountClassificationEnum), nullable=False, server_default=AccountClassificationEnum.OTHER.name),
        sa.Column('product_description', sa.VARCHAR(255), nullable=False),
        sa.Column('website', sa.VARCHAR(255), nullable=False),
        sa.Column('address', sa.VARCHAR(255)),
        sa.Column('city', sa.VARCHAR(100)),
        sa.Column('state', sa.VARCHAR(50)),
        sa.Column('zip_code', sa.INTEGER()),
        sa.Column('sole_first_name', sa.VARCHAR(255)),
        sa.Column('sole_last_name', sa.VARCHAR(255)),
        sa.Column('sole_job_title', sa.VARCHAR(100)),
        sa.Column('sole_phone_number', sa.VARCHAR(12)),
        sa.Column('sole_classification', sa.Enum(AccountClassificationEnum), nullable=False, server_default=AccountClassificationEnum.OTHER.name),
        sa.Column('sole_email', sa.VARCHAR(255), nullable=False),
        sa.Column('sole_birthday', sa.DateTime(), nullable=False),
        sa.Column('sole_ssn', sa.VARCHAR(50)),
        sa.Column('sole_address', sa.VARCHAR(255)),
        sa.Column('sole_city', sa.VARCHAR(100)),
        sa.Column('sole_state', sa.VARCHAR(50)),
        sa.Column('sole_zip_code', sa.INTEGER()),
        sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema='account'
    )

    op.create_table(
        'account_store',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('account_company_id', sa.INTEGER, sa.ForeignKey("account.account_company.id", ondelete="CASCADE"), nullable=False),
        sa.Column('ein', sa.VARCHAR(50), nullable=False, unique=True),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.Column('phone_number', sa.VARCHAR(12)),
        sa.Column('website', sa.VARCHAR(255), nullable=False),
        sa.Column('fax_number', sa.VARCHAR(30)),
        sa.Column('tax_rate_applied', sa.FLOAT, nullable=False),
        sa.Column('image', sa.VARCHAR()),
        sa.Column('thumb_nail', sa.VARCHAR()),
        sa.Column('images', postgresql.ARRAY(sa.String())),
        sa.Column('logo', sa.VARCHAR()),
        sa.Column('logo_thumbnail', sa.VARCHAR()),
        sa.Column('is_closed', sa.BOOLEAN(), nullable=False, server_default='f'),
        sa.Column('return_policy', sa.VARCHAR()),
        sa.Column('address', sa.VARCHAR(255)),
        sa.Column('city', sa.VARCHAR(100)),
        sa.Column('state', sa.VARCHAR(50)),
        sa.Column('zip_code', sa.INTEGER()),
        sa.Column('latitude', sa.FLOAT),
        sa.Column('longitude', sa.FLOAT),
        sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema='account'
    )
    
    op.create_table(
        'account_store_employee',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('account_company_id', sa.INTEGER, sa.ForeignKey("account.account_company.id", ondelete="CASCADE"), nullable=False),
        sa.Column('account_store_id', sa.INTEGER, sa.ForeignKey("account.account_store.id", ondelete="CASCADE"), nullable=False),
        sa.Column('account_info_id', sa.INTEGER, sa.ForeignKey("account.account_info.id", ondelete="CASCADE"), nullable=False),
        sa.Column('user_role', sa.Enum(AccountRoleEnum), nullable=False, server_default=AccountRoleEnum.GUEST.name),
        sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema='account'
    )

    op.create_table(
        'account_saga_state',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('account_info_id', sa.INTEGER, nullable=False),
        sa.Column('last_message_id', sa.VARCHAR(100), nullable=True),
        sa.Column('status', sa.VARCHAR(100), nullable=True),
        sa.Column('failed_step', sa.VARCHAR(100), nullable=True),
        sa.Column('failed_at', sa.DateTime(), nullable=True),
        sa.Column('failure_details', sa.VARCHAR(), nullable=True),
        sa.Column('body', postgresql.JSONB, nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        sa.Column('updated', sa.DateTime(), nullable=False, server_default=sa.sql.func.now()),
        schema='account'
    )
    
def downgrade() -> None:
    op.drop_table('account_saga_state', schema='account')
    op.drop_table('account_store_employee', schema='account')
    op.drop_table('account_store', schema='account')
    op.drop_table('account_company', schema='account')
    op.drop_table('account_info', schema='account')

    op.execute("drop schema account")

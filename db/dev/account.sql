-- schema.sql

CREATE DATABASE dev_secure_postgresql_movie;
\c dev_secure_postgresql_movie;

CREATE TABLE IF NOT EXISTS account_info(
	account_info_id SERIAL PRIMARY KEY,
	account_info_email varchar(100),
	account_info_password varchar(255),
	account_info_registered_on timestamp,
	account_info_registration_status varchar(50) DEFAULT 'NOTCOMPLETE',
	account_info_verified_email BOOLEAN DEFAULT False,
	account_info_last_login_date timestamp,
	account_info_last_logout_date timestamp,
	account_info_profile_image Text,
	account_info_profile_thumbnail Text,
	account_info_status varchar(100) DEFAULT 'ACTIVE',
	account_info_forgot_password_expire_date timestamp
);
CREATE SEQUENCE IF NOT EXISTS account_info_sequence start 1 increment 1;

CREATE TABLE IF NOT EXISTS account_contact (
	account_contact_info_id int references account_info(account_info_id) ON DELETE CASCADE,
	account_contact_first_name varchar(100),
	account_contact_last_name varchar(100),
	account_contact_middle_name varchar(100),
	account_contact_maiden_name varchar(100),
	account_contact_title varchar(50),
	account_contact_preferred_name varchar(100),
	account_contact_birthday timestamp,
	account_contact_address_first varchar(100),
	account_contact_address_second varchar(100),
	account_contact_city varchar(100),
	account_contact_state varchar(100),
	account_contact_zip_code varchar(50),
	account_contact_address_type varchar(100)
);

CREATE TABLE IF NOT EXISTS account_archive(
	account_info_id int,
	account_info_email varchar(100),
	account_info_password varchar(255),
	account_info_registered_on timestamp,
	account_info_registration_status varchar(50) DEFAULT 'NotComplete',
	account_info_verified_email BOOLEAN DEFAULT False,
	account_info_last_login_date timestamp,
	account_info_last_logout_date timestamp,
	account_info_profile_image Text,
	account_info_profile_thumbnail Text,
	account_info_status varchar(100) DEFAULT 'ACTIVE',
	account_contact_first_name varchar(100),
	account_contact_last_name varchar(100),
	account_contact_middle_name varchar(100),
	account_contact_maiden_name varchar(100),
	account_contact_title varchar(50),
	account_contact_preferred_name varchar(100),
	account_contact_birthday timestamp,
	account_contact_address_first varchar(100),
	account_contact_address_second varchar(100),
	account_contact_city varchar(100),
	account_contact_state varchar(100),
	account_contact_zip_code varchar(50),
	account_contact_address_type varchar(100)
);
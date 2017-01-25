-- I decided for simplicity to make the username the primary
-- key however if I want to expand on this to add functionality
-- like account recovery, I would want to split up the tables
-- and link via primary_key and foriegn_key... for example
-- if I wanted to make sure only one account could be made per
-- email address I would need a table that could link emails to
-- usernames using a user_pk and email_pk etc.  I also want to
-- eventually add hash values for password so I will need to
-- modify the password length to allow for long hash values
CREATE TABLE user_accounts(
	username varchar(16) primary key,
	password varchar(16),
	role_fk integer REFERENCES roles(role_pk),
	email text
);

CREATE TABLE roles(
	role_pk SERIAL primary key,
	role text
);

CREATE TABLE assets(
	asset_pk SERIAL primary key,
	asset_tag varchar(16),
	description text
);

CREATE TABLE facilities(
	facility_pk SERIAL primary key,
	common_name varchar(32),
	fcode varchar(6)
);

-- Attempt to solve future linking as suggested in prompt.
CREATE TABLE asset_at(
	asset_fk integer REFERENCES assets(asset_pk),
	facility_fk integer REFERENCES facilities(facility_pk)
);


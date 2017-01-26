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
	role text,
	active text
);

CREATE TABLE assets(
	asset_pk SERIAL primary key,
	asset_tag varchar(16),
	description text
);

CREATE TABLE facilities(
	facility_pk SERIAL primary key,
	fcode varchar(6),
	common_name varchar(32)
);

-- Attempt to solve future linking as suggested in prompt.
CREATE TABLE asset_at(
	asset_fk integer REFERENCES assets(asset_pk) ON DELETE CASCADE,
	facility_fk integer REFERENCES facilities(facility_pk) ON DELETE CASCADE,
	arrive_dt text,
	dispose_dt text
);

CREATE TABLE transfer_requests(
	transfer_pk SERIAL primary key,
	requester varchar(16),
	src_fk integer REFERENCES facilities(facility_pk),
	dest_fk integer REFERENCES facilities(facility_pk),
	asset_fk integer REFERENCES assets(asset_pk),
	approver varchar(16) DEFAULT NULL,
	approval text,
	request_dt text,
	approve_dt text
);

CREATE TABLE in_transit(
	transit_pk SERIAL primary key,
	asset_fk integer REFERENCES assets(asset_pk),
	src_fk integer REFERENCES facilities(facility_pk),
	load_dt text DEFAULT NULL,
	dest_fk integer REFERENCES facilities(facility_pk),
	unload_dt text DEFAULT NULL
);


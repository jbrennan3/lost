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
	email text
);

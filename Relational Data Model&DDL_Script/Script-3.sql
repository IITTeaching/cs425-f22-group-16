DROP TABLE IF EXISTS manager;
DROP TABLE IF EXISTS teller;
DROP TABLE IF EXISTS branch CASCADE;
DROP TABLE IF EXISTS usesbranch CASCADE;
DROP TABLE IF EXISTS hasaccount CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS account CASCADE;
DROP TABLE IF EXISTS transact CASCADE;


CREATE TABLE branch
	(
	 branch_id   varchar(5) NOT NULL,
	 state       char(2),
	 city        TEXT,
	 zip_code    NUMERIC(5,0),
	 PRIMARY KEY (branch_id)
	);

CREATE TABLE customer
	(
	 c_id		varchar(5) NOT NULL,
	 name       char(20) NOT NULL,
	 state      char(2),
	 city       TEXT,
	 zip_code   NUMERIC(5,0),
	 salary     NUMERIC(8,2) CHECK (salary > 0),
	 PRIMARY KEY (c_id)
	);

CREATE TABLE account
	(
	 acc_id	     NUMERIC(6) NOT NULL,
	 acc_type    char(12),
	 balance     NUMERIC(10,2),
	 int_rate    DECIMAL(3,2) CHECK (int_rate < 1.00),
	 PRIMARY KEY(acc_id)
	);

CREATE TABLE manager
	(
	 SSN	      NUMERIC(9) NOT NULL,
	 branch_id    varchar(5) NOT NULL,
	 name         char(20) NOT NULL,
	 state        char(2),
	 city         TEXT,
	 zip_code     NUMERIC(5,0),
	 salary       NUMERIC(8,2) CHECK (salary >= 32000),
	 PRIMARY KEY (SSN),
	 FOREIGN KEY (branch_id) REFERENCES branch
	 	ON DELETE CASCADE
	 	ON UPDATE CASCADE
	);

CREATE TABLE teller
	(
	 SSN	     NUMERIC(9) NOT NULL,
	 branch_id   varchar(5) NOT NULL,
	 name        char(20) NOT NULL,
	 state       char(2),
	 city        TEXT,
	 zip_code    NUMERIC(5,0),
	 salary      NUMERIC(8,2) CHECK (salary >= 19000),
	 booth       NUMERIC(2),
	 PRIMARY KEY (SSN),
	 FOREIGN KEY (branch_id) REFERENCES branch
	 	ON DELETE CASCADE
	 	ON UPDATE CASCADE
	);


CREATE TABLE usesBranch
	(
	 c_id	    varchar(5) NOT NULL,
	 branch_id  varchar(5) NOT NULL,
	 PRIMARY KEY(c_id, branch_id),
	 FOREIGN KEY (c_id) REFERENCES customer
	     ON DELETE CASCADE,
	 FOREIGN KEY (branch_id) REFERENCES branch
	     ON DELETE CASCADE
	     ON UPDATE CASCADE
	);


CREATE TABLE hasAccount
	(
	 c_id		varchar(5) NOT NULL,
	 acc_id     NUMERIC(6) NOT NULL,
	 PRIMARY KEY (c_id, acc_id),
	 FOREIGN KEY (c_id) REFERENCES customer
	 	ON DELETE CASCADE,
	 FOREIGN KEY (acc_id) REFERENCES account
	    ON DELETE SET NULL
	);


CREATE TABLE transact 
	(
	 trans_id	  NUMERIC(6),
	 acc_id       NUMERIC(6) NOT NULL,
	 trans_type   char(12),
	 amount       NUMERIC(8,2),
	 description  timestamp,
	 t_from       char(10),
	 t_to         char(10),
	 PRIMARY KEY(trans_id),
	 FOREIGN KEY (acc_id) REFERENCES account
	 	ON DELETE CASCADE
	);
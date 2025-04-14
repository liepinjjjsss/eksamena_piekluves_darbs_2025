PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	TEXT,
	"name"	TEXT,
	"email"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id")
);
INSERT INTO users VALUES('16','vards','uzvards@gmail.com','asdasdasd');
INSERT INTO users VALUES('17','liepinjjjsss','liepa@gmail.com','liepuks');
INSERT INTO users VALUES('18','liepinjjjsss','liepa@gmail.com','liepuks');
INSERT INTO users VALUES('19','liepinjjjsss','liepa@gmail.com','liepuks');
INSERT INTO users VALUES('20','liepinjjjsss','liepa@gmail.com','liepuks');
INSERT INTO users VALUES('21','liepinjjjsss','liepa@gmail.com','asdasd');
INSERT INTO users VALUES('22','liepinjjjsss','liepa@gmail.com','asdasd');
INSERT INTO users VALUES('23','oompa','oompa@gmail.com','7f7c7bbb32c1b28784c6fa1258ebdff5019292fb62ef4598523566e573d537bd');
INSERT INTO users VALUES('24','liepinjjjsss','renars.liepa1@gmail.com','a45de0924fbff6743f038af2dc4bed29751767b4823fa4131253c5461506a59c');
INSERT INTO users VALUES('25','Arturs','arturs.ausejs@gmail.com','ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f');
INSERT INTO users VALUES('26','renars','renars@gmail.com','0c9527fc7d1c9a26919ab08d9e4a05faab03ea433f2d34659349ef2fd2138d20');
INSERT INTO users VALUES('27','renarsz','lieparenars6@gmail.com','0c9527fc7d1c9a26919ab08d9e4a05faab03ea433f2d34659349ef2fd2138d20');
INSERT INTO users VALUES('55b21e4d-552b-451e-9e7d-3b1152ebcae4','turtulis','turtulis@gmail.com','13746a06e4018e737b26e7e0295fba9c05d1e442d6d858ebab36c08619bebd9f');
CREATE TABLE IF NOT EXISTS "transactions" (
	"id"	TEXT,
	"user_id"	TEXT,
	"amount"	NUMERIC,
	"sender"	TEXT,
	"reciever"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
INSERT INTO transactions VALUES('1','27',1000,'renarsz','renarsz');
INSERT INTO transactions VALUES('2','27',123123123,'renarsz','tavamamma');
INSERT INTO transactions VALUES('3','27',123456,'renarsz','tavamamma');
INSERT INTO transactions VALUES('4','27',1000,'ouagadogou','tavamamma');
INSERT INTO transactions VALUES('5','27',1000,'ouagadogou','tavamamma');
CREATE TABLE IF NOT EXISTS "businesses" (
	"id"	TEXT,
	"owner_id"	TEXT,
	"business_name"	TEXT,
	"business_type"	TEXT,
	"net_worth"	REAL,
	PRIMARY KEY("id"),
	FOREIGN KEY("owner_id") REFERENCES "users"("id")
);
INSERT INTO businesses VALUES('1','27','aaaa','uuuu',123.540000000000006);
INSERT INTO businesses VALUES('2','27','ouagadogou','laudamsco',9896.68999999999869);
CREATE TABLE IF NOT EXISTS "business_history" (
	"id"	TEXT,
	"business_id"	TEXT,
	"timestamp"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"net_worth"	REAL,
	PRIMARY KEY("id"),
	FOREIGN KEY("business_id") REFERENCES "businesses"("id")
);
INSERT INTO business_history VALUES('1','2','2025-03-18 11:49:51',8896.68999999999869);
INSERT INTO business_history VALUES('2','2','2025-03-18 11:50:41',9896.68999999999869);
DELETE FROM sqlite_sequence;
COMMIT;

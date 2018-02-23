PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `users` (
	`userID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT NOT NULL UNIQUE,
	`password`	NUMERIC NOT NULL,
	`email`	TEXT,
	`mobile`	TEXT,
	`website`	TEXT,
	`isAdmin`	INTEGER DEFAULT 0,
	`createdAt`	INTEGER,
	`modifiedAt`	INTEGER,
	UNIQUE(`userID`,`username`)
);
CREATE TABLE IF NOT EXISTS `reservations` (
	`reservationID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`userID`	INTEGER NOT NULL,
	`machineID`	INTEGER NOT NULL,
	`startTime`	INTEGER,
	`endTime`	INTEGER,
	`reservationDate`	INTEGER,
	`isActive`	INTEGER NOT NULL DEFAULT 1,
	`createdAt`	INTEGER,
	`createdBy`	INTEGER,
	`updatedAt`	INTEGER,
	`updateBy`	INTEGER,
	FOREIGN KEY(userID) REFERENCES users(userID) ON DELETE CASCADE,
	FOREIGN KEY(machineID) REFERENCES machines(machineID) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS `messages` (
	`messageID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`fromUserID`	INTEGER,
	`toUserID`	INTEGER,
	`content`	TEXT,
	`createdAt`	INTEGER,
	FOREIGN KEY(fromUserID) REFERENCES users(userID) ON DELETE CASCADE,
	FOREIGN KEY(toUserID) REFERENCES users(userID) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS `machinetypes` (
	`typeID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`typeName`	TEXT UNIQUE,
	`pastProject`	TEXT,
	`createdAt`	INTEGER,
	`modifiedAt`	INTEGER,
	`createdBy`	INTEGER,
	`modifiedBy`	INTEGER);
CREATE TABLE IF NOT EXISTS `machines` (
	`machineID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`machinename`	TEXT UNIQUE,
	`typeID`	INTEGER NOT NULL,
	`tutorial`	TEXT,
	`createdAt`	INTEGER,
	`updatedAt`	INTEGER,
	`createdBy`	INTEGER,
	`updateBy`	INTEGER,
	FOREIGN KEY(typeID) REFERENCES machinetypes(typeID) ON DELETE CASCADE);
COMMIT;
PRAGMA foreign_keys=ON;

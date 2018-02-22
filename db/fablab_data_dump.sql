BEGIN TRANSACTION;
INSERT INTO `users` (userID,username,password,isAdmin,createdAt,modifiedAt) VALUES (2,'daniel','123456',0,NULL,NULL);
INSERT INTO `machinetypes` (typeID,typeName,pastProject,createdAt,modifiedAt,createdBy,modifiedBy) VALUES (1,'3D printer','google',1,1,1,'');
INSERT INTO `machines` (machineID,machinename,typeid,tutorial,createdAt,updatedAt,createdBy,updateBy) VALUES (3,'1',1,NULL,NULL,NULL,1,NULL);
COMMIT;

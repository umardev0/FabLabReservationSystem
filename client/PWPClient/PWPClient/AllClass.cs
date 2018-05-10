public class fablabUser
{
    public string userID;
    public string userName;
    public string password;
    public string email;
    public string mobile;
    public string website;
    public bool isAdmin;
    public string createdAt;
    public string updatedAt;
    public string createdBy;
    public string updatedBy;


    public fablabUser(string userID, string userName)
    {
        this.userID = userID;
        this.userName = userName;
    }

    public fablabUser(string userID, string userName, string password, string email, string mobile, string website, bool isAdmin, string createdAt, string updatedAt, string createdBy, string updatedBy)
    {
        this.userID = userID;
        this.userName = userName;
        this.password = password;
        this.email = email;
        this.mobile = mobile;
        this.website = website;
        this.isAdmin = isAdmin;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.createdBy = createdBy;
        this.updatedBy = updatedBy;
    }
}

public class fablabMachineType
{
    public string typeID;
    public string typeName;
    public string typeFullname;
    public string pastProject;
    public string createdAt;
    public string updatedAt;
    public string createdBy;
    public string updatedBy;

    public fablabMachineType(string typeID, string typeName, string typeFullname, string pastProject, string createdAt, string updatedAt, string createdBy, string updatedBy)
    {
        this.typeID = typeID;
        this.typeName = typeName;
        this.typeFullname = typeFullname;
        this.pastProject = pastProject;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.createdBy = createdBy;
        this.updatedBy = updatedBy;
    }

    public fablabMachineType(string typeID, string typeFullname)
    {
        this.typeID = typeID;
        this.typeFullname = typeFullname;
    }
}

public class fablabMachine
{
    public string machineID;
    public string machineName;
    public string typeID;
    public string tutorial;
    public string createdAt;
    public string createdBy;
    public string updatedAt;
    public string updatedBy;

    public fablabMachine(string machineID, string machineName, string typeID, string tutorial, string createdAt, string createdBy, string updatedAt, string updatedBy)
    {
        this.machineID = machineID;
        this.machineName = machineName;
        this.typeID = typeID;
        this.tutorial = tutorial;
        this.createdAt = createdAt;
        this.createdBy = createdBy;
        this.updatedAt = updatedAt;
        this.updatedBy = updatedBy;
    }

    public fablabMachine(string machineID, string machineName, string typeID)
    {
        this.machineID = machineID;
        this.machineName = machineName;
        this.typeID = typeID;
    }

    public fablabMachine()
    {
    }
}

public class fablabReservation
{
    public string reservationID;
    public string userID;
    public string machineID;
    public string startTime;
    public string endTime;
    public bool isActive;
    public string createdAt;
    public string createdBy;
    public string updatedAt;
    public string updatedBy;

    public fablabReservation(string reservationID, string userID, string machineID)
    {
        this.reservationID = reservationID;
        this.userID = userID;
        this.machineID = machineID;
    }

    public fablabReservation(string userID, string machineID, string startTime, string endTime, bool isActive, string createdAt, string createdBy, string updatedAt, string updatedBy)
    {
        this.userID = userID;
        this.machineID = machineID;
        this.startTime = startTime;
        this.endTime = endTime;
        this.isActive = isActive;
        this.createdAt = createdAt;
        this.createdBy = createdBy;
        this.updatedAt = updatedAt;
        this.updatedBy = updatedBy;
    }

    public fablabReservation(string reservationID, string userID, string machineID, string startTime, string endTime, bool isActive)
    {
        this.reservationID = reservationID;
        this.userID = userID;
        this.machineID = machineID;
        this.startTime = startTime;
        this.endTime = endTime;
        this.isActive = isActive;
    }
}


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

}

public class fablabMachine
{

}

public class fablabReservation
{

}


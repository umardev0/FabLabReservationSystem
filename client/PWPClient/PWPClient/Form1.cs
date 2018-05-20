using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Windows.Forms;

namespace PWPClient
{
    public partial class Form1 : Form
    {
        private RESTfulHandler handler = new RESTfulHandler();
        private TimeZoneInfo timeZone = TimeZoneInfo.FindSystemTimeZoneById("FLE Standard Time");

        public Form1()
        {
            InitializeComponent();
            tabControl.Visible = false;

        }

        private void tabControl_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (tabControl.SelectedTab == users)
            {
                updateListUser();
            }
            else if (tabControl.SelectedTab == machineTypes)
            {
                updateListMachineTypes();
            } 
            else if (tabControl.SelectedTab == machines)
            {
                updateListMachine();
            }
            else if (tabControl.SelectedTab == reservations)
            {
                updateListReservation();
            }
        }

        private void buttonConnectServer_Click(object sender, EventArgs e)
        {
            tabControl.Visible = true;
            tableLayoutPanelUser.Visible = false;
            updateListUser();
        }

        private void userPanelClear()
        {
            textBoxUsername.Clear();
            textBoxPassword.Clear();
            textBoxEmail.Clear();
            textBoxMobile.Clear();
            textBoxWebsite.Clear();
            checkBoxAdmin.Text = "Regular User";
            checkBoxAdmin.Checked = false;
            textBoxUserCreatedAt.Clear();
            textBoxUserUpdatedAt.Clear();
            textBoxUserCreatedBy.Clear();
            textBoxUserUpdatedBy.Clear();
        }

        private void userPanelUpdate(fablabUser user)
        {
            textBoxUsername.Text = user.userName;
            textBoxPassword.Text = user.password;
            textBoxEmail.Text = user.email;
            textBoxMobile.Text = user.mobile;
            textBoxWebsite.Text = user.website;
            checkBoxAdmin.Text = ((user.isAdmin)?"Administrator":"Regular User");
            checkBoxAdmin.Checked = ((user.isAdmin) ?  true : false);
            textBoxUserCreatedAt.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(user.createdAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            textBoxUserUpdatedAt.Text = (user.updatedAt != null) ? DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(user.updatedAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss") : "";
            textBoxUserCreatedBy.Text = user.createdBy;
            textBoxUserUpdatedBy.Text = user.updatedBy;
        }

        private void typePanelClear()
        {
            textBoxTypeID.Clear();
            textBoxTypeName.Clear();
            textBoxTypeFullName.Clear();
            textBoxTypePastProjects.Clear();
            textBoxTypeCreatedAt.Clear();
            textBoxTypeUpdatedAt.Clear();
            textBoxTypeCreatedBy.Clear();
            textBoxTypeUpdatedBy.Clear();
        }

        private void typePanelUpdate(fablabMachineType type)
        {
            textBoxTypeID.Text = type.typeID;
            textBoxTypeName.Text = type.typeName;
            textBoxTypeFullName.Text = type.typeFullname;
            textBoxTypePastProjects.Text = type.pastProject;
            textBoxTypeCreatedAt.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(type.createdAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            textBoxTypeUpdatedAt.Text = (type.updatedAt!= null) ? DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(type.updatedAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss"): "";
            textBoxTypeCreatedBy.Text = type.createdBy;
            textBoxTypeUpdatedBy.Text = type.updatedBy;
        }

        private void machinePanelClear()
        {
            textBoxMachineID.Clear();
            textBoxMachineName.Clear();
            textBoxMachineTypeID.Clear();
            textBoxMachineTutorial.Clear();
            textBoxMachineCreatedAt.Clear();
            textBoxMachineUpdatedAt.Clear();
            textBoxMachineCreatedBy.Clear();
            textBoxMachineUpdatedBy.Clear();
        }

        private void machinePanelUpdate(fablabMachine machine)
        {
            textBoxMachineID.Text = machine.machineID;
            textBoxMachineName.Text = machine.machineName;
            textBoxMachineTypeID.Text = machine.typeID;
            textBoxMachineTutorial.Text = machine.tutorial;
            textBoxMachineCreatedAt.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(machine.createdAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            textBoxMachineUpdatedAt.Text = (machine.updatedAt != null) ? DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(machine.updatedAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss") : "";
            textBoxMachineCreatedBy.Text = machine.createdBy;
            textBoxMachineUpdatedBy.Text = machine.updatedBy;
            buttonHistory.Visible = false;
        }

        private void reservationPanelClear()
        {
            textBoxReservationID.Clear();
            textBoxReservationUserID.Clear();
            textBoxReservationMachineID.Clear();
            textBoxReservationStartTime.Text = "dd/MMM/yyyy hh:mm:ss";
            textBoxReservationEndTime.Text = "dd/MMM/yyyy hh:mm:ss";
            checkBoxReservationActive.Checked = false;
            textBoxReservationCreatedAt.Clear();
            textBoxReservationUpdatedAt.Clear();
            textBoxReservationCreatedBy.Clear();
            textBoxReservationUpdatedBy.Clear();
        }

        private void reservationPanelUpdate(fablabReservation reservation)
        {
            textBoxReservationUserID.Text = reservation.userID;
            textBoxReservationMachineID.Text = reservation.machineID;
            textBoxReservationStartTime.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(reservation.startTime)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            textBoxReservationEndTime.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(reservation.endTime)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            checkBoxReservationActive.Checked = reservation.isActive;
            textBoxReservationCreatedAt.Text = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(reservation.createdAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss");
            textBoxReservationUpdatedAt.Text = (reservation.updatedAt != null) ? DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(reservation.updatedAt)).ToOffset(new TimeSpan(+3, 0, 0)).ToString("dd/MMM/yyyy HH:mm:ss") : "";
            textBoxMachineCreatedBy.Text = reservation.createdBy;
            textBoxMachineUpdatedBy.Text = reservation.updatedBy;
        }
        //---------------------Utility functions----------------------
        private List<fablabUser> parseUsers (String input)
        {
            List<fablabUser> res = new List<fablabUser>();
            JObject obj = JObject.Parse(input);
            JArray userList = (JArray) obj["items"];
            foreach (JObject item in userList)
            {
                fablabUser tmp = new fablabUser((string)item["userID"], (string)item["username"]);
                res.Add(tmp);
            }
            return res;
        }

        private fablabUser parseUser (String input)
        {
            JObject obj = JObject.Parse(input);
            bool isAdmin = false;
            isAdmin = ((string)obj["isAdmin"] == "1") ? true : false;
            fablabUser tmp = new fablabUser((string)obj["userID"], (string)obj["username"], (string)obj["password"], (string)obj["email"], (string)obj["mobile"], (string)obj["website"], isAdmin, (string)obj["createdAt"], (string)obj["updatedAt"], (string)obj["createdBy"], (string)obj["updatedBy"]);
            return tmp;

        }

        private List<fablabMachineType> parseTypes(String input)
        {
            List<fablabMachineType> res = new List<fablabMachineType>();
            JObject obj = JObject.Parse(input);
            JArray typeList = (JArray)obj["items"];
            foreach (JObject item in typeList)
            {
                fablabMachineType tmp = new fablabMachineType((string)item["id"], (string)item["typeFullname"]);
                res.Add(tmp);
            }
            return res;
        }

        private fablabMachineType parseType(String input)
        {
            JObject obj = JObject.Parse(input);
            fablabMachineType tmp = new fablabMachineType((string)obj["typeID"], (string)obj["typeName"], (string)obj["typeFullname"], (string)obj["pastProject"], (string)obj["createdAt"], (string)obj["updatedAt"], (string)obj["createdBy"], (string)obj["updatedBy"]);
            return tmp;

        }

        private List<fablabMachine> parseMachines(String input)
        {
            List<fablabMachine> res = new List<fablabMachine>();
            JObject obj = JObject.Parse(input);
            JArray machineList = (JArray)obj["items"];
            foreach (JObject item in machineList)
            {
                fablabMachine tmp = new fablabMachine((string)item["machineID"], (string)item["machinename"], (string)item["typeID"]);
                res.Add(tmp);
            }
            return res;
        }

        private fablabMachine parseMachine(String input)
        {
            JObject obj = JObject.Parse(input);
            fablabMachine tmp = new fablabMachine(machineID: (string)obj["machineID"], machineName: (string)obj["machinename"], typeID: (string)obj["typeID"], tutorial: (string)obj["tutorial"], createdAt: (string)obj["createdAt"], createdBy: (string)obj["createdBy"], updatedAt: (string)obj["updatedAt"], updatedBy: (string)obj["updatedBy"]);
            return tmp;

        }

        private List<fablabReservation> parseReservations(String input)
        {
            List<fablabReservation> res = new List<fablabReservation>();
            JObject obj = JObject.Parse(input);
            JArray machineList = (JArray)obj["items"];
            foreach (JObject item in machineList)
            {
                fablabReservation tmp = new fablabReservation((string)item["reservationID"], (string)item["userID"], (string)item["machineID"]);
                res.Add(tmp);
            }
            return res;
        }

        private fablabReservation parseReservation(String input)
        {
            JObject obj = JObject.Parse(input);
            fablabReservation tmp = new fablabReservation(userID: (string)obj["userID"], machineID: (string)obj["machineID"], startTime: (string)obj["startTime"], endTime: (string)obj["endTime"], isActive: (bool)obj["isActive"], createdAt: (string)obj["createdAt"], createdBy: (string)obj["createdBy"], updatedAt: (string)obj["updatedAt"], updatedBy: (string)obj["updatedBy"]);
            return tmp;

        }
        private void updateListUser()
        {
            listViewUsers.Items.Clear();
            tableLayoutPanelUser.Visible = false;
            List<fablabUser> list = parseUsers(handler.HTTPGet(@"http://" + textBoxServerIPPort.Text + "/fablab/api/users/"));
            foreach (fablabUser user in list)
            {
                string[] row = { user.userID, user.userName };
                listViewUsers.Items.Add(new ListViewItem(row));
            }
        }

        private void updateListMachineTypes()
        {
            listViewMachineTypes.Items.Clear();
            List<fablabMachineType> list = parseTypes(handler.HTTPGet(@"http://" + textBoxServerIPPort.Text + "/fablab/api/machinetypes/"));
            foreach (fablabMachineType type in list)
            {
                string[] row = { type.typeID, type.typeFullname };
                listViewMachineTypes.Items.Add(new ListViewItem(row));
            }
        }

        private void updateListMachine()
        {
            listViewMachine.Items.Clear();
            List<fablabMachine> list = parseMachines(handler.HTTPGet(@"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/"));
            foreach (fablabMachine machine in list)
            {
                string[] row = { machine.machineID, machine.machineName, machine.typeID };
                listViewMachine.Items.Add(new ListViewItem(row));
            }
        }

        private void updateListReservation()
        {
            listViewReservations.Items.Clear();
            List<fablabReservation> list = parseReservations(handler.HTTPGet(@"http://" + textBoxServerIPPort.Text + "/fablab/api/reservations/"));
            foreach (fablabReservation reservation in list)
            {
                string[] row = { reservation.reservationID, reservation.userID, reservation.machineID };
                listViewReservations.Items.Add(new ListViewItem(row));
            }
        }
        //------------------
        private void listViewUsers_ItemActivate(object sender, EventArgs e)
        {
            userPanelClear();
            tableLayoutPanelUser.Visible = true;
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/users/" + listViewUsers.SelectedItems[0].SubItems[1].Text + "/";
            userPanelUpdate(parseUser(handler.HTTPGet(URL)));
            buttonAddUser.Visible = false;
            buttonModifyUser.Enabled = true;
            buttonDeleteUser.Enabled = true;
            if (tableLayoutPanelUser.Visible == false)
            {
                tableLayoutPanelUser.Visible = true;
            }
            textBoxUsername.Enabled = false;
        }

        private void buttonModify_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/users/" + textBoxUsername.Text + "/";
            JObject newData = new JObject(
                                new JProperty("password", textBoxPassword.Text),
                                new JProperty("email", textBoxEmail.Text),
                                new JProperty("mobile", textBoxMobile.Text),
                                new JProperty("website", textBoxWebsite.Text),
                                new JProperty("isAdmin", ((checkBoxAdmin.Checked) ? "1" : "0")),
                                new JProperty("updatedBy", textBoxUserUpdatedBy.Text)
                                );
            Console.WriteLine(newData.ToString());
            
            handler.HTTPPut(URL, newData);
        }

        private void checkBoxAdmin_CheckedChanged(object sender, EventArgs e)
        {
            checkBoxAdmin.Text = (checkBoxAdmin.Checked) ? "Administrator" : "Regular User";
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/users/" + textBoxUsername.Text + "/";
            handler.HTTPDelete(URL);
            updateListUser();
        }

        private void buttonAddNewUser_Click(object sender, EventArgs e)
        {
            userPanelClear();
            buttonAddUser.Visible = true;
            buttonModifyUser.Enabled = false;
            buttonDeleteUser.Enabled = false;
            if (tableLayoutPanelUser.Visible == false)
            {
                tableLayoutPanelUser.Visible = true;
            }
            textBoxUsername.Enabled = true;
        }

        private void buttonAdd_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/users/";
            if (textBoxUsername.Text == "")
            {
                MessageBox.Show("Username cannot be blanked");
                return;
            }
            JObject newData = new JObject(
                                new JProperty("username", textBoxUsername.Text),
                                new JProperty("password", textBoxPassword.Text),
                                new JProperty("email", textBoxEmail.Text),
                                new JProperty("mobile", textBoxMobile.Text),
                                new JProperty("website", textBoxWebsite.Text),
                                new JProperty("isAdmin", (checkBoxAdmin.Checked) ? 1 : 0),
                                new JProperty("createdBy", textBoxUserCreatedBy.Text)
                                );
            handler.HTTPPost(URL, newData);
            userPanelClear();
            buttonAddUser.Visible = false;
            buttonModifyUser.Enabled = true;
            buttonDeleteUser.Enabled = true;
            if (tableLayoutPanelUser.Visible == false)
            {
                tableLayoutPanelUser.Visible = true;
            }
            textBoxUsername.Enabled = false;
            updateListUser();

        }


        private void listViewMachineTypes_ItemActivate(object sender, EventArgs e)
        {
            typePanelClear();
            tableLayoutPanelTypes.Visible = true;
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machinetypes/" + listViewMachineTypes.SelectedItems[0].SubItems[0].Text + "/";
            typePanelUpdate(parseType(handler.HTTPGet(URL)));
            buttonAddType.Visible = false;
            buttonModifyType.Enabled = true;
            buttonDeleteType.Enabled = true;
            if (tableLayoutPanelTypes.Visible == false)
            {
                tableLayoutPanelTypes.Visible = true;
            }
        }

        private void buttonModifyType_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machinetypes/" + textBoxTypeID.Text + "/";
            JObject newData = new JObject(
                                new JProperty("typeName", textBoxTypeName.Text),
                                new JProperty("typeFullname", textBoxTypeFullName.Text),
                                new JProperty("pastProject", textBoxTypePastProjects.Text),
                                new JProperty("updatedBy", textBoxTypeUpdatedBy.Text)
                                );
            handler.HTTPPut(URL, newData);
        }

        private void buttonDeleteType_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machinetypes/" + textBoxTypeID.Text + "/";
            handler.HTTPDelete(URL);
            updateListMachineTypes();
            tableLayoutPanelTypes.Visible = false;
        }

        private void buttonClearTypeForm_Click(object sender, EventArgs e)
        {
            typePanelClear();
            buttonAddType.Visible = true;
            buttonModifyType.Enabled = false;
            buttonDeleteType.Enabled = false;
            if (tableLayoutPanelTypes.Visible == false)
            {
                tableLayoutPanelTypes.Visible = true;
            }
        }

        private void buttonAddType_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machinetypes/";
            JObject newData = new JObject(
                                new JProperty("typeName", textBoxTypeName.Text),
                                new JProperty("typeFullname", textBoxTypeFullName.Text),
                                new JProperty("pastProject", textBoxTypePastProjects.Text),
                                new JProperty("createdBy", textBoxTypeCreatedBy.Text)
                                );
            handler.HTTPPost(URL, newData);
            typePanelClear();
            buttonAddType.Visible = false;
            buttonModifyType.Enabled = true;
            buttonDeleteType.Enabled = true;
            if (tableLayoutPanelTypes.Visible == false)
            {
                tableLayoutPanelTypes.Visible = true;
            }
            updateListMachineTypes();
        }

        private void listViewMachine_ItemActivate(object sender, EventArgs e)
        {
            machinePanelClear();
            tableLayoutPanelMachine.Visible = true;
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/" + listViewMachine.SelectedItems[0].SubItems[0].Text + "/";
            machinePanelUpdate(parseMachine(handler.HTTPGet(URL)));
            buttonAddMachine.Enabled = true;
            buttonDeleteMachine.Enabled = true;
            buttonHistory.Visible = true;
            if (tableLayoutPanelMachine.Visible == false)
            {
                tableLayoutPanelMachine.Visible = true;
            }
        }

        private void buttonHistory_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/" + textBoxMachineID.Text + "/history/";
            History history = new History(URL);
            history.Show();
        }

        private void buttonClearMachineForm_Click(object sender, EventArgs e)
        {
            machinePanelClear();
            buttonAddMachine.Visible = true;
            buttonModifyMachine.Enabled = false;
            buttonDeleteMachine.Enabled = false;
            buttonHistory.Visible = false;
            if (tableLayoutPanelMachine.Visible == false)
            {
                tableLayoutPanelMachine.Visible = true;
            }
        }

        private void buttonModifyMachine_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/" + textBoxMachineID.Text + "/";
            JObject newData = new JObject(
                                new JProperty("machinename", textBoxMachineName.Text),
                                new JProperty("typeID", textBoxMachineTypeID.Text),
                                new JProperty("tutorial", textBoxMachineTutorial.Text),
                                new JProperty("updatedBy", textBoxMachineUpdatedBy.Text)
                                );
            handler.HTTPPut(URL, newData);
        }

        private void buttonDeleteMachine_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/" + textBoxMachineID.Text + "/";
            handler.HTTPDelete(URL);
            updateListMachine();
            tableLayoutPanelMachine.Visible = false;
        }

        private void buttonAddMachine_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/machines/";
            JObject newData = new JObject(
                                new JProperty("machinename", textBoxMachineName.Text),
                                new JProperty("typeID", textBoxMachineTypeID.Text),
                                new JProperty("tutorial", textBoxMachineTutorial.Text),
                                new JProperty("createdBy", textBoxMachineCreatedBy.Text)
                                );
            handler.HTTPPost(URL, newData);
            machinePanelClear();
            buttonAddMachine.Visible = false;
            buttonModifyMachine.Enabled = true;
            buttonDeleteMachine.Enabled = true;
            if (tableLayoutPanelMachine.Visible == false)
            {
                tableLayoutPanelMachine.Visible = true;
            }
            updateListMachine();
        }

        private void listViewReservations_ItemActivate(object sender, EventArgs e)
        {
            reservationPanelClear();
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/reservations/" + listViewReservations.SelectedItems[0].SubItems[0].Text + "/";
            reservationPanelUpdate(parseReservation(handler.HTTPGet(URL)));
            textBoxReservationID.Text = listViewReservations.SelectedItems[0].SubItems[0].Text;
            buttonAddReservation.Visible = false;
            buttonUpdateReservation.Enabled = true;
            if (tableLayoutPanel1.Visible == false)
            {
                tableLayoutPanel1.Visible = true;
            }
        }

        private void buttonUpdateReservation_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/reservations/" + textBoxReservationID.Text + "/";
            JObject newData = new JObject(
                                new JProperty("updatedBy", textBoxReservationUpdatedBy.Text)
                                );
            handler.HTTPPut(URL, newData);
        }

        private void buttonClearFormReservation_Click(object sender, EventArgs e)
        {
            reservationPanelClear();
            buttonAddReservation.Visible = true;
            buttonUpdateReservation.Enabled = false;
            if (tableLayoutPanel1.Visible == false)
            {
                tableLayoutPanel1.Visible = true;
            }
        }

        private void buttonAddReservation_Click(object sender, EventArgs e)
        {
            String URL = @"http://" + textBoxServerIPPort.Text + "/fablab/api/reservations/";
            Console.WriteLine(DateTimeOffset.ParseExact(textBoxReservationStartTime.Text, "dd/MMM/yyyy HH:mm:ss", CultureInfo.InvariantCulture).ToOffset(new TimeSpan(+3, 0, 0)).ToUnixTimeSeconds());
            JObject newData = new JObject(
                                new JProperty("userID", textBoxReservationUserID.Text),
                                new JProperty("machineID", textBoxReservationMachineID.Text),
                                new JProperty("startTime", DateTimeOffset.ParseExact(textBoxReservationStartTime.Text, "dd/MMM/yyyy HH:mm:ss", CultureInfo.InvariantCulture).ToOffset(new TimeSpan(+3, 0, 0)).ToUnixTimeSeconds().ToString()),
                                new JProperty("endTime", DateTimeOffset.ParseExact(textBoxReservationEndTime.Text, "dd/MMM/yyyy HH:mm:ss", CultureInfo.InvariantCulture).ToOffset(new TimeSpan(+3, 0, 0)).ToUnixTimeSeconds().ToString())
                                );
            handler.HTTPPost(URL, newData);
            reservationPanelClear();
            buttonAddReservation.Visible = false;
            buttonUpdateReservation.Enabled = true;
            if (tableLayoutPanel1.Visible == false)
            {
                tableLayoutPanel1.Visible = true;
            }
            updateListReservation();
        }
    }
}

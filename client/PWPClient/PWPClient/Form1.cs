using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace PWPClient
{
    public partial class Form1 : Form
    {
        private RESTfulHandler handler = new RESTfulHandler();

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
            textBoxUserCreatedAt.Text = user.createdAt;
            textBoxUserUpdatedAt.Text = user.updatedAt;
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
            textBoxTypeCreatedAt.Text = type.createdAt;
            textBoxTypeUpdatedAt.Text = type.updatedAt;
            textBoxTypeCreatedBy.Text = type.createdBy;
            textBoxTypeUpdatedBy.Text = type.updatedBy;
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
                                new JProperty("isAdmin", (checkBoxAdmin.Checked) ? 1 : 0),
                                new JProperty("updatedBy", textBoxUserUpdatedBy.Text)
                                );
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
    }
}

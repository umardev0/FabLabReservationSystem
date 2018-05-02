using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace PWPClient
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            tabControl.Visible = false;

        }

        private void tabControl_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (tabControl.SelectedTab == users)
            {
                listViewUsers.Items.Clear();
                tableLayoutPanelUser.Visible = false;
            }
        }

        private void buttonConnectServer_Click(object sender, EventArgs e)
        {
            tabControl.Visible = true;
            RESTfulHandler handler = new RESTfulHandler();
            List<fablabUser> list = parseUsers(handler.HTTPGet(@"http://127.0.0.1:5000/fablab/api/users/"));
            foreach (fablabUser user in list)
            {
                string[] row = {user.userID, user.userName };
                listViewUsers.Items.Add(new ListViewItem(row));
            }
        }

        private void userPanelClear()
        {
            textBoxUsername.Clear();
            textBoxPassword.Clear();
            textBoxEmail.Clear();
            textBoxMobile.Clear();
            textBoxWebsite.Clear();
            textBoxRole.Clear();
            textBoxCreatedAt.Clear();
            textBoxUpdatedAt.Clear();
            textBoxCreatedBy.Clear();
            textBoxUpdatedBy.Clear();
        }

        private void userPanelUpdate(fablabUser user)
        {
            textBoxUsername.Text = user.userName;
            textBoxPassword.Text = user.password;
            textBoxEmail.Text = user.email;
            textBoxMobile.Text = user.mobile;
            textBoxWebsite.Text = user.website;
            textBoxRole.Text = ((user.isAdmin)?"Administrator":"Regular User");
            textBoxCreatedAt.Text = user.createdAt;
            textBoxUpdatedAt.Text = user.updatedAt;
            textBoxCreatedBy.Text = user.createdBy;
            textBoxUpdatedBy.Text = user.updatedBy;
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
            fablabUser tmp = new fablabUser((string)obj["userID"], (string)obj["username"], (string)obj["password"], (string)obj["email"], (string)obj["mobile"], (string)obj["website"], isAdmin, (string)obj["createdAt"], (string)obj["updateAt"], (string)obj["createdBy"], (string)obj["updateBy"]);
            return tmp;

        }
  
        private void listViewUsers_ItemActivate(object sender, EventArgs e)
        {
            userPanelClear();
            tableLayoutPanelUser.Visible = true;
            RESTfulHandler handler = new RESTfulHandler();
            String URL = @"http://127.0.0.1:5000/fablab/api/users/" + listViewUsers.SelectedItems[0].SubItems[1].Text + "/";
            userPanelUpdate(parseUser(handler.HTTPGet(URL)));
            

        }

        private void buttonModify_Click(object sender, EventArgs e)
        {
            HTTPPut()
        }
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
                ListViewItem tmp = new ListViewItem("1");
                tmp.SubItems.Add("Titan");
                listViewUsers.Items.Add(tmp);
            }
        }

        private void buttonConnectServer_Click(object sender, EventArgs e)
        {
            tabControl.Visible = true;

        }
    }
}

namespace PWPClient
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.reservations = new System.Windows.Forms.TabPage();
            this.machines = new System.Windows.Forms.TabPage();
            this.machineTypes = new System.Windows.Forms.TabPage();
            this.users = new System.Windows.Forms.TabPage();
            this.tableLayoutPanelUser = new System.Windows.Forms.TableLayoutPanel();
            this.buttonDelete = new System.Windows.Forms.Button();
            this.textBoxUpdatedBy = new System.Windows.Forms.TextBox();
            this.textBoxCreatedBy = new System.Windows.Forms.TextBox();
            this.textBoxUpdatedAt = new System.Windows.Forms.TextBox();
            this.textBoxCreatedAt = new System.Windows.Forms.TextBox();
            this.textBoxRole = new System.Windows.Forms.TextBox();
            this.textBoxWebsite = new System.Windows.Forms.TextBox();
            this.textBoxMobile = new System.Windows.Forms.TextBox();
            this.textBoxEmail = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.buttonModify = new System.Windows.Forms.Button();
            this.textBoxUsername = new System.Windows.Forms.TextBox();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.buttonAddNewUser = new System.Windows.Forms.Button();
            this.listViewUsers = new System.Windows.Forms.ListView();
            this.userID = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.userName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.tabControl = new System.Windows.Forms.TabControl();
            this.textBoxServerIPPort = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.buttonConnectServer = new System.Windows.Forms.Button();
            this.users.SuspendLayout();
            this.tableLayoutPanelUser.SuspendLayout();
            this.tabControl.SuspendLayout();
            this.SuspendLayout();
            // 
            // reservations
            // 
            this.reservations.Location = new System.Drawing.Point(4, 22);
            this.reservations.Name = "reservations";
            this.reservations.Size = new System.Drawing.Size(768, 380);
            this.reservations.TabIndex = 3;
            this.reservations.Text = "Reservations";
            this.reservations.UseVisualStyleBackColor = true;
            // 
            // machines
            // 
            this.machines.Location = new System.Drawing.Point(4, 22);
            this.machines.Name = "machines";
            this.machines.Size = new System.Drawing.Size(768, 380);
            this.machines.TabIndex = 2;
            this.machines.Text = "Machines";
            this.machines.UseVisualStyleBackColor = true;
            // 
            // machineTypes
            // 
            this.machineTypes.Location = new System.Drawing.Point(4, 22);
            this.machineTypes.Name = "machineTypes";
            this.machineTypes.Padding = new System.Windows.Forms.Padding(3);
            this.machineTypes.Size = new System.Drawing.Size(768, 380);
            this.machineTypes.TabIndex = 1;
            this.machineTypes.Text = "MachineTypes";
            this.machineTypes.UseVisualStyleBackColor = true;
            // 
            // users
            // 
            this.users.Controls.Add(this.tableLayoutPanelUser);
            this.users.Controls.Add(this.buttonAddNewUser);
            this.users.Controls.Add(this.listViewUsers);
            this.users.Location = new System.Drawing.Point(4, 22);
            this.users.Name = "users";
            this.users.Padding = new System.Windows.Forms.Padding(3);
            this.users.Size = new System.Drawing.Size(768, 380);
            this.users.TabIndex = 0;
            this.users.Text = "Users";
            this.users.UseVisualStyleBackColor = true;
            // 
            // tableLayoutPanelUser
            // 
            this.tableLayoutPanelUser.ColumnCount = 3;
            this.tableLayoutPanelUser.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanelUser.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanelUser.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.tableLayoutPanelUser.Controls.Add(this.buttonDelete, 2, 1);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUpdatedBy, 1, 9);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxCreatedBy, 1, 8);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUpdatedAt, 1, 7);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxCreatedAt, 1, 6);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxRole, 1, 5);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxWebsite, 1, 4);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxMobile, 1, 3);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxEmail, 1, 2);
            this.tableLayoutPanelUser.Controls.Add(this.label4, 0, 2);
            this.tableLayoutPanelUser.Controls.Add(this.label5, 0, 3);
            this.tableLayoutPanelUser.Controls.Add(this.label6, 0, 4);
            this.tableLayoutPanelUser.Controls.Add(this.label7, 0, 5);
            this.tableLayoutPanelUser.Controls.Add(this.label8, 0, 6);
            this.tableLayoutPanelUser.Controls.Add(this.label9, 0, 7);
            this.tableLayoutPanelUser.Controls.Add(this.label10, 0, 8);
            this.tableLayoutPanelUser.Controls.Add(this.label11, 0, 9);
            this.tableLayoutPanelUser.Controls.Add(this.label2, 0, 0);
            this.tableLayoutPanelUser.Controls.Add(this.buttonModify, 2, 0);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUsername, 1, 0);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxPassword, 1, 1);
            this.tableLayoutPanelUser.Controls.Add(this.label3, 0, 1);
            this.tableLayoutPanelUser.Location = new System.Drawing.Point(196, 6);
            this.tableLayoutPanelUser.Name = "tableLayoutPanelUser";
            this.tableLayoutPanelUser.RowCount = 10;
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelUser.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanelUser.Size = new System.Drawing.Size(566, 368);
            this.tableLayoutPanelUser.TabIndex = 2;
            // 
            // buttonDelete
            // 
            this.buttonDelete.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonDelete.Location = new System.Drawing.Point(399, 42);
            this.buttonDelete.Name = "buttonDelete";
            this.buttonDelete.Size = new System.Drawing.Size(164, 23);
            this.buttonDelete.TabIndex = 30;
            this.buttonDelete.Text = "Delete";
            this.buttonDelete.UseVisualStyleBackColor = true;
            // 
            // textBoxUpdatedBy
            // 
            this.textBoxUpdatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUpdatedBy.Location = new System.Drawing.Point(116, 336);
            this.textBoxUpdatedBy.Name = "textBoxUpdatedBy";
            this.textBoxUpdatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxUpdatedBy.TabIndex = 28;
            // 
            // textBoxCreatedBy
            // 
            this.textBoxCreatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxCreatedBy.Location = new System.Drawing.Point(116, 296);
            this.textBoxCreatedBy.Name = "textBoxCreatedBy";
            this.textBoxCreatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxCreatedBy.TabIndex = 26;
            // 
            // textBoxUpdatedAt
            // 
            this.textBoxUpdatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUpdatedAt.Location = new System.Drawing.Point(116, 260);
            this.textBoxUpdatedAt.Name = "textBoxUpdatedAt";
            this.textBoxUpdatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxUpdatedAt.TabIndex = 24;
            // 
            // textBoxCreatedAt
            // 
            this.textBoxCreatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxCreatedAt.Location = new System.Drawing.Point(116, 224);
            this.textBoxCreatedAt.Name = "textBoxCreatedAt";
            this.textBoxCreatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxCreatedAt.TabIndex = 22;
            // 
            // textBoxRole
            // 
            this.textBoxRole.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxRole.Location = new System.Drawing.Point(116, 188);
            this.textBoxRole.Name = "textBoxRole";
            this.textBoxRole.Size = new System.Drawing.Size(277, 20);
            this.textBoxRole.TabIndex = 20;
            // 
            // textBoxWebsite
            // 
            this.textBoxWebsite.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxWebsite.Location = new System.Drawing.Point(116, 152);
            this.textBoxWebsite.Name = "textBoxWebsite";
            this.textBoxWebsite.Size = new System.Drawing.Size(277, 20);
            this.textBoxWebsite.TabIndex = 18;
            // 
            // textBoxMobile
            // 
            this.textBoxMobile.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMobile.Location = new System.Drawing.Point(116, 116);
            this.textBoxMobile.Name = "textBoxMobile";
            this.textBoxMobile.Size = new System.Drawing.Size(277, 20);
            this.textBoxMobile.TabIndex = 16;
            // 
            // textBoxEmail
            // 
            this.textBoxEmail.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxEmail.Location = new System.Drawing.Point(116, 80);
            this.textBoxEmail.Name = "textBoxEmail";
            this.textBoxEmail.Size = new System.Drawing.Size(277, 20);
            this.textBoxEmail.TabIndex = 14;
            // 
            // label4
            // 
            this.label4.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(3, 83);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(73, 13);
            this.label4.TabIndex = 2;
            this.label4.Text = "Email Address";
            // 
            // label5
            // 
            this.label5.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(3, 119);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(78, 13);
            this.label5.TabIndex = 3;
            this.label5.Text = "Mobile Number";
            // 
            // label6
            // 
            this.label6.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(3, 155);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(46, 13);
            this.label6.TabIndex = 4;
            this.label6.Text = "Website";
            // 
            // label7
            // 
            this.label7.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(3, 191);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(29, 13);
            this.label7.TabIndex = 5;
            this.label7.Text = "Role";
            // 
            // label8
            // 
            this.label8.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(3, 227);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(53, 13);
            this.label8.TabIndex = 6;
            this.label8.Text = "createdAt";
            // 
            // label9
            // 
            this.label9.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(3, 263);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(56, 13);
            this.label9.TabIndex = 7;
            this.label9.Text = "updatedAt";
            // 
            // label10
            // 
            this.label10.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(3, 299);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(55, 13);
            this.label10.TabIndex = 8;
            this.label10.Text = "createdBy";
            // 
            // label11
            // 
            this.label11.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(3, 339);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(58, 13);
            this.label11.TabIndex = 9;
            this.label11.Text = "updatedBy";
            // 
            // label2
            // 
            this.label2.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(3, 11);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(55, 13);
            this.label2.TabIndex = 0;
            this.label2.Text = "Username";
            // 
            // buttonModify
            // 
            this.buttonModify.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonModify.Location = new System.Drawing.Point(399, 6);
            this.buttonModify.Name = "buttonModify";
            this.buttonModify.Size = new System.Drawing.Size(164, 23);
            this.buttonModify.TabIndex = 29;
            this.buttonModify.Text = "Update";
            this.buttonModify.UseVisualStyleBackColor = true;
            this.buttonModify.Click += new System.EventHandler(this.buttonModify_Click);
            // 
            // textBoxUsername
            // 
            this.textBoxUsername.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUsername.Enabled = false;
            this.textBoxUsername.Location = new System.Drawing.Point(116, 8);
            this.textBoxUsername.Name = "textBoxUsername";
            this.textBoxUsername.Size = new System.Drawing.Size(277, 20);
            this.textBoxUsername.TabIndex = 12;
            // 
            // textBoxPassword
            // 
            this.textBoxPassword.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxPassword.Location = new System.Drawing.Point(116, 44);
            this.textBoxPassword.Name = "textBoxPassword";
            this.textBoxPassword.Size = new System.Drawing.Size(277, 20);
            this.textBoxPassword.TabIndex = 12;
            // 
            // label3
            // 
            this.label3.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(3, 47);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(53, 13);
            this.label3.TabIndex = 0;
            this.label3.Text = "Password";
            // 
            // buttonAddNewUser
            // 
            this.buttonAddNewUser.Location = new System.Drawing.Point(0, 353);
            this.buttonAddNewUser.Name = "buttonAddNewUser";
            this.buttonAddNewUser.Size = new System.Drawing.Size(190, 23);
            this.buttonAddNewUser.TabIndex = 1;
            this.buttonAddNewUser.Text = "Add New User";
            this.buttonAddNewUser.UseVisualStyleBackColor = true;
            // 
            // listViewUsers
            // 
            this.listViewUsers.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listViewUsers.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.userID,
            this.userName});
            this.listViewUsers.FullRowSelect = true;
            this.listViewUsers.GridLines = true;
            this.listViewUsers.Location = new System.Drawing.Point(0, 0);
            this.listViewUsers.MultiSelect = false;
            this.listViewUsers.Name = "listViewUsers";
            this.listViewUsers.Size = new System.Drawing.Size(190, 347);
            this.listViewUsers.TabIndex = 0;
            this.listViewUsers.UseCompatibleStateImageBehavior = false;
            this.listViewUsers.View = System.Windows.Forms.View.Details;
            this.listViewUsers.ItemActivate += new System.EventHandler(this.listViewUsers_ItemActivate);
            // 
            // userID
            // 
            this.userID.Text = "User ID";
            // 
            // userName
            // 
            this.userName.Text = "Username";
            this.userName.Width = 127;
            // 
            // tabControl
            // 
            this.tabControl.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tabControl.Controls.Add(this.users);
            this.tabControl.Controls.Add(this.machineTypes);
            this.tabControl.Controls.Add(this.machines);
            this.tabControl.Controls.Add(this.reservations);
            this.tabControl.Location = new System.Drawing.Point(12, 32);
            this.tabControl.Name = "tabControl";
            this.tabControl.SelectedIndex = 0;
            this.tabControl.Size = new System.Drawing.Size(776, 406);
            this.tabControl.TabIndex = 0;
            this.tabControl.SelectedIndexChanged += new System.EventHandler(this.tabControl_SelectedIndexChanged);
            // 
            // textBoxServerIPPort
            // 
            this.textBoxServerIPPort.Location = new System.Drawing.Point(88, 6);
            this.textBoxServerIPPort.Name = "textBoxServerIPPort";
            this.textBoxServerIPPort.Size = new System.Drawing.Size(156, 20);
            this.textBoxServerIPPort.TabIndex = 1;
            this.textBoxServerIPPort.Text = "127.0.0.1:5000";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(9, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(73, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "Server IP:Port";
            // 
            // buttonConnectServer
            // 
            this.buttonConnectServer.Location = new System.Drawing.Point(250, 4);
            this.buttonConnectServer.Name = "buttonConnectServer";
            this.buttonConnectServer.Size = new System.Drawing.Size(75, 23);
            this.buttonConnectServer.TabIndex = 3;
            this.buttonConnectServer.Text = "Connect";
            this.buttonConnectServer.UseVisualStyleBackColor = true;
            this.buttonConnectServer.Click += new System.EventHandler(this.buttonConnectServer_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.buttonConnectServer);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBoxServerIPPort);
            this.Controls.Add(this.tabControl);
            this.Name = "Form1";
            this.Text = "PWP Client";
            this.users.ResumeLayout(false);
            this.tableLayoutPanelUser.ResumeLayout(false);
            this.tableLayoutPanelUser.PerformLayout();
            this.tabControl.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TabPage reservations;
        private System.Windows.Forms.TabPage machines;
        private System.Windows.Forms.TabPage machineTypes;
        private System.Windows.Forms.TabPage users;
        private System.Windows.Forms.TabControl tabControl;
        private System.Windows.Forms.ListView listViewUsers;
        private System.Windows.Forms.ColumnHeader userID;
        private System.Windows.Forms.ColumnHeader userName;
        private System.Windows.Forms.TextBox textBoxServerIPPort;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button buttonConnectServer;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanelUser;
        private System.Windows.Forms.Button buttonDelete;
        private System.Windows.Forms.TextBox textBoxUpdatedBy;
        private System.Windows.Forms.TextBox textBoxCreatedBy;
        private System.Windows.Forms.TextBox textBoxUpdatedAt;
        private System.Windows.Forms.TextBox textBoxCreatedAt;
        private System.Windows.Forms.TextBox textBoxRole;
        private System.Windows.Forms.TextBox textBoxWebsite;
        private System.Windows.Forms.TextBox textBoxMobile;
        private System.Windows.Forms.TextBox textBoxEmail;
        private System.Windows.Forms.TextBox textBoxUsername;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button buttonModify;
        private System.Windows.Forms.Button buttonAddNewUser;
        private System.Windows.Forms.TextBox textBoxPassword;
        private System.Windows.Forms.Label label3;
    }
}


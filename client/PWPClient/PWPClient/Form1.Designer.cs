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
            this.tabControl = new System.Windows.Forms.TabControl();
            this.listViewUsers = new System.Windows.Forms.ListView();
            this.userID = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.userName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.textBoxServerIPPort = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.buttonConnectServer = new System.Windows.Forms.Button();
            this.users.SuspendLayout();
            this.tabControl.SuspendLayout();
            this.SuspendLayout();
            // 
            // reservations
            // 
            this.reservations.Location = new System.Drawing.Point(4, 22);
            this.reservations.Name = "reservations";
            this.reservations.Size = new System.Drawing.Size(768, 400);
            this.reservations.TabIndex = 3;
            this.reservations.Text = "Reservations";
            this.reservations.UseVisualStyleBackColor = true;
            // 
            // machines
            // 
            this.machines.Location = new System.Drawing.Point(4, 22);
            this.machines.Name = "machines";
            this.machines.Size = new System.Drawing.Size(768, 400);
            this.machines.TabIndex = 2;
            this.machines.Text = "Machines";
            this.machines.UseVisualStyleBackColor = true;
            // 
            // machineTypes
            // 
            this.machineTypes.Location = new System.Drawing.Point(4, 22);
            this.machineTypes.Name = "machineTypes";
            this.machineTypes.Padding = new System.Windows.Forms.Padding(3);
            this.machineTypes.Size = new System.Drawing.Size(768, 400);
            this.machineTypes.TabIndex = 1;
            this.machineTypes.Text = "MachineTypes";
            this.machineTypes.UseVisualStyleBackColor = true;
            // 
            // users
            // 
            this.users.Controls.Add(this.listViewUsers);
            this.users.Location = new System.Drawing.Point(4, 22);
            this.users.Name = "users";
            this.users.Padding = new System.Windows.Forms.Padding(3);
            this.users.Size = new System.Drawing.Size(768, 380);
            this.users.TabIndex = 0;
            this.users.Text = "Users";
            this.users.UseVisualStyleBackColor = true;
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
            this.listViewUsers.Size = new System.Drawing.Size(190, 380);
            this.listViewUsers.TabIndex = 0;
            this.listViewUsers.UseCompatibleStateImageBehavior = false;
            this.listViewUsers.View = System.Windows.Forms.View.Details;
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
    }
}


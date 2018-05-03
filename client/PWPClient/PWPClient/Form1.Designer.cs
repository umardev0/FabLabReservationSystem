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
            this.tableLayoutPanelMachine = new System.Windows.Forms.TableLayoutPanel();
            this.buttonAddMachine = new System.Windows.Forms.Button();
            this.buttonDeleteMachine = new System.Windows.Forms.Button();
            this.textBoxMachineTutorial = new System.Windows.Forms.TextBox();
            this.textBoxMachineTypeID = new System.Windows.Forms.TextBox();
            this.label14 = new System.Windows.Forms.Label();
            this.label15 = new System.Windows.Forms.Label();
            this.label22 = new System.Windows.Forms.Label();
            this.buttonUpdateMachine = new System.Windows.Forms.Button();
            this.textBoxMachineName = new System.Windows.Forms.TextBox();
            this.label23 = new System.Windows.Forms.Label();
            this.textBoxMachineID = new System.Windows.Forms.TextBox();
            this.label24 = new System.Windows.Forms.Label();
            this.label25 = new System.Windows.Forms.Label();
            this.label26 = new System.Windows.Forms.Label();
            this.label27 = new System.Windows.Forms.Label();
            this.textBoxMachineCreatedBy = new System.Windows.Forms.TextBox();
            this.textBoxMachineCreatedAt = new System.Windows.Forms.TextBox();
            this.textBoxMachineUpdatedAt = new System.Windows.Forms.TextBox();
            this.textBoxMachineUpdatedBy = new System.Windows.Forms.TextBox();
            this.buttonClearMachineForm = new System.Windows.Forms.Button();
            this.listViewMachine = new System.Windows.Forms.ListView();
            this.machineID = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.machineName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.machineType = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.machineTypes = new System.Windows.Forms.TabPage();
            this.buttonClearTypeForm = new System.Windows.Forms.Button();
            this.tableLayoutPanelTypes = new System.Windows.Forms.TableLayoutPanel();
            this.buttonAddType = new System.Windows.Forms.Button();
            this.buttonDeleteType = new System.Windows.Forms.Button();
            this.textBoxTypePastProjects = new System.Windows.Forms.TextBox();
            this.textBoxTypeFullName = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.label20 = new System.Windows.Forms.Label();
            this.buttonModifyType = new System.Windows.Forms.Button();
            this.textBoxTypeName = new System.Windows.Forms.TextBox();
            this.label21 = new System.Windows.Forms.Label();
            this.textBoxTypeID = new System.Windows.Forms.TextBox();
            this.label16 = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            this.label18 = new System.Windows.Forms.Label();
            this.label19 = new System.Windows.Forms.Label();
            this.textBoxTypeCreatedBy = new System.Windows.Forms.TextBox();
            this.textBoxTypeCreatedAt = new System.Windows.Forms.TextBox();
            this.textBoxTypeUpdatedAt = new System.Windows.Forms.TextBox();
            this.textBoxTypeUpdatedBy = new System.Windows.Forms.TextBox();
            this.listViewMachineTypes = new System.Windows.Forms.ListView();
            this.columnHeader1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.users = new System.Windows.Forms.TabPage();
            this.tableLayoutPanelUser = new System.Windows.Forms.TableLayoutPanel();
            this.buttonAddUser = new System.Windows.Forms.Button();
            this.buttonDeleteUser = new System.Windows.Forms.Button();
            this.textBoxUserUpdatedBy = new System.Windows.Forms.TextBox();
            this.textBoxUserCreatedBy = new System.Windows.Forms.TextBox();
            this.textBoxUserUpdatedAt = new System.Windows.Forms.TextBox();
            this.textBoxUserCreatedAt = new System.Windows.Forms.TextBox();
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
            this.buttonModifyUser = new System.Windows.Forms.Button();
            this.textBoxUsername = new System.Windows.Forms.TextBox();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.checkBoxAdmin = new System.Windows.Forms.CheckBox();
            this.buttonClearUserForm = new System.Windows.Forms.Button();
            this.listViewUsers = new System.Windows.Forms.ListView();
            this.userID = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.userName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.tabControl = new System.Windows.Forms.TabControl();
            this.textBoxServerIPPort = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.buttonConnectServer = new System.Windows.Forms.Button();
            this.buttonHistory = new System.Windows.Forms.Button();
            this.machines.SuspendLayout();
            this.tableLayoutPanelMachine.SuspendLayout();
            this.machineTypes.SuspendLayout();
            this.tableLayoutPanelTypes.SuspendLayout();
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
            this.machines.Controls.Add(this.tableLayoutPanelMachine);
            this.machines.Controls.Add(this.buttonClearMachineForm);
            this.machines.Controls.Add(this.listViewMachine);
            this.machines.Location = new System.Drawing.Point(4, 22);
            this.machines.Name = "machines";
            this.machines.Size = new System.Drawing.Size(768, 380);
            this.machines.TabIndex = 2;
            this.machines.Text = "Machines";
            this.machines.UseVisualStyleBackColor = true;
            // 
            // tableLayoutPanelMachine
            // 
            this.tableLayoutPanelMachine.ColumnCount = 3;
            this.tableLayoutPanelMachine.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanelMachine.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanelMachine.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.tableLayoutPanelMachine.Controls.Add(this.buttonAddMachine, 2, 2);
            this.tableLayoutPanelMachine.Controls.Add(this.buttonDeleteMachine, 2, 1);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineTutorial, 1, 3);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineTypeID, 1, 2);
            this.tableLayoutPanelMachine.Controls.Add(this.label14, 0, 2);
            this.tableLayoutPanelMachine.Controls.Add(this.label15, 0, 3);
            this.tableLayoutPanelMachine.Controls.Add(this.label22, 0, 0);
            this.tableLayoutPanelMachine.Controls.Add(this.buttonUpdateMachine, 2, 0);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineName, 1, 1);
            this.tableLayoutPanelMachine.Controls.Add(this.label23, 0, 1);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineID, 1, 0);
            this.tableLayoutPanelMachine.Controls.Add(this.label24, 0, 4);
            this.tableLayoutPanelMachine.Controls.Add(this.label25, 0, 5);
            this.tableLayoutPanelMachine.Controls.Add(this.label26, 0, 6);
            this.tableLayoutPanelMachine.Controls.Add(this.label27, 0, 7);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineCreatedBy, 1, 6);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineCreatedAt, 1, 4);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineUpdatedAt, 1, 5);
            this.tableLayoutPanelMachine.Controls.Add(this.textBoxMachineUpdatedBy, 1, 7);
            this.tableLayoutPanelMachine.Controls.Add(this.buttonHistory, 2, 3);
            this.tableLayoutPanelMachine.Location = new System.Drawing.Point(199, 3);
            this.tableLayoutPanelMachine.Name = "tableLayoutPanelMachine";
            this.tableLayoutPanelMachine.RowCount = 8;
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelMachine.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanelMachine.Size = new System.Drawing.Size(566, 368);
            this.tableLayoutPanelMachine.TabIndex = 6;
            // 
            // buttonAddMachine
            // 
            this.buttonAddMachine.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonAddMachine.Location = new System.Drawing.Point(399, 103);
            this.buttonAddMachine.Name = "buttonAddMachine";
            this.buttonAddMachine.Size = new System.Drawing.Size(164, 23);
            this.buttonAddMachine.TabIndex = 32;
            this.buttonAddMachine.Text = "Create Machine";
            this.buttonAddMachine.UseVisualStyleBackColor = true;
            this.buttonAddMachine.Visible = false;
            // 
            // buttonDeleteMachine
            // 
            this.buttonDeleteMachine.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonDeleteMachine.Location = new System.Drawing.Point(399, 57);
            this.buttonDeleteMachine.Name = "buttonDeleteMachine";
            this.buttonDeleteMachine.Size = new System.Drawing.Size(164, 23);
            this.buttonDeleteMachine.TabIndex = 30;
            this.buttonDeleteMachine.Text = "Delete";
            this.buttonDeleteMachine.UseVisualStyleBackColor = true;
            // 
            // textBoxMachineTutorial
            // 
            this.textBoxMachineTutorial.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineTutorial.Location = new System.Drawing.Point(116, 151);
            this.textBoxMachineTutorial.Name = "textBoxMachineTutorial";
            this.textBoxMachineTutorial.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineTutorial.TabIndex = 16;
            // 
            // textBoxMachineTypeID
            // 
            this.textBoxMachineTypeID.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineTypeID.Location = new System.Drawing.Point(116, 105);
            this.textBoxMachineTypeID.Name = "textBoxMachineTypeID";
            this.textBoxMachineTypeID.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineTypeID.TabIndex = 14;
            // 
            // label14
            // 
            this.label14.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(3, 108);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(31, 13);
            this.label14.TabIndex = 2;
            this.label14.Text = "Type";
            // 
            // label15
            // 
            this.label15.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label15.AutoSize = true;
            this.label15.Location = new System.Drawing.Point(3, 154);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(42, 13);
            this.label15.TabIndex = 3;
            this.label15.Text = "Tutorial";
            // 
            // label22
            // 
            this.label22.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label22.AutoSize = true;
            this.label22.Location = new System.Drawing.Point(3, 16);
            this.label22.Name = "label22";
            this.label22.Size = new System.Drawing.Size(62, 13);
            this.label22.TabIndex = 0;
            this.label22.Text = "Machine ID";
            // 
            // buttonUpdateMachine
            // 
            this.buttonUpdateMachine.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonUpdateMachine.Location = new System.Drawing.Point(399, 11);
            this.buttonUpdateMachine.Name = "buttonUpdateMachine";
            this.buttonUpdateMachine.Size = new System.Drawing.Size(164, 23);
            this.buttonUpdateMachine.TabIndex = 29;
            this.buttonUpdateMachine.Text = "Update";
            this.buttonUpdateMachine.UseVisualStyleBackColor = true;
            // 
            // textBoxMachineName
            // 
            this.textBoxMachineName.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineName.Location = new System.Drawing.Point(116, 59);
            this.textBoxMachineName.Name = "textBoxMachineName";
            this.textBoxMachineName.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineName.TabIndex = 12;
            // 
            // label23
            // 
            this.label23.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label23.AutoSize = true;
            this.label23.Location = new System.Drawing.Point(3, 62);
            this.label23.Name = "label23";
            this.label23.Size = new System.Drawing.Size(79, 13);
            this.label23.TabIndex = 0;
            this.label23.Text = "Machine Name";
            // 
            // textBoxMachineID
            // 
            this.textBoxMachineID.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineID.Enabled = false;
            this.textBoxMachineID.Location = new System.Drawing.Point(116, 13);
            this.textBoxMachineID.Name = "textBoxMachineID";
            this.textBoxMachineID.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineID.TabIndex = 12;
            // 
            // label24
            // 
            this.label24.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label24.AutoSize = true;
            this.label24.Location = new System.Drawing.Point(3, 200);
            this.label24.Name = "label24";
            this.label24.Size = new System.Drawing.Size(53, 13);
            this.label24.TabIndex = 6;
            this.label24.Text = "createdAt";
            // 
            // label25
            // 
            this.label25.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label25.AutoSize = true;
            this.label25.Location = new System.Drawing.Point(3, 246);
            this.label25.Name = "label25";
            this.label25.Size = new System.Drawing.Size(56, 13);
            this.label25.TabIndex = 7;
            this.label25.Text = "updatedAt";
            // 
            // label26
            // 
            this.label26.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label26.AutoSize = true;
            this.label26.Location = new System.Drawing.Point(3, 292);
            this.label26.Name = "label26";
            this.label26.Size = new System.Drawing.Size(55, 13);
            this.label26.TabIndex = 8;
            this.label26.Text = "createdBy";
            // 
            // label27
            // 
            this.label27.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label27.AutoSize = true;
            this.label27.Location = new System.Drawing.Point(3, 338);
            this.label27.Name = "label27";
            this.label27.Size = new System.Drawing.Size(58, 13);
            this.label27.TabIndex = 9;
            this.label27.Text = "updatedBy";
            // 
            // textBoxMachineCreatedBy
            // 
            this.textBoxMachineCreatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineCreatedBy.Location = new System.Drawing.Point(116, 289);
            this.textBoxMachineCreatedBy.Name = "textBoxMachineCreatedBy";
            this.textBoxMachineCreatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineCreatedBy.TabIndex = 18;
            // 
            // textBoxMachineCreatedAt
            // 
            this.textBoxMachineCreatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineCreatedAt.Enabled = false;
            this.textBoxMachineCreatedAt.Location = new System.Drawing.Point(116, 197);
            this.textBoxMachineCreatedAt.Name = "textBoxMachineCreatedAt";
            this.textBoxMachineCreatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineCreatedAt.TabIndex = 22;
            // 
            // textBoxMachineUpdatedAt
            // 
            this.textBoxMachineUpdatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineUpdatedAt.Enabled = false;
            this.textBoxMachineUpdatedAt.Location = new System.Drawing.Point(116, 243);
            this.textBoxMachineUpdatedAt.Name = "textBoxMachineUpdatedAt";
            this.textBoxMachineUpdatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineUpdatedAt.TabIndex = 24;
            // 
            // textBoxMachineUpdatedBy
            // 
            this.textBoxMachineUpdatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxMachineUpdatedBy.Location = new System.Drawing.Point(116, 335);
            this.textBoxMachineUpdatedBy.Name = "textBoxMachineUpdatedBy";
            this.textBoxMachineUpdatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxMachineUpdatedBy.TabIndex = 26;
            // 
            // buttonClearMachineForm
            // 
            this.buttonClearMachineForm.Location = new System.Drawing.Point(4, 354);
            this.buttonClearMachineForm.Name = "buttonClearMachineForm";
            this.buttonClearMachineForm.Size = new System.Drawing.Size(190, 23);
            this.buttonClearMachineForm.TabIndex = 5;
            this.buttonClearMachineForm.Text = "Add New Machine";
            this.buttonClearMachineForm.UseVisualStyleBackColor = true;
            // 
            // listViewMachine
            // 
            this.listViewMachine.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listViewMachine.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.machineID,
            this.machineName,
            this.machineType});
            this.listViewMachine.FullRowSelect = true;
            this.listViewMachine.GridLines = true;
            this.listViewMachine.Location = new System.Drawing.Point(3, 3);
            this.listViewMachine.MultiSelect = false;
            this.listViewMachine.Name = "listViewMachine";
            this.listViewMachine.Size = new System.Drawing.Size(191, 347);
            this.listViewMachine.TabIndex = 2;
            this.listViewMachine.UseCompatibleStateImageBehavior = false;
            this.listViewMachine.View = System.Windows.Forms.View.Details;
            this.listViewMachine.ItemActivate += new System.EventHandler(this.listViewMachine_ItemActivate);
            // 
            // machineID
            // 
            this.machineID.Text = "ID";
            this.machineID.Width = 42;
            // 
            // machineName
            // 
            this.machineName.Text = "Name";
            this.machineName.Width = 82;
            // 
            // machineType
            // 
            this.machineType.Text = "Type";
            // 
            // machineTypes
            // 
            this.machineTypes.Controls.Add(this.buttonClearTypeForm);
            this.machineTypes.Controls.Add(this.tableLayoutPanelTypes);
            this.machineTypes.Controls.Add(this.listViewMachineTypes);
            this.machineTypes.Location = new System.Drawing.Point(4, 22);
            this.machineTypes.Name = "machineTypes";
            this.machineTypes.Padding = new System.Windows.Forms.Padding(3);
            this.machineTypes.Size = new System.Drawing.Size(768, 380);
            this.machineTypes.TabIndex = 1;
            this.machineTypes.Text = "MachineTypes";
            this.machineTypes.UseVisualStyleBackColor = true;
            // 
            // buttonClearTypeForm
            // 
            this.buttonClearTypeForm.Location = new System.Drawing.Point(3, 354);
            this.buttonClearTypeForm.Name = "buttonClearTypeForm";
            this.buttonClearTypeForm.Size = new System.Drawing.Size(190, 23);
            this.buttonClearTypeForm.TabIndex = 4;
            this.buttonClearTypeForm.Text = "Add New Type";
            this.buttonClearTypeForm.UseVisualStyleBackColor = true;
            this.buttonClearTypeForm.Click += new System.EventHandler(this.buttonClearTypeForm_Click);
            // 
            // tableLayoutPanelTypes
            // 
            this.tableLayoutPanelTypes.ColumnCount = 3;
            this.tableLayoutPanelTypes.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanelTypes.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanelTypes.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.tableLayoutPanelTypes.Controls.Add(this.buttonAddType, 2, 2);
            this.tableLayoutPanelTypes.Controls.Add(this.buttonDeleteType, 2, 1);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypePastProjects, 1, 3);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeFullName, 1, 2);
            this.tableLayoutPanelTypes.Controls.Add(this.label12, 0, 2);
            this.tableLayoutPanelTypes.Controls.Add(this.label13, 0, 3);
            this.tableLayoutPanelTypes.Controls.Add(this.label20, 0, 0);
            this.tableLayoutPanelTypes.Controls.Add(this.buttonModifyType, 2, 0);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeName, 1, 1);
            this.tableLayoutPanelTypes.Controls.Add(this.label21, 0, 1);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeID, 1, 0);
            this.tableLayoutPanelTypes.Controls.Add(this.label16, 0, 4);
            this.tableLayoutPanelTypes.Controls.Add(this.label17, 0, 5);
            this.tableLayoutPanelTypes.Controls.Add(this.label18, 0, 6);
            this.tableLayoutPanelTypes.Controls.Add(this.label19, 0, 7);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeCreatedBy, 1, 6);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeCreatedAt, 1, 4);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeUpdatedAt, 1, 5);
            this.tableLayoutPanelTypes.Controls.Add(this.textBoxTypeUpdatedBy, 1, 7);
            this.tableLayoutPanelTypes.Location = new System.Drawing.Point(199, 3);
            this.tableLayoutPanelTypes.Name = "tableLayoutPanelTypes";
            this.tableLayoutPanelTypes.RowCount = 8;
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 10F));
            this.tableLayoutPanelTypes.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanelTypes.Size = new System.Drawing.Size(566, 368);
            this.tableLayoutPanelTypes.TabIndex = 3;
            // 
            // buttonAddType
            // 
            this.buttonAddType.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonAddType.Location = new System.Drawing.Point(399, 103);
            this.buttonAddType.Name = "buttonAddType";
            this.buttonAddType.Size = new System.Drawing.Size(164, 23);
            this.buttonAddType.TabIndex = 32;
            this.buttonAddType.Text = "Create Type";
            this.buttonAddType.UseVisualStyleBackColor = true;
            this.buttonAddType.Visible = false;
            this.buttonAddType.Click += new System.EventHandler(this.buttonAddType_Click);
            // 
            // buttonDeleteType
            // 
            this.buttonDeleteType.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonDeleteType.Location = new System.Drawing.Point(399, 57);
            this.buttonDeleteType.Name = "buttonDeleteType";
            this.buttonDeleteType.Size = new System.Drawing.Size(164, 23);
            this.buttonDeleteType.TabIndex = 30;
            this.buttonDeleteType.Text = "Delete";
            this.buttonDeleteType.UseVisualStyleBackColor = true;
            this.buttonDeleteType.Click += new System.EventHandler(this.buttonDeleteType_Click);
            // 
            // textBoxTypePastProjects
            // 
            this.textBoxTypePastProjects.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypePastProjects.Location = new System.Drawing.Point(116, 151);
            this.textBoxTypePastProjects.Name = "textBoxTypePastProjects";
            this.textBoxTypePastProjects.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypePastProjects.TabIndex = 16;
            // 
            // textBoxTypeFullName
            // 
            this.textBoxTypeFullName.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeFullName.Location = new System.Drawing.Point(116, 105);
            this.textBoxTypeFullName.Name = "textBoxTypeFullName";
            this.textBoxTypeFullName.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeFullName.TabIndex = 14;
            // 
            // label12
            // 
            this.label12.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(3, 108);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(87, 13);
            this.label12.TabIndex = 2;
            this.label12.Text = "Type Description";
            // 
            // label13
            // 
            this.label13.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(3, 154);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(89, 13);
            this.label13.TabIndex = 3;
            this.label13.Text = "Previous Projects";
            // 
            // label20
            // 
            this.label20.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label20.AutoSize = true;
            this.label20.Location = new System.Drawing.Point(3, 16);
            this.label20.Name = "label20";
            this.label20.Size = new System.Drawing.Size(45, 13);
            this.label20.TabIndex = 0;
            this.label20.Text = "Type ID";
            // 
            // buttonModifyType
            // 
            this.buttonModifyType.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonModifyType.Location = new System.Drawing.Point(399, 11);
            this.buttonModifyType.Name = "buttonModifyType";
            this.buttonModifyType.Size = new System.Drawing.Size(164, 23);
            this.buttonModifyType.TabIndex = 29;
            this.buttonModifyType.Text = "Update";
            this.buttonModifyType.UseVisualStyleBackColor = true;
            this.buttonModifyType.Click += new System.EventHandler(this.buttonModifyType_Click);
            // 
            // textBoxTypeName
            // 
            this.textBoxTypeName.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeName.Location = new System.Drawing.Point(116, 59);
            this.textBoxTypeName.Name = "textBoxTypeName";
            this.textBoxTypeName.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeName.TabIndex = 12;
            // 
            // label21
            // 
            this.label21.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label21.AutoSize = true;
            this.label21.Location = new System.Drawing.Point(3, 62);
            this.label21.Name = "label21";
            this.label21.Size = new System.Drawing.Size(90, 13);
            this.label21.TabIndex = 0;
            this.label21.Text = "Type Short Name";
            // 
            // textBoxTypeID
            // 
            this.textBoxTypeID.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeID.Enabled = false;
            this.textBoxTypeID.Location = new System.Drawing.Point(116, 13);
            this.textBoxTypeID.Name = "textBoxTypeID";
            this.textBoxTypeID.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeID.TabIndex = 12;
            // 
            // label16
            // 
            this.label16.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(3, 200);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(53, 13);
            this.label16.TabIndex = 6;
            this.label16.Text = "createdAt";
            // 
            // label17
            // 
            this.label17.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label17.AutoSize = true;
            this.label17.Location = new System.Drawing.Point(3, 246);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(56, 13);
            this.label17.TabIndex = 7;
            this.label17.Text = "updatedAt";
            // 
            // label18
            // 
            this.label18.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label18.AutoSize = true;
            this.label18.Location = new System.Drawing.Point(3, 292);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(55, 13);
            this.label18.TabIndex = 8;
            this.label18.Text = "createdBy";
            // 
            // label19
            // 
            this.label19.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.label19.AutoSize = true;
            this.label19.Location = new System.Drawing.Point(3, 338);
            this.label19.Name = "label19";
            this.label19.Size = new System.Drawing.Size(58, 13);
            this.label19.TabIndex = 9;
            this.label19.Text = "updatedBy";
            // 
            // textBoxTypeCreatedBy
            // 
            this.textBoxTypeCreatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeCreatedBy.Location = new System.Drawing.Point(116, 289);
            this.textBoxTypeCreatedBy.Name = "textBoxTypeCreatedBy";
            this.textBoxTypeCreatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeCreatedBy.TabIndex = 18;
            // 
            // textBoxTypeCreatedAt
            // 
            this.textBoxTypeCreatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeCreatedAt.Enabled = false;
            this.textBoxTypeCreatedAt.Location = new System.Drawing.Point(116, 197);
            this.textBoxTypeCreatedAt.Name = "textBoxTypeCreatedAt";
            this.textBoxTypeCreatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeCreatedAt.TabIndex = 22;
            // 
            // textBoxTypeUpdatedAt
            // 
            this.textBoxTypeUpdatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeUpdatedAt.Enabled = false;
            this.textBoxTypeUpdatedAt.Location = new System.Drawing.Point(116, 243);
            this.textBoxTypeUpdatedAt.Name = "textBoxTypeUpdatedAt";
            this.textBoxTypeUpdatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeUpdatedAt.TabIndex = 24;
            // 
            // textBoxTypeUpdatedBy
            // 
            this.textBoxTypeUpdatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxTypeUpdatedBy.Location = new System.Drawing.Point(116, 335);
            this.textBoxTypeUpdatedBy.Name = "textBoxTypeUpdatedBy";
            this.textBoxTypeUpdatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxTypeUpdatedBy.TabIndex = 26;
            // 
            // listViewMachineTypes
            // 
            this.listViewMachineTypes.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.listViewMachineTypes.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeader1,
            this.columnHeader2});
            this.listViewMachineTypes.FullRowSelect = true;
            this.listViewMachineTypes.GridLines = true;
            this.listViewMachineTypes.Location = new System.Drawing.Point(3, 3);
            this.listViewMachineTypes.MultiSelect = false;
            this.listViewMachineTypes.Name = "listViewMachineTypes";
            this.listViewMachineTypes.Size = new System.Drawing.Size(191, 347);
            this.listViewMachineTypes.TabIndex = 1;
            this.listViewMachineTypes.UseCompatibleStateImageBehavior = false;
            this.listViewMachineTypes.View = System.Windows.Forms.View.Details;
            this.listViewMachineTypes.ItemActivate += new System.EventHandler(this.listViewMachineTypes_ItemActivate);
            // 
            // columnHeader1
            // 
            this.columnHeader1.Text = "Type ID";
            // 
            // columnHeader2
            // 
            this.columnHeader2.Text = "Type Name";
            this.columnHeader2.Width = 127;
            // 
            // users
            // 
            this.users.Controls.Add(this.tableLayoutPanelUser);
            this.users.Controls.Add(this.buttonClearUserForm);
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
            this.tableLayoutPanelUser.Controls.Add(this.buttonAddUser, 2, 2);
            this.tableLayoutPanelUser.Controls.Add(this.buttonDeleteUser, 2, 1);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUserUpdatedBy, 1, 9);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUserCreatedBy, 1, 8);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUserUpdatedAt, 1, 7);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUserCreatedAt, 1, 6);
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
            this.tableLayoutPanelUser.Controls.Add(this.buttonModifyUser, 2, 0);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxUsername, 1, 0);
            this.tableLayoutPanelUser.Controls.Add(this.textBoxPassword, 1, 1);
            this.tableLayoutPanelUser.Controls.Add(this.label3, 0, 1);
            this.tableLayoutPanelUser.Controls.Add(this.checkBoxAdmin, 1, 5);
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
            // buttonAddUser
            // 
            this.buttonAddUser.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonAddUser.Location = new System.Drawing.Point(399, 78);
            this.buttonAddUser.Name = "buttonAddUser";
            this.buttonAddUser.Size = new System.Drawing.Size(164, 23);
            this.buttonAddUser.TabIndex = 32;
            this.buttonAddUser.Text = "Create User";
            this.buttonAddUser.UseVisualStyleBackColor = true;
            this.buttonAddUser.Visible = false;
            this.buttonAddUser.Click += new System.EventHandler(this.buttonAdd_Click);
            // 
            // buttonDeleteUser
            // 
            this.buttonDeleteUser.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonDeleteUser.Location = new System.Drawing.Point(399, 42);
            this.buttonDeleteUser.Name = "buttonDeleteUser";
            this.buttonDeleteUser.Size = new System.Drawing.Size(164, 23);
            this.buttonDeleteUser.TabIndex = 30;
            this.buttonDeleteUser.Text = "Delete";
            this.buttonDeleteUser.UseVisualStyleBackColor = true;
            this.buttonDeleteUser.Click += new System.EventHandler(this.buttonDelete_Click);
            // 
            // textBoxUserUpdatedBy
            // 
            this.textBoxUserUpdatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUserUpdatedBy.Location = new System.Drawing.Point(116, 336);
            this.textBoxUserUpdatedBy.Name = "textBoxUserUpdatedBy";
            this.textBoxUserUpdatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxUserUpdatedBy.TabIndex = 28;
            // 
            // textBoxUserCreatedBy
            // 
            this.textBoxUserCreatedBy.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUserCreatedBy.Location = new System.Drawing.Point(116, 296);
            this.textBoxUserCreatedBy.Name = "textBoxUserCreatedBy";
            this.textBoxUserCreatedBy.Size = new System.Drawing.Size(277, 20);
            this.textBoxUserCreatedBy.TabIndex = 26;
            // 
            // textBoxUserUpdatedAt
            // 
            this.textBoxUserUpdatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUserUpdatedAt.Enabled = false;
            this.textBoxUserUpdatedAt.Location = new System.Drawing.Point(116, 260);
            this.textBoxUserUpdatedAt.Name = "textBoxUserUpdatedAt";
            this.textBoxUserUpdatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxUserUpdatedAt.TabIndex = 24;
            // 
            // textBoxUserCreatedAt
            // 
            this.textBoxUserCreatedAt.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.textBoxUserCreatedAt.Enabled = false;
            this.textBoxUserCreatedAt.Location = new System.Drawing.Point(116, 224);
            this.textBoxUserCreatedAt.Name = "textBoxUserCreatedAt";
            this.textBoxUserCreatedAt.Size = new System.Drawing.Size(277, 20);
            this.textBoxUserCreatedAt.TabIndex = 22;
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
            this.label7.Size = new System.Drawing.Size(67, 13);
            this.label7.TabIndex = 5;
            this.label7.Text = "Administrator";
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
            // buttonModifyUser
            // 
            this.buttonModifyUser.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonModifyUser.Location = new System.Drawing.Point(399, 6);
            this.buttonModifyUser.Name = "buttonModifyUser";
            this.buttonModifyUser.Size = new System.Drawing.Size(164, 23);
            this.buttonModifyUser.TabIndex = 29;
            this.buttonModifyUser.Text = "Update";
            this.buttonModifyUser.UseVisualStyleBackColor = true;
            this.buttonModifyUser.Click += new System.EventHandler(this.buttonModify_Click);
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
            // checkBoxAdmin
            // 
            this.checkBoxAdmin.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.checkBoxAdmin.AutoSize = true;
            this.checkBoxAdmin.Location = new System.Drawing.Point(116, 189);
            this.checkBoxAdmin.Name = "checkBoxAdmin";
            this.checkBoxAdmin.Size = new System.Drawing.Size(88, 17);
            this.checkBoxAdmin.TabIndex = 31;
            this.checkBoxAdmin.Text = "Regular User";
            this.checkBoxAdmin.UseVisualStyleBackColor = true;
            this.checkBoxAdmin.CheckedChanged += new System.EventHandler(this.checkBoxAdmin_CheckedChanged);
            // 
            // buttonClearUserForm
            // 
            this.buttonClearUserForm.Location = new System.Drawing.Point(0, 353);
            this.buttonClearUserForm.Name = "buttonClearUserForm";
            this.buttonClearUserForm.Size = new System.Drawing.Size(190, 23);
            this.buttonClearUserForm.TabIndex = 1;
            this.buttonClearUserForm.Text = "Add New User";
            this.buttonClearUserForm.UseVisualStyleBackColor = true;
            this.buttonClearUserForm.Click += new System.EventHandler(this.buttonAddNewUser_Click);
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
            // buttonHistory
            // 
            this.buttonHistory.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.buttonHistory.Location = new System.Drawing.Point(399, 149);
            this.buttonHistory.Name = "buttonHistory";
            this.buttonHistory.Size = new System.Drawing.Size(164, 23);
            this.buttonHistory.TabIndex = 32;
            this.buttonHistory.Text = "History";
            this.buttonHistory.UseVisualStyleBackColor = true;
            this.buttonHistory.Visible = false;
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
            this.machines.ResumeLayout(false);
            this.tableLayoutPanelMachine.ResumeLayout(false);
            this.tableLayoutPanelMachine.PerformLayout();
            this.machineTypes.ResumeLayout(false);
            this.tableLayoutPanelTypes.ResumeLayout(false);
            this.tableLayoutPanelTypes.PerformLayout();
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
        private System.Windows.Forms.Button buttonDeleteUser;
        private System.Windows.Forms.TextBox textBoxUserUpdatedBy;
        private System.Windows.Forms.TextBox textBoxUserCreatedBy;
        private System.Windows.Forms.TextBox textBoxUserUpdatedAt;
        private System.Windows.Forms.TextBox textBoxUserCreatedAt;
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
        private System.Windows.Forms.Button buttonModifyUser;
        private System.Windows.Forms.Button buttonClearUserForm;
        private System.Windows.Forms.TextBox textBoxPassword;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.CheckBox checkBoxAdmin;
        private System.Windows.Forms.Button buttonAddUser;
        private System.Windows.Forms.ListView listViewMachineTypes;
        private System.Windows.Forms.ColumnHeader columnHeader1;
        private System.Windows.Forms.ColumnHeader columnHeader2;
        private System.Windows.Forms.Button buttonClearTypeForm;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanelTypes;
        private System.Windows.Forms.Button buttonAddType;
        private System.Windows.Forms.Button buttonDeleteType;
        private System.Windows.Forms.TextBox textBoxTypePastProjects;
        private System.Windows.Forms.TextBox textBoxTypeFullName;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label20;
        private System.Windows.Forms.Button buttonModifyType;
        private System.Windows.Forms.TextBox textBoxTypeName;
        private System.Windows.Forms.Label label21;
        private System.Windows.Forms.TextBox textBoxTypeID;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.Label label19;
        private System.Windows.Forms.TextBox textBoxTypeCreatedBy;
        private System.Windows.Forms.TextBox textBoxTypeCreatedAt;
        private System.Windows.Forms.TextBox textBoxTypeUpdatedAt;
        private System.Windows.Forms.TextBox textBoxTypeUpdatedBy;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanelMachine;
        private System.Windows.Forms.Button buttonAddMachine;
        private System.Windows.Forms.Button buttonDeleteMachine;
        private System.Windows.Forms.TextBox textBoxMachineTutorial;
        private System.Windows.Forms.TextBox textBoxMachineTypeID;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.Label label22;
        private System.Windows.Forms.Button buttonUpdateMachine;
        private System.Windows.Forms.TextBox textBoxMachineName;
        private System.Windows.Forms.Label label23;
        private System.Windows.Forms.TextBox textBoxMachineID;
        private System.Windows.Forms.Label label24;
        private System.Windows.Forms.Label label25;
        private System.Windows.Forms.Label label26;
        private System.Windows.Forms.Label label27;
        private System.Windows.Forms.TextBox textBoxMachineCreatedBy;
        private System.Windows.Forms.TextBox textBoxMachineCreatedAt;
        private System.Windows.Forms.TextBox textBoxMachineUpdatedAt;
        private System.Windows.Forms.TextBox textBoxMachineUpdatedBy;
        private System.Windows.Forms.Button buttonClearMachineForm;
        private System.Windows.Forms.ListView listViewMachine;
        private System.Windows.Forms.ColumnHeader machineID;
        private System.Windows.Forms.ColumnHeader machineName;
        private System.Windows.Forms.ColumnHeader machineType;
        private System.Windows.Forms.Button buttonHistory;
    }
}


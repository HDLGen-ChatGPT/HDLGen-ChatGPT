#Internal signals section in HDL Designer. This class will call int_sig_dialog when adding/editing internal signal and will call internal_help.py when help is called
import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta

sys.path.append("../..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.InternalSignal.int_sig_dialog import IntSignalDialog
from HDLDesigner.InternalSignal.internal_help import IntHelpDialog
from PySide2.QtCore import QObject, Signal
BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "../../Resources/icons/"

class InternalSignal(QWidget):
    save_signal = Signal(bool)
    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setPointSize(10)
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)

        self.all_intSignals = []
        self.all_signals_names = []
        self.stateTypes_names = []

        self.port_heading_layout = QHBoxLayout()
        self.intSig_action_layout = QVBoxLayout()
        self.intSig_list_layout = QVBoxLayout()
        self.instSig_list_title_layout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.io_list_label = QLabel("Internal Signals")
        self.io_list_label.setFont(title_font)
        self.io_list_label.setStyleSheet(WHITE_COLOR)

        self.add_btn = QPushButton("Add Signal")
        self.add_btn.setFont(input_font)
        #self.add_btn.setFixedSize(80, 25)
        self.add_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.int_info_btn = QPushButton()
        self.int_info_btn.setIcon(qta.icon("mdi.help"))
        self.int_info_btn.setFixedSize(25, 25)
        self.int_info_btn.clicked.connect(self.internal_help_window)

        # Port list layout widgets
        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.size_label = QLabel("Size")
        self.size_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.intSig_table = QTableWidget()


        self.intSig_list_frame = QFrame()
        self.intSig_action_frame = QFrame()


        self.setup_ui()

        if proj_dir != None:
            self.load_data(proj_dir)

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)
        # Port List section
        self.port_heading_layout.addWidget(self.io_list_label, alignment=Qt.AlignLeft)
        self.port_heading_layout.addWidget(self.add_btn, alignment=Qt.AlignRight)
        self.port_heading_layout.addWidget(self.int_info_btn, alignment=Qt.AlignRight)
        self.add_btn.clicked.connect(self.add_intSignal)

        self.instSig_list_title_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.size_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addSpacerItem(QSpacerItem(40, 1))
        self.instSig_list_title_layout.addSpacerItem(QSpacerItem(40, 1))

        self.intSig_list_layout.setAlignment(Qt.AlignTop)

        self.intSig_table.setColumnCount(5)
        self.intSig_table.setShowGrid(False)
        self.intSig_table.setHorizontalHeaderLabels(['Name',' Type', 'Size', '', ''])
        header = self.intSig_table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)
        self.intSig_table.horizontalHeader().setFont(bold_font)
        self.intSig_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.intSig_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.intSig_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.intSig_table.setColumnWidth(3, 1)
        self.intSig_table.setColumnWidth(4, 1)
        self.intSig_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vert = self.intSig_table.verticalHeader()
        vert.hide()
        self.intSig_table.setFrameStyle(QFrame.NoFrame)
        self.intSig_list_layout.addWidget(self.intSig_table)


        self.intSig_list_frame.setFrameShape(QFrame.StyledPanel)
        self.intSig_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.intSig_list_frame.setLayout(self.intSig_list_layout)

        self.intSig_action_layout.addLayout(self.port_heading_layout)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.intSig_action_layout.addWidget(self.intSig_list_frame)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))

        self.intSig_action_frame.setFrameShape(QFrame.StyledPanel)
        self.intSig_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.intSig_action_frame.setLayout(self.intSig_action_layout)


        self.mainLayout.addWidget(self.intSig_action_frame)

        self.setLayout(self.mainLayout)

    def add_intSignal(self):
        add_intSig = IntSignalDialog("add", self.all_signals_names)
        add_intSig.exec_()

        if not add_intSig.cancelled:
            intSignal_data = add_intSig.get_data()
            CSIntSignal_data = add_intSig.get_data()
            CSIntSignal_data[0] = "CS" + CSIntSignal_data[0]
            self.all_signals_names.append((intSignal_data[0]))

            if intSignal_data[1] == "bus state signal pair(NS/CS)" or intSignal_data[1] == "Enumerated type state signal pair(NS/CS)" or intSignal_data[1] == "integer state signal pair(NS/CS)":
                i = 2
            else:
                i = 1
            while i > 0:
                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_intSignal)

                row_position = self.intSig_table.rowCount()
                self.intSig_table.insertRow(row_position)
                self.intSig_table.setRowHeight(row_position, 5)

                self.intSig_table.setItem(row_position, 1, QTableWidgetItem(intSignal_data[1]))
                if type(intSignal_data[2]) is list:
                    intSignal_data[2] = str(intSignal_data[2])
                size = QTableWidgetItem(intSignal_data[2])
                size.setTextAlignment(Qt.AlignCenter)
                self.intSig_table.setItem(row_position, 2, size)
                self.intSig_table.setCellWidget(row_position, 3, edit_btn)
                self.intSig_table.setCellWidget(row_position, 4, delete_btn)
                if intSignal_data[1] == "bus state signal pair(NS/CS)" or intSignal_data[1] == "Enumerated type state signal pair(NS/CS)" or intSignal_data[1] == "integer state signal pair(NS/CS)":
                    if (i == 2) :
                        self.intSig_table.removeCellWidget(row_position, 3)
                        self.intSig_table.removeCellWidget(row_position, 4)
                        intSignal_data[0] = "NS" + intSignal_data[0]
                        add_intSig.makeIdeal()
                        if intSignal_data[1] == "Enumerated type state signal pair(NS/CS)":
                            self.stateTypes_names = add_intSig.get_stateTypes()
                        self.all_intSignals.append(intSignal_data)
                        self.all_signals_names.append(intSignal_data[0])
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                    else:
                        self.all_intSignals.append(CSIntSignal_data)
                        self.all_signals_names.append(CSIntSignal_data[0])
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(CSIntSignal_data[0]))
                else:
                    self.all_intSignals.append(intSignal_data)
                    self.all_signals_names.append(intSignal_data[0])
                    self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                i=i-1
            self.save_data()
    def edit_intSignal(self):
        button = self.sender()
        if button:
            row = self.intSig_table.indexAt(button.pos()).row()
            rowBefore = row - 1
            add_intSig = IntSignalDialog("edit", self.all_signals_names, self.all_intSignals[row])
            add_intSig.exec_()
        if not add_intSig.cancelled:
            intSignal_data = add_intSig.get_data()
            CSIntSignal_data = add_intSig.get_data()
            self.intSig_table.removeRow(row)
            self.all_intSignals.pop(row)
            self.all_signals_names.pop(row)
            CSIntSignal_data[0] = "CS" + CSIntSignal_data[0]

            if intSignal_data[1] == "bus state signal pair(NS/CS)" or intSignal_data[1] == "Enumerated type state signal pair(NS/CS)" or intSignal_data[1] == "integer state signal pair(NS/CS)":
                i = 2
                self.intSig_table.removeRow(rowBefore)
                self.all_intSignals.pop(rowBefore)

            else:
                i = 1
            while i > 0:
                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_intSignal)

                row_position = self.intSig_table.rowCount()
                self.intSig_table.insertRow(row_position)
                self.intSig_table.setRowHeight(row_position, 5)
                if intSignal_data[1][0:6] == "array,":
                    self.intSig_table.setItem(row_position, 1, QTableWidgetItem("array"))
                else:
                    self.intSig_table.setItem(row_position, 1, QTableWidgetItem(intSignal_data[1]))
                if type(intSignal_data[2]) is list:
                    intSignal_data[2] = str(intSignal_data[2])
                size = QTableWidgetItem(intSignal_data[2])
                size.setTextAlignment(Qt.AlignCenter)
                self.intSig_table.setItem(row_position, 2, size)
                self.intSig_table.setCellWidget(row_position, 3, edit_btn)
                self.intSig_table.setCellWidget(row_position, 4, delete_btn)
                if intSignal_data[1] == "bus state signal pair(NS/CS)" or intSignal_data[1] == "Enumerated type state signal pair(NS/CS)" or intSignal_data[1] == "integer state signal pair(NS/CS)":
                    if (i == 2) :
                        self.intSig_table.removeCellWidget(row_position, 3)
                        self.intSig_table.removeCellWidget(row_position, 4)
                        intSignal_data[0] = "NS" + intSignal_data[0]
                        add_intSig.makeIdeal()
                        if intSignal_data[1] == "Enumerated type state signal pair(NS/CS)":
                            self.stateTypes_names = add_intSig.get_stateTypes()
                        self.all_intSignals.append(intSignal_data)
                        self.all_signals_names.append(intSignal_data[0])
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                    else:
                        self.all_intSignals.append(CSIntSignal_data)
                        self.all_signals_names.append(CSIntSignal_data[0])
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(CSIntSignal_data[0]))
                else:
                    self.all_intSignals.append(intSignal_data)
                    self.all_signals_names.append(intSignal_data[0])
                    self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                i=i-1
            self.save_data()
        else:
            self.all_intSignals[row][3]=self.all_intSignals[row][3].replace("\n", "&#10;")




    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.intSig_table.indexAt(button.pos()).row()

            rowBefore = row -1
            if str(self.all_intSignals[row][1]) == "Enumerated type state signal pair(NS/CS)":
                self.stateTypes_names = []
            if str(self.all_intSignals[row][1]) == "Enumerated type state signal pair(NS/CS)" or str(self.all_intSignals[row][1]) == "bus state signal pair(NS/CS)" or str(self.all_intSignals[row][1]) == "integer state signal pair(NS/CS)":
                self.intSig_table.removeRow(row)
                self.all_intSignals.pop(row)
                self.all_intSignals.pop(rowBefore)
                self.intSig_table.removeRow(rowBefore)
                self.all_signals_names.pop(row)
                self.all_signals_names.pop(rowBefore)

            else:
                self.intSig_table.removeRow(row)
                self.all_intSignals.pop(row)
                self.all_signals_names.pop(row)
            self.save_data()




    def save_data(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        new_intSigs = root.createElement('internalSignals')

        for signal in self.all_intSignals:
            signal_node = root.createElement('signal')

            name_node = root.createElement('name')
            name_node.appendChild(root.createTextNode(signal[0]))
            signal_node.appendChild(name_node)
            type_node = root.createElement('type')
            if signal[1] == "single bit":
                sig_type = "single bit"
            elif signal[1] == "Enumerated type state signal pair(NS/CS)":
                sig_type = "Enumerated type state signal pair(NS/CS)"
            elif signal[1] == "integer" or signal[1] == "integer state signal pair(NS/CS)":
                sig_type = "integer range 0 to " + str(int(signal[2]) - 1)
            elif signal[1] == "signed" or signal[1] == "unsigned" or signal[1][:3] == "bus":
                sig_size = ("(" + str(int(signal[2]) - 1) + " downto 0)")
                if signal[1] == "signed":
                    sig_type = "signed" + sig_size
                elif signal[1] == "unsigned":
                    sig_type = "unsigned" + sig_size
                else:
                    sig_type = "bus" + sig_size
            else:
                sig_type = signal[1]
            type_node.appendChild(root.createTextNode(sig_type))
            signal_node.appendChild(type_node)

            desc_node = root.createElement('description')
            desc_node.appendChild(root.createTextNode(signal[3]))
            signal_node.appendChild(desc_node)

            new_intSigs.appendChild(signal_node)

        for states in self.stateTypes_names:
            stateTypes_nodes = root.createElement('stateTypes')
            stateTypes_nodes.appendChild(root.createTextNode(states))
            new_intSigs.appendChild(stateTypes_nodes)
        hdlDesign[0].replaceChild(new_intSigs, hdlDesign[0].getElementsByTagName('internalSignals')[0])

        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = '\n'.join([line for line in xml_str.splitlines() if line.strip()])
        # Writing xml file
        with open(xml_data_path, "w", encoding='UTF-8', newline='\n') as f:
            f.write(xml_str)
        hdl = False
        self.save_signal.emit(hdl)
        print("Saved internal signal(s)")

    def internal_help_window(self):
        internal_help_dialog = IntHelpDialog()
        internal_help_dialog.exec_()

    def load_data(self, proj_dir):

        root = minidom.parse(str(proj_dir))
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        io_ports = hdlDesign[0].getElementsByTagName('internalSignals')
        signal_nodes = io_ports[0].getElementsByTagName('signal')

        for i in range(0, len(signal_nodes)):
            self.intSig_table.insertRow(i)
            self.intSig_table.setRowHeight(i, 5)
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_intSignal)

            self.intSig_table.setCellWidget(i, 3, edit_btn)
            self.intSig_table.setCellWidget(i, 4, delete_btn)
            name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
            self.all_signals_names.append(name)
            signal = signal_nodes[i].getElementsByTagName('type')[0].firstChild.data
            value = ""
            if signal == "single bit":
                type = signal
                value = "1"
            elif signal[:7] == "integer":
                signal = signal.split(" ")
                type = signal[0]
                value = str(int(signal[4]) + 1)
            elif signal == "Enumerated type state signal pair(NS/CS)":
                type = signal
                stateTypesList = []
                for stateType in io_ports[0].getElementsByTagName("stateTypes"):
                    stateTypesList.append(stateType.firstChild.data)
                self.stateTypes_names = stateTypesList
                value = ' '.join(stateTypesList)
                if name[:2] == "NS":
                    self.intSig_table.removeCellWidget(i, 3)
                    self.intSig_table.removeCellWidget(i, 4)
            elif signal.endswith(")"):
                type = signal[0:signal.index("(")]
                if type == "bus" or type == "signed" or type == "unsigned":
                    value = str(int(signal[signal.index("(") + 1:signal.index(" downto")]) + 1)
            elif signal[0:6] == "array,":
                value = ""
                type = signal
            else:
                signal=signal.split(" ")
                type = str(signal[0])
                value = ""
            desc = signal_nodes[i].getElementsByTagName('description')[0].firstChild.data

            loaded_sig_data = [
                name,
                type,
                value,
                desc
            ]

            self.all_intSignals.append(loaded_sig_data)
            self.intSig_table.setItem(i, 0, QTableWidgetItem(loaded_sig_data[0]))
            if loaded_sig_data[1][0:6] == "array,":
                self.intSig_table.setItem(i, 1, QTableWidgetItem("array"))
            else:
                self.intSig_table.setItem(i, 1, QTableWidgetItem(loaded_sig_data[1]))
            size = QTableWidgetItem(str(loaded_sig_data[2]))
            size.setTextAlignment(Qt.AlignCenter)
            self.intSig_table.setItem(i, 2, size)

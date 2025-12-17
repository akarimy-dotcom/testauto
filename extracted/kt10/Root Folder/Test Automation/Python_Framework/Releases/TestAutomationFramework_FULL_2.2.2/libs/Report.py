"""
This class manage the writings of report in given file

Changelog:

[2.0.0] - 2025-03-06
- Modified default name of report from "Report_xxx" to "xxx"
- Added method set_report_name to allows to change report name

[1.7.0] - 2024-03-15
- Update only for tag

[1.6.0] - 2024-01-23

- Modify name of report from "Report_Cxxx" to "Report_xxx"

[1.5.0] - 2023-11-15
- Update only for tag

1.0 2022-01-31
"""
__version__ = '2.2.2'
__author__ = 'Intelligentia SRL & Juan Pablo Perruzza, Ruggeri Nicolò'

import datetime
import os
import string
import sys
import openpyxl
from openpyxl.styles import Alignment, PatternFill, Font


class Report:
    options = {
        "path":   None,
        "device": None
    }
    # devices container
    _devices = []
    # report container for txt file
    _reports = []
    # rows container for xlsx file
    _rows = []
    # report name
    _reports_file_name = None


    def __init__(self, settings):
        # update options with customs
        self.options.update(settings)
        file_name = os.path.basename(sys.argv[0])
        self._reports_path = f"{self.options['path']}"
        self._reports_file_name = f"{os.path.splitext(file_name)[0]}"


    def __del__(self):
        pass


    def add_device(self, device):
        """
        Add device
        :param string device
        """
        self._devices.append(device)


    def add_comment(self, comment, print_on_console=True):
        """
        Add comment and print on screen
        :param string comment
        :param bool printOnConsole
        """
        self._reports.append(f"{comment}")
        if print_on_console:
            print(comment)


    def create_report(self, testResult):
        """
        Create report
        :param string testResult
        """
        file_name = os.path.basename(sys.argv[0])
        # Create Report
        if not os.path.exists(self.options['path']):
            os.makedirs(self.options['path'])

        # in this way, a file is created (or open and written as "append") with the name of the Script and the
        # extensione ".txt"
        file = open(f"{self._reports_path}{self._reports_file_name}.txt", "a")
        # Save information

        file.write(
                f"-------------------- Report of Script C{os.path.basename(sys.argv[0])} -------------------------\n\n")
        file.write(f"Date and time: {self.get_formatted_date()}")

        file.write("\n\nDevices")
        for device in self._devices:
            file.write(f"\n{device}")
        file.write("\n")

        for i in range(len(self._reports)):
            file.write(f"\n{self._reports[i]}")

        file.write(f"\n\nResult of Test: {testResult} \n\n")

        # Close file
        file.close()


    @staticmethod
    def print_on_console(text):
        """
        Print text on console
        :param string text
        """
        print(text)


    @staticmethod
    def get_formatted_date():
        """
        Get formatted datetime
        """
        return str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))


    def add_action_row(self, device="", action="", dgto="", value="", expected_value="", result="SUCCESS", note=""):
        """
        Add row for action
        :param device: string
        :param ['READ', 'WRITE', 'PING', 'CHANGE'] action
        :param dgto: string
        :param value: string
        :param expected_value: string
        :param result: ['SUCCESS', 'ERROR', 'WARNING'] [result]
        :param note: string
        """
        if isinstance(expected_value, range):
            expected_value = ', '.join([str(x) for x in expected_value])

        # split device name in order to get only name, not the version
        self._rows.append(
                (self.get_formatted_date(), device.split(" ")[0], action, dgto, value, expected_value, result, note))


    def add_comment_row(self, comment, background_color="TRANSPARENT", print_on_console=False):
        """
        Add row for comment
        :param string comment
        """
        self._rows.append((self.get_formatted_date(), comment, background_color))
        if print_on_console:
            print(comment)


    def set_report_name(self, report_name: str):
        """
        :param report_name: the new name to use when update_report is called without file extension

        :Return values : None
        :Description   : this function allows to change the name of the report
        :Remarks: none
        """
        self._reports_file_name = report_name


    """ --- Start: openpyxl --- """


    def update_report(self, test_passed, test_result_info: int = None):
        """
        :param test_passed:	If set to False and test_result_info is none or "Failed" the last row in the generated
        report will be TEST FAILED, if set to true the report will be generated with last row as "TEST PASSED"

        :param test_result_info: Additional info for FAILED test (explains why the test is failed):

        0 = STANDARD FAIL (text on report: "TEST FAILED", associated to a fail in the final check on Test Result)
        1 = PRECONDITION FAIL (text on report: "TEST FAILED PRECONDITION")
        2 = STEP FAIL (text on report: "TEST FAILED STEP")
        3 = BLOCKED (text on report: "TEST BLOCKED")
        4 = TO BE COMPLETED (text on report: "TEST TO BE COMPLETED",
        associated to a script who fail but has already tested some case)

        :Return values : None
        :Description   : This function will add a new tab in the report file with the test result passed
        if the report.xlsx already exist, otherwise will add a new .xlsx file
        :Remarks: none
        """

        if test_result_info is not None and (test_result_info < 0 or test_result_info > 4):
            test_result_info = None

        file_name = os.path.basename(sys.argv[0])
        # set file name
        file_name = f"{self._reports_path}{self._reports_file_name}.xlsx"
        # set sheet name
        sheet_name = str(datetime.datetime.now()).replace(":", "-").split(".")[0]
        # check file exists
        if os.path.isfile(file_name):
            wb = openpyxl.load_workbook(file_name)
            sheet = wb.create_sheet(sheet_name, 0)
        else:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.title = sheet_name

        # add header
        sheet.append(("DATETIME", "DEVICE", "ACTION", "DATA", "VALUE", "WRITTEN/EXPECTED VALUE", "RESULT", "NOTE"))

        # append test result to the end
        if test_result_info is None or test_passed:
            test_result = "TEST PASSED" if test_passed else "TEST FAILED"
        else:
            if test_result_info == 0:
                test_result = "TEST FAILED"
            elif test_result_info == 1:
                test_result = "TEST FAILED PRECONDITION"
            elif test_result_info == 2:
                test_result = "TEST FAILED STEP"
            elif test_result_info == 3:
                test_result = "TEST BLOCKED"
            elif test_result_info == 4:
                test_result = "TO BE COMPLETED"
        self.add_comment_row(test_result.upper())

        for i in range(len(self._rows)):
            row = self._rows[i]
            # cell background color
            if len(row) == 3:
                result = row[2]
            elif len(row) == 8:
                result = row[6]

            if result == "SUCCESS":
                color = "70AD47"
            elif result == "ERROR":
                color = "C00000"
            elif result == "WARNING":
                color = "FFC000"
            elif result == "INFO":
                color = "4397B1"
            else:
                color = None

            # row for action
            if len(row) > 3:
                sheet.append(row)
                sheet['G' + str(sheet.max_row)].fill = PatternFill(
                        start_color=color, end_color=color, fill_type="solid")
                sheet['G' + str(sheet.max_row)].font = Font(color="FFFFFF")
            # 	comment row
            else:
                current_row = i + 2
                sheet.append(row)
                # merge cells
                sheet.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=8)
                # background color
                if color is not None:
                    sheet['B' + str(sheet.max_row)].fill = PatternFill(
                            start_color=color, end_color=color, fill_type="solid")
                    sheet['B' + str(sheet.max_row)].font = Font(color="FFFFFF")

        # set test result color
        color = "70AD47" if test_passed else "C00000"
        sheet['B' + str(sheet.max_row)].fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        sheet['B' + str(sheet.max_row)].font = Font(color="FFFFFF")

        cols = list(string.ascii_uppercase)
        # add devices
        col_index_start = sheet.max_column + 2
        sheet[cols[col_index_start] + "1"].value = "TOPOLOGY"
        sheet[cols[col_index_start] + "1"].alignment = Alignment(horizontal='center')
        sheet.merge_cells(start_row=1, start_column=col_index_start + 1, end_row=1, end_column=col_index_start + 2)

        sheet[cols[col_index_start] + "2"].value = "DEVICE"
        sheet[cols[col_index_start] + "2"].font = Font(bold=True)
        sheet[cols[col_index_start + 1] + "2"].value = "VERSION"
        sheet[cols[col_index_start + 1] + "2"].font = Font(bold=True)

        # sheet.append(("DEVICE NAME", "VERSION"))
        # # insert empty row before device
        # sheet.insert_rows(sheet.max_row, amount=1)
        # deviceHeaderRow = sheet.max_row
        #
        for i in range(len(self._devices)):
            name, version = self._devices[i].split(" ")
            sheet[cols[col_index_start] + str(i + 3)].value = name
            sheet[cols[col_index_start + 1] + str(i + 3)].value = version

        # set col's style
        for i in range(sheet.max_column):
            sheet[cols[i] + "1"].font = Font(bold=True)
        # sheet[cols[i] + str(deviceHeaderRow)].font = Font(bold=True)

        # save updates
        wb.save(file_name)


    """ --- End: openpyxl --- """

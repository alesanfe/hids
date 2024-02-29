import os
import glob
import re
from datetime import datetime
from typing import List, Set, Tuple


def process_daily_logs() -> List[str]:
    """
    Retrieve a list of log files for the previous month.

    Returns:
        List[str]: A list of log file paths for the previous month.
    """
    path = "../logs"
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Calculate the month and year of the previous month
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    pattern = os.path.join(path, f"{previous_year:04d}-{previous_month:02d}-*.txt")
    logs_of_the_month = glob.glob(pattern)

    return logs_of_the_month


def get_non_integrated_files(last_log: str) -> List[str]:
    """
    Given the path to the latest log file, extract the names of non-integrated files.

    Args:
        last_log (str): Path to the latest log file.

    Returns:
        List[str]: Names of non-integrated files.
    """
    non_integrated_files = []

    try:
        with open(last_log, 'r', encoding='utf-8') as file:
            for line in file:
                file_match = re.search(r"File ([^\s]+) has been modified", line)
                if file_match:
                    file_name = file_match.group(1)
                    non_integrated_files.append(os.path.basename(file_name))

    except Exception:
        pass

    return non_integrated_files


def get_non_integrated_files_by_day(log_list: List[str]) -> Set[Tuple[str, str]]:
    """
    Process a list of log files and extract information about non-integrated files by day.

    Args:
        log_list (List[str]): List of log files.

    Returns:
        Set[Tuple[str, str]]: A set containing tuples of non-integrated file names and their corresponding dates.
    """
    non_integrated_files = set()

    for log in log_list:
        try:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', log)
            date = match.group(1)
            with open(log, 'r', encoding='utf-8') as file:
                for line in file:
                    file_match = re.search(r"File ([^\s]+) has been modified", line)
                    if file_match:
                        file_name = file_match.group(1)
                        non_integrated_files.add((file_name, date))
        except Exception:
            pass

    return non_integrated_files


def compile_monthly_report_by_day() -> None:
    """
    Compile a monthly report by day, creating a report file in the 'monthly_reports' directory.
    The report includes information about currently non-integrated files, non-integrated files during the month,
    and details about the last daily log.
    """
    log_list = process_daily_logs()
    non_integrated_files_currently = get_non_integrated_files(log_list[-1])
    non_integrated_files = get_non_integrated_files_by_day(log_list)
    sorted_files = sorted(list(non_integrated_files), key=lambda x: x[0])

    if not os.path.exists("../reports"):
        os.makedirs("../reports")

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    # Create the name of the monthly report file
    report_name = f"Report-{previous_year:04d}_{previous_month:02d}.txt"
    report_file_path = os.path.join("../reports/", report_name)

    # Write the monthly report
    with open(report_file_path, 'w', encoding='utf-8') as report_file:
        report_file.write("=" * 50 + "\n")
        report_file.write(f"Monthly Report - {previous_month:02d}/{previous_year:04d}\n")
        report_file.write("=" * 50 + "\n\n")

        report_file.write("Non-Integrated Files Currently:\n")
        for file in non_integrated_files_currently:
            report_file.write(f"\t- {file};\n")
        report_file.write("\n")

        report_file.write("Non-Integrated Files During the Month:\n")
        for element in sorted_files:
            parts_date = element[1].split("-")
            inverted_date = "-".join(reversed(parts_date))
            report_file.write(f"\t- File in path {element[0]} ceased to be integrated on {inverted_date};\n")
        report_file.write("\n")
        report_file.write("=" * 50 + "\n")

        report_file.write("Last Daily Log:\n")
        report_file.write("\t" + log_list[-1].replace("../logs\\", "") + "\n")
        report_file.write("=" * 50 + "\n\n")

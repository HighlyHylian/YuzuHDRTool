import sys
import zipfile
import glob
import requests
import os
import datetime
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QProgressDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from YuzuToolMenu import Ui_MainWindow  # Import the generated UI module
from configparser import ConfigParser


def copy_folder(source_folder, destination_folder):
    try:
        # Use shutil.copytree to copy the entire folder and its contents
        shutil.copytree(source_folder, destination_folder)
        print(
            f"Successfully copied '{source_folder}' to '{destination_folder}'")
        return True
    except Exception as e:
        print(
            f"Error copying '{source_folder}' to '{destination_folder}': {str(e)}")
        return False


def delete_folders(folder_paths):
    for folder_path in folder_paths:
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted {folder_path}")
        except Exception as e:
            print(f"Failed to delete {folder_path}: {str(e)}")


def extract_zip(zip_file_path, target_directory):
    try:
        # Extract the contents of the ZIP file to the target directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_directory)
        print(f"Extracted {zip_file_path} to {target_directory}")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(60)  # Increased vertical size

        self.layout = QHBoxLayout()  # Use a horizontal layout for the title bar
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.title_label = QLabel("YuzuHDRHelper")
        self.title_label.setStyleSheet("font-size: 30px;")
        self.layout.addWidget(self.title_label)

        # Create a square "Cancel" button on the right
        self.cancel_button = QPushButton("Close")
        self.cancel_button.setFixedWidth(60)  # Make it square
        self.cancel_button.clicked.connect(self.window().close)

        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

        # Initialize variables to track mouse events
        self.mouse_pressed = False
        self.old_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            delta = event.globalPos() - self.old_pos
            self.window().move(self.window().pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False

class MyMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Set up the user interface from the generated UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.draggable = True



        # Create a custom title bar and set it as the window's menu bar.
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        # Create a central widget for your content
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a widget for your buttons and add them to a layout
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.addWidget(self.ui.FolderButton)
        button_layout.addWidget(self.ui.HDRVersion)
        button_layout.addWidget(self.ui.line)
        button_layout.addWidget(self.ui.NightlyButton)
        button_layout.addWidget(self.ui.BetaButton)
        button_layout.addWidget(self.ui.Legacy)
        button_layout.addWidget(self.ui.line_2)
        button_layout.addWidget(self.ui.Legacy_2)
        button_layout.addWidget(self.ui.WifiFixButton)
        button_layout.addWidget(self.ui.UninstallWifiButton)
        button_layout.addWidget(self.ui.line_3)
        button_layout.addWidget(self.ui.NightlyPatch)
        button_layout.addWidget(self.ui.BetaPatch)

        # Set the widget's layout
        button_widget.setLayout(button_layout)

        # Add the button widget to the central layout
        layout.addWidget(button_widget)



        # Connect buttons to empty functions (no functionality yet)
        self.ui.NightlyButton.clicked.connect(self.NightlyDownload)
        self.ui.BetaButton.clicked.connect(self.BetaDownload)
        self.ui.WifiFixButton.clicked.connect(self.InstallOnlineFix)
        self.ui.UninstallWifiButton.clicked.connect(self.UninstallOnlineFix)
        self.ui.FolderButton.clicked.connect(self.set_folder)
        self.ui.NightlyPatch.clicked.connect(self.NightlyPatch)
        self.ui.BetaPatch.clicked.connect(self.BetaPatch)
        self.ui.Legacy.clicked.connect(self.legacyDL)
        self.ui.Legacy_2.clicked.connect(self.installLegacy)


        config = ConfigParser()
        config['cfg'] = {
            'directory_path': '',
            'isDark' : True
        }

        config.read('config.ini')

        # Retrieve and set the configured values
        directory_path = config.get('cfg', 'directory_path')
        directory_path = directory_path.replace('\'', '')
        self.selected_directory = directory_path

        self.isDark = config.getboolean('cfg', 'isDark')
        self.setTheme(self.isDark)

        # Display to terminal the path read from config
        print(f"Directory path read from file: {directory_path}")

        # Initialize the version label to the right value
        if os.path.exists(os.path.join(self.selected_directory, 'ultimate', 'mods', 'hdr', 'ui', 'hdr_version.txt')):
            file = open(os.path.join(self.selected_directory,
                        'ultimate', 'mods', 'hdr', 'ui', 'hdr_version.txt'))
            self.ui.HDRVersion.setText('Current HDR Version: ' + file.read())
        else:
            print('Directory Not Set')
            self.origin = None

    # Define empty functions for the buttons (add functionality later)
    def empty_function(self):
        self.show_error_message("Coming Soon(tm)")

    # Checks if the path given is a valid SDMC path and that it exists. Returns true if so
    def isValidPath(self):
        if self.selected_directory and self.selected_directory.endswith("/yuzu/sdmc"):
            return True
        return False

    # Display an error message with the given message argument
    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

    # Downloads the legacy_discovery file.
    def legacyDL(self):
        url = "https://cdn.discordapp.com/attachments/410208534861447170/1139219391611949096/legacy_discovery"
        file_name = "legacy_discovery"
        download_dir = os.getcwd()
        try:
            # Send a GET request to the URL to fetch the file
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Specify the local file path where you want to save the downloaded file
                local_file_path = os.path.join(download_dir, file_name)

                with open(local_file_path, 'wb') as file:
                    file.write(response.content)

                print(f"Downloaded {file_name} to {local_file_path}")
                self.display_message_and_continue(
                    'Downloaded legacy_discovery')
            else:
                print(
                    f"Failed to download {file_name}. Status code: {response.status_code}")
        except Exception as e:
            self.show_error_message(f"An error occurred: {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

    # Displays the message argument and continue after
    def display_message_and_continue(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Message")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Show the QMessageBox and wait for user interaction
        result = msg_box.exec_()

        # Check if the "Continue" (Ok) button was clicked
        if result == QMessageBox.Ok:
            return

    # Prompts user for a question and returns their yes or no answer
    def ask_question(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle("Question")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = msg_box.exec_()

        # Return True if the user clicked Yes, otherwise False
        return result == QMessageBox.Yes

    # Folder prompt function
    def set_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Make the dialog read-only
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", options=options)

        if directory:
            # Check if the selected directory ends with "\yuzu\sdmc\ultimate\mods"
            if not directory.endswith("/yuzu/sdmc"):
                self.show_error_message(
                    "Selected directory must end with '/yuzu/sdmc'")
                return

            # Set the selected directory to the variable
            self.selected_directory = directory
            print("Directory: ", self.selected_directory)
            

            try:
                # Update config files
                config = ConfigParser()
                config.read("config.ini")
                config.set('Paths', 'directory_path', self.selected_directory)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

            except Exception as e:
                self.show_error_message(f"An error occurred: {str(e)}")
            except:
                self.show_error_message("An unknown error occurred")

            # Check if some version of HDR is installed
            if not os.path.exists(os.path.join(self.selected_directory, 'ultimate', 'mods', 'hdr', 'ui', 'hdr_version.txt')):
                self.ui.HDRVersion.setText(
                    'Current HDR Version: NOT INSTALLED')
                print('Version not found')
            else:
                file = open(os.path.join(self.selected_directory,
                            'ultimate', 'mods', 'hdr', 'ui', 'hdr_version.txt'))
                self.ui.HDRVersion.setText(
                    'Current HDR Version: ' + file.read())

    # Downloads the specified file from the url, names it the file_name, and saves it to download_dir 
    def download_file(self, url, file_name, download_dir):
        try:
            # Send a GET request to the GitHub API to fetch the latest release information
            # Use stream=True for streaming the file download
            response = requests.get(url, stream=True)

            # Check if the request was successful
            if response.status_code == 200:
                release_info = response.json()
                asset_url = None
                bytes_downloaded = 0

                # Iterate through the assets to find the file you want to download
                for asset in release_info['assets']:
                    if asset['name'] == file_name:
                        asset_url = asset['browser_download_url']
                        break

                if asset_url:
                    # Download the file
                    response = requests.get(asset_url, stream=True)

                    # Check if the download was successful
                    if response.status_code == 200:
                        # Specify the local file path where you want to save the downloaded file
                        local_file_path = os.path.join(download_dir, file_name)

                        with open(local_file_path, 'wb') as file:
                            for data in response.iter_content(chunk_size=1024):
                                file.write(data)
                                bytes_downloaded += len(data)
                                # Calculate the download progress
                                if response.headers.get('content-length'):
                                    total_size = int(
                                        response.headers['content-length'])
                                    progress = int(
                                        bytes_downloaded / total_size * 100)
                                    self.progress_dialog.setValue(progress)
                                else:
                                    # If content-length is not available, use a dynamic approach
                                    self.progress_dialog.setValue(
                                        100 * bytes_downloaded // (1024 * 1024))  # MB progress

                        print(f"Downloaded {file_name} to {local_file_path}")
                    else:
                        print(f"Failed to download {file_name}")
                else:
                    print(
                        f"File {file_name} not found in the latest release assets")
            else:
                print("Failed to fetch latest release information")
        except Exception as e:
            self.show_error_message(f"An error occurred: {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

    # Handle cancellation of the download (NOT IMPLEMENTED PROPERLY)
    def handle_cancel(self):
        # Handle the cancellation action here
        # You can add code to stop the download or perform cleanup
        if self.progress_dialog.wasCanceled():
            self.show_error_message("Download canceled")
            # Implement code here to stop the download if it's in progress
            # You can also delete any temporary files
            self.progress_dialog.reset()  # Reset the progress dialog
            # Add code to delete temporary files or any cleanup actions

    # Create the progress bar popup
    def show_progress_popup(self, title, label):
        self.progress_dialog = QProgressDialog(title, "", 0, 100, self)
        self.progress_dialog.setWindowModality(2)
        self.progress_dialog.setLabelText(label)

        # Set the cancel button text to an empty string
        self.progress_dialog.setCancelButtonText("Cancel")

        # Increase the size of the progress bar by setting the dialog size
        self.progress_dialog.resize(800, 200)  # Adjust the size as needed

        self.progress_dialog.setValue(0)

    # Download the latest nightly to parent directory
    def NightlyDownload(self):

        # github api call
        nightly_url = f'https://api.github.com/repos/HDR-Development/HDR-Nightlies/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'nightly'

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_progress_popup("Nightly Download", "Downloading...")

        self.download_file(nightly_url, file_name, download_dir)

        self.progress_dialog.close()

        self.display_message_and_continue('Finished downloading nightly')

    # Download the latest beta to parent directory
    def BetaDownload(self):

        # gihub api call
        beta_url = f'https://api.github.com/repos/HDR-Development/HDR-Releases/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'beta'

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_progress_popup("Beta Download", "Downloading...")
        self.download_file(beta_url, file_name, download_dir)

        self.progress_dialog.close()

        self.display_message_and_continue('Finished downloading beta')

    # Patches in the nightly
    def NightlyPatch(self):
        # Check if the current path is valid
        if not self.isValidPath():
            self.show_error_message("Please select the yuzu/sdmc folder first")
            return

        # Check if nightly is downloaded
        if not os.path.exists(os.path.join(os.getcwd(), "nightly", "ryujinx-package.zip")):
            self.show_error_message("Please download the nightly first")
            return

        # Is it ok to delete everything?
        if self.ask_question("This process will delete everything in your atmosphere and ultimate folders.\nA backup of your mod folder will be made\nProceed?"):

            # Patching process
            try:
                if (self.backup_folder(os.path.join(self.selected_directory, "ultimate"))):
                    if extract_zip(os.path.join(os.getcwd(), "nightly/ryujinx-package.zip"), self.selected_directory):
                        folders = [
                            os.path.join(
                                self.selected_directory, "atmosphere"),
                            os.path.join(self.selected_directory, "ultimate"),
                            os.path.join(os.getcwd(), "normal_exefs")
                        ]
                        delete_folders(folders)

                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000"), os.path.join(
                            self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents",
                                    "01006A800016E000", "exefs"), os.path.join(os.getcwd(), "normal_exefs", "exefs"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "ultimate"), os.path.join(
                            self.selected_directory, "ultimate"))

                        folders = [
                            os.path.join(
                                self.selected_directory, "atmosphere", "contents", "0100000000000013"),
                            os.path.join(self.selected_directory, "sdcard")
                        ]
                        delete_folders(folders)
                        self.display_message_and_continue(
                            "Boot up the game. Wait for the intro scene to start.\nThen close the game and press the \'Install Legacy Discovery\' button.")
                        self.display_message_and_continue(
                            'Finished patching nightly in')
                    else:
                        self.show_error_message(
                            "The ryujinx-package.zip file is missing. Download it first")
            except Exception as e:
                self.show_error_message(f"Error:  {str(e)}")
            except:
                self.show_error_message("An unknown error occurred")

    # Patches in the beta
    def BetaPatch(self):
        # Check if the current path is valid
        if not self.isValidPath():
            self.show_error_message("Please select the yuzu/sdmc folder first")
            return

        # Check if beta is downloaded
        if not os.path.exists(os.path.join(os.getcwd(), "beta", "ryujinx-package.zip")):
            self.show_error_message("Please download the beta first")
            return

        # Is it ok to delete everything?
        if self.ask_question("This process will delete everything in your atmosphere and ultimate folders.\nA backup of your mod folder will be made\nProceed?"):

            # Patching process
            try:
                if (self.backup_folder(os.path.join(self.selected_directory, "ultimate"))):
                    if extract_zip(os.path.join(os.getcwd(), "beta/ryujinx-package.zip"), self.selected_directory):
                        folders = [
                            os.path.join(
                                self.selected_directory, "atmosphere"),
                            os.path.join(self.selected_directory, "ultimate"),
                            os.path.join(os.getcwd(), "normal_exefs")
                        ]
                        delete_folders(folders)

                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000"), os.path.join(
                            self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents",
                                    "01006A800016E000", "exefs"), os.path.join(os.getcwd(), "normal_exefs", "exefs"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "ultimate"), os.path.join(
                            self.selected_directory, "ultimate"))

                        folders = [
                            os.path.join(
                                self.selected_directory, "atmosphere", "contents", "0100000000000013"),
                            os.path.join(self.selected_directory, "sdcard")
                        ]
                        delete_folders(folders)
                        self.display_message_and_continue(
                            "Boot up the game. Wait for the intro scene to start.\nThen close the game and press the \'Install Legacy Discovery\' button.")
                        self.display_message_and_continue(
                            'Finished patching beta in')
                    else:
                        self.show_error_message(
                            "The ryujinx-package.zip file is missing. Download it first")
            except Exception as e:
                self.show_error_message(f"Error:  {str(e)}")
            except:
                self.show_error_message("An unknown error occurred")

    # Installs the online fix (I DON'T KNOW IF THIS EVEN WORKS ANYMORE)
    def InstallOnlineFix(self):
        if not self.isValidPath():
            self.show_error_message(
                "Please select your yuzu/sdmc/ folder first")
            return

        if not os.path.exists(os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")):
            self.show_error_message("Please install hdr first")
            return  # HERE

        try:
            folders = [
                os.path.join(self.selected_directory, "atmosphere",
                             "contents", "01006A800016E000")
            ]
            delete_folders(folders)
            copy_folder(os.path.join(os.getcwd(), "fixed_exefs"), os.path.join(
                self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
        except Exception as e:
            self.show_error_message(f"Error:  {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

        self.display_message_and_continue('Finished installing online fix')

    # Uninstalls the online fix
    def UninstallOnlineFix(self):
        if not self.isValidPath():
            self.show_error_message(
                "Please select your yuzu/sdmc/ folder first")
            return

        if not os.path.exists(os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")):
            self.show_error_message("Please install hdr first")
            return  # HERE

        if not os.path.exists(os.path.join(os.getcwd(), "normal_exefs")):
            self.show_error_message(
                "Error: Normal exefs not stored. Run the nightly or beta patcher first.")
            return  # HERE

        try:
            folders = [
                os.path.join(self.selected_directory, "atmosphere",
                             "contents", "01006A800016E000")
            ]
            delete_folders(folders)
            copy_folder(os.path.join(os.getcwd(), "normal_exefs"), os.path.join(
                self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
        except Exception as e:
            self.show_error_message(f"Error:  {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

        self.display_message_and_continue(
            'Finished uninstalling the online fix')

    # Installs legacy discovery to all files matching the criteria
    def installLegacy(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'legacy_discovery')):
            self.show_error_message(
                "Please click the \'Download Legacy Discovery\' button first.")
            return

        if not self.isValidPath():
            self.show_error_message(
                "Please select your yuzu/sdmc/ folder first")
            return

        # Set the source file to legacy discovery's path
        source_file = os.path.join(os.getcwd(), 'legacy_discovery')

        # Get the regex directory path
        target_directory_pattern = os.path.join(
            self.selected_directory, 'ultimate', 'arcropolis', 'config', '*', '*')

        # Get all directories matching the regex path
        matching_directories = glob.glob(target_directory_pattern)

        # Iterate over the matching directories and copy the file to each of them
        for directory in matching_directories:

            # Construct the full path for the target directory
            target_directory = os.path.join(directory, 'legacy_discovery')

            # Copy the source file to the target directory
            shutil.copy(source_file, target_directory)

        self.display_message_and_continue(
            "Finished installing \'legacy_discovery\'")

    # Makes a backup of the specified folder with a date and time stamp
    def backup_folder(self, source_path):
        if source_path:
            try:
                # Get the current date and time to create the backup folder name
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_folder_name = f"backup-{current_datetime}"

                # Determine the directory where the Python script is located
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Create the full path for the backup folder
                backup_folder = os.path.join(
                    script_directory, backup_folder_name)

                # Copy the contents of the source path to the backup folder
                shutil.copytree(source_path, backup_folder)

                print(
                    f"Backup completed. Contents of '{source_path}' copied to '{backup_folder}'.")
                return True
            except Exception as e:
                self.show_error_message(f"Backup failed: {str(e)}")
                return True
        else:
            return False

    # Sets the theme based on a bool passed in
    def setTheme(self, isDark):
        if isDark:  

            # Dark window style creation and set
            dark_window_style = """
QMainWindow {
    background-color: rgb(20,20,20); 
    border: 4px green;
}
"""
            self.setStyleSheet(dark_window_style)

            # Dark version style set
            self.ui.HDRVersion.setStyleSheet("color: white")

            # Dark button style creation and set
            dark_button_style = """
QPushButton {
    background-color: rgb(80, 165, 120);
    border: 2px solid rgb(80, 165, 120);
    border-radius: 10px;
    padding: 5px 10px;
    color: white
}

QPushButton:hover {
    background-color: rgb(100, 185, 140);
}

QPushButton:pressed {
    background-color: rgb(20, 145, 100);
    border: 2px solid rgb(20, 145, 100);
}
"""

            self.ui.NightlyButton.setStyleSheet(dark_button_style)
            self.ui.BetaButton.setStyleSheet(dark_button_style)
            self.ui.WifiFixButton.setStyleSheet(dark_button_style)
            self.ui.UninstallWifiButton.setStyleSheet(dark_button_style)
            self.ui.FolderButton.setStyleSheet(dark_button_style)
            self.ui.NightlyPatch.setStyleSheet(dark_button_style)
            self.ui.BetaPatch.setStyleSheet(dark_button_style)
            self.ui.Legacy.setStyleSheet(dark_button_style)
            self.ui.Legacy_2.setStyleSheet(dark_button_style)

            # Dark cancel button set
            self.title_bar.cancel_button.setStyleSheet("background-color: rgb(160, 50, 63); color: white;")

            # Light title bar set
            self.title_bar.setStyleSheet("background-color: rgb(100, 185, 140); color: White; text-align: center;")  # Mint green color and center text

        else:  
            # Set main bg colour to white
            self.setStyleSheet("background-color: rgb(255, 255, 255)")

            # Light window style creation and set
            light_window_style = """
QMainWindow {
    background-color: white; 
    border: 4px green;
}
"""
            self.setStyleSheet(light_window_style)

            # Light button style creation and set
            light_button_style = """
QPushButton {
    background-color: rgb(170, 255, 210);
    border: 2px solid rgb(170, 255, 210);
    border-radius: 10px;
    padding: 5px 10px;
}

QPushButton:hover {
    background-color: rgb(180, 255, 220);
}

QPushButton:pressed {
    background-color: rgb(140, 215, 170);
    border: 2px solid rgb(140, 215, 170);
}
"""

            self.ui.NightlyButton.setStyleSheet(light_button_style)
            self.ui.BetaButton.setStyleSheet(light_button_style)
            self.ui.WifiFixButton.setStyleSheet(light_button_style)
            self.ui.UninstallWifiButton.setStyleSheet(light_button_style)
            self.ui.FolderButton.setStyleSheet(light_button_style)
            self.ui.NightlyPatch.setStyleSheet(light_button_style)
            self.ui.BetaPatch.setStyleSheet(light_button_style)
            self.ui.Legacy.setStyleSheet(light_button_style)
            self.ui.Legacy_2.setStyleSheet(light_button_style)

            # Light cancel button set
            self.title_bar.cancel_button.setStyleSheet("background-color: rgb(255, 194, 228); color: black;")

            # Light title bar set
            self.title_bar.setStyleSheet("background-color: rgb(170, 255, 210); color: black; text-align: center;")  # Mint green color and center text

    def updateCfg():
        pass

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

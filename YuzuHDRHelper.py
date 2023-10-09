import sys
import requests
import os
import datetime
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from YuzuToolMenu import Ui_MainWindow  # Import the generated UI module

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from the generated UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to empty functions (no functionality yet)
        self.ui.NightlyButton.clicked.connect(self.NightlyDownload)
        self.ui.BetaButton.clicked.connect(self.BetaDownload)
        self.ui.WifiFixButton.clicked.connect(self.empty_function)
        self.ui.UninstallWifiButton.clicked.connect(self.empty_function)
        self.ui.FolderButton.clicked.connect(self.set_folder)
        self.ui.NightlyPatch.clicked.connect(self.NightlyPatch)
        self.ui.BetaPatch.clicked.connect(self.empty_function)

        self.selected_directory = None

    # Define empty functions for the buttons (add functionality later)
    def empty_function(self):
        pass
    
    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

    def ask_question(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(message)
        msg_box.setWindowTitle("Question")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = msg_box.exec_()

        # Return True if the user clicked Yes, otherwise False
        return result == QMessageBox.Yes

    def set_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Make the dialog read-only
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            # Check if the selected directory ends with "\yuzu\sdmc\ultimate\mods"
            if not directory.endswith("/yuzu/sdmc"):
                self.show_error_message("Selected directory must end with '/yuzu/sdmc'")
                return

            # Set the selected directory to the variable
            self.selected_directory = directory

    def download_file(self, url, file_name, download_dir):
        try:
            # Send a GET request to the GitHub API to fetch the latest release information
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                release_info = response.json()
                asset_url = None

                # Iterate through the assets to find the file you want to download
                for asset in release_info['assets']:
                    if asset['name'] == file_name:
                        asset_url = asset['browser_download_url']
                        break

                if asset_url:
                    # Download the file
                    response = requests.get(asset_url)

                    # Check if the download was successful
                    if response.status_code == 200:
                        # Specify the local file path where you want to save the downloaded file
                        local_file_path = os.path.join(download_dir, file_name)

                        with open(local_file_path, 'wb') as file:
                            file.write(response.content)
                        
                        print(f"Downloaded {file_name} to {local_file_path}")
                    else:
                        print(f"Failed to download {file_name}")
                else:
                    print(f"File {file_name} not found in the latest release assets")
            else:
                print("Failed to fetch latest release information")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        except:
            print("An unknown error occurred")

    def NightlyDownload(self):
        nightly_url = f'https://api.github.com/repos/HDR-Development/HDR-Nightlies/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'nightly'  # Change this to the desired download directory

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_error_message("Press OK to start downloading.\nWHEN IT SAYS NOT RESPONDING, DO NOT CLOSE\nFILE IS DOWNLOADING PROPERLY")

        self.download_file(nightly_url, file_name, download_dir)

    def BetaDownload(self):
        beta_url = f'https://api.github.com/repos/HDR-Development/HDR-Releases/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'beta'  # Change this to the desired download directory

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_error_message("Press OK to start downloading.\nWHEN IT SAYS NOT RESPONDING, DO NOT CLOSE\nFILE IS DOWNLOADING PROPERLY")

        self.download_file(beta_url, file_name, download_dir)

    def NightlyPatch(self):
        if self.ask_question("This process will delete everything in your arcropolis and ultimate folders.\nA backup of your mod folder will be made\nProceed?"):
            if(self.backup_mods_folder(self.selected_directory)):
                self.show_error_message("Success")
            else:
                self.show_error_message("Please select the sdmc folder first")

    def BetaPatch(self):
        if(self.backup_mods_folder(self.selected_directory)):
            self.show_error_message("Success")
        else:
            self.show_error_message("Please select the sdmc folder first")



    
    
    def backup_mods_folder(self, source_folder):
        if source_folder and source_folder.endswith("/yuzu/sdmc"):
            # Define the excluded subfolders
            excluded_subfolders = [
                "hdr",
                "hdr-assets",
                "hdr-stages",
            ]

            # Create a backup folder with the current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_folder_name = f"mods-backup-{current_datetime}"
            script_directory = os.path.dirname(os.path.abspath(__file__))
            backup_folder = os.path.join(script_directory, backup_folder_name)

            # Create the backup folder
            os.makedirs(backup_folder)

            # Source and destination paths for the 'mods' folder
            mods_source = os.path.join(source_folder, "ultimate/mods")
            mods_destination = os.path.join(backup_folder, "ultimate/mods")

            try:
                # Copy the 'mods' folder and its contents, excluding specified subfolders
                shutil.copytree(mods_source, mods_destination, ignore=shutil.ignore_patterns(*excluded_subfolders))
                print("Backup of 'mods' folder completed.")
                return True
            except Exception as e:
                print(f"Backup of 'mods' folder failed: {str(e)}")
                return False
        else:
            print("Invalid source folder.")
            return False


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
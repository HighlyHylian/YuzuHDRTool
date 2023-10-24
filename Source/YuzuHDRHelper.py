import sys
import zipfile
import glob
import requests
import os
import datetime
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from YuzuToolMenu import Ui_MainWindow  # Import the generated UI module

 
def copy_folder(source_folder, destination_folder):
    try:
        # Use shutil.copytree to copy the entire folder and its contents
        shutil.copytree(source_folder, destination_folder)
        print(f"Successfully copied '{source_folder}' to '{destination_folder}'")
        return True
    except Exception as e:
        print(f"Error copying '{source_folder}' to '{destination_folder}': {str(e)}")
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
    
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from the generated UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.selected_directory = None

    # Define empty functions for the buttons (add functionality later)
    def empty_function(self):
        self.show_error_message("Coming Soon(tm)")
    
    def isValidPath(self):
        if self.selected_directory and self.selected_directory.endswith("/yuzu/sdmc"):
            return True
        return False

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

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
            else:
                print(f"Failed to download {file_name}. Status code: {response.status_code}")
        except Exception as e:
            self.show_error_message(f"An error occurred: {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

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
            self.show_error_message(f"An error occurred: {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")

    def NightlyDownload(self):

        # github api call
        nightly_url = f'https://api.github.com/repos/HDR-Development/HDR-Nightlies/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'nightly'

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_error_message("Press OK to start downloading.\nWHEN IT SAYS NOT RESPONDING, DO NOT CLOSE\nFILE IS DOWNLOADING PROPERLY")

        self.download_file(nightly_url, file_name, download_dir)

        self.display_message_and_continue('Finished downloading nightly')

    def BetaDownload(self):
            
        # gihub api call
        beta_url = f'https://api.github.com/repos/HDR-Development/HDR-Releases/releases/latest'
        file_name = 'ryujinx-package.zip'
        download_dir = 'beta' 

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.show_error_message("Press OK to start downloading.\nWHEN IT SAYS NOT RESPONDING, DO NOT CLOSE\nFILE IS DOWNLOADING PROPERLY")

        self.download_file(beta_url, file_name, download_dir)

        self.display_message_and_continue('Finished downloading beta')

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
                if(self.backup_folder(os.path.join(self.selected_directory, "ultimate"))):
                    if extract_zip(os.path.join(os.getcwd(), "nightly/ryujinx-package.zip"), self.selected_directory):
                        folders = [
                            os.path.join(self.selected_directory, "atmosphere"),
                            os.path.join(self.selected_directory, "ultimate"),
                            os.path.join(os.getcwd(), "normal_exefs")
                        ]
                        delete_folders(folders)

                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000"), os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000", "exefs"), os.path.join(os.getcwd(), "normal_exefs", "exefs"))                        
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "ultimate"), os.path.join(self.selected_directory, "ultimate"))

                        folders = [
                            os.path.join(self.selected_directory, "atmosphere", "contents", "0100000000000013"),
                            os.path.join(self.selected_directory, "sdcard")
                        ]
                        delete_folders(folders)
                        self.display_message_and_continue("Boot up the game. Wait for the intro scene to start.\nThen close the game and press the \'Install Legacy Discovery\' button.")
                    else:
                        self.show_error_message("The ryujinx-package.zip file is missing. Download it first")
            except Exception as e:
                self.show_error_message(f"Error:  {str(e)}")
            except:
                self.show_error_message("An unknown error occurred")
        
        self.display_message_and_continue('Finished patching nightly in')

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
                if(self.backup_folder(os.path.join(self.selected_directory, "ultimate"))):
                    if extract_zip(os.path.join(os.getcwd(), "beta/ryujinx-package.zip"), self.selected_directory):
                        folders = [
                            os.path.join(self.selected_directory, "atmosphere"),
                            os.path.join(self.selected_directory, "ultimate"),
                            os.path.join(os.getcwd(), "normal_exefs")
                        ]
                        delete_folders(folders)

                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000"), os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "atmosphere", "contents", "01006A800016E000", "exefs"), os.path.join(os.getcwd(), "normal_exefs", "exefs"))                        
                        copy_folder(os.path.join(self.selected_directory, "sdcard", "ultimate"), os.path.join(self.selected_directory, "ultimate"))

                        folders = [
                            os.path.join(self.selected_directory, "atmosphere", "contents", "0100000000000013"),
                            os.path.join(self.selected_directory, "sdcard")
                        ]
                        delete_folders(folders)
                        self.display_message_and_continue("Boot up the game. Wait for the intro scene to start.\nThen close the game and press the \'Install Legacy Discovery\' button.")
                    else:
                        self.show_error_message("The ryujinx-package.zip file is missing. Download it first")
            except Exception as e:
                self.show_error_message(f"Error:  {str(e)}")
            except:
                self.show_error_message("An unknown error occurred")
        
        self.display_message_and_continue('Finished patching beta in')

    def InstallOnlineFix(self):
        if not self.isValidPath():
            self.show_error_message("Please select your yuzu/sdmc/ folder first")
            return
        
        if not os.path.exists(os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")):
            self.show_error_message("Please install hdr first")
            return # HERE

        try:
            folders = [
                os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")
            ]
            delete_folders(folders)
            copy_folder(os.path.join(os.getcwd(), "fixed_exefs"), os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
        except Exception as e:
            self.show_error_message(f"Error:  {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")
        
        self.display_message_and_continue('Finished installing online fix')

    def UninstallOnlineFix(self):
        if not self.isValidPath():
            self.show_error_message("Please select your yuzu/sdmc/ folder first")
            return
        
        if not os.path.exists(os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")):
            self.show_error_message("Please install hdr first")
            return # HERE
        
        if not os.path.exists(os.path.join(os.getcwd(), "normal_exefs")):
            self.show_error_message("Error: Normal exefs not stored. Run the nightly or beta patcher first.")
            return # HERE

        try:
            folders = [
                os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000")
            ]
            delete_folders(folders)
            copy_folder(os.path.join(os.getcwd(), "normal_exefs"), os.path.join(self.selected_directory, "atmosphere", "contents", "01006A800016E000"))
        except Exception as e:
            self.show_error_message(f"Error:  {str(e)}")
        except:
            self.show_error_message("An unknown error occurred")
        
        self.display_message_and_continue('Finished uninstalling the online fix')
    
    def installLegacy(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'legacy_discovery')):
            self.show_error_message("Please click the \'Download Legacy Discovery\' button first.")
            return

        if not self.isValidPath():
            self.show_error_message("Please select your yuzu/sdmc/ folder first")
            return

        # Set the source file to legacy discovery's path
        source_file = os.path.join(os.getcwd(), 'legacy_discovery')

        # Get the regex directory path
        target_directory_pattern = os.path.join(self.selected_directory, 'ultimate', 'arcropolis', 'config', '*', '*')

        # Get all directories matching the regex path
        matching_directories = glob.glob(target_directory_pattern)

        # Iterate over the matching directories and copy the file to each of them
        for directory in matching_directories:

            # Construct the full path for the target directory
            target_directory = os.path.join(directory, 'legacy_discovery')

            # Copy the source file to the target directory
            shutil.copy(source_file, target_directory)

        self.display_message_and_continue("Finished installing \'legacy_discovery\'")


    def backup_folder(self, source_path):
        if source_path:
            try:
                # Get the current date and time to create the backup folder name
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_folder_name = f"backup-{current_datetime}"

                # Determine the directory where the Python script is located
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Create the full path for the backup folder
                backup_folder = os.path.join(script_directory, backup_folder_name)

                # Copy the contents of the source path to the backup folder
                shutil.copytree(source_path, backup_folder)

                print(f"Backup completed. Contents of '{source_path}' copied to '{backup_folder}'.")
                return True
            except Exception as e:
                self.show_error_message(f"Backup failed: {str(e)}")
                return True
        else:
            return False
        
def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
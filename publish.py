import os
import shutil

# Use your Sublime Text Packages directory
packages_dir = 'C:\\Users\\austin.craft\\AppData\\Roaming\\Sublime Text 3\\Packages\\'

package_name = 'Gherkin Auto-Complete Plus'
target_dir = os.path.join(packages_dir, package_name)

# Remove folder if it exists
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

# Copy to ST Package Folder
shutil.copytree(os.getcwd(), target_dir)

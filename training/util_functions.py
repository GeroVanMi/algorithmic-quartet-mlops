import subprocess

def install_packages(requirements_path):
    """Install packages from a given requirements file."""
    process = subprocess.Popen(['pip', 'install', '-r', requirements_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print('Installation successful')
    else:
        print('An error occurred:', stderr.decode())


def load_image(row):
    # Load the image from the path specified in the DataFrame
    print(row)
    image_path = row['image_path']
    image = Image.open(image_path).convert('RGB')  # Convert to RGB to ensure 3 color channels
    return image


# This allows the script to be used as a module or be run directly
#if __name__ == "__main__":
#    requirements_path = 'requirements.txt'  # Default path
#    install_packages(requirements_path)

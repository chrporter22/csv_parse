# macOS Setup with Homebrew, Python 3, pip, and venv

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26%2B-%23013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-%23150458?logo=pandas&logoColor=white)
![Regex](https://img.shields.io/badge/Regex-✔️-lightgrey)
![JSON](https://img.shields.io/badge/JSON-✔️-yellow)
![PCA](https://img.shields.io/badge/PCA-(Principal%20Component%20Analysis)-orange)
![Eigen-Decomposition](https://img.shields.io/badge/Eigen-Decomposition-teal)
![Covariance-Matrix](https://img.shields.io/badge/Covariance-Matrix-green)
![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnu-bash&logoColor=white)
![Homebrew](https://img.shields.io/badge/Package%20Manager-Homebrew-FBB040?logo=homebrew&logoColor=white)
![pip](https://img.shields.io/badge/pip-Installer-blue?logo=pypi&logoColor=white)
![venv](https://img.shields.io/badge/VirtualEnv-.venv-lightblue)

The setup script configures a complete Python development environment to run a csv parsing tool for malformed csv data with nested json. Execute the 'top_components.py' file to run a PCA pipeline to extract top features leading to variance. PCA summary data saved in json format. 

**The setup script will:**
- Install Homebrew (if missing)
- Install Python 3 and pip
- Create a .venv virtual environment
- Install dependencies from requirements.txt 
- Run main.py automatically after setup

**Edit main.py and top_component.py file to update source csv file path**

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/chrpoter22/csv_parse.git
   cd csv_parse 

2. **Make the script executable**
    ```bash
    chmod +x setup.sh

3. **Run the script**
    ```bash
    ./setup.sh

4. **Activate the virtual environment manually (if needed)**
    ```bash
    source .venv/bin/activate

5. **Re-run your app**
    ```bash
    python main.py

6. **Run PCA pipeline**
    ```bash
    python top_components.py

7. **Optional - Cleanup**
    ```bash
    rm -rf .venv

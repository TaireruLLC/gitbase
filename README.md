# GitBase

GitBase is a Python package for custom databases powered by GitHub ("Gitbases"/"GitBase"), with encryption using `cryptography`. It provides Python developers with a quick and easy-to-use database solution without requiring knowledge of a new programming language. Additionally, GitBase offers offline backups, allowing users to save, load, and delete their data even without an internet connection. The online database will automatically sync with the latest file, whether offline or online.

---

## Latest Update
- Enhanced error handling: GitBases now raise exceptions for certain errors instead of just printing them, making debugging more efficient.

---

## Example Code

```python
# Example for GitBase 0.4.2
from gitbase import GitBase, PlayerDataSystem, DataSystem, KeyValue
from cryptography.fernet import Fernet
import sys

# Initialize GitHub database and encryption key
GITHUB_TOKEN = "YOUR_TOKEN"
REPO_OWNER = "YOUR_GITHUB_USERNAME"
REPO_NAME = "YOUR_REPO_NAME"
encryption_key = Fernet.generate_key()

# Setup GitBase with GitHub credentials
database = GitBase(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
player_data_system = PlayerDataSystem(db=database, encryption_key=encryption_key)
data_system = DataSystem(db=database, encryption_key=encryption_key)

# Upload and download example files to/from GitHub
database.upload_file(file_path="my_file.txt", remote_path="saved_files")
database.download_file(remote_path="my_file.txt", local_path="files")

# Define the Player class to manage individual player instances
class Player:
    def __init__(self, username, score, password):
        self.username = username
        self.score = score
        self.password = password

# Create a sample player instance
player = Player(username="john_doe", score=100, password="123")

# Save specific attributes of the player instance with encryption
player_data_system.save_account(
    username="john_doe",
    player_instance=player,
    encryption=True,
    attributes=["username", "score", "password"],
    path="players"
)

# Load player data
player_data_system.load_account(username="john_doe", player_instance=player, encryption=True)

# Placeholder functions for game flow
def load_game():
    print("Game starting...")

def main_menu():
    sys.exit("Exiting game...")

# Check if an account exists and validate user password
if player_data_system.get_all(path="players"):
    if player.password == input("Enter your password: "):
        print("Login successful!")
        load_game()
    else:
        print("Incorrect password!")
        main_menu()

# Save key-value data with encryption
data_system.save_data(key="key_name", value=69, path="data", encryption=True)

# Load and display a specific key-value pair
loaded_key_value: KeyValue = data_system.load_data(key="key_name", encryption=True)
print(f"Key: {loaded_key_value.key}, Value: {loaded_key_value.value}")

# Retrieve and display all key-value pairs in the data path
print("All stored data:", data_system.get_all(path="data"))

# Delete specific key-value data
data_system.delete_data(key="key_name")

# Retrieve and display all player accounts
print("All player accounts:", player_data_system.get_all(path="players"))

# Delete a specific player account
player_data_system.delete_account(username="john_doe")
```

---

## Consider Using [GitBase Web](https://tairerullc.vercel.app/apps/gitbase_web.html)

### GitBase Web
GitBase Web is an extension of the Python project developed by Taireru LLC called GitBase. This extension allows developers to view all their saved data via the web. 

**Note:** To use GitBase Web, you **must**:
1. Use a private GitHub repository.
2. Host the website using a service such as [Vercel](https://vercel.com).

---

## Links
- **GitBase:** [https://tairerullc.vercel.app/apps/gitbase.html](https://tairerullc.vercel.app/apps/gitbase.html)
- **Website:** [https://tairerullc.vercel.app/](https://tairerullc.vercel.app/)

---

## Contact
For any inquiries, please email us at **tairerullc@gmail.com**. We’ll get back to you as soon as possible.  
Thank you for using GitBase, and happy coding!

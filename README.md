# GitBase

GitBase is a Python package for custom databases powered by GitHub, with encryption using `cryptography`. It allows you, as a python developer to have a simple but powerful way to use database without learning a whole new programming language. Furthermore, we offer offline backups for users of your application, this means their data can be saved, loaded, and deleted even if they have no internet. Moreover, the online version will be updated based on which file, the offline or online, is the latest.

# Latest Update: 
* Added file upload and downloading

# Attention Developers: 

We are both excited and grateful to announce that **GitBase** has transitioned to a paid product! You can now purchase it directly from our website: [GitBase Product Page](https://tairerullc.vercel.app/packages/gitbase).

For just **$5 USD**, you will receive the full version of GitBase after payment. We sincerely thank you for your support and for using the free version of our product. We hope you will continue to be part of our community as we evolve. 

Thank you for your continued support!

Warm regards,  
**Tyrell Scott**  
**CEO & Founder, Taireru LLC**

# Example code: 

```py
# Example for GitBase 0.4.0
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

# Consider using [GitBase Web](https://tairerullc.vercel.app/extensions/gitbase-web): 
## Gitbase Web: 

### Gitbase Web is an extension of the python project by Taireru LLC called GitBase. This extension allows the developer to veiw all of their saved data via the web.
### Please note that to view said data you **MUST** use a private repo and use a website hosting service such as vercel.

## Links: 
### GitBase: https://tairerullc.vercel.app/packages/gitbase
### Website: https://tairerullc.vercel.app/


#### Contact 'tairerullc.help@gmail.com' for any inquires and we will get back at our latest expense. Thank you for using our product and happy coding!

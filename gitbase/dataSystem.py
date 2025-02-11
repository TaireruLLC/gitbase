import requests
import json
import os
from cryptography.fernet import Fernet
from typing import Optional, Dict, Any
from altcolor import cPrint
from .gitbase import GitBase, is_online
from moviepy.video.io.VideoFileClip import VideoFileClip  # Video handling
import math


class KeyValue:
    """
    Represents a key-value pair for storing data.
    """
    def __init__(self, key: str, value: Any):
        self.key: str = key
        self.value: Any = value


class DataSystem:
    """
    Handles data storage and retrieval, supporting online GitBase and offline backups.

    Attributes:
        db (GitBase): The database object for interacting with GitBase.
        encryption_key (bytes): Key for encrypting and decrypting data.
        fernet (Fernet): Encryption handler from the `cryptography` package.
    """
    def __init__(self, db: GitBase, encryption_key: bytes) -> None:
        self.db: GitBase = db
        self.encryption_key: bytes = encryption_key
        self.fernet: Fernet = Fernet(self.encryption_key)

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypts a string using the configured encryption key.

        Args:
            data (str): The plaintext string to encrypt.

        Returns:
            bytes: The encrypted data as bytes.
        """
        return self.fernet.encrypt(data.encode('utf-8'))

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypts a string using the configured encryption key.

        Args:
            encrypted_data (bytes): The encrypted data to decrypt.

        Returns:
            str: The decrypted plaintext string.
        """
        return self.fernet.decrypt(encrypted_data).decode('utf-8')

    def save_data(self, key: str, value: Any, path: str = "data", encryption: bool = False) -> None:
        """
        Saves data to the GitBase repository or an offline backup.

        Args:
            key (str): The key to associate with the data.
            value (Any): The value to save.
            path (str): The directory path to save the data in.
            encryption (bool): Whether to encrypt the data before saving.
        """
        try:
            if encryption:
                data = self.encrypt_data(json.dumps(value)).decode('utf-8')
            else:
                data = json.dumps(value)

            path = f"{path}/{key}.json" if not path.endswith("/") else f"{path}{key}.json"

            if is_online():
                response_code = self.db.write_data(path, data, message=f"Saved {key}")
                if response_code in (200, 201):
                    cPrint("GREEN", f"Successfully saved online data for {key}.")
                else:
                    cPrint("RED", f"Error saving online data for {key}. HTTP Status: {response_code}")
            else:
                cPrint("YELLOW", "Network is offline, saving to offline backup version.")
                self.save_offline_data(key, value)
        except Exception as e:
            cPrint("RED", f"Error: {e}")
            cPrint("GREEN", "Attempting to save to offline backup version anyway.")
            
            try:
                self.save_offline_data(key, value)
            except Exception as e:
                raise Exception(f"Error saving to offline backup: {e}")

    def load_data(self, key: str, encryption: bool) -> Optional[Any]:
        """
        Loads data from the GitBase repository or an offline backup.

        Args:
            key (str): The key of the data to load.
            encryption (bool): Whether to decrypt the data after loading.

        Returns:
            Optional[Any]: The loaded data, or None if not found.
        """
        path = f"data/{key}.json"
        try:
            if is_online():
                online_data, _ = self.db.read_data(path)
                if online_data:
                    if encryption:
                        decrypted_data = self.decrypt_data(online_data.encode('utf-8'))
                    else:
                        decrypted_data = online_data.encode('utf-8')
                    return KeyValue(key, json.loads(decrypted_data))
                cPrint("RED", f"No online data found for {key}.")
            else:
                cPrint("YELLOW", "Network is offline, loading from offline backup.")
                return self.load_offline_data(key)
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def save_offline_data(self, key: str, value: Any) -> None:
        """
        Saves data to an offline backup file.

        Args:
            key (str): The key to associate with the data.
            value (Any): The value to save.
        """
        os.makedirs("gitbase/data", exist_ok=True)
        data = self.encrypt_data(json.dumps(value))
        path = os.path.join("gitbase/data", f"{key}.gitbase")

        try:
            with open(path, "wb") as file:
                file.write(data)
            cPrint("GREEN", f"Successfully saved offline backup for {key}.")
        except Exception as e:
            raise Exception(f"Error: {e}")

    def load_offline_data(self, key: str) -> Optional[Any]:
        """
        Loads data from an offline backup file.

        Args:
            key (str): The key of the data to load.

        Returns:
            Optional[Any]: The loaded data, or None if not found.
        """
        path = os.path.join("gitbase/data", f"{key}.gitbase")
        try:
            with open(path, "rb") as file:
                data = file.read()
            decrypted_data = self.decrypt_data(data)
            return KeyValue(key, json.loads(decrypted_data))
        except Exception as e:
            raise Exception(f"Error loading offline data for {key}: {e}")
    
    def delete_data(self, key: str, delete_offline: bool = False) -> None:
        """
        Deletes data from the GitBase repository and optionally from offline storage.

        Args:
            key (str): The key of the data to delete.
            delete_offline (bool): Whether to delete the offline backup as well.
        """
        path = f"data/{key}.json"
        try:
            response_code = self.db.delete_data(path, message=f"Deleted {key}")
            if response_code == 204:
                cPrint("GREEN", f"Successfully deleted online data for {key}.")
            elif response_code == 404:
                cPrint("RED", f"No online data found for {key}.")
            else:
                cPrint("RED", f"Error deleting online data for {key}. HTTP Status: {response_code}")
        except Exception as e:
            cPrint("RED", f"Error deleting online data: {e}")

        if delete_offline:
            offline_path = os.path.join("gitbase/data", f"{key}.gitbase")
            if os.path.exists(offline_path):
                os.remove(offline_path)
                cPrint("GREEN", f"Successfully deleted offline backup for {key}.")
            else:
                cPrint("RED", f"No offline backup found for {key}.")

    def get_all(self, path: str = "data") -> Dict[str, Any]:
        """
        Retrieves all key-value pairs stored in the system.

        Args:
            path (str): The directory path to retrieve data from.

        Returns:
            Dict[str, Any]: A dictionary of all key-value pairs.
        """
        all_data = {}
        if is_online():
            try:
                response = requests.get(self.db._get_file_url(path), headers=self.db.headers)
                if response.status_code == 200:
                    files = response.json()
                    for file in files:
                        if file['name'].endswith('.json'):
                            content, _ = self.db.read_data(file['name'])
                            if content:
                                key = file['name'].rsplit('.', 1)[0]
                                decrypted_content = self.decrypt_data(content.encode('utf-8'))
                                all_data[key] = json.loads(decrypted_content)
                else:
                    cPrint("RED", f"Error retrieving files from online database. HTTP Status: {response.status_code}")
            except Exception as e:
                cPrint("RED", f"Error retrieving online data: {e}")
        else:
            cPrint("YELLOW", "Network is offline, loading data from local storage.")
            for filename in os.listdir("gitbase/data"):
                if filename.endswith('.gitbase'):
                    key = filename.rsplit('.', 1)[0]
                    all_data[key] = self.load_offline_data(key)

        return all_data

    def chunk(self, file_path: str, output_dir: str, duration_per_chunk: int = 90) -> None:
        """
        Splits a video file into smaller chunks.

        Args:
            file_path (str): Path to the input video file.
            output_dir (str): Directory to save the video chunks.
            duration_per_chunk (int): Duration per chunk in seconds.

        Notes:
            - Ensures a minimum of 4 chunks.
        """
        os.makedirs(output_dir, exist_ok=True)
        try:
            with VideoFileClip(file_path) as video:
                total_duration = video.duration
                num_chunks = max(4, math.ceil(total_duration / duration_per_chunk))
                chunk_duration = total_duration / num_chunks

                for i in range(num_chunks):
                    start_time = i * chunk_duration
                    end_time = min((i + 1) * chunk_duration, total_duration)
                    chunk_path = os.path.join(output_dir, f"chunk_{i + 1}.mp4")
                    video.subclip(start_time, end_time).write_videofile(chunk_path, codec="libx264", audio_codec="aac")
                    cPrint("GREEN", f"Chunk {i + 1} created: {chunk_path}")
        except Exception as e:
            raise Exception(f"Error during chunking: {e}")

    def pack(self, chunks_dir: str, output_file: str) -> None:
        """
        Combines video chunks into a single file.

        Args:
            chunks_dir (str): Directory containing the video chunks.
            output_file (str): Path for the combined output file.

        Notes:
            - Assumes chunks are in order and in the same format.
        """
        try:
            chunk_files = sorted(
                [os.path.join(chunks_dir, f) for f in os.listdir(chunks_dir) if f.endswith(".mp4")],
                key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0])
            )
            with VideoFileClip(chunk_files[0]) as final_clip:
                for chunk_file in chunk_files[1:]:
                    with VideoFileClip(chunk_file) as chunk:
                        final_clip = final_clip.concatenate(chunk)

                final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
            cPrint("GREEN", f"Packed video saved to: {output_file}")
        except Exception as e:
            raise Exception(f"Error during packing: {e}")
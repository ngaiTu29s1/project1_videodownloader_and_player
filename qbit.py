import subprocess
import time
import qbittorrentapi
import os

# Paths to qBittorrent
QB_INSTALLER_PATH = r"C:\Users\ADMIN\Documents\Code\Project1\qbittorrent\qBittorrent.exe"
QB_PORTABLE_PATH = r"C:\Users\ADMIN\Documents\Code\Project1\qbittorrent\qBittorrentPortable\App\qBittorrent\qBittorrent.exe"

# Default download location
DEFAULT_DOWNLOAD_LOCATION = r"C:\Users\ADMIN\Downloads"

# Function to start qBittorrent in headless mode
def start_qbittorrent():
    # Check if portable version exists
    if os.path.exists(QB_PORTABLE_PATH):
        print(f"Starting qBittorrent Portable from: {QB_PORTABLE_PATH}")
        process = subprocess.Popen([QB_PORTABLE_PATH, "--webui-port=8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        qb_path_used = QB_PORTABLE_PATH
    else:
        # If portable doesn't exist, check if installer exists
        if os.path.exists(QB_INSTALLER_PATH):
            print(f"First run detected. Starting qBittorrent installer: {QB_INSTALLER_PATH}")
            # Run the installer - you might want to add flags for silent install if available
            process = subprocess.Popen([QB_INSTALLER_PATH])
            
            # Wait for installation to complete - user needs to go through installer steps
            print("Please complete the qBittorrent installation. The script will continue after installation.")
            process.wait()
            
            # Check if portable is now available after installation
            if os.path.exists(QB_PORTABLE_PATH):
                print(f"Installation complete. Starting qBittorrent Portable from: {QB_PORTABLE_PATH}")
                process = subprocess.Popen([QB_PORTABLE_PATH, "--webui-port=8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                qb_path_used = QB_PORTABLE_PATH
            else:
                raise FileNotFoundError(f"qBittorrent portable executable not found at: {QB_PORTABLE_PATH} after installation")
        else:
            raise FileNotFoundError(f"Neither installer nor portable executable found")
    
    time.sleep(8)  # Increased wait time to ensure qBittorrent is fully started
    print("qBittorrent started in background!")
    return process

# Rest of the code remains unchanged
def stop_qbittorrent(qb_process):
    qb_process.terminate()
    print("qBittorrent stopped.")

# Function to add torrent by info hash and set download location
def add_torrent_by_hash(qb_client, info_hash, download_location):
    try:
        # First, check if the download location exists
        if not os.path.exists(download_location):
            os.makedirs(download_location, exist_ok=True)
            print(f"Created download directory: {download_location}")
        
        # Create magnet link
        magnet_uri = f"magnet:?xt=urn:btih:{info_hash}"
        print(f"Using magnet URI: {magnet_uri}")
        
        # Add the torrent
        response = qb_client.torrents_add(urls=magnet_uri, save_path=download_location)
        print(f"Torrent add response: {response}")
        
        if response == "Ok.":
            print(f"Torrent with hash {info_hash} added successfully! Download location: {download_location}")
            # Wait a bit for qBittorrent to process the magnet link
            print("Waiting for qBittorrent to process the magnet link...")
            time.sleep(5)
        else:
            print(f"Failed to add torrent. Response: {response}")
            
    except Exception as e:
        print(f"Error adding torrent: {e}")
        raise

# Function to monitor download progress
def monitor_torrents(qb_client, target_hash):
    print(f"Monitoring for torrent with hash: {target_hash}")
    attempts = 0
    max_attempts = 12  # Try for about 2 minutes (12 attempts × 10 seconds)
    
    while attempts < max_attempts:
        try:
            attempts += 1
            print(f"Checking torrents (attempt {attempts}/{max_attempts})...")
            
            # First, get a list of all torrents
            all_torrents = qb_client.torrents_info()
            print(f"Found {len(all_torrents)} torrents in qBittorrent")
            
            # Debug: Print all torrent hashes
            if all_torrents:
                print("Torrent hashes in qBittorrent:")
                for torrent in all_torrents:
                    print(f"  - {torrent.hash} ({torrent.name})")
            
            # Look for our specific torrent
            matching_torrents = [t for t in all_torrents if t.hash.lower() == target_hash.lower()]
            
            if matching_torrents:
                torrent = matching_torrents[0]
                print(f"Found torrent: {torrent.name}")
                
                # Monitor until complete or timeout
                monitor_start_time = time.time()
                
                while time.time() - monitor_start_time < 600:  # Monitor for up to 10 minutes
                    torrent = qb_client.torrents_info(torrent_hashes=torrent.hash)[0]
                    print(f"\r{torrent.name} - {torrent.progress * 100:.2f}% - {torrent.state} - Speed: {torrent.dlspeed / 1024:.2f} KB/s", end="")
                    
                    if torrent.progress >= 1.0 or torrent.state in ['stalledUP', 'uploading', 'completed']:
                        print(f"\nDownload complete for {torrent.name}")
                        return True
                    
                    time.sleep(2)
                
                print("\nTimeout while monitoring torrent")
                return False
            
            time.sleep(10)  # Wait before checking again
            
        except Exception as e:
            print(f"Error monitoring torrents: {e}")
            time.sleep(5)
    
    print("No matching torrent found after multiple attempts")
    return False

# Main function to run the script
def main():
    qb_process = None
    
    try:
        # Start qBittorrent
        qb_process = start_qbittorrent()
        
        # Connect to qBittorrent Web API
        print("Connecting to qBittorrent Web API...")
        qb = qbittorrentapi.Client(host="localhost", port=8080, username="admin", password="adminadmin")
        qb.auth_log_in()
        print("Successfully connected to qBittorrent Web API")
        
        # Check if qBitTorrent is responsive
        version = qb.app_version()
        print(f"qBittorrent version: {version}")

        # Prompt user for torrent info hash
        info_hash = input("Enter the torrent info hash: ").strip()
        
        # Use default download location or prompt user for a different location
        use_default_location = input(f"Use default download location ({DEFAULT_DOWNLOAD_LOCATION})? (y/n): ").strip().lower()
        if use_default_location == 'y':
            download_location = DEFAULT_DOWNLOAD_LOCATION
        else:
            download_location = input("Enter the download location (absolute path): ").strip()

        # Add torrent by info hash and set download location
        add_torrent_by_hash(qb, info_hash, download_location)

        # Monitor download progress
        monitor_torrents(qb, info_hash)

    except qbittorrentapi.LoginFailed as e:
        print(f"Login failed: {e}")
        print("Make sure Web UI is enabled in qBittorrent settings:")
        print("  1. Open qBittorrent")
        print("  2. Go to Tools > Options > Web UI")
        print("  3. Check 'Web User Interface (Remote Control)'")
        print("  4. Set username and password (default: admin/adminadmin)")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Stop qBittorrent when done
        if qb_process:
            stop_qbittorrent(qb_process)

if __name__ == "__main__":
    main()
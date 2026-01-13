"""
Version manager for tracking and updating League of Legends patch versions.
"""
import os
import json
from datetime import datetime
from .common.utils import get_latest_patch_version


VERSION_FILE = "version.json"


def get_srv_directory():
    """Get the absolute path to the srv directory."""
    directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
    srv_dir = os.path.join(directory, "srv")
    if not os.path.exists(srv_dir):
        os.makedirs(srv_dir)
    return srv_dir


def get_version_file_path():
    """Get the full path to the version.json file."""
    return os.path.join(get_srv_directory(), VERSION_FILE)


def load_current_version():
    """Load the current version from version.json file."""
    version_path = get_version_file_path()
    if os.path.exists(version_path):
        try:
            with open(version_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_version(version_number):
    """Save the current version to version.json file."""
    version_data = {
        "version": version_number,
        "lastUpdate": datetime.utcnow().isoformat() + "Z",
        "timestamp": int(datetime.utcnow().timestamp())
    }
    
    version_path = get_version_file_path()
    print(f"Saving version to: {version_path}")
    
    try:
        with open(version_path, 'w') as f:
            json.dump(version_data, f, indent=2)
        print(f"✓ Version file updated successfully: {version_number}")
        
        # Verify the file was written
        if os.path.exists(version_path):
            with open(version_path, 'r') as f:
                saved_data = json.load(f)
                print(f"✓ Verified: {saved_data}")
        else:
            print(f"✗ Warning: Version file not found after save!")
            
    except Exception as e:
        print(f"✗ Error saving version file: {e}")
        raise
    
    return version_data


def check_for_new_version():
    """
    Check if a new patch version is available.
    Returns tuple: (has_new_version, current_version, latest_version)
    """
    try:
        latest_version = get_latest_patch_version()
        current_data = load_current_version()
        
        if current_data is None:
            # No version file exists, this is a new version
            return True, None, latest_version
        
        current_version = current_data.get("version")
        
        if current_version != latest_version:
            print(f"New version detected: {current_version} -> {latest_version}")
            return True, current_version, latest_version
        else:
            print(f"Already up to date: {current_version}")
            return False, current_version, latest_version
            
    except Exception as e:
        print(f"Error checking for new version: {e}")
        return False, None, None


def update_version_after_generation():
    """Update version.json after successfully generating champion/item data."""
    try:
        latest_version = get_latest_patch_version()
        save_version(latest_version)
        return True
    except Exception as e:
        print(f"Error updating version: {e}")
        return False


if __name__ == "__main__":
    # When run directly, just check and display version info
    has_new, current, latest = check_for_new_version()
    print(f"\nCurrent version: {current}")
    print(f"Latest version: {latest}")
    print(f"Update needed: {has_new}")

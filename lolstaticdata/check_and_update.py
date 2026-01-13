"""
Script to check for new patch versions and trigger data generation if needed.
This script is designed to be run by cron or a scheduler.
"""
import sys
import subprocess
from .version_manager import check_for_new_version, update_version_after_generation


def run_data_generation():
    """Run the champion and item data generation."""
    print("Starting data generation...")
    
    try:
        # Run champions generation
        print("Generating champion data...")
        result = subprocess.run(
            [sys.executable, "-m", "lolstaticdata.champions"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        # Run items generation
        print("Generating item data...")
        result = subprocess.run(
            [sys.executable, "-m", "lolstaticdata.items"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        
        print("Data generation completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error during data generation: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error during data generation: {e}")
        return False


def main():
    """Main function to check for updates and regenerate data if needed."""
    print("=" * 60)
    print("Checking for League of Legends patch updates...")
    print("=" * 60)
    
    has_new_version, current_version, latest_version = check_for_new_version()
    
    if not has_new_version:
        print(f"✓ No update needed. Current version {current_version} is up to date.")
        print("=" * 60)
        return 0
    
    print(f"\n🔄 New version available: {latest_version}")
    if current_version:
        print(f"   Updating from version {current_version}")
    else:
        print("   No previous version found, generating initial data")
    
    print("\n" + "=" * 60)
    
    # Run data generation
    success = run_data_generation()
    
    if success:
        print("\n" + "=" * 60)
        print("Updating version file...")
        # Update version file after successful generation
        try:
            update_version_after_generation()
            print(f"✓ Successfully updated to version {latest_version}")
            print("=" * 60)
            return 0
        except Exception as e:
            print(f"✗ Error updating version file: {e}")
            print("=" * 60)
            return 1
    else:
        print("\n" + "=" * 60)
        print("✗ Failed to generate data. Version file not updated.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

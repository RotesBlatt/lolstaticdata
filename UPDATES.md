# League of Legends Static Data - Automatic Updates

This directory contains scripts for automatically checking and updating League of Legends patch data.

## How It Works

The system automatically:
1. Checks for new patch versions every hour
2. Compares against the stored version in `srv/version.json`
3. Regenerates all champion and item data when a new patch is detected
4. Updates the version file with the new patch number and timestamp

## Version File Format

The `srv/version.json` file contains:
```json
{
  "version": "14.23.1",
  "lastUpdate": "2026-01-13T10:30:00Z",
  "timestamp": 1736765400
}
```

- `version`: The current League of Legends patch version
- `lastUpdate`: ISO 8601 timestamp of when the data was last generated
- `timestamp`: Unix timestamp of the last update

## Running Updates Manually

### Using Docker
```bash
# Force an immediate update check
docker-compose exec lol-data-generator python -m lolstaticdata.check_and_update

# View current version
docker-compose exec lol-data-generator cat /app/srv/version.json
```

### Running Locally
```bash
# Check and update if needed
python update_checker.py

# Or use the module directly
python -m lolstaticdata.check_and_update

# Just check version without updating
python -m lolstaticdata.version_manager
```

## Scheduling Updates (Non-Docker)

### Linux/macOS (cron)
Add to your crontab (`crontab -e`):
```cron
# Check for updates every hour
0 * * * * cd /path/to/lolstaticdata && /usr/bin/python3 update_checker.py >> /var/log/lol-updates.log 2>&1
```

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily, repeat every 1 hour
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `C:\path\to\lolstaticdata\update_checker.py`
   - Start in: `C:\path\to\lolstaticdata`

## Files

- `version_manager.py`: Core version tracking functionality
- `check_and_update.py`: Main update script
- `update_checker.py`: Standalone executable script
- `check_updates.sh`: Shell script for cron (used in Docker)

## Logging

In Docker, logs are written to `/var/log/cron.log` and can be viewed with:
```bash
docker-compose logs -f lol-data-generator
```

For local execution, redirect output to a log file:
```bash
python update_checker.py >> updates.log 2>&1
```

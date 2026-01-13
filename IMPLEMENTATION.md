# Implementation Summary: Automatic Updates & Version Tracking

## Features Implemented

### 1. Version Tracking (`version.json`)
- **Location**: `srv/version.json`
- **Format**:
  ```json
  {
    "version": "14.23.1",
    "lastUpdate": "2026-01-13T10:30:00Z",
    "timestamp": 1736765400
  }
  ```
- **Purpose**: Tracks the current League of Legends patch version and when data was last generated

### 2. Automatic Update Checking
- **Frequency**: Every hour (via cron job in Docker)
- **Process**:
  1. Fetches latest patch version from Data Dragon API
  2. Compares with stored version in `version.json`
  3. If new version detected, triggers champion and item data generation
  4. Updates `version.json` after successful generation

### 3. Docker Integration
- **Service**: Runs continuously with cron daemon
- **Initial Run**: Generates data on first startup
- **Ongoing**: Checks for updates every hour automatically
- **Volume**: Data stored in `lol-static-data` volume accessible by other containers

## Files Created/Modified

### New Files:
1. **`lolstaticdata/version_manager.py`** - Core version tracking functionality
2. **`lolstaticdata/check_and_update.py`** - Main update orchestration script
3. **`check_updates.sh`** - Shell script for cron execution
4. **`update_checker.py`** - Standalone script for manual execution
5. **`UPDATES.md`** - Documentation for the update system

### Modified Files:
1. **`Dockerfile`** - Added cron, startup script, and automatic update checking
2. **`docker-compose.yml`** - Changed to keep container running for continuous updates
3. **`README.md`** - Updated with Docker usage and version tracking info
4. **`lolstaticdata/champions/__main__.py`** - Calls version update after generation
5. **`lolstaticdata/items/__main__.py`** - Calls version update after generation
6. **`.dockerignore`** - Updated to exclude documentation

## Usage

### Docker (Automatic - Recommended):
```bash
# Start the service (runs continuously)
docker-compose up -d

# View logs including update checks
docker-compose logs -f lol-data-generator

# Force immediate update check
docker-compose exec lol-data-generator python -m lolstaticdata.check_and_update

# Check current version
docker-compose exec lol-data-generator cat /app/srv/version.json
```

### Manual (Local):
```bash
# Check and update if needed
python update_checker.py

# Or using module
python -m lolstaticdata.check_and_update

# Just check version
python -m lolstaticdata.version_manager
```

### Accessing Data from Other Containers:
```yaml
services:
  my-app:
    image: my-image
    volumes:
      - lol-static-data:/data:ro  # Read-only access

volumes:
  lol-static-data:
    external: true
```

## Cron Schedule
- **Pattern**: `0 * * * *` (every hour at minute 0)
- **Examples**: 
  - 1:00 AM, 2:00 AM, 3:00 AM... 
  - 1:00 PM, 2:00 PM, 3:00 PM...

## Technical Details

### Version Detection:
- Uses `get_latest_patch_version()` from `common/utils.py`
- Fetches from: `http://ddragon.leagueoflegends.com/api/versions.json`
- Filters out beta versions (those with underscores)
- Uses natural sorting to get the latest version

### Data Generation:
- Champions: `python -m lolstaticdata.champions`
- Items: `python -m lolstaticdata.items`
- Version file updated only after successful generation

### Error Handling:
- Continues running even if update fails
- Logs all operations to `/var/log/cron.log` (in Docker)
- Version file only updated on successful generation

## Benefits

1. **Always Current**: Data automatically updates when new patches release
2. **No Manual Work**: Set it and forget it
3. **Shareable**: Volume can be mounted by multiple containers
4. **Verifiable**: Version file tracks exactly what data you have
5. **Flexible**: Works in Docker or standalone

# Example: Using the LOL Static Data Volume

This example demonstrates how to use the `lol-static-data` volume in your own Docker containers.

## Example Docker Compose Setup

Create a `docker-compose.yml` in your project:

```yaml
version: '3.8'

services:
  # Your application that needs LOL data
  my-lol-app:
    image: nginx:alpine  # Replace with your actual image
    ports:
      - "8080:80"
    volumes:
      # Mount the LOL data volume as read-only
      - lol-static-data:/usr/share/nginx/html:ro
    restart: unless-stopped

# Reference the external volume created by lolstaticdata
volumes:
  lol-static-data:
    external: true
```

## Example Node.js Application

```javascript
// app.js
const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const DATA_PATH = '/data/lol';  // Mount point in your container

// Get version info
app.get('/api/version', async (req, res) => {
  try {
    const versionData = await fs.readFile(
      path.join(DATA_PATH, 'version.json'),
      'utf8'
    );
    res.json(JSON.parse(versionData));
  } catch (err) {
    res.status(500).json({ error: 'Failed to read version' });
  }
});

// Get all champions
app.get('/api/champions', async (req, res) => {
  try {
    const championsData = await fs.readFile(
      path.join(DATA_PATH, 'champions.json'),
      'utf8'
    );
    res.json(JSON.parse(championsData));
  } catch (err) {
    res.status(500).json({ error: 'Failed to read champions' });
  }
});

// Get specific champion
app.get('/api/champions/:name', async (req, res) => {
  try {
    const championData = await fs.readFile(
      path.join(DATA_PATH, 'champions', `${req.params.name}.json`),
      'utf8'
    );
    res.json(JSON.parse(championData));
  } catch (err) {
    res.status(404).json({ error: 'Champion not found' });
  }
});

app.listen(3000, () => {
  console.log('LOL API running on port 3000');
});
```

### Docker Compose for Node.js App

```yaml
version: '3.8'

services:
  lol-api:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - lol-static-data:/data/lol:ro
    environment:
      - NODE_ENV=production
    restart: unless-stopped

volumes:
  lol-static-data:
    external: true
```

## Example Python Flask Application

```python
# app.py
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)
DATA_PATH = '/data/lol'  # Mount point in your container

@app.route('/api/version')
def get_version():
    try:
        with open(os.path.join(DATA_PATH, 'version.json'), 'r') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/champions')
def get_champions():
    try:
        with open(os.path.join(DATA_PATH, 'champions.json'), 'r') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/champions/<name>')
def get_champion(name):
    try:
        filepath = os.path.join(DATA_PATH, 'champions', f'{name}.json')
        with open(filepath, 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({'error': 'Champion not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Example Nginx Configuration

Serve the files directly with nginx:

```nginx
server {
    listen 80;
    server_name localhost;
    
    root /usr/share/nginx/html;
    
    # Enable CORS
    add_header 'Access-Control-Allow-Origin' '*' always;
    
    # Serve JSON files
    location ~* \.json$ {
        add_header Content-Type application/json;
        add_header Cache-Control "public, max-age=3600";
    }
    
    # Version endpoint
    location = /version {
        try_files /version.json =404;
    }
    
    # Champions endpoint
    location /champions {
        autoindex on;
        autoindex_format json;
    }
}
```

## Checking if Data is Available

Before starting your application, you can check if the data volume exists:

```bash
# List all volumes
docker volume ls

# Inspect the lol-static-data volume
docker volume inspect lol-static-data

# Check the contents
docker run --rm -v lol-static-data:/data alpine ls -la /data
```

## Watching for Updates

If you want your application to detect when data is updated:

```python
import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VersionChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('version.json'):
            with open(event.src_path, 'r') as f:
                version = json.load(f)
                print(f"Data updated to version {version['version']}")
                # Reload your application data here

# Watch the data directory
observer = Observer()
observer.schedule(
    VersionChangeHandler(),
    path='/data/lol',
    recursive=False
)
observer.start()
```

## Multi-Container Setup

Complete example with both data generator and API:

```yaml
version: '3.8'

services:
  # Data generator (from lolstaticdata project)
  lol-data-generator:
    build: ./lolstaticdata
    volumes:
      - lol-static-data:/app/srv
      - ./lolstaticdata/__cache__:/app/__cache__
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  # Your API service
  lol-api:
    build: ./api
    ports:
      - "3000:3000"
    volumes:
      - lol-static-data:/data/lol:ro
    depends_on:
      - lol-data-generator
    restart: unless-stopped

volumes:
  lol-static-data:
    driver: local
```

## Tips

1. **Always mount as read-only** (`:ro`) in consuming containers
2. **Check version.json** to know when data was last updated
3. **Handle missing files gracefully** - data generation takes time on first run
4. **Cache responses** in your application for better performance
5. **Monitor the data generator logs** to know when updates happen

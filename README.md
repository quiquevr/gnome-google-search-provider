# GNOME Google Search

A simple GNOME extension that allows you to submit a Google query directly from the Activities Overview search box (activated by the Super key).

<img width="2220" height="400" alt="image" src="https://github.com/user-attachments/assets/9a26a63e-412f-4925-8a42-890878af3e00" />




https://github.com/user-attachments/assets/9a09cf49-9090-4516-88d8-8c6f98644149




## Goals

* **P0** - Submit a simple Google search
* **P0** - Package as a real extension
* **P1** - Integrate suggestions for partial search terms

## Non-Goals

* Update the Activities Overview search results UI elements

## Use Cases

* Submit a Google search without having to manually activate a different Google Chrome window.

## Deployment

**Note:** While I update the project to be a real extension, you can manually give it a try by deploying the files yourself.

### 1. Clone the repository
Clone the repo to a temporary folder:

```bash
git clone https://github.com/quiquevr/gnome-google-search-provider.git
cd gnome-google-search-provider
```

### 2. Install System Dependencies
*Install these first to ensure the Python libraries build correctly.*

**Fedora:**
```bash
sudo dnf install gobject-introspection-devel cairo-gobject-devel
```

**Ubuntu/Debian:**
```bash
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev
```

### 3. Install Python Dependencies
```bash
pip install PyGObject requests beautifulsoup4 lxml
```

### 4. Copy files and set permissions
Copy the source files to their respective system locations and make them executable.

**Desktop file:**
```bash
sudo cp data/org.gnome.GoogleSearch.SearchProvider.desktop /usr/share/applications/
sudo chmod +x /usr/share/applications/org.gnome.GoogleSearch.SearchProvider.desktop
```

**Ini file:**
```bash
sudo cp data/org.gnome.GoogleSearch.SearchProvider.ini /usr/share/gnome-shell/search-providers/
sudo chmod +x /usr/share/gnome-shell/search-providers/org.gnome.GoogleSearch.SearchProvider.ini
```

**Service file:**
```bash
sudo cp data/org.gnome.GoogleSearch.SearchProvider.service /usr/share/dbus-1/services/
sudo chmod +x /usr/share/dbus-1/services/org.gnome.GoogleSearch.SearchProvider.service
```

**Python implementation:**
```bash
sudo cp src/google-search-provider.py /usr/local/bin/
sudo chmod +x /usr/local/bin/google-search-provider.py
```

### 5. Activate the Provider
1.  **Log out** of your current GNOME session and log back in (or restart GNOME Shell).
2.  Go to **Settings > Search**.
3.  Find **Google Search Provider** in the list and ensure it is toggled **ON**.

### 6. Ready!
You will now see a Google Search entry in the Activities Overview when you press the `Super` key and type a search term.

## Reporting Issues

Standard [issue tracker](https://github.com/quiquevr/gnome-google-search-provider/issues).

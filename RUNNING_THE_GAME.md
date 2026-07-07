# Running the Integrated Adventure Game

The frontend and backend are now running as **one contiguous program**, no longer as separate processes.

## Quick Start

### Option 1: VS Code (Recommended) ⭐
The easiest way! Just press `Ctrl+Shift+B` to run the build task, or:
1. Open the Command Palette: `Ctrl+Shift+P`
2. Type: `Tasks: Run Build Task`
3. Select: `🎮 Run Adventure Game`
4. The server starts in VS Code's integrated terminal

Then visit **http://localhost:5000** in your browser.

### Option 2: Using the Batch File (Windows)
Simply double-click `start.bat` in the project root directory. This will:
1. Navigate to the backend folder
2. Activate the virtual environment
3. Install any missing dependencies
4. Start the Flask server which serves both the API and the React frontend

### Option 3: Manual Start
Open a terminal in the project root and run:
```bash
cd backend
python app.py
```

The application will start on **http://localhost:5000**

## What's Changed

### Previous Setup (Two Separate Processes)
- **Frontend**: React dev server on `http://localhost:3000`
- **Backend**: Flask API server on `http://localhost:5000`
- These ran as two completely separate processes

### New Setup (Single Integrated Program)
- **Single Flask Server**: Runs on `http://localhost:5000`
- Serves the React frontend (built version from `frontend/build/`)
- Handles all API routes (`/api/*`)
- Everything runs from one Python process

## Architecture

```
Flask Server (Port 5000)
├── Static Files (React build)
│   ├── index.html
│   ├── /static/js/main.*.js
│   └── /static/css/main.*.css
└── API Routes
    ├── /api/init
    ├── /api/event
    ├── /api/choose
    └── ... (other game logic endpoints)
```

## How It Works

1. When you visit `http://localhost:5000`, Flask serves the React `index.html`
2. React loads and makes API calls to `/api/*` endpoints
3. All requests are handled by the same Flask server
4. No need for separate processes or ports

## Updating the Frontend

If you need to make changes to the React components:

1. **Modify files** in `frontend/src/`
2. **Rebuild** the React app:
   ```bash
   cd frontend
   npm run build
   ```
3. The new build will be used the next time you start the server

## Port Configuration

- The application runs on **Port 5000**
- This is configured in [backend/app.py](backend/app.py) line with `app.run(debug=True, port=5000)`

## Troubleshooting

### "Module not found" error
Make sure dependencies are installed:
```bash
cd backend
python -m pip install -r requirements.txt
```

### Changes to Frontend Not Showing
You need to rebuild the React app and restart the server:
```bash
cd frontend
npm run build
```

### Port 5000 Already in Use
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=8000)  # Use 8000 instead
```

### VS Code Shows "Python Extension Not Found"
Install the Python extension from the VS Code marketplace or click the recommendation when it appears.

## VS Code Keyboard Shortcuts

- **Run the game**: `Ctrl+Shift+B`
- **Open Command Palette**: `Ctrl+Shift+P` → Type "Run Task"
- **Debug**: `F5` (if launch configuration is set up)
- **Stop server**: Press `Ctrl+C` in the terminal

## Benefits of This Setup

✅ Single server process - simpler to manage and deploy  
✅ No need to manage multiple ports  
✅ Easier to package and distribute  
✅ Better production deployment options  
✅ Simplified development workflow  
✅ Run directly from VS Code with one keystroke  

---

**The game is now a unified, contiguous program that runs from VS Code!**


## What's Changed

### Previous Setup (Two Separate Processes)
- **Frontend**: React dev server on `http://localhost:3000`
- **Backend**: Flask API server on `http://localhost:5000`
- These ran as two completely separate processes

### New Setup (Single Integrated Program)
- **Single Flask Server**: Runs on `http://localhost:5000`
- Serves the React frontend (built version from `frontend/build/`)
- Handles all API routes (`/api/*`)
- Everything runs from one Python process

## Architecture

```
Flask Server (Port 5000)
├── Static Files (React build)
│   ├── index.html
│   ├── /static/js/main.*.js
│   └── /static/css/main.*.css
└── API Routes
    ├── /api/init
    ├── /api/event
    ├── /api/choose
    └── ... (other game logic endpoints)
```

## How It Works

1. When you visit `http://localhost:5000`, Flask serves the React `index.html`
2. React loads and makes API calls to `/api/*` endpoints
3. All requests are handled by the same Flask server
4. No need for separate processes or ports

## Updating the Frontend

If you need to make changes to the React components:

1. **Modify files** in `frontend/src/`
2. **Rebuild** the React app:
   ```bash
   cd frontend
   npm run build
   ```
3. The new build will be used the next time you start the server

## Port Configuration

- The application runs on **Port 5000**
- This is configured in [backend/app.py](backend/app.py) line with `app.run(debug=True, port=5000)`

## Troubleshooting

### "Module not found" error
Make sure dependencies are installed:
```bash
cd backend
python -m pip install -r requirements.txt
```

### Changes to Frontend Not Showing
You need to rebuild the React app and restart the server:
```bash
cd frontend
npm run build
```

### Port 5000 Already in Use
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=8000)  # Use 8000 instead
```

## Benefits of This Setup

✅ Single server process - simpler to manage and deploy  
✅ No need to manage multiple ports  
✅ Easier to package and distribute  
✅ Better production deployment options  
✅ Simplified development workflow  

---

**The game is now a unified, contiguous program!**

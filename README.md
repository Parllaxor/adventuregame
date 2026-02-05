# Adventure Game - Web Version

## Setup Instructions

### Backend (Flask)

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask server:**
   ```bash
   python app.py
   ```
   
   Server will run on `http://localhost:5000`

---

### Frontend (React)

1. **In a NEW terminal, navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   
   App will open on `http://localhost:3000`

---

## How to Add New Events

### 1. Create Event Function (Backend - app.py)

In `backend/app.py`, add your event function in the **Events** section (around line 30):

```python
def trigger_my_event():
    text = "Event description\n\n1. Choice 1\n2. Choice 2\n3. Choice 3"
    choices = ["Choice 1", "Choice 2", "Choice 3"]
    return text, choices
```

### 2. Add Event Handler (Backend - app.py)

In the `process_choice()` function (around line 140), add:

```python
elif event_name == "trigger_my_event":
    if choice == "Choice 1":
        character_stats["XP"] += 10
        return {"text": "Outcome text", "continue": True}
    elif choice == "Choice 2":
        character_stats["HP"] -= 5
        return {"text": "Different outcome", "continue": True}
    # ... etc
```

### 3. Add to Biome Pool (Backend - app.py)

In the `EVENTS` dictionary (around line 50), add your event:

```python
EVENTS = {
    "Forest": [trigger_forest_encounter, trigger_goblin_fight, trigger_my_event],
    "Ocean": [trigger_pirate_attack, trigger_my_event],
}
```

---

## File Structure

```
backend/
├── app.py              # Flask server + game logic
└── requirements.txt    # Python packages

frontend/
├── public/
│   └── index.html      # HTML entry point
├── src/
│   ├── components/     # React components
│   │   ├── ClassSelection.js
│   │   ├── GameScreen.js
│   │   └── Stats.js
│   ├── App.js          # Main app component
│   ├── App.css
│   └── index.js        # React entry point
└── package.json        # npm dependencies
```

---

## Frontend Components Overview

- **ClassSelection** - Character class picker
- **GameScreen** - Main game loop (events + choices)
- **Stats** - Character stats and inventory display

---

## Tips for Quick Expansion

1. **Add more stats?** Update `character_stats` object in `app.py`
2. **Add items?** Update `inventory` object in `app.py`
3. **Add biomes?** Add new key to `EVENTS` dict in `app.py`
4. **Style changes?** Edit `.css` files in `frontend/src/components/`

---

## Troubleshooting

- **CORS error?** Make sure both servers are running (port 5000 for Flask, 3000 for React)
- **Event not appearing?** Check that event is added to `EVENTS` dict for the biome
- **Stats not updating?** Make sure you're calling `setStats()` and `setGameState()` in `GameScreen.js`

# Aliiitown - Project Overview

A personal portfolio web application featuring interactive games and projects. This is a FastAPI backend serving static HTML pages with Tailwind CSS styling and interactive JavaScript games.

## Project Type & Architecture

**Type**: Full-stack web application (personal portfolio + games)
**Backend**: FastAPI (Python) serving static files
**Frontend**: Vanilla HTML/CSS/JavaScript with Tailwind CSS
**Build System**: Node.js scripts for CSS processing and asset management

### Key Technologies
- **Backend**: FastAPI, uvicorn
- **Frontend**: Tailwind CSS, vanilla JavaScript
- **Build**: Node.js scripts for CSS hashing and HTML updates
- **Deployment**: Docker multi-stage build

## Essential Development Commands

### Development Workflow
```bash
# Start development (watches CSS changes)
npm run dev
# Equivalent to: npm run build-css

# Production build (minifies CSS and adds cache-busting hashes)
npm run build-css-prod

# Run the FastAPI server
python main.py
# Serves on http://localhost:8000

# Docker build and run
docker build -t aliiitown .
docker run -p 8000:8000 aliiitown
```

### Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for build tools)
npm install
```

## Architecture & Code Organization

### Project Structure
```
/Users/aliabid/aliiitown/
├── main.py              # FastAPI application entry point
├── fishwish.py          # Game-specific route handler
├── pages/               # HTML templates
│   ├── index.html       # Landing page
│   └── fishwish.html    # Fishwish game page
├── src/                 # Source CSS (Tailwind)
│   └── index.css        # Main stylesheet with Tailwind directives
├── static/              # Static assets served by FastAPI
│   ├── styles.css       # Compiled CSS (development)
│   ├── styles.*.css     # Hashed CSS files (production)
│   ├── *.png           # Images and icons
│   └── *.js            # Client-side JavaScript
├── scripts/             # Build automation
│   ├── hash-css.js      # Generate cache-busting CSS filenames
│   ├── update-html.js   # Update HTML to reference hashed CSS
│   └── reset-html-dev.js # Reset HTML to use non-hashed CSS
└── package.json         # Node.js build dependencies
```

### Backend Architecture
- **FastAPI** serves as a lightweight file server
- Static file mounting at `/static` route
- Modular route handling (fishwish game in separate module)
- Simple file responses for HTML pages

### Frontend Architecture
- **Tailwind CSS** for styling with custom component classes
- **Vanilla JavaScript** for game logic and interactions
- **Responsive design** with dark mode support
- **Component-based CSS** using Tailwind's @apply directives

## Key Patterns & Conventions

### CSS Asset Management
The project uses a sophisticated CSS cache-busting system:

1. **Development**: CSS files use standard names (`styles.css`)
2. **Production**: CSS files get MD5 hashes (`styles.41ccec48.css`)
3. **HTML updates**: Scripts automatically update HTML references

**Build Process**:
1. `reset-html-dev.js` - Resets HTML to use non-hashed CSS for development
2. `tailwindcss` - Compiles and watches CSS changes
3. `hash-css.js` - Generates hashed CSS filenames for production
4. `update-html.js` - Updates HTML files to reference hashed CSS

### Component Patterns
- **Game cards**: Reusable card components with state-based styling
- **Modular CSS**: Page-specific styles using class namespacing (`.index`, `.fishwish`)
- **Dark mode**: Built-in dark mode support using Tailwind's `dark:` variants

### Game Architecture (Fishwish)
- **Daily puzzles**: JSON-based game data in `static/fishwish-games.json`
- **Timer system**: JavaScript timer with pause/resume functionality
- **Modal system**: Instruction modals with localStorage persistence
- **Responsive grid**: Adaptive card layout for different screen sizes

## Development Workflow

### Local Development
1. Run `npm run dev` to start CSS watching
2. Run `python main.py` to start the FastAPI server
3. Visit `http://localhost:8000` for the landing page
4. Visit `http://localhost:8000/fishwish` for the game

### Production Deployment
1. Run `npm run build-css-prod` to generate optimized assets
2. Build Docker image with multi-stage build (Node.js → Python)
3. Docker handles both CSS compilation and Python server setup

### File Modification Patterns
- **HTML changes**: Direct editing, build scripts handle CSS references
- **CSS changes**: Edit `src/index.css`, Tailwind compiles automatically
- **Game logic**: Edit JavaScript files in `static/`
- **New games**: Add route in `main.py` or create new module like `fishwish.py`

## Special Configuration

### Claude Code Integration
- `.claude/settings.local.json` contains permission settings
- Pre-approved commands for build processes and Node.js operations

### Docker Multi-Stage Build
- **Stage 1 (Node.js)**: Installs dependencies and builds CSS assets
- **Stage 2 (Python)**: Sets up FastAPI server and copies built assets
- Optimized for production deployment

## Project Context

This is a personal portfolio showcasing interactive games and projects. The main feature is "Fishwish," a word-puzzle game where users find rhyming pairs from definitions. The architecture emphasizes simplicity, fast loading times, and a clean development experience.

### Current Games/Projects
- **Fishwish**: Daily word puzzle game with rhyming pairs
- **Landing page**: Portfolio-style grid of projects (some marked as "coming soon")

### Notable Features
- Daily puzzle rotation system
- Timer functionality with pause/resume
- Responsive design with dark mode
- Cache-busting for optimal performance
- Clean, minimal UI with custom island-themed footer graphics
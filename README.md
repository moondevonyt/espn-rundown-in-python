# ESPN Rundown in Python

A terminal-based rundown tool that recreates ESPN's iconic "rundown" sidebar for coding streams. Keep yourself on track and let your audience know exactly what you're working on with real-time countdown timers and visual highlights.

## What This Recreates

ESPN's famous rundown display that shows:
- Current active segment highlighted in yellow
- Completed segments marked with checkmarks
- Upcoming segments listed in order
- Real-time countdown timers
- Clean, professional broadcast look

Perfect for coding streams where viewers want to know what's coming up next.

## Features

- **Live Countdown Timer**: Real-time MM:SS countdown for each project
- **Random Project Order**: Shuffles projects each session for variety
- **Project Search**: Override starting project with smart search
- **Dynamic Task Creation**: Add new tasks on-the-fly with unknown search terms
- **Auto-Loop**: Automatically reshuffles and continues when all projects complete
- **ESPN-Style Colors**: Yellow highlight for current project, clean layout
- **Flexible Input**: Single command handles both time and project selection

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
```bash
python main.py
```
Enter time and project in one input:
- `75 arb` - 75 minutes starting with Stat Arb Bots
- `90 search` - 90 minutes starting with Researching  
- `45` - 45 minutes, random order
- `backtesting` - 60 minutes (default) starting with Backtesting
- `60 build a computer` - 60 minutes starting with new task "build a computer"

### Command Line Arguments
```bash
python main.py 75 arb                # 75 minutes starting with Stat Arb
python main.py 90 search             # 90 minutes starting with Researching
python main.py 45                    # 45 minutes, random order
python main.py backtesting           # 60 minutes starting with Backtesting
python main.py 60 build a computer   # 60 minutes starting with new task
```

### Controls
- **Enter**: Advance to next project
- **r**: Restart current project timer
- **q**: Quit

## Projects

Current trading bot projects:
- Stat Arb Bots
- Polymarket Bots
- Hyperliquid Bots
- Solana Bots
- Backtesting
- Researching

Edit the `PROJECTS` list in `main.py` to customize your projects.

## Configuration

- **Default Time**: 60 minutes per project (change `DEFAULT_MINUTES` in main.py)
- **Project Search**: Partial matches work (e.g., "arb" finds "Stat Arb Bots")
- **New Tasks**: Unknown search terms become new tasks (e.g., "build a computer" creates new task)
- **Auto-Loop**: Automatically reshuffles when all projects complete

## Sound Configuration

To enable completion sounds when projects finish:

1. **Enable Sound**: Set `SOUND_ENABLED = True` in main.py
2. **Set Sound Path**: Update `SOUND_FILE_PATH` to your sound file location
3. **Supported Formats**: WAV files work best across all platforms

```python
# 🔊 Sound configuration
SOUND_ENABLED = True  # Set to True to enable sounds
SOUND_FILE_PATH = "/path/to/your/sound.wav"  # Path to your sound file
```

**Note**: You'll need to provide your own sound file. The rundown will work perfectly without sound if disabled.
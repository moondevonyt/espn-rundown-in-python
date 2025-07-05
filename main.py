#!/usr/bin/env python3
"""
🌙 Moon Dev's Epic Coding Rundown 🌙
CLI sidebar that behaves like ESPN's "rundown" but for coding streams!

• Shows randomized daily coding projects
• Countdown timers for each segment
• Override specific projects with search terms
• Gamified with colors and emojis for streaming

Usage: python main.py [minutes] [project_search_term]
Example: python main.py 75 arb    # 75 minutes starting with Stat Arb
"""

from termcolor import colored, cprint
import os
import time
import random
import threading
import sys
from datetime import datetime, timedelta
import re
import subprocess
import platform
import select

# 🚀 Moon Dev's Daily Coding Projects 🚀
PROJECTS = [
    "Stat Arb Bots",
    "Polymarket Bots", 
    "Hyperliquid Bots",
    "Solana Bots",
    "Backtesting",
    "Researching"
]

# ⏰ Default time per project (minutes)
DEFAULT_MINUTES = 60

# 🔊 Sound configuration
SOUND_ENABLED = False
SOUND_FILE_PATH = "/Users/md/Dropbox/dev/github/Untitled/sounds/yahoooo.wav"

class MoonDevRundown:
    def __init__(self, minutes_per_project=DEFAULT_MINUTES, starting_project=None):
        self.minutes_per_project = minutes_per_project
        self.projects = PROJECTS.copy()
        self.current_idx = 0
        self.start_time = None
        self.is_running = False
        self.timer_thread = None
        self.should_update = True
        self.last_time_remaining = None
        self.auto_advance_flag = False
        
        # Randomize project order
        random.shuffle(self.projects)
        
        # Handle starting project override
        if starting_project:
            self.override_starting_project(starting_project)
    
    def play_sound(self):
        """🔊 Play completion sound for Moon Dev"""
        if not SOUND_ENABLED:
            return
            
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["afplay", SOUND_FILE_PATH], check=False)
            elif platform.system() == "Windows":
                subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{SOUND_FILE_PATH}').PlaySync()"], check=False)
            else:  # Linux
                subprocess.run(["aplay", SOUND_FILE_PATH], check=False)
        except:
            pass  # Silently fail if sound can't play
    
    def override_starting_project(self, search_term):
        """🔍 Moon Dev's project search and override system"""
        search_term_lower = search_term.lower()
        
        # First, try to find a match in existing projects
        for i, project in enumerate(self.projects):
            if search_term_lower in project.lower():
                # Move match to the beginning
                self.projects.pop(i)
                self.projects.insert(0, project)
                print(f"🎯 Moon Dev found matching project: {project}! 🚀")
                return
        
        # If no match found, treat as new task
        print(f"🆕 Moon Dev adding new task: {search_term}! 🌟")
        self.projects.insert(0, search_term)
        
        # Randomize the remaining projects (excluding the new first one)
        remaining_projects = self.projects[1:]
        random.shuffle(remaining_projects)
        self.projects = [self.projects[0]] + remaining_projects
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
    
    def get_time_remaining(self):
        """⏱️ Calculate time remaining for current project"""
        if not self.start_time:
            return self.minutes_per_project * 60
        
        elapsed = time.time() - self.start_time
        remaining = (self.minutes_per_project * 60) - elapsed
        return max(0, remaining)
    
    def format_time(self, seconds):
        """🕒 Format seconds into MM:SS for Moon Dev"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def paint_rundown(self):
        """🎨 Moon Dev's colorful rundown display"""
        self.clear_screen()
        
        print("📈 TRADING BOT RUNDOWN")
        print()
        
        time_remaining = self.get_time_remaining()
        
        for i, project in enumerate(self.projects):
            if i == self.current_idx:  # 🔥 Currently working - yellow background, black text
                timer_display = self.format_time(time_remaining)
                line = colored(f"🔥 {project} [{timer_display}]", "black", "on_yellow", attrs=["bold"])
            elif i < self.current_idx:  # ✅ Completed
                line = colored(f"✅ {project}", "white", "on_grey", attrs=["bold"])
            else:  # 📅 Coming up
                line = colored(f"📅 {project}", "white")
            
            print(f"  {line}")
        
        print()
        
        if self.current_idx >= len(self.projects):
            print("🎊 Moon Dev completed all projects! Reshuffling for next round! 🎊")
    
    def update_display(self):
        """🔄 Continuously update the display"""
        while self.should_update:
            time_remaining = self.get_time_remaining()
            
            # Check if time just hit zero
            if (self.last_time_remaining is not None and 
                self.last_time_remaining > 0 and 
                time_remaining == 0):
                
                # Play sound and set flag for auto-advance
                self.play_sound()
                self.auto_advance_flag = True
                
            self.last_time_remaining = time_remaining
            self.paint_rundown()
            time.sleep(1)
    
    def start_project_timer(self):
        """🕐 Start timing the current project"""
        self.start_time = time.time()
        self.is_running = True
        self.last_time_remaining = None
        
        # Stop previous timer thread if running
        if self.timer_thread and self.timer_thread.is_alive():
            self.should_update = False
            self.timer_thread.join()
        
        # Start new timer thread
        self.should_update = True
        self.timer_thread = threading.Thread(target=self.update_display, daemon=True)
        self.timer_thread.start()
    
    def advance_project(self):
        """➡️ Move to next project"""
        if self.current_idx < len(self.projects) - 1:
            self.current_idx += 1
            self.start_project_timer()
        else:
            # Loop back - reshuffle and start over
            print("🔄 Moon Dev completed all projects! Reshuffling for next round! 🎲")
            random.shuffle(self.projects)
            self.current_idx = 0
            self.start_project_timer()
    
    def restart_timer(self):
        """🔄 Restart current project timer"""
        self.start_project_timer()
    
    def get_input_with_timeout(self, prompt, timeout=0.1):
        """Get input with timeout to allow checking auto-advance flag"""
        if platform.system() == "Windows":
            # Windows doesn't support select, so we'll use a simpler approach
            import msvcrt
            print(prompt, end='', flush=True)
            
            while True:
                if self.auto_advance_flag:
                    return "auto_advance"
                
                if msvcrt.kbhit():
                    line = input()
                    return line
                
                time.sleep(0.1)
        else:
            # Unix-like systems (macOS, Linux)
            print(prompt, end='', flush=True)
            
            while True:
                if self.auto_advance_flag:
                    return "auto_advance"
                
                # Check if input is available
                if select.select([sys.stdin], [], [], timeout)[0]:
                    line = sys.stdin.readline().strip()
                    return line
                
                time.sleep(0.1)
    
    def run(self):
        """🏃 Main Moon Dev rundown loop"""
        # Start first project timer
        self.start_project_timer()
        
        while True:
            try:
                choice = self.get_input_with_timeout("\n🌙 Moon Dev command: ")
                
                if choice == "auto_advance":
                    self.auto_advance_flag = False
                    self.advance_project()
                elif choice == "q":
                    break
                elif choice == "r":
                    self.restart_timer()
                elif choice == "":
                    if self.get_time_remaining() <= 0:
                        print("⏰ Time's up! Moon Dev moving to next project! 🎯")
                    self.advance_project()
                    
            except KeyboardInterrupt:
                break
        
        # Stop timer and final display
        self.should_update = False
        self.paint_rundown()
        cprint("\n🎉 Moon Dev's coding session complete! Epic work! 🌟", "white", "on_magenta", attrs=["bold"])

def parse_single_input(user_input):
    """📝 Parse single input for both time and project search"""
    if not user_input.strip():
        return DEFAULT_MINUTES, None
    
    # Split input into words
    parts = user_input.strip().split()
    minutes = DEFAULT_MINUTES
    project_search = None
    
    # Look for numbers (time) and words (project search)
    numbers = []
    words = []
    
    for part in parts:
        if part.isdigit():
            numbers.append(int(part))
        else:
            words.append(part)
    
    # Use first number as minutes
    if numbers:
        minutes = numbers[0]
    
    # Use all words as project search (joined together)
    if words:
        project_search = " ".join(words)
    
    return minutes, project_search

def get_interactive_input():
    """💬 Single input for Moon Dev's preferences"""
    print("🌙" + "="*60 + "🌙")
    print("    🚀 Welcome to Moon Dev's Epic Coding Rundown! 🚀")
    print("🌙" + "="*60 + "🌙")
    print()
    
    user_input = input("⏰ Enter minutes and/or project (e.g. '75 arb' or '90' or 'search'): ").strip()
    
    try:
        minutes, project_search = parse_single_input(user_input)
        return minutes, project_search
    except:
        return DEFAULT_MINUTES, None

def main():
    """🌙 Moon Dev's main entry point"""
    # Parse command line args or get interactive input
    if len(sys.argv) > 1:
        # Join all command line args and parse as single input
        user_input = " ".join(sys.argv[1:])
        try:
            minutes, project_search = parse_single_input(user_input)
        except:
            minutes, project_search = DEFAULT_MINUTES, None
    else:
        minutes, project_search = get_interactive_input()
    
    # Create and run the rundown
    rundown = MoonDevRundown(minutes, project_search)
    rundown.run()

if __name__ == "__main__":
    main()

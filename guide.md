# Tournament System Guide

## Overview
This tournament system uses a bracket-based structure with qualifiers to determine player placement and progression through different difficulty levels.

## Qualifiers Instructions
Qualifying rounds are used to place players into their respective brackets.

### Qualification Process
1. **Map Selection**: Choose one map from each bracket that each player will attempt. 
2. **Progression System**: If the player passes or maintains a specified accuracy throughout the play, they can move on to the next map for the next bracket. Each player does this until they reach a map that they cannot pass.
3. **Bracket Assignment**: The players will be organized into the respective brackets. If there are an odd number of players in a bracket and it is possible to be fixed by moving other players, the player with the highest score will be moved to the next bracket, and vice versa.

## Bracket Structure

### Difficulty Brackets
The tournament features six progressive difficulty brackets:

1. **Normal** - Entry-level bracket for beginners
2. **Hard** - Intermediate difficulty
3. **Insane** - Advanced difficulty
4. **Expert** - High-level play
5. **Expert+** - Very high difficulty
6. **Expert++** - Maximum difficulty

### Bracket Characteristics
- Each bracket contains specific beatmaps tailored to the difficulty level
- Players are placed based on their qualification performance
- Brackets ensure balanced competition among similarly-skilled players

## Tournament Phases

### Phase 1: Qualifiers
- Players attempt maps from each bracket
- Performance determines initial placement
- Progressive difficulty testing

### Phase 2: Bracket Play
- Players compete within their assigned brackets
- Head-to-head matches using bracket-specific maps
- Elimination or point-based advancement

### Phase 3: Finals
- Top players from each bracket may advance
- Cross-bracket competition possible
- Championship matches

## Match Format

### Standard Matches
- **Best of 7**: First to 4 map wins
- **Map Pool**: 7 maps selected per match
- **Tiebreaker**: Final map if score is 3-3

### Scoring System
- **Accuracy**: Primary scoring metric
- **Combo**: Secondary factor for tie-breaking
- **Mod Multipliers**: Applied based on selected mods

### Live Match Features
- Real-time score updates
- Current map display
- Player statistics
- Match status indicators

## Tournament Data Management

### JSON Structure
The tournament uses two main JSON files:

#### beatmaps.json
- Contains all tournament beatmaps
- Organized by bracket difficulty
- Auto-sorted by bracket level
- Used by website for beatmap display

#### tournament-data.json
- Tournament metadata (name, dates, status)
- Player information and rankings
- Bracket matchups and results
- Live match data
- Recent match history

### Data Updates
- **Auto-refresh**: Website updates every 30 seconds
- **Real-time**: Live scores update immediately
- **Persistent**: All data saved in JSON format

## Website Features

### Navigation Tabs
- **Home**: Tournament overview and announcements
- **Brackets**: Visual bracket display and match results
- **Live Scores**: Real-time match updates and current games
- **Rules**: Tournament regulations and guidelines
- **Beatmap List**: Searchable and filterable beatmap database

### Beatmap Explorer
- **Search**: Find maps by title or artist
- **Filter**: Filter by bracket difficulty
- **Sort**: Sort by title, artist, bracket, difficulty, or length
- **Visual Pills**: Color-coded bracket indicators

### Tournament Display
- **Bracket Visualization**: Interactive tournament tree
- **Live Match Cards**: Real-time match information
- **Recent Results**: Historical match outcomes
- **Player Statistics**: Individual performance data

## Management Tools

### main.py Features
- **Beatmap Management**: Add/remove beatmaps from JSON
- **Score Calculator**: Calculate tournament scores with mods
- **JSON Tools**: Load, save, and manage tournament data
- **Auto-sorting**: Automatic bracket organization

### Score Calculation
- **Base Formula**: Accuracy and combo-based scoring
- **Mod Multipliers**: EZ (0.50x), HR (1.12x), HD (1.05x), FL (1.10x)
- **Dual Display**: Original score + scaled score (1'000'000 max)
- **Formatted Output**: Apostrophe separators for readability

## Technical Implementation

### File Structure
```
/
├── index.html          # Main tournament website
├── beatmaps.json       # Beatmap database
├── tournament-data.json # Tournament information
├── main.py            # Management tool
└── guide.md           # This documentation
```

### Data Flow
1. **main.py** → Updates JSON files
2. **JSON files** → Data storage
3. **index.html** → Reads JSON and displays data
4. **Website** → Auto-refreshes for live updates

### Hosting Requirements
- **GitHub Pages**: Static hosting compatible
- **JSON Support**: CORS-enabled for file loading
- **Auto-refresh**: JavaScript-based updates
- **Responsive Design**: Works on all screen sizes

## Best Practices

### Tournament Organization
- **Test Qualifiers**: Ensure balanced bracket placement
- **Map Selection**: Choose appropriate difficulty progression
- **Schedule Management**: Plan match timing and availability
- **Player Communication**: Clear rules and expectations

### Data Management
- **Regular Backups**: Save JSON file copies
- **Validation**: Check data integrity before updates
- **Version Control**: Track changes with git
- **Testing**: Verify website updates after changes

### Website Maintenance
- **Update Frequency**: Regular tournament data refreshes
- **Performance**: Monitor auto-refresh functionality
- **User Experience**: Ensure smooth navigation
- **Mobile Support**: Test on various devices
#
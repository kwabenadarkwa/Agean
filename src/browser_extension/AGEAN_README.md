# Agean - YouTube Code Extractor

A powerful browser extension that extracts code content from YouTube programming tutorials using advanced computer vision and machine learning techniques.

## Features

### 🎯 Core Functionality
- **YouTube Integration**: Automatically detects YouTube programming videos
- **Code Extraction**: Uses AI to extract code from video frames
- **Smart Processing**: Configurable FPS, duplicate removal, and processing levels
- **Real-time Detection**: Monitors video changes and navigation
- **Caching System**: Stores extraction results for quick access

### 🎨 User Interface
- **Dark Theme**: Modern, developer-friendly interface
- **Side Panel**: Non-intrusive sidebar integration
- **Video Info Display**: Shows current video metadata with thumbnails
- **Configuration Panel**: Adjustable extraction parameters
- **Code Display**: Syntax-highlighted output with copy/download options
- **Status Indicators**: Real-time feedback and progress tracking

### ⚙️ Configuration Options
- **Frame Extraction FPS**: 1-5 frames per second
- **Duplicate Removal Threshold**: 0.1-1.0 similarity filtering
- **Processing Level**: 1-4 quality levels
- **API Settings**: Configurable endpoint and timeout

## Architecture

### Extension Structure
```
├── chrome-extension/          # Manifest and build config
├── pages/
│   ├── side-panel/           # Main UI (Agean interface)
│   └── content/              # YouTube integration scripts
├── packages/
│   ├── shared/               # Services, hooks, utilities
│   ├── storage/              # Configuration and caching
│   └── ui/                   # Agean-specific components
```

### Key Components

#### Content Script (`pages/content/src/matches/youtube/`)
- **YouTubeVideoDetector**: Monitors video changes and extracts metadata
- **DOM Observers**: Handles YouTube's SPA navigation
- **Message Passing**: Communicates with side panel

#### API Service (`packages/shared/lib/services/`)
- **ExtractCodeService**: Handles API communication
- **Error Handling**: Robust retry and timeout logic
- **Health Checks**: API availability monitoring

#### Storage System (`packages/storage/lib/impl/`)
- **AgeanConfigStorage**: User preferences and settings
- **VideoCacheStorage**: Extraction results caching
- **Automatic Cleanup**: Manages storage limits

#### UI Components (`packages/ui/lib/components/agean/`)
- **VideoInfoCard**: Video metadata display
- **ConfigurationPanel**: Settings controls
- **ExtractButton**: Primary action with loading states
- **CodeDisplay**: Formatted code output
- **StatusIndicator**: Real-time status feedback

## API Integration

### Request Format
```json
{
  "video_url": "https://www.youtube.com/watch?v=...",
  "title": "Video Title",
  "duration": "15:42",
  "frame_extraction_fps": 1,
  "duplicate_removal_threshold": 0.8,
  "level": 1
}
```

### Response Format
```json
{
  "success": true,
  "code_content": "extracted Python code...",
  "metadata": {
    "frames_processed": 156,
    "code_blocks_found": 3,
    "processing_time": 12500
  }
}
```

## Development

### Prerequisites
- Node.js 22.15.1+
- pnpm 10.11.0+
- Python API server running on localhost:8000

### Setup
```bash
# Install dependencies
pnpm install

# Start development mode
pnpm dev

# Build for production
pnpm build

# Run tests
pnpm e2e
```

### Development Features
- **Hot Reload**: Automatic extension reloading
- **TypeScript**: Full type safety
- **ESLint/Prettier**: Code formatting and linting
- **Tailwind CSS**: Utility-first styling
- **Mock Data**: Development testing utilities

## Usage

### Installation
1. Build the extension: `pnpm build`
2. Load unpacked extension from `dist/` folder
3. Navigate to any YouTube programming video
4. Click the extension icon or use the side panel

### Extraction Process
1. **Video Detection**: Extension automatically detects YouTube videos
2. **Configuration**: Adjust FPS, threshold, and level settings
3. **Extraction**: Click "Extract Code" to process the video
4. **Results**: View, copy, or download the extracted code

### Configuration Guide
- **FPS (1-5)**: Higher values capture more frames but take longer
- **Threshold (0.1-1.0)**: Higher values remove more duplicate frames
- **Level (1-4)**: Processing quality from basic to maximum

## Error Handling

### Common Issues
- **API Connection**: Check if Python server is running
- **No Video Detected**: Ensure you're on a YouTube video page
- **Extraction Timeout**: Reduce FPS or try a shorter video
- **No Code Found**: Video may not contain extractable code

### Troubleshooting
- Check browser console for detailed error messages
- Verify API server is accessible at configured URL
- Ensure YouTube page has fully loaded before extraction
- Try refreshing the page if video detection fails

## Security & Privacy

### Permissions
- **YouTube Access**: Only `*://www.youtube.com/*`
- **Storage**: Local configuration and caching
- **Active Tab**: Current video detection
- **API Communication**: Configurable endpoints only

### Data Handling
- **No Personal Data**: Only video URLs and extracted code
- **Local Storage**: All data stored locally in browser
- **Cache Management**: Automatic cleanup of old results
- **Secure Communication**: HTTPS API endpoints in production

## Contributing

### Code Style
- Follow existing TypeScript/React patterns
- Use Tailwind CSS for styling
- Implement proper error boundaries
- Add comprehensive type definitions
- Write descriptive commit messages

### Testing
- Test on various YouTube video types
- Verify API integration with different responses
- Check error handling edge cases
- Validate UI responsiveness

## License

MIT License - see LICENSE file for details.

## Support

For issues, feature requests, or contributions, please visit the project repository.
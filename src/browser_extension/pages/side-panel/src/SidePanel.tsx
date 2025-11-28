import '@src/SidePanel.css';
import { useState, useCallback } from 'react';
import { useYouTubeVideo, useCodeExtraction } from '@extension/shared';
import { sanitizeTitle } from '@extension/shared';
import { ageanConfigStorage } from '@extension/storage';
import type { ExtractCodeRequest } from '@extension/shared';

const SidePanel = () => {
  const { videoData, isLoading: videoLoading, error: videoError } = useYouTubeVideo();
  const { isExtracting, extractedCode, extractionError, extractCode } = useCodeExtraction();
  const [config, setConfig] = useState<{
    fps: number;
    level: number;
  }>({
    fps: 1,
    level: 1,
  });
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [copiedAll, setCopiedAll] = useState(false);

  const copyToClipboard = useCallback(async (text: string, index?: number) => {
    try {
      await navigator.clipboard.writeText(text);

      if (index !== undefined) {
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
      } else {
        setCopiedAll(true);
        setTimeout(() => setCopiedAll(false), 2000);
      }
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
      // Fallback for older browsers or when clipboard API is not available
      try {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        textArea.remove();

        if (index !== undefined) {
          setCopiedIndex(index);
          setTimeout(() => setCopiedIndex(null), 2000);
        } else {
          setCopiedAll(true);
          setTimeout(() => setCopiedAll(false), 2000);
        }
      } catch (fallbackError) {
        console.error('Fallback copy failed:', fallbackError);
      }
    }
  }, []);

  const copyAllCode = useCallback(() => {
    const allCode = extractedCode.join('\n\n// ========== Next Code Block ==========\n\n');
    copyToClipboard(allCode);
  }, [extractedCode, copyToClipboard]);

  const handleExtract = useCallback(async () => {
    if (!videoData) return;

    const request: ExtractCodeRequest = {
      videoId: videoData.videoId,
      title: sanitizeTitle(videoData.title),
      duration: videoData.duration,
      fps: config.fps,
      threshold: 0.8, // Fixed value
      level: config.level === 1 ? 'beginner' : config.level === 2 ? 'intermediate' : 'advanced',
    };

    await extractCode(request);
  }, [videoData, config, extractCode]);

  if (videoLoading) {
    return (
      <div className="agean-container">
        <div className="animate-pulse">
          <div className="mb-4 h-4 rounded bg-gray-600"></div>
          <div className="mb-2 h-4 rounded bg-gray-600"></div>
          <div className="h-4 rounded bg-gray-600"></div>
        </div>
      </div>
    );
  }

  if (videoError) {
    return (
      <div className="agean-container">
        <div className="agean-card border-yellow-600 bg-yellow-900/20">
          <h3 className="font-medium text-yellow-300">Notice</h3>
          <p className="mt-1 text-sm text-yellow-200">{videoError}</p>
        </div>
      </div>
    );
  }

  if (!videoData) {
    return (
      <div className="agean-container">
        {/* Header */}
        <div className="agean-header">
          <div className="agean-app-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <div>
            <h1 className="agean-title">Agean</h1>
            <p className="agean-subtitle">YouTube Code Extractor</p>
          </div>
        </div>

        <div className="agean-card border-gray-600 bg-gray-800/50">
          <h3 className="font-medium text-gray-300">No Video Detected</h3>
          <p className="mt-1 text-sm text-gray-400">Please navigate to a YouTube video page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="agean-container">
      {/* Header */}
      <div className="agean-header">
        <div className="agean-app-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div>
          <h1 className="agean-title">Agean</h1>
          <p className="agean-subtitle">YouTube Code Extractor</p>
        </div>
      </div>

      {/* Status Card */}
      <div className="agean-status-card">
        <div className="agean-status-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div>
          <div className="agean-status-text">YouTube video detected</div>
          <div className="agean-status-subtext">Ready to extract code content</div>
        </div>
      </div>

      {/* Video Information Card */}
      <div className="agean-card">
        <div className="agean-video-card">
          <div className="agean-thumbnail-container">
            <img
              src={videoData.thumbnail || `https://img.youtube.com/vi/${videoData.videoId}/maxresdefault.jpg`}
              alt="Video thumbnail"
              className="agean-thumbnail"
              onError={e => {
                const img = e.target as HTMLImageElement;
                // Try different thumbnail sizes in order of preference
                if (img.src.includes('maxresdefault.jpg')) {
                  img.src = `https://img.youtube.com/vi/${videoData.videoId}/hqdefault.jpg`;
                } else if (img.src.includes('hqdefault.jpg')) {
                  img.src = `https://img.youtube.com/vi/${videoData.videoId}/mqdefault.jpg`;
                } else if (img.src.includes('mqdefault.jpg')) {
                  img.src = `https://img.youtube.com/vi/${videoData.videoId}/default.jpg`;
                } else {
                  // All thumbnail attempts failed, show fallback icon
                  img.style.display = 'none';
                  const fallback = img.nextElementSibling as HTMLElement;
                  if (fallback) fallback.style.display = 'flex';
                }
              }}
            />
            <div className="agean-code-preview" style={{ display: 'none' }}>
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
          </div>
          <div className="agean-video-info">
            <div className="agean-video-indicator">
              <div className="agean-green-dot"></div>
              <span className="agean-detected-text">Video Detected</span>
            </div>
            <div className="agean-video-title">{videoData.title || '5 Unintuitive Python Features'}</div>
            <div className="agean-video-meta">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
                <polyline
                  points="12,6 12,12 16,14"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span>{videoData.duration || '00:00'}</span>
            </div>
            <div className="agean-video-url">youtube.com/watch?v={videoData.videoId}</div>
          </div>
        </div>
      </div>

      {/* Configuration Section */}
      <div className="agean-card">
        <div className="agean-config-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2" />
            <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1" stroke="currentColor" strokeWidth="2" />
          </svg>
          <span>Configuration</span>
        </div>

        <div className="space-y-6">
          {/* Frame Extraction FPS */}
          <div>
            <div className="agean-config-label">Frame Extraction FPS: {config.fps}</div>
            <div className="agean-slider-container">
              <input
                type="range"
                min="1"
                max="5"
                step="1"
                value={config.fps}
                onChange={e => setConfig(prev => ({ ...prev, fps: parseInt(e.target.value) }))}
                className="agean-slider"
              />
              <div className="agean-slider-labels">
                <span>1</span>
                <span>5</span>
              </div>
            </div>
            <div className="agean-help-text">Lower FPS captures more frames but takes longer to process</div>
          </div>

          {/* Processing Level */}
          <div>
            <div className="agean-config-label">Processing Level</div>
            <div className="agean-level-buttons">
              {[1, 2, 3, 4].map(level => (
                <button
                  key={level}
                  onClick={() => setConfig(prev => ({ ...prev, level }))}
                  className={`agean-level-button ${config.level === level ? 'active' : ''}`}>
                  {level}
                </button>
              ))}
            </div>
            <div className="agean-help-text">Level 1: Basic extraction</div>
          </div>
        </div>
      </div>

      {/* Extract Button */}
      <button onClick={handleExtract} disabled={isExtracting} className="agean-extract-button">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4m4-5l5 5 5-5m-5 5V3"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        {isExtracting ? 'Extracting Code...' : 'Extract Code'}
      </button>

      {/* Results */}
      {extractionError && (
        <div className="agean-card border-red-600 bg-red-900/20">
          <h4 className="font-medium text-red-300">Extraction Error</h4>
          <p className="mt-1 text-sm text-red-200">{extractionError}</p>
        </div>
      )}

      {extractedCode.length > 0 && (
        <div className="agean-card">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="font-semibold text-white">Extracted Code</h3>
            <button onClick={copyAllCode} className={`agean-copy-all-button ${copiedAll ? 'copied' : ''}`}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                {copiedAll ? (
                  <path
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                ) : (
                  <path
                    d="M8 4v12a2 2 0 002 2h8a2 2 0 002-2V7.242a2 2 0 00-.602-1.43L16.83 2.83A2 2 0 0015.415 2H10a2 2 0 00-2 2z"
                    stroke="currentColor"
                    strokeWidth="2"
                    fill="none"
                  />
                )}
              </svg>
              {copiedAll ? 'Copied!' : 'Copy All'}
            </button>
          </div>
          <div className="space-y-3">
            {extractedCode.map((code, index) => (
              <div key={index} className="agean-code-block">
                <button
                  onClick={() => copyToClipboard(code, index)}
                  className={`agean-copy-button ${copiedIndex === index ? 'copied' : ''}`}
                  title={copiedIndex === index ? 'Copied!' : 'Copy code block'}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    {copiedIndex === index ? (
                      <path
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    ) : (
                      <path
                        d="M8 4v12a2 2 0 002 2h8a2 2 0 002-2V7.242a2 2 0 00-.602-1.43L16.83 2.83A2 2 0 0015.415 2H10a2 2 0 00-2 2z"
                        stroke="currentColor"
                        strokeWidth="2"
                        fill="none"
                      />
                    )}
                  </svg>
                </button>
                <pre className="whitespace-pre-wrap font-mono text-sm text-gray-200" style={{ paddingRight: '48px' }}>
                  {code}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SidePanel;

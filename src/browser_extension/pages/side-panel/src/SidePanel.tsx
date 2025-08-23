import '@src/SidePanel.css';
import { useCallback, useMemo } from 'react';
import { useStorage, useYouTubeVideo, useCodeExtraction, withErrorBoundary, withSuspense } from '@extension/shared';
import { sanitizeTitle } from '@extension/shared';
import { ageanConfigStorage } from '@extension/storage';
import {
  ErrorDisplay,
  LoadingSpinner,
  VideoInfoCard,
  ConfigurationPanel,
  ExtractButton,
  CodeDisplay,
  StatusIndicator,
} from '@extension/ui';
import type { StatusType } from '@extension/ui';
import type { ExtractCodeRequest } from '@extension/shared';

const SidePanel = () => {
  const config = useStorage(ageanConfigStorage);
  const { videoData, isLoading: videoLoading, error: videoError, refreshVideo } = useYouTubeVideo();
  const { isExtracting, extractionResult, error: extractionError, extractCode, clearResult } = useCodeExtraction();

  // Determine current status
  const status = useMemo(() => {
    if (videoLoading) {
      return {
        type: 'loading' as StatusType,
        message: 'Checking for YouTube video...',
        details: undefined,
      };
    }

    if (videoError) {
      return {
        type: 'warning' as StatusType,
        message: videoError,
        details:
          videoError === 'Not on YouTube'
            ? 'Please navigate to a YouTube video page'
            : videoError === 'Please refresh the page to use Agean'
              ? 'Refresh this YouTube page and reopen the extension'
              : undefined,
      };
    }

    if (extractionError) {
      return {
        type: 'error' as StatusType,
        message: 'Extraction failed',
        details: extractionError,
      };
    }

    if (isExtracting) {
      return {
        type: 'loading' as StatusType,
        message: 'Extracting code from video...',
        details: 'This may take a few minutes depending on video length',
      };
    }

    if (extractionResult?.status === 'success') {
      return {
        type: 'success' as StatusType,
        message: 'Code extraction completed',
        details: `Found ${extractionResult.metadata?.code_blocks_found || 'unknown'} code blocks`,
      };
    }

    if (videoData?.isValid) {
      return {
        type: 'success' as StatusType,
        message: 'YouTube video detected',
        details: 'Ready to extract code content',
      };
    }

    return {
      type: 'warning' as StatusType,
      message: 'No YouTube video detected',
      details: 'Navigate to a YouTube video page to begin',
    };
  }, [videoLoading, videoError, extractionError, isExtracting, extractionResult, videoData]);

  const handleExtractCode = useCallback(async () => {
    if (!videoData?.isValid) return;

    clearResult();

    const request: ExtractCodeRequest = {
      video_url: videoData.url,
      title: sanitizeTitle(videoData.title),
      duration: videoData.duration,
      frame_extraction_fps: config.frameExtractionFps,
      duplicate_removal_threshold: config.duplicateRemovalThreshold,
      level: config.level,
    };

    await extractCode(request);
  }, [videoData, config, extractCode, clearResult]);

  const handleConfigChange = useCallback(async (key: string, value: number) => {
    switch (key) {
      case 'fps':
        await ageanConfigStorage.setFps(value);
        break;
      case 'threshold':
        await ageanConfigStorage.setThreshold(value);
        break;
      case 'level':
        await ageanConfigStorage.setLevel(value);
        break;
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <div className="sticky top-0 z-10 border-b border-gray-800 bg-gray-900/95 backdrop-blur-sm">
        <div className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
              <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h4a1 1 0 110 2H4a1 1 0 01-1-1zm8-8a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1zm1 4a1 1 0 100 2h4a1 1 0 100-2h-4z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">Agean</h1>
              <p className="text-xs text-gray-400">YouTube Code Extractor</p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-4 p-4">
        {/* Status */}
        <StatusIndicator
          status={status.type}
          message={status.message}
          details={status.details}
          showRefreshButton={videoError === 'Please refresh the page to use Agean'}
          onRefresh={() => {
            chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
              if (tabs[0]?.id) {
                chrome.tabs.reload(tabs[0].id);
              }
            });
          }}
        />

        {/* Video Info */}
        {videoData && (
          <VideoInfoCard
            title={videoData.title}
            duration={videoData.duration}
            url={videoData.url}
            isValid={videoData.isValid}
          />
        )}

        {/* Configuration */}
        <ConfigurationPanel
          fps={config.frameExtractionFps}
          threshold={config.duplicateRemovalThreshold}
          level={config.level}
          onFpsChange={fps => handleConfigChange('fps', fps)}
          onThresholdChange={threshold => handleConfigChange('threshold', threshold)}
          onLevelChange={level => handleConfigChange('level', level)}
          disabled={isExtracting}
        />

        {/* Extract Button */}
        <ExtractButton onClick={handleExtractCode} loading={isExtracting} disabled={!videoData?.isValid} />

        {/* Results */}
        {extractionResult?.result && (
          <CodeDisplay
            code={extractionResult.result}
            metadata={
              extractionResult.metadata
                ? {
                    frames_processed: extractionResult.metadata.frames_processed || 0,
                    code_blocks_found: extractionResult.metadata.code_blocks_found || 0,
                    processing_time: extractionResult.metadata.processing_time || 0,
                  }
                : undefined
            }
          />
        )}
      </div>
    </div>
  );
};

export default withErrorBoundary(withSuspense(SidePanel, <LoadingSpinner />), ErrorDisplay);

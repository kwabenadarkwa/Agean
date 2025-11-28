import { colorfulLogger } from '@extension/shared';

interface VideoData {
  url: string;
  title: string;
  duration: string;
  isValid: boolean;
}

interface YouTubeOEmbedResponse {
  title: string;
  author_name: string;
  author_url: string;
  type: string;
  height: number;
  width: number;
  version: string;
  provider_name: string;
  provider_url: string;
  thumbnail_height: number;
  thumbnail_width: number;
  thumbnail_url: string;
  html: string;
}

const AD_INDICATORS = [
  '.ytp-ad-player-overlay',
  '.ytp-ad-skip-button',
  '.ytp-ad-skip-button-modern',
  '.ytp-ad-text',
  '.ytp-ad-preview-text',
  '.ad-showing',
  '[class*="ad-showing"]',
  '.video-ads',
  '.ytp-ad-module',
  '.ytp-ad-image-overlay',
  '.ytp-ad-overlay-container',
  '.ytp-ad-progress',
  '.ytp-ad-persistent-progress-bar',
];

const DURATION_SELECTORS = [
  '.ytp-time-duration',
  '.ytd-thumbnail-overlay-time-status-renderer .badge-style-type-simple',
  '.ytd-thumbnail-overlay-time-status-renderer',
  '.style-scope.ytd-thumbnail-overlay-time-status-renderer',
  '[aria-label*="Duration"]',
];

class YouTubeVideoDetector {
  private logger = colorfulLogger.create('YouTube Detector');
  private currentVideoData: VideoData | null = null;
  private detectionTimeout: NodeJS.Timeout | null = null;
  private lastDetectionTime: number = 0;
  private videoDataCache: Map<string, VideoData> = new Map();
  private adCompletionWatcher: NodeJS.Timeout | null = null;
  private isWaitingForAdCompletion: boolean = false;

  constructor() {
    this.init();
  }

  private init(): void {
    this.setupUrlWatcher();
    // Try immediate detection first, then fallback to delayed detection
    this.performDetection().catch(() => this.detectCurrentVideo());
    this.setupMessageListener();
  }

  private setupUrlWatcher(): void {
    let lastUrl = window.location.href;

    const checkUrlChange = () => {
      const currentUrl = window.location.href;
      if (currentUrl !== lastUrl) {
        lastUrl = currentUrl;
        this.detectCurrentVideo();
      }
    };

    // Reduce URL check interval from 5000ms to 1000ms for faster navigation detection
    setInterval(checkUrlChange, 1000);
    window.addEventListener('yt-navigate-finish', this.detectCurrentVideo.bind(this), { passive: true });
  }

  private isYouTubeVideoPage(): boolean {
    return (
      window.location.hostname === 'www.youtube.com' &&
      window.location.pathname === '/watch' &&
      window.location.search.includes('v=')
    );
  }

  private getVideoId(): string | null {
    return new URLSearchParams(window.location.search).get('v');
  }

  private async fetchVideoDataFromYouTubeAPI(videoId: string): Promise<{ title: string; duration: string } | null> {
    try {
      const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      const response = await fetch(oembedUrl, {
        signal: controller.signal,
        mode: 'cors',
        cache: 'force-cache',
      });

      clearTimeout(timeoutId);

      if (!response.ok) return null;

      const data: YouTubeOEmbedResponse = await response.json();
      const duration = await this.getVideoDurationWithRetry();

      return {
        title: data.title || 'Unknown Title',
        duration: duration || 'Unknown Duration',
      };
    } catch (error) {
      const docTitle = document.title;
      const fallbackTitle = docTitle && docTitle !== 'YouTube' ? docTitle.replace(' - YouTube', '') : 'Unknown Title';
      const fallbackDuration = this.getVideoDurationFromPlayer() || 'Unknown Duration';

      return {
        title: fallbackTitle,
        duration: fallbackDuration,
      };
    }
  }

  private getVideoDurationFromPlayer(): string | null {
    try {
      if (this.isAdPlaying()) {
        if (!this.isWaitingForAdCompletion) {
          this.startWatchingForAdCompletion();
        }
        return null;
      }

      return this.getDurationFromPageData() || this.getDurationFromUI() || this.getDurationFromVideoElement();
    } catch (error) {
      this.logger.warn('Failed to get duration from player:', error);
      return null;
    }
  }

  private getDurationFromPageData(): string | null {
    try {
      const ytInitialPlayerResponse = (window as any).ytInitialPlayerResponse;
      if (ytInitialPlayerResponse?.videoDetails?.lengthSeconds) {
        const seconds = parseInt(ytInitialPlayerResponse.videoDetails.lengthSeconds);
        if (!isNaN(seconds) && seconds > 0) {
          return this.formatDuration(seconds);
        }
      }

      const ytInitialData = (window as any).ytInitialData;
      const contents = ytInitialData?.contents?.twoColumnWatchNextResults?.results?.results?.contents;

      if (contents && Array.isArray(contents)) {
        for (const content of contents) {
          const videoInfo = content?.videoPrimaryInfoRenderer;
          if (videoInfo?.lengthText?.simpleText) {
            return videoInfo.lengthText.simpleText;
          }
          if (videoInfo?.lengthText?.runs?.[0]?.text) {
            return videoInfo.lengthText.runs[0].text;
          }
        }
      }

      return null;
    } catch (error) {
      return null;
    }
  }

  private getDurationFromUI(): string | null {
    try {
      for (const selector of DURATION_SELECTORS) {
        const element = document.querySelector(selector);
        if (element) {
          const duration = element.textContent?.trim();
          if (duration && this.isValidDuration(duration)) {
            const seconds = this.parseDurationToSeconds(duration);
            if (seconds > 10) return duration;
          }
        }
      }
      return null;
    } catch (error) {
      return null;
    }
  }

  private getDurationFromVideoElement(): string | null {
    try {
      if (this.isAdPlaying()) return null;

      const videoElement = document.querySelector('video') as HTMLVideoElement;
      if (videoElement?.duration && !isNaN(videoElement.duration) && videoElement.duration > 10) {
        return this.formatDuration(videoElement.duration);
      }
      return null;
    } catch (error) {
      return null;
    }
  }

  private isAdPlaying(): boolean {
    try {
      for (const selector of AD_INDICATORS) {
        const element = document.querySelector(selector);
        if (element && this.isElementVisible(element)) {
          return true;
        }
      }

      const playerContainer = document.querySelector('#movie_player, .html5-video-player');
      if (
        playerContainer?.classList.contains('ad-showing') ||
        playerContainer?.classList.contains('ad-interrupting') ||
        playerContainer?.classList.contains('ytp-ad-showing')
      ) {
        return true;
      }

      const displayedDuration = this.getDurationFromUI();
      if (displayedDuration) {
        const seconds = this.parseDurationToSeconds(displayedDuration);
        if (seconds > 0 && seconds < 90 && !this.isLegitimateShortContent()) {
          return true;
        }
      }

      return false;
    } catch (error) {
      return false;
    }
  }

  private isElementVisible(element: Element): boolean {
    return (
      element instanceof HTMLElement &&
      element.offsetWidth > 0 &&
      element.offsetHeight > 0 &&
      getComputedStyle(element).display !== 'none'
    );
  }

  private isLegitimateShortContent(): boolean {
    const title = document.title;
    return !!(
      title &&
      (title.toLowerCase().includes('#shorts') ||
        title.toLowerCase().includes('youtube shorts') ||
        window.location.search.includes('&t='))
    );
  }

  private isValidDuration(duration: string): boolean {
    return duration.includes(':') && /^\d+:\d{2}(:\d{2})?$/.test(duration);
  }

  private async getVideoDurationWithRetry(maxRetries: number = 3, delayMs: number = 1000): Promise<string | null> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      const duration = this.getVideoDurationFromPlayer();
      if (duration && duration !== 'Unknown Duration') {
        return duration;
      }

      if (this.isWaitingForAdCompletion) {
        delayMs = Math.max(delayMs, 5000);
      }

      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
        delayMs = this.isWaitingForAdCompletion ? Math.min(delayMs * 1.5, 15000) : Math.min(delayMs * 1.2, 10000);
      }
    }

    return this.isWaitingForAdCompletion ? 'Waiting for ad completion' : null;
  }

  private formatDuration(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }

  private parseDurationToSeconds(duration: string): number {
    try {
      const parts = duration.split(':');
      if (parts.length === 2) {
        return parseInt(parts[0]) * 60 + parseInt(parts[1]);
      } else if (parts.length === 3) {
        return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseInt(parts[2]);
      }
      return 0;
    } catch (error) {
      return 0;
    }
  }

  private startWatchingForAdCompletion(): void {
    this.isWaitingForAdCompletion = true;

    if (this.adCompletionWatcher) {
      clearInterval(this.adCompletionWatcher);
    }

    this.adCompletionWatcher = setInterval(() => {
      if (!this.isAdPlaying()) {
        if (this.adCompletionWatcher) {
          clearInterval(this.adCompletionWatcher);
          this.adCompletionWatcher = null;
        }
        this.isWaitingForAdCompletion = false;

        setTimeout(() => this.detectCurrentVideo(), 1000);
      }
    }, 2000);

    setTimeout(
      () => {
        if (this.adCompletionWatcher) {
          clearInterval(this.adCompletionWatcher);
          this.adCompletionWatcher = null;
          this.isWaitingForAdCompletion = false;
        }
      },
      5 * 60 * 1000,
    );
  }

  private detectCurrentVideo(): void {
    if (this.detectionTimeout) {
      clearTimeout(this.detectionTimeout);
    }

    // Reduce detection delay from 3000ms to 1000ms for faster response
    this.detectionTimeout = setTimeout(() => this.performDetection(), 1000);
  }

  private async performDetection(): Promise<void> {
    const now = Date.now();
    // Reduce throttling from 5000ms to 2000ms for faster updates
    if (now - this.lastDetectionTime < 2000) return;
    this.lastDetectionTime = now;

    if (!this.isYouTubeVideoPage()) {
      if (this.currentVideoData?.isValid) {
        this.currentVideoData = null;
        this.notifyVideoChange();
      }
      return;
    }

    const url = window.location.href;
    const videoId = this.getVideoId();

    if (!videoId || this.currentVideoData?.url === url) return;

    if (this.videoDataCache.has(videoId)) {
      this.currentVideoData = this.videoDataCache.get(videoId)!;
      this.notifyVideoChange();
      return;
    }

    try {
      const apiData = await this.fetchVideoDataFromYouTubeAPI(videoId);
      if (!apiData) return;

      const videoData: VideoData = {
        url,
        title: apiData.title,
        duration: apiData.duration,
        isValid: true,
      };

      this.videoDataCache.set(videoId, videoData);
      if (this.videoDataCache.size > 50) {
        const firstKey = this.videoDataCache.keys().next().value;
        if (firstKey) this.videoDataCache.delete(firstKey);
      }

      this.currentVideoData = videoData;
      this.notifyVideoChange();
    } catch (error) {
      this.logger.error('Error during video detection:', error);
    }
  }

  private notifyVideoChange(): void {
    chrome.runtime
      .sendMessage({
        type: 'VIDEO_DETECTED',
        data: this.currentVideoData,
      })
      .catch(() => {});
  }

  private setupMessageListener(): void {
    chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
      if (message.type === 'GET_CURRENT_VIDEO') {
        sendResponse({
          type: 'CURRENT_VIDEO_RESPONSE',
          data: this.currentVideoData,
        });
        return true;
      }
      return false;
    });
  }

  public getCurrentVideoData(): VideoData | null {
    return this.currentVideoData;
  }

  public destroy(): void {
    if (this.detectionTimeout) {
      clearTimeout(this.detectionTimeout);
    }
    if (this.adCompletionWatcher) {
      clearInterval(this.adCompletionWatcher);
    }
  }
}

const detector = new YouTubeVideoDetector();

window.addEventListener('beforeunload', () => detector.destroy());

(window as any).ageanYouTubeDetector = detector;

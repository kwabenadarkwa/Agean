import 'webextension-polyfill';
import { colorfulLogger } from '@extension/shared';
import { ageanConfigStorage } from '@extension/storage';

const logger = colorfulLogger.create('Background');

// Initialize Agean extension
ageanConfigStorage.get().then(config => {
  logger.info('Agean configuration loaded:', config);
});

// Handle extension installation
chrome.runtime.onInstalled.addListener(details => {
  if (details.reason === 'install') {
    logger.info('Agean extension installed');
    logger.info('Click the extension icon on YouTube pages to open the side panel');
  }
});

// Log when navigating to YouTube videos
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.includes('youtube.com/watch')) {
    logger.info('YouTube video page detected:', tab.url);
  }
});

// Handle action button click - only open side panel on YouTube
chrome.action.onClicked.addListener(tab => {
  if (tab.id && tab.url?.includes('youtube.com')) {
    chrome.sidePanel.open({ tabId: tab.id });
    logger.info('Side panel opened for YouTube tab');
  } else {
    // Show notification that extension only works on YouTube
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon-34.png',
      title: 'Agean - YouTube Code Extractor',
      message: 'This extension only works on YouTube video pages. Please navigate to a YouTube video first.',
    });
    logger.info('Extension icon clicked on non-YouTube page');
  }
});

// Handle messages from side panel and content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  logger.info('Message received:', message.type);

  if (message.type === 'GET_CURRENT_VIDEO_FROM_SIDEPANEL') {
    // Get the current active tab
    chrome.tabs.query({ active: true, currentWindow: true }, async tabs => {
      const tab = tabs[0];

      if (!tab?.id || !tab.url?.includes('youtube.com/watch')) {
        sendResponse({
          type: 'CURRENT_VIDEO_RESPONSE',
          data: null,
        });
        return;
      }

      try {
        // Send message to content script to get current video data
        const response = await chrome.tabs.sendMessage(tab.id, {
          type: 'GET_CURRENT_VIDEO',
        });

        logger.info('Video data from content script:', response);
        sendResponse(response);
      } catch (error) {
        logger.error('Error getting video data from content script:', error);
        sendResponse({
          type: 'CURRENT_VIDEO_RESPONSE',
          data: null,
        });
      }
    });

    return true; // Keep message channel open for async response
  }

  // Forward VIDEO_DETECTED messages from content script to side panel
  if (message.type === 'VIDEO_DETECTED') {
    logger.info('Forwarding VIDEO_DETECTED message');
    // This message will be forwarded to all listeners (including side panel)
  }

  return false;
});

logger.info('Agean background script loaded');
logger.info('YouTube Code Extractor ready');

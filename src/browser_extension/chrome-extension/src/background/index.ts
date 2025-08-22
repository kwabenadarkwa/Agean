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
    // Open side panel on YouTube if user is already there
    chrome.tabs.query({ url: '*://www.youtube.com/*' }, tabs => {
      if (tabs.length > 0 && tabs[0].id) {
        chrome.sidePanel.open({ tabId: tabs[0].id });
      }
    });
  }
});

// Auto-open side panel when navigating to YouTube videos (optional)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.includes('youtube.com/watch')) {
    // Optionally auto-open side panel - you can disable this if you prefer manual opening
    // chrome.sidePanel.open({ tabId });
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

logger.info('Agean background script loaded');
logger.info('YouTube Code Extractor ready');

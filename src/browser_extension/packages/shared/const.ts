export const PROJECT_URL_OBJECT = {
  url: 'https://olympus.ntu.ac.uk/n1287962/Agean',
} as const;

// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://0.0.0.0:8000',
  ENDPOINTS: {
    EXTRACT_CODE: '/extract_code',
  },
  FALLBACK_URLS: ['http://localhost:8000', 'http://127.0.0.1:8000'],
} as const;

// Chrome Extension Manifest Types
export interface ManifestType {
  manifest_version: number;
  default_locale?: string;
  name: string;
  version: string;
  description: string;
  browser_specific_settings?: {
    gecko?: {
      id: string;
      strict_min_version: string;
    };
  };
  host_permissions?: string[];
  permissions?: string[];
  action?: {
    default_icon?: string;
    default_popup?: string;
    default_title?: string;
  };
  icons?: Record<string, string>;
  content_scripts?: Array<{
    matches: string[];
    js?: string[];
    css?: string[];
    run_at?: 'document_start' | 'document_end' | 'document_idle';
  }>;
  web_accessible_resources?: Array<{
    resources: string[];
    matches: string[];
  }>;
  side_panel?: {
    default_path: string;
  };
  background?: {
    service_worker?: string;
    scripts?: string[];
    type?: 'module';
  };
}

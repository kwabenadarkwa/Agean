import { resolve } from 'node:path';
import { defineConfig, type PluginOption } from 'vite';
import libAssetsPlugin from '@laynezh/vite-plugin-lib-assets';
import makeManifestPlugin from './utils/plugins/make-manifest-plugin.js';
import { watchPublicPlugin, watchRebuildPlugin } from '@extension/hmr';
import { watchOption } from '@extension/vite-config';
import env, { IS_DEV, IS_PROD } from '@extension/env';
import { nodePolyfills } from 'vite-plugin-node-polyfills';
import { copyFileSync, mkdirSync } from 'node:fs';

const rootDir = resolve(import.meta.dirname);
const srcDir = resolve(rootDir, 'src');

const outDir = resolve(rootDir, '..', 'dist');

// Plugin to copy locales
const copyLocalesPlugin = (): PluginOption => ({
  name: 'copy-locales',
  buildStart() {
    const localesDir = resolve(rootDir, '..', 'packages', 'i18n', 'locales');
    const distLocalesDir = resolve(outDir, '_locales');

    try {
      // Copy English locales
      mkdirSync(resolve(distLocalesDir, 'en'), { recursive: true });
      copyFileSync(resolve(localesDir, 'en', 'messages.json'), resolve(distLocalesDir, 'en', 'messages.json'));

      // Copy Korean locales
      mkdirSync(resolve(distLocalesDir, 'ko'), { recursive: true });
      copyFileSync(resolve(localesDir, 'ko', 'messages.json'), resolve(distLocalesDir, 'ko', 'messages.json'));

      console.log('✅ Locales copied to dist/_locales');
    } catch (error) {
      console.error('❌ Failed to copy locales:', error);
    }
  },
});
export default defineConfig({
  define: {
    'process.env': env,
  },
  resolve: {
    alias: {
      '@root': rootDir,
      '@src': srcDir,
      '@assets': resolve(srcDir, 'assets'),
    },
  },
  plugins: [
    libAssetsPlugin({
      outputPath: outDir,
    }) as PluginOption,
    watchPublicPlugin(),
    makeManifestPlugin({ outDir }),
    copyLocalesPlugin(),
    IS_DEV && watchRebuildPlugin({ reload: true, id: 'chrome-extension-hmr' }),
    nodePolyfills(),
  ],
  publicDir: resolve(rootDir, 'public'),
  build: {
    lib: {
      name: 'BackgroundScript',
      fileName: 'background',
      formats: ['es'],
      entry: resolve(srcDir, 'background', 'index.ts'),
    },
    outDir,
    emptyOutDir: false,
    sourcemap: IS_DEV,
    minify: IS_PROD,
    reportCompressedSize: IS_PROD,
    watch: watchOption,
    rollupOptions: {
      external: ['chrome'],
    },
  },
});

import { defineConfig } from '@playwright/test';
export default defineConfig({testDir: './e2e', use: {baseURL: process.env.BASE_URL || 'http://localhost:8090'}, workers: 1, timeout: 60000});

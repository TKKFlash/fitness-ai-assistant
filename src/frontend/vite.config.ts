import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "健身助手",
        short_name: "健身助手",
        display: "standalone",
        start_url: "/",
        theme_color: "#0f766e",
        background_color: "#ffffff",
        lang: "zh-CN",
      },
    }),
  ],
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/echo": "http://127.0.0.1:8000",
      "/healthz": "http://127.0.0.1:8000",
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test-setup.ts"],
  },
});

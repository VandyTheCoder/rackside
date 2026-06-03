import { defineConfig, envField, passthroughImageService } from "astro/config";
import vercel from "@astrojs/vercel";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  output: "server",
  adapter: vercel(),
  security: {
    checkOrigin: false,
  },
  image: {
    service: passthroughImageService(),
  },
  vite: {
    plugins: [tailwindcss()],
  },
  env: {
    schema: {
      API_URL: envField.string({
        context: "server",
        access: "secret",
        default: "http://127.0.0.1:8000",
      }),
    },
  },
});

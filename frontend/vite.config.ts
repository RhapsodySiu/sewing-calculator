import { defineConfig, loadEnv } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default ({ mode }: { mode: string }) => {
  const env = loadEnv(mode, process.cwd());
  console.log(env);

  return defineConfig({
    plugins: [svelte()],
    server: {
      port: 3000,
      proxy: {
        '/api': `${env.VITE_API_HOST}:${env.VITE_API_PORT}`,
      }
    }
  });
};

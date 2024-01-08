import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    define: {
      'process.env.DEPLOYER_SERVER_HOST': JSON.stringify(env.DEPLOYER_SERVER_HOST),
      'process.env.DEPLOYER_SERVER_PORT': JSON.stringify(env.DEPLOYER_SERVER_PORT),
      'process.env.RESOURCES_SERVER_HOST': JSON.stringify(env.RESOURCES_SERVER_HOST),
      'process.env.RESOURCES_SERVER_PORT': JSON.stringify(env.RESOURCES_SERVER_PORT),
    },
    plugins: [react()],
  }
})

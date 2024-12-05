import type { NextConfig } from "next";

const nextConfig: NextConfig = {

  webpack(config, { isServer }) {

    const env = process.env.NODE_ENV;

    console.log('Current environment:', env);
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        buffer: require.resolve('buffer/'),
      };
    }
    return config;
  },
};

export default nextConfig;

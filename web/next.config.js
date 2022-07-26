/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    styledComponents: true,
    reactRemoveProperties: true,
    removeConsole: process.env.NODE_ENV === 'production',
  },
};

module.exports = nextConfig;

// Avoid importing Next types to prevent "Cannot find module 'next'" when
// @types/next is not installed in the environment.
const nextConfig = {
  allowedDevOrigins: ["http://172.17.16.1:3001"],
};

export default nextConfig;

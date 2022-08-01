import to from 'await-to-js';
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

import apiError from 'src/utils/api';
import { axios } from 'src/utils/axios';
import { User } from 'src/utils/types/shared';

type LoginPayload = {
  email: string;
  password: string;
};

type LoginResponse = {
  data: User;
};

export default NextAuth({
  providers: [
    CredentialsProvider({
      id: 'signin',
      name: 'Signin',
      credentials: {},
      async authorize(credentials) {
        const userInfo = credentials as unknown as LoginPayload;
        const { email, password } = userInfo;
        const payload = { email, password };

        const [err, data] = await to<LoginResponse>(
          axios.post('auth/login/', payload)
        );

        if (data) {
          const { user } = data.data;
          return user;
        } else if (err) throw new Error(apiError(err));

        return null;
      },
    }),
  ],
  pages: {
    signIn: '/login',
    signOut: '/',
    error: '/login',
  },
  callbacks: {
    async session({ session, user }) {
      session.accessToken = user.access_token;
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.token;
        token.user = user;
      }
      return token;
    },
    async redirect({ url, baseUrl }) {
      // Allows relative callback URLs
      if (url.startsWith('/')) return `${baseUrl}${url}`;
      // Allows callback URLs on the same origin
      else if (new URL(url).origin === baseUrl) return url;
      return baseUrl;
    },
  },
  secret: process.env.NEXT_AUTH_SECRET,
});

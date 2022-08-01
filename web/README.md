# Getting Started - Prerequisites

✔️ Prior experience with the Next.js framework.

✔️ A basic understanding of how NextAuth.js authentication works.

## About NextAuth.js

NextAuth.js is a complete open source authentication solution for [Next.js](http://nextjs.org/) applications. It adds session support without using client side accessible session tokens, providing protection against Cross Site Scripting (XSS) and session hijacking, while leveraging localStorage where available to cache non-critical session state for optimal performance in Single Page Apps.

Go to [next-auth.js.org](https://next-auth.js.org) for more information and documentation.

## Installation

1 - Clone the repository.

```bash
git@github.com:GeofreyMuindeMunguti/unicn.git
```

2 - Run `yarn install` to install dependencies.

3 - Run `yarn dev` to run a development server.

4 - Now point your browser to <http://localhost:3000/>

## ENV Setup

Copy the .env.local.example file in this directory to .env.local (which will be ignored by Git):

```bash
cp .env.local.example .env.local
```

## Commands

| `yarn <command>` | Description                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------- |
| `build`          | Compiles `src` app to `.next/static` and `api` to `build` for production.
| `dev`            | Starts development servers (`localhost:3000`)        |
| `lint`           | Lints all `.ts`/`.tsx` files in  `src`
| `start`          | Starts production servers (must run `build` first).
| `format`         | Formats `.ts`/`.tsx` files in `src`.

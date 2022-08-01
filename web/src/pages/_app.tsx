import type { AppProps } from 'next/app';
import { Toaster } from 'react-hot-toast';

import GlobalStyles from 'styles/global';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <GlobalStyles />
      <Toaster position="top-center" toastOptions={{ duration: 6000 }} />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;

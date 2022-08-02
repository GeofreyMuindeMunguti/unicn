import type { AppProps } from 'next/app';
import { Toaster } from 'react-hot-toast';
import { SWRConfig } from 'swr';

import { axiosClient } from 'src/utils/axios';
import { User } from 'src/utils/types/shared';

import GlobalStyles from 'styles/global';

function MyApp({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  const user = session ? (session.user as unknown as User) : null;

  // swr configs
  const swrConfigs = {
    fetcher: (url: string) => {
      const axios = axiosClient(user);
      return axios.get(url).then((res) => res.data);
    },
    errorRetryCount: 1,
    errorRetryInterval: 15000,
  };

  return (
    <SWRConfig value={swrConfigs}>
      <GlobalStyles />
      <Toaster position="top-center" toastOptions={{ duration: 6000 }} />
      <Component {...pageProps} />
    </SWRConfig>
  );
}

export default MyApp;

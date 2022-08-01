import HttpClient from 'axios';

import { User } from './types/shared';

const baseURL = process.env.API_BASE_URL as string;

const axios = HttpClient.create({ baseURL });

function axiosClient(user: User | null) {
  if (user) {
    axios.defaults.headers.common.Authorization = `Bearer ${user.access_token}`;
  }
  return axios;
}

export { axios, axiosClient };

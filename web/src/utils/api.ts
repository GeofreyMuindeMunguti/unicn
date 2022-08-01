import { AxiosError } from 'axios';

type ResponseError = {
  detail: string;
};

function apiError(err: Error) {
  const { response } = err as AxiosError<ResponseError>;
  if (response && response.data) return response.data.detail;
  return 'Something went wrong';
}

export default apiError;

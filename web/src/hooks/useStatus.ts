import React from 'react';

export type Status = 'idle' | 'pending' | 'resolved' | 'rejected';

function useStatus() {
  const [status, setStatus] = React.useState<Status>('idle');

  const isLoading = status === 'pending';
  const isResolved = status === 'resolved';
  const isRejected = status === 'rejected';

  return { isLoading, isResolved, isRejected, status, setStatus };
}

export default useStatus;

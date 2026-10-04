import React from 'react';
import { getStatusBadgeColor } from '../../utils/formatters';

interface StatusBadgeProps {
  status: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'sm' }) => {
  const { bg, text, border } = getStatusBadgeColor(status);
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs font-semibold';

  return (
    <span className={`inline-flex items-center rounded-md font-medium border ${bg} ${text} ${border} ${sizeClasses}`}>
      {status}
    </span>
  );
};

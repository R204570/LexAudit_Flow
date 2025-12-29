import React from 'react';
import { Bell } from 'lucide-react';

export const NotificationBadge = ({ count }) => {
  if (count === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg">
        <Bell size={20} />
        <span className="font-semibold">{count} new update{count !== 1 ? 's' : ''}</span>
      </div>
    </div>
  );
};

export default NotificationBadge;

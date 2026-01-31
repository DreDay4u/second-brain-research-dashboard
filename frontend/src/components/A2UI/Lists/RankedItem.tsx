/**
 * RankedItem Component
 *
 * Displays a numbered/ranked list item with optional description, badge, and score.
 * Supports rank badges (1st, 2nd, 3rd, etc.) with dark theme support.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface RankedItemProps {
  /** Rank number (1, 2, 3, etc.) */
  rank: number;

  /** Item title/label */
  label: string;

  /** Optional description text */
  value?: string;

  /** Optional color theme (default uses primary) */
  color?: string;

  /** Optional badge text */
  badge?: string;

  /** Optional score/metric to display */
  score?: string | number;
}

/**
 * RankedItem Component
 *
 * A list item component with a numbered rank badge, title, optional description,
 * badge, and score. Perfect for leaderboards, top lists, rankings, etc.
 */
export function RankedItem({
  rank,
  label,
  value,
  color,
  badge,
  score,
}: RankedItemProps): React.ReactElement {
  const getBgColor = () => {
    if (color) return `bg-${color}-500`;
    return 'bg-primary';
  };

  const getTextColor = () => {
    if (color) return `text-${color}-foreground`;
    return 'text-primary-foreground';
  };

  return (
    <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors">
      <div className={`flex items-center justify-center w-8 h-8 rounded-full ${getBgColor()} ${getTextColor()} font-bold text-sm shrink-0`}>
        {rank}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1 flex-wrap">
          <span className="font-semibold">{label}</span>
          {badge && <Badge variant="secondary">{badge}</Badge>}
        </div>
        {value && <p className="text-sm text-muted-foreground">{value}</p>}
      </div>
      {score !== undefined && score !== null && (
        <div className="text-lg font-bold text-muted-foreground shrink-0">
          {score}
        </div>
      )}
    </div>
  );
}

export default RankedItem;

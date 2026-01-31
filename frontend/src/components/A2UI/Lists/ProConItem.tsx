/**
 * ProConItem Component
 *
 * Displays a pro or con item with icon, text, and optional weight/importance.
 * Shows green checkmark for pros, red X for cons.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface ProConItemProps {
  /** Type of item: 'pro' (positive) or 'con' (negative) */
  type: 'pro' | 'con';

  /** Item text/description */
  label: string;

  /** Optional description for more details */
  description?: string;

  /** Optional weight/importance indicator */
  weight?: string | number;
}

/**
 * ProConItem Component
 *
 * A component for displaying pros and cons with color-coded icons.
 * Green checkmark for pros, red X for cons. Perfect for decision matrices,
 * comparisons, and analysis.
 */
export function ProConItem({
  type,
  label,
  description,
  weight,
}: ProConItemProps): React.ReactElement {
  const isPro = type === 'pro';

  const bgColor = isPro ? 'bg-green-500/10' : 'bg-red-500/10';
  const textColor = isPro ? 'text-green-500' : 'text-red-500';
  const icon = isPro ? '✓' : '✗';

  return (
    <div className={`flex items-start gap-2 p-2 rounded-lg ${bgColor}`}>
      <span className={`text-lg ${textColor} shrink-0 mt-0.5`}>
        {icon}
      </span>
      <div className="flex-1 min-w-0">
        <span className="text-sm block">{label}</span>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
      </div>
      {weight !== undefined && weight !== null && (
        <Badge variant="secondary" className="shrink-0">
          {weight}
        </Badge>
      )}
    </div>
  );
}

export default ProConItem;

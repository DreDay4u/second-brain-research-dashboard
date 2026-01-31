/**
 * ComparisonBar Component
 *
 * Displays horizontal bars comparing two values side-by-side.
 * Auto-scales to the maximum value and shows labels for each bar.
 */

import React from 'react';

export interface ComparisonBarProps {
  /** Main label for the comparison */
  label: string;

  /** First value to compare */
  value_a: number;

  /** Second value to compare */
  value_b: number;

  /** Label for first value */
  label_a: string;

  /** Label for second value */
  label_b: string;

  /** Optional maximum value for scaling (defaults to max of both values) */
  max_value?: number;

  /** Optional color for first bar (defaults to blue) */
  color_a?: string;

  /** Optional color for second bar (defaults to purple) */
  color_b?: string;
}

/**
 * ComparisonBar Component
 *
 * A horizontal bar chart component for comparing two values
 * with automatic scaling and customizable colors.
 */
export function ComparisonBar({
  label,
  value_a,
  value_b,
  label_a,
  label_b,
  max_value,
  color_a = 'blue',
  color_b = 'purple',
}: ComparisonBarProps): React.ReactElement {
  const maxVal = max_value || Math.max(value_a, value_b);
  const percentA = (value_a / maxVal) * 100;
  const percentB = (value_b / maxVal) * 100;

  return (
    <div className="space-y-3 p-4 rounded-xl bg-secondary/30 border border-blue-500/10">
      <div className="text-sm font-medium text-blue-200">{label}</div>
      <div className="flex items-center gap-2">
        <span className="text-xs w-20 text-right text-blue-300/70">
          {label_a}
        </span>
        <div className="flex-1 h-6 bg-secondary rounded-full overflow-hidden flex">
          <div
            className="bg-gradient-to-r from-blue-600 to-blue-400 h-full transition-all duration-500 shadow-lg shadow-blue-500/30"
            style={{ width: `${percentA}%` }}
          />
        </div>
        <span className="text-xs w-12 font-semibold text-white">{value_a}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs w-20 text-right text-blue-300/70">
          {label_b}
        </span>
        <div className="flex-1 h-6 bg-secondary rounded-full overflow-hidden flex">
          <div
            className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full transition-all duration-500 shadow-lg shadow-cyan-500/30"
            style={{ width: `${percentB}%` }}
          />
        </div>
        <span className="text-xs w-12 font-semibold text-white">{value_b}</span>
      </div>
    </div>
  );
}

export default ComparisonBar;

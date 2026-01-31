/**
 * TrendIndicator Component
 *
 * Displays a metric with its current value, change percentage,
 * and trend direction (up, down, or stable).
 */

import React from 'react';

export interface TrendIndicatorProps {
  /** Name of the metric being tracked */
  metric: string;

  /** Current value of the metric */
  value: string | number;

  /** Change amount or percentage */
  change: string;

  /** Trend direction */
  trend: 'up' | 'down' | 'stable';

  /** Optional time period for the trend */
  period?: string;
}

/**
 * TrendIndicator Component
 *
 * A compact component showing metric trends with visual indicators
 * for up/down/stable changes.
 */
export function TrendIndicator({
  metric,
  value,
  change,
  trend,
  period,
}: TrendIndicatorProps): React.ReactElement {
  const getTrendColor = () => {
    if (trend === 'up') return 'text-blue-400';
    if (trend === 'down') return 'text-blue-300';
    return 'text-blue-400/60';
  };

  const getTrendIcon = () => {
    if (trend === 'up') return '↑';
    if (trend === 'down') return '↓';
    return '→';
  };

  return (
    <div className="flex items-center gap-2 p-3 rounded-lg bg-gradient-to-br from-card to-secondary/30 border border-blue-500/20 hover:border-blue-400/40 transition-all duration-300">
      <div className="flex-1">
        <div className="text-sm font-medium text-blue-200">{metric}</div>
        <div className="text-2xl font-bold text-white">{value}</div>
      </div>
      <div className={`flex items-center gap-1 ${getTrendColor()}`}>
        <span className="text-lg animate-pulse" aria-label={`Trend ${trend}`}>
          {getTrendIcon()}
        </span>
        <span className="font-semibold">{change}</span>
      </div>
      {period && (
        <div className="text-xs text-blue-300/70">{period}</div>
      )}
    </div>
  );
}

export default TrendIndicator;

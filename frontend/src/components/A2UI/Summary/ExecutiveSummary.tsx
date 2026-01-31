/**
 * ExecutiveSummary Component
 *
 * Displays a comprehensive summary with optional title, overview text,
 * metrics array, and recommendations list.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface SummaryMetric {
  /** Metric label */
  label: string;

  /** Metric value */
  value: string | number;

  /** Optional unit (%, $, etc.) */
  unit?: string;

  /** Optional trend indicator */
  trend?: 'up' | 'down' | 'neutral';
}

export interface ExecutiveSummaryProps {
  /** Main title */
  title?: string;

  /** Overview/summary text */
  summary: string;

  /** Optional array of metrics */
  metrics?: SummaryMetric[];

  /** Optional array of recommendation strings */
  recommendations?: string[];
}

/**
 * ExecutiveSummary Component
 *
 * A comprehensive summary card with title, summary text,
 * metrics display, and actionable recommendations.
 */
export function ExecutiveSummary({
  title = 'Executive Summary',
  summary,
  metrics,
  recommendations,
}: ExecutiveSummaryProps): React.ReactElement {
  const getTrendIcon = (trend?: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up':
        return <span className="text-green-500">↑</span>;
      case 'down':
        return <span className="text-red-500">↓</span>;
      case 'neutral':
        return <span className="text-yellow-500">→</span>;
      default:
        return null;
    }
  };

  return (
    <Card className="dark:bg-slate-900 dark:border-slate-800">
      <CardHeader>
        <CardTitle className="dark:text-slate-100">{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm dark:text-slate-200">{summary}</p>

        {metrics && metrics.length > 0 && (
          <div>
            <h4 className="font-semibold text-sm mb-3 dark:text-slate-100">Key Metrics</h4>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {metrics.map((metric, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-muted dark:bg-slate-800 space-y-1"
                >
                  <div className="text-xs text-muted-foreground dark:text-slate-400">
                    {metric.label}
                  </div>
                  <div className="flex items-baseline gap-1">
                    <span className="text-lg font-bold dark:text-slate-100">
                      {metric.value}
                    </span>
                    {metric.unit && (
                      <span className="text-sm text-muted-foreground dark:text-slate-400">
                        {metric.unit}
                      </span>
                    )}
                    {metric.trend && getTrendIcon(metric.trend)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {recommendations && recommendations.length > 0 && (
          <div>
            <h4 className="font-semibold text-sm mb-2 dark:text-slate-100">Recommendations</h4>
            <ul className="space-y-2">
              {recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <Badge variant="outline" className="shrink-0 mt-0.5 dark:border-slate-700 dark:text-slate-300">
                    {idx + 1}
                  </Badge>
                  <span className="text-sm text-muted-foreground dark:text-slate-300">
                    {rec}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default ExecutiveSummary;

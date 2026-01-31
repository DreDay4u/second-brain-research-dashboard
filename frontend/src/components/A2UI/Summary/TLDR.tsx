/**
 * TLDR Component
 *
 * Displays a quick summary in a highlighted box with optional key points.
 * Max 300 chars for summary text, with optional icon customization.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface TLDRProps {
  /** Main summary text (max 300 chars recommended) */
  summary: string;

  /** Optional array of key points */
  key_points?: string[];

  /** Optional icon or emoji (defaults to ⚡) */
  icon?: string;
}

/**
 * TLDR Component
 *
 * A highlighted card component for displaying quick summaries
 * with optional bulleted key points.
 */
export function TLDR({
  summary,
  key_points,
  icon = '⚡',
}: TLDRProps): React.ReactElement {
  return (
    <Card className="bg-yellow-500/10 border-yellow-500 dark:bg-yellow-500/20 dark:border-yellow-500/50">
      <CardHeader>
        <CardTitle className="text-sm flex items-center gap-2 dark:text-slate-100">
          <span>{icon}</span> TL;DR
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <p className="text-sm font-medium dark:text-slate-200">{summary}</p>
        {key_points && key_points.length > 0 && (
          <ul className="space-y-1 mt-2">
            {key_points.map((point: string, idx: number) => (
              <li key={idx} className="text-sm text-muted-foreground dark:text-slate-400 flex gap-2">
                <span>•</span>
                <span>{point}</span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

export default TLDR;

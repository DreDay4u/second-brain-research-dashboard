/**
 * ExpertTip Component
 *
 * Displays expert advice with expertise area badge, tip title, and description.
 * Features distinctive styling with optional icon support.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface ExpertTipProps {
  /** The tip or advice text */
  tip: string;

  /** Expert's name */
  expert?: string;

  /** Category or expertise area */
  category?: string;

  /** Optional title for the tip */
  title?: string;

  /** Optional icon or emoji */
  icon?: string;
}

/**
 * ExpertTip Component
 *
 * A card component for displaying expert tips and advice with
 * category badges and distinctive styling.
 */
export function ExpertTip({
  tip,
  expert,
  category,
  title,
  icon,
}: ExpertTipProps): React.ReactElement {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-l-4 border-blue-500 border-blue-500/20">
      <CardHeader>
        <div className="flex items-center gap-2">
          <span className="text-xl text-blue-400">{icon || '💡'}</span>
          <CardTitle className="text-sm text-white">
            {title || 'Expert Tip'}
          </CardTitle>
          {category && (
            <Badge variant="secondary" className="bg-blue-950/50 text-blue-200 border border-blue-500/30">
              {category}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        <p className="text-sm text-slate-200">{tip}</p>
        {expert && (
          <p className="text-xs text-blue-300 mt-2 pt-2 border-t border-blue-500/20">
            — {expert}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default ExpertTip;

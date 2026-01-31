/**
 * QuoteCard Component
 *
 * Displays a quote with attribution, author title, and optional avatar.
 * Features subtle border and background styling.
 */

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface QuoteCardProps {
  /** The quote text */
  quote: string;

  /** Author name */
  author: string;

  /** Author's title or role */
  title?: string;

  /** Optional context or source information */
  context?: string;

  /** Optional avatar URL for the author */
  avatar_url?: string;
}

/**
 * QuoteCard Component
 *
 * A card component for displaying quotes with attribution and styling.
 * Features a left border accent and elegant typography.
 */
export function QuoteCard({
  quote,
  author,
  title,
  context,
  avatar_url,
}: QuoteCardProps): React.ReactElement {
  return (
    <Card className="border-l-4 border-primary dark:border-primary/70 dark:border-slate-700 dark:bg-slate-900/50">
      <CardContent className="pt-6">
        <blockquote className="text-lg italic mb-4 text-foreground dark:text-slate-200">
          "{quote}"
        </blockquote>
        <div className="flex items-center gap-3">
          {avatar_url ? (
            <img
              src={avatar_url}
              alt={author}
              className="w-10 h-10 rounded-full border border-border dark:border-slate-600"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-primary/10 dark:bg-primary/20 flex items-center justify-center">
              <span className="text-sm font-semibold text-primary dark:text-primary/80">
                {author.charAt(0).toUpperCase()}
              </span>
            </div>
          )}
          <div>
            <div className="font-semibold dark:text-slate-100">{author}</div>
            {title && (
              <div className="text-sm text-muted-foreground dark:text-slate-400">{title}</div>
            )}
          </div>
        </div>
        {context && (
          <p className="text-sm text-muted-foreground dark:text-slate-400 mt-3 pt-3 border-t dark:border-slate-700">
            {context}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default QuoteCard;

/**
 * HeadlineCard Component
 *
 * Displays a news headline with title, summary, source, date, and optional image.
 * Supports sentiment indicators (positive, negative, neutral).
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface HeadlineCardProps {
  /** Main headline title */
  title: string;

  /** Brief summary or description of the article */
  summary?: string;

  /** News source (e.g., "TechCrunch", "Reuters") */
  source: string;

  /** Publication date in ISO format or Date object */
  published_at: string | Date;

  /** Sentiment of the article (positive, negative, neutral) */
  sentiment?: 'positive' | 'negative' | 'neutral';

  /** Optional image URL for the headline */
  image_url?: string;
}

/**
 * HeadlineCard Component
 *
 * A card component for displaying news headlines with optional image,
 * sentiment indicator, source, and publication date.
 */
export function HeadlineCard({
  title,
  summary,
  source,
  published_at,
  sentiment,
  image_url,
}: HeadlineCardProps): React.ReactElement {
  const getBorderColor = () => {
    if (sentiment === 'positive') return 'border-blue-400/40';
    if (sentiment === 'negative') return 'border-blue-500/30';
    return 'border-blue-500/20';
  };

  const getSentimentBadgeClasses = () => {
    if (sentiment === 'positive') return 'bg-blue-500/20 text-blue-300 border-blue-400/50 hover:bg-blue-500/30';
    if (sentiment === 'negative') return 'bg-blue-600/20 text-blue-200 border-blue-500/50 hover:bg-blue-600/30';
    return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
  };

  const formatDate = (date: string | Date): string => {
    try {
      return new Date(date).toLocaleDateString();
    } catch {
      return String(date);
    }
  };

  return (
    <Card className={`${getBorderColor()} bg-gradient-to-br from-card to-secondary/30 group cursor-pointer hover:border-blue-400/60 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10`}>
      {image_url && (
        <div className="overflow-hidden rounded-t-lg">
          <img
            src={image_url}
            alt={title}
            className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-lg text-white group-hover:text-blue-300 transition-colors duration-200">{title}</CardTitle>
          {sentiment && sentiment !== 'neutral' && (
            <Badge variant="outline" className={`shrink-0 ${getSentimentBadgeClasses()}`}>
              {sentiment}
            </Badge>
          )}
        </div>
        <CardDescription className="text-blue-300/80">
          {source} • {formatDate(published_at)}
        </CardDescription>
      </CardHeader>
      {summary && (
        <CardContent>
          <p className="text-sm text-blue-100/70">{summary}</p>
        </CardContent>
      )}
    </Card>
  );
}

export default HeadlineCard;

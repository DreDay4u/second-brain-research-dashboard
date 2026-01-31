/**
 * DifficultyBadge Component
 *
 * Displays difficulty level with appropriate color-coding and optional icons.
 * Supports beginner, intermediate, advanced, and expert levels.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert';

/** Difficulty configuration */
interface DifficultyConfig {
  label: string;
  color: string;
  bars: number;
  emoji?: string;
}

const DIFFICULTY_CONFIGS: Record<DifficultyLevel, DifficultyConfig> = {
  beginner: {
    label: 'Beginner',
    color: 'bg-green-500/20 text-green-700 dark:bg-green-500/30 dark:text-green-300 border-green-500/50',
    bars: 1,
    emoji: '🟢',
  },
  intermediate: {
    label: 'Intermediate',
    color: 'bg-blue-500/20 text-blue-700 dark:bg-blue-500/30 dark:text-blue-300 border-blue-500/50',
    bars: 2,
    emoji: '🔵',
  },
  advanced: {
    label: 'Advanced',
    color: 'bg-orange-500/20 text-orange-700 dark:bg-orange-500/30 dark:text-orange-300 border-orange-500/50',
    bars: 3,
    emoji: '🟠',
  },
  expert: {
    label: 'Expert',
    color: 'bg-red-500/20 text-red-700 dark:bg-red-500/30 dark:text-red-300 border-red-500/50',
    bars: 4,
    emoji: '🔴',
  },
};

export interface DifficultyBadgeProps {
  /** Difficulty level */
  level: DifficultyLevel;

  /** Show icon representation (bars or emoji) */
  icon?: boolean;

  /** Icon style: 'bars' for horizontal bars, 'emoji' for colored circle emoji */
  iconStyle?: 'bars' | 'emoji';

  /** Show text label */
  showLabel?: boolean;
}

/**
 * DifficultyBadge Component
 *
 * A badge component for displaying difficulty levels with color-coding and optional icons.
 */
export function DifficultyBadge({
  level,
  icon = true,
  iconStyle = 'bars',
  showLabel = true,
}: DifficultyBadgeProps): React.ReactElement {
  const config = DIFFICULTY_CONFIGS[level] || DIFFICULTY_CONFIGS.beginner;

  // Render bar icons
  const renderBars = () => {
    return (
      <div className="flex items-center gap-0.5">
        {Array.from({ length: 4 }).map((_, idx) => (
          <div
            key={idx}
            className={`
              w-1 h-3 rounded-sm
              ${idx < config.bars
                ? 'bg-current'
                : 'bg-current opacity-20'
              }
            `}
          />
        ))}
      </div>
    );
  };

  // Render emoji icon
  const renderEmoji = () => {
    return <span className="text-sm">{config.emoji}</span>;
  };

  return (
    <Badge
      variant="outline"
      className={`
        ${config.color}
        font-medium
        flex items-center gap-2
        px-2.5 py-1
        w-fit
      `}
    >
      {icon && (
        <span className="flex-shrink-0">
          {iconStyle === 'bars' ? renderBars() : renderEmoji()}
        </span>
      )}
      {showLabel && <span>{config.label}</span>}
    </Badge>
  );
}

export default DifficultyBadge;

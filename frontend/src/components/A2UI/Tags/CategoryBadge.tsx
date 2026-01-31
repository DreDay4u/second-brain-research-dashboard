/**
 * CategoryBadge Component
 *
 * Displays a category with color-coded background and optional icon.
 * Supports predefined color schemes for common categories.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";
import { X } from 'lucide-react';

export type CategorySize = 'sm' | 'md' | 'lg';

/** Predefined category color schemes */
const CATEGORY_COLORS: Record<string, string> = {
  tech: 'bg-blue-500/20 text-blue-700 dark:bg-blue-500/30 dark:text-blue-300 border-blue-500/50',
  science: 'bg-purple-500/20 text-purple-700 dark:bg-purple-500/30 dark:text-purple-300 border-purple-500/50',
  business: 'bg-green-500/20 text-green-700 dark:bg-green-500/30 dark:text-green-300 border-green-500/50',
  health: 'bg-red-500/20 text-red-700 dark:bg-red-500/30 dark:text-red-300 border-red-500/50',
  education: 'bg-yellow-500/20 text-yellow-700 dark:bg-yellow-500/30 dark:text-yellow-300 border-yellow-500/50',
  entertainment: 'bg-pink-500/20 text-pink-700 dark:bg-pink-500/30 dark:text-pink-300 border-pink-500/50',
  sports: 'bg-orange-500/20 text-orange-700 dark:bg-orange-500/30 dark:text-orange-300 border-orange-500/50',
  politics: 'bg-indigo-500/20 text-indigo-700 dark:bg-indigo-500/30 dark:text-indigo-300 border-indigo-500/50',
  finance: 'bg-emerald-500/20 text-emerald-700 dark:bg-emerald-500/30 dark:text-emerald-300 border-emerald-500/50',
  lifestyle: 'bg-cyan-500/20 text-cyan-700 dark:bg-cyan-500/30 dark:text-cyan-300 border-cyan-500/50',
};

export interface CategoryBadgeProps {
  /** Category name */
  category: string;

  /** Custom color class (overrides predefined colors) */
  color?: string;

  /** Optional icon (emoji or component) */
  icon?: string | React.ReactNode;

  /** Badge size */
  size?: CategorySize;

  /** Show remove button */
  removable?: boolean;

  /** Callback when remove button is clicked */
  onRemove?: () => void;
}

/**
 * CategoryBadge Component
 *
 * A badge component for displaying categories with predefined or custom colors.
 * Supports icons and removable functionality.
 */
export function CategoryBadge({
  category,
  color,
  icon,
  size = 'md',
  removable = false,
  onRemove,
}: CategoryBadgeProps): React.ReactElement {
  // Get color from predefined schemes or use custom
  const categoryKey = category.toLowerCase();
  const badgeColor = color || CATEGORY_COLORS[categoryKey] || 'bg-slate-500/20 text-slate-700 dark:bg-slate-500/30 dark:text-slate-300 border-slate-500/50';

  // Size classes
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-1',
    lg: 'text-base px-3 py-1.5',
  };

  return (
    <Badge
      variant="outline"
      className={`
        ${badgeColor}
        ${sizeClasses[size]}
        font-medium
        flex items-center gap-1.5
        w-fit
      `}
    >
      {icon && (
        <span className="flex-shrink-0">
          {typeof icon === 'string' ? icon : icon}
        </span>
      )}
      <span>{category}</span>
      {removable && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove?.();
          }}
          className="ml-0.5 hover:bg-black/10 dark:hover:bg-white/10 rounded-full p-0.5 transition-colors"
          aria-label="Remove category"
        >
          <X className="w-3 h-3" />
        </button>
      )}
    </Badge>
  );
}

export default CategoryBadge;

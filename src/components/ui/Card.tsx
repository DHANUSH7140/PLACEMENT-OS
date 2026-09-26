import React from 'react';
import { cn } from '../../utils/utils';

export const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & { variant?: 'porcelain' | 'charcoal' }>(
  ({ className, variant = 'porcelain', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'rounded-[20px] p-5 shadow-nested-card',
          variant === 'porcelain' && 'bg-white border border-[#eceeed] text-on-surface',
          variant === 'charcoal' && 'bg-[#18191c] text-white overflow-hidden',
          className
        )}
        {...props}
      />
    );
  }
);
Card.displayName = 'Card';

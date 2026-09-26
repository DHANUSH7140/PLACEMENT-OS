import React from 'react';
import { cn } from '../../utils/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'default', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-full font-sans font-semibold transition-transform active:scale-[0.98] outline-none focus-visible:ring-2 focus-visible:ring-chartreuse focus-visible:ring-offset-2',
          {
            'bg-[#d6f254] text-[#121316] hover:bg-[#e8fa8c] shadow-chartreuse-glow': variant === 'primary',
            'bg-[#1c1e22] text-white border border-white/10 hover:bg-[#26292f] shadow-nested-card': variant === 'secondary',
            'bg-[rgba(18,19,22,0.04)] text-[#1a1c1c] hover:bg-[#e8fa8c]': variant === 'ghost',
            'h-11 px-5 text-body-md': size === 'default',
            'h-9 px-4 text-body-sm': size === 'sm',
            'h-14 px-8 text-headline-sm': size === 'lg',
            'h-11 w-11': size === 'icon',
          },
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

import React from 'react';
import { cn } from '../../utils/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1 w-full">
        {label && <label className="text-label-md text-on-surface-variant mb-1">{label}</label>}
        <input
          ref={ref}
          className={cn(
            'flex h-12 w-full rounded-[16px] bg-[#f3f4f6] px-4 py-2 text-body-md shadow-sm transition-all text-on-surface file:border-0 file:bg-transparent file:text-body-md file:font-semibold placeholder:text-outline outline-none focus-visible:ring-2 focus-visible:ring-chartreuse disabled:cursor-not-allowed disabled:opacity-50 border-none',
            error && 'ring-2 ring-danger',
            className
          )}
          {...props}
        />
        {error && <span className="text-body-sm text-danger mt-1">{error}</span>}
      </div>
    );
  }
);
Input.displayName = 'Input';

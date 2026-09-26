import React from 'react';
import { cn } from '../../utils/utils';

interface CapsuleMeterProps {
  score: number; // 0 to 100
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const CapsuleMeter: React.FC<CapsuleMeterProps> = ({ score, size = 'md', className }) => {
  const isFilled = score > 0;
  
  return (
    <div className={cn("w-full bg-[#ecefed] rounded-full overflow-hidden flex items-center relative", {
      'h-2': size === 'sm',
      'h-3': size === 'md',
      'h-4': size === 'lg',
    }, className)}>
      <div 
        className="h-full bg-chartreuse transition-all duration-1000 ease-out"
        style={{ width: `${Math.max(Math.min(score, 100), 0)}%` }}
      />
    </div>
  );
};

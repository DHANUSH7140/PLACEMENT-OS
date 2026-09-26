import React, { useEffect, useState } from 'react';
import { getPlacementRoute } from '../services/api/dashboard';
import type { PlacementRouteData } from '../types';
import { Card } from '../components/ui/Card';
import { Compass, Check, Lock, ChevronDown, Zap } from 'lucide-react';

export const PlacementGPS = () => {
  const [route, setRoute] = useState<PlacementRouteData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPlacementRoute().then(setRoute).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-outline p-8 text-center">Plotting your route...</div>;
  if (!route) return null;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto space-y-8">
      <div className="flex flex-col border-b border-[#eceeed] pb-6">
        <h1 className="text-headline-lg flex items-center gap-3"><Compass size={28} className="text-matte-charcoal"/> Placement GPS</h1>
        <p className="text-body-lg text-on-surface-variant mt-2">Target Destination: <span className="font-bold text-on-surface">{route.target}</span></p>
      </div>

      {route.reasonForChange && (
        <Card variant="charcoal" className="bg-matte-charcoal">
          <div className="flex items-start gap-4">
            <Zap className="text-chartreuse shrink-0" />
            <div>
              <h3 className="text-body-md font-bold text-chartreuse mb-1">Route Recalculated</h3>
              <p className="text-body-sm text-[#8a8f98] whitespace-pre-wrap">{route.reasonForChange}</p>
            </div>
          </div>
        </Card>
      )}

      <div className="relative pl-8 pt-4 pb-12">
        {/* Dynamic Route Line */}
        <div className="absolute left-10 top-8 bottom-8 w-[2px] bg-gradient-to-b from-chartreuse via-[#eceeed] to-[#eceeed] -z-10"></div>
        
        <div className="flex flex-col gap-6">
          {route.nodes.map((node, i) => (
            <div key={node.id} className="relative flex items-center gap-6 group">
              <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 z-10 transition-all ${
                node.status === 'completed' ? 'bg-matte-charcoal text-white scale-100' :
                node.status === 'active' ? 'bg-chartreuse text-[#121316] ring-4 ring-chartreuse/20 scale-125 shadow-chartreuse-glow' :
                node.status === 'upcoming' ? 'bg-white border-2 border-[#eceeed] text-outline scale-100' :
                'bg-[#f3f4f6] border border-[#eceeed] text-outline/50 scale-100'
              }`}>
                {node.status === 'completed' && <Check size={12} />}
                {node.status === 'active' && <ChevronDown size={14} className="animate-bounce" />}
                {node.status === 'blocked' && <Lock size={10} />}
              </div>
              
              <Card className={`flex-1 transition-all ${
                node.status === 'active' ? 'bg-white border-chartreuse/50 shadow-nested-card' : 
                node.status === 'blocked' ? 'opacity-50 bg-[#f9f9f9] shadow-none' : 'shadow-none bg-[#fbfbfb]'
              }`}>
                <div className="flex justify-between items-center">
                  <h3 className={`text-headline-sm ${node.status === 'active' ? 'text-matte-charcoal' : 'text-on-surface-variant'}`}>
                    {node.title}
                  </h3>
                  <span className="text-label-sm uppercase tracking-wider text-outline px-2 py-1 bg-[#f3f4f6] rounded-md border border-[#eceeed]">
                    {node.status}
                  </span>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

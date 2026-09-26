import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Compass, LogOut, Crosshair, PenTool, BarChart } from 'lucide-react';
import { cn } from '../../utils/utils';

export const AppLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Skill Gap', path: '/skill-gap', icon: Crosshair },
    { name: 'GPS', path: '/placement-gps', icon: Compass },
    { name: 'Practice', path: '/practice', icon: PenTool },
    { name: 'Analytics', path: '/analytics', icon: BarChart },
  ];

  return (
    <div className="min-h-screen bg-sage-slate p-3 md:p-5 flex flex-col md:flex-row gap-5">
      {/* Sidebar Navigation */}
      <nav className="fixed bottom-3 left-4 right-4 md:static md:w-[72px] bg-matte-charcoal rounded-full md:rounded-full py-2 px-4 md:px-0 md:py-6 flex md:flex-col items-center justify-between shadow-charcoal-dock z-50 order-2 md:order-1">
        <div className="flex md:flex-col items-center gap-2 w-full justify-between md:justify-start">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname.startsWith(item.path);
            return (
              <button
                key={item.name}
                onClick={() => navigate(item.path)}
                className={cn(
                  "w-11 h-11 rounded-full flex items-center justify-center transition-all group relative",
                  isActive ? "bg-chartreuse text-[#121316]" : "text-[#8a8f98] hover:bg-[#26292f]"
                )}
                title={item.name}
              >
                <Icon size={20} className={cn(isActive && "text-[#121316]")} />
                {isActive && (
                  <span className="absolute -bottom-1 md:-right-1 md:bottom-auto md:top-1/2 md:-translate-y-1/2 w-1.5 h-1.5 bg-chartreuse rounded-full md:hidden"></span>
                )}
              </button>
            );
          })}
        </div>
        <button className="hidden md:flex w-11 h-11 rounded-full items-center justify-center text-[#8a8f98] hover:bg-[#26292f] transition-all">
          <LogOut size={20} />
        </button>
      </nav>

      {/* Main Workspace Area */}
      <main className="flex-1 bg-porcelain rounded-3xl md:rounded-[32px] overflow-hidden shadow-low-elevation flex flex-col items-center order-1 md:order-2 h-[calc(100vh-6rem)] md:h-[calc(100vh-2.5rem)] mb-16 md:mb-0">
        <div className="w-full h-full overflow-y-auto w-full p-4 md:p-8 max-w-7xl mx-auto pb-[100px]">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

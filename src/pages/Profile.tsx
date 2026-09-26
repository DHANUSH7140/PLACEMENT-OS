import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { User, LogOut } from 'lucide-react';
import { getAuth, signOut } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';

export const Profile = () => {
  const navigate = useNavigate();
  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center border-b border-[#eceeed] pb-6">
        <h1 className="text-headline-xl text-matte-charcoal flex items-center gap-3">
          <User size={32} /> User Profile
        </h1>
        <Button variant="ghost" onClick={async () => {
          try {
             await signOut(getAuth());
             navigate('/login');
          } catch(e) {}
        }} className="text-danger hover:bg-danger/10 hover:text-danger gap-2">
          <LogOut size={16}/> Logout
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="flex flex-col gap-4">
          <h2 className="text-headline-sm">Personal Info</h2>
          <Input label="Name" defaultValue="Jane Doe" />
          <Input label="Email" defaultValue="jane.doe@university.edu" disabled />
          <Input label="University" defaultValue="Tech State University" />
          <Input label="Graduation Year" defaultValue="2027" type="number" />
        </Card>

        <Card className="flex flex-col gap-4">
          <h2 className="text-headline-sm">Preparation State</h2>
          <Input label="Placement Timeline (Months)" defaultValue="6" type="number" />
          <Input label="Daily Commitment (Minutes)" defaultValue="120" type="number" />
          <div>
            <label className="text-label-md text-on-surface-variant block mb-2">Target Roles</label>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-[#121316] text-white rounded-md text-body-sm">Software Engineer</span>
              <span className="px-3 py-1 bg-[#121316] text-white rounded-md text-body-sm">Backend Developer</span>
            </div>
          </div>
        </Card>
      </div>

      <div className="flex justify-end pt-4">
         <Button>Save Changes</Button>
      </div>
    </div>
  );
};

export interface UserProfile {
  uid?: string;
  name?: string;
  email?: string;
  targetRoles: string[];
  targetCompanies: string[];
  skills: string[];
  programmingLanguages: string[];
  dailyPreparationTime: number; // in hours or minutes
  placementTimeline: number; // in months
  experienceLevel: string;
}

export interface DimensionData {
  title: string;
  score: number;
  trend: 'up' | 'down' | 'flat';
  status: 'good' | 'warning' | 'critical';
  recommendedAction: string;
}

export interface DashboardData {
  readinessScore: number;
  dimensions: DimensionData[];
  strengths: string[];
  criticalGaps: string[];
  riskAreas: string[];
  mission: MissionData;
  nextBestAction: string;
}

export interface MissionTask {
  id: string;
  type: 'learn' | 'practice' | 'validate';
  title: string;
  description: string;
  status: 'pending' | 'active' | 'completed';
}

export interface MissionData {
  title: string;
  description: string;
  tasks: MissionTask[];
  estimatedTime: number; // in minutes
  status: 'pending' | 'active' | 'completed';
}

export interface SkillGap {
  topic: string;
  currentScore: number;
  targetScore: number;
  priority: 'High' | 'Medium' | 'Low';
  status: 'critical' | 'warning' | 'good';
  trend: 'up' | 'down' | 'flat';
  recommendedTopics: string[];
}

export interface PlacementRouteNode {
  id: string;
  title: string;
  status: 'completed' | 'active' | 'upcoming' | 'blocked';
}

export interface PlacementRouteData {
  currentNode: string;
  nodes: PlacementRouteNode[];
  target: string;
  reasonForChange?: string;
}

export interface PracticeQuestion {
  id: string;
  question: string;
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard';
  questionType: 'mcq' | 'coding' | 'sql' | 'theory' | 'debugging' | 'aptitude';
  options?: string[];
  codeTemplate?: string;
  sqlSchema?: string;
  companyTags: string[];
  roleTags: string[];
}

export interface PracticeEvaluation {
  score: number;
  correctness: number;
  approach?: number;
  understanding?: number;
  explanation: string;
  mistakeType?: string;
  whyItHappened?: string;
  correctConcept?: string;
  recommendedTopic?: string;
  recommendedAction?: string;
}

export interface Mistake {
  id: string;
  topic: string;
  question: string;
  mistakeType: string;
  whyItHappened: string;
  correctConcept: string;
  recommendedRemediation: string;
  attemptCount: number;
  status: 'unresolved' | 'fixed';
  createdAt: string;
}

export interface InterviewResult {
  scores: {
    correctness: number;
    technicalDepth: number;
    clarity: number;
    relevance: number;
    structure: number;
    conciseness: number;
  };
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  nextBestAction: string;
}

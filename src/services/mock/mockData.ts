import type { DimensionData, Mistake, MissionTask, PracticeQuestion } from '../../types';

export const MOCK_DIMENSIONS: DimensionData[] = [
  { title: 'Aptitude', score: 78, trend: 'up', status: 'good', recommendedAction: 'Maintain current practice rate' },
  { title: 'DSA', score: 64, trend: 'flat', status: 'warning', recommendedAction: 'Focus on Trees and Graphs' },
  { title: 'CS Fundamentals', score: 72, trend: 'up', status: 'good', recommendedAction: 'Review OS concepts' },
  { title: 'SQL', score: 81, trend: 'up', status: 'good', recommendedAction: 'Ready for advanced queries' },
  { title: 'Communication', score: 75, trend: 'flat', status: 'good', recommendedAction: 'Practice behavioral interviews' },
  { title: 'Interview', score: 58, trend: 'down', status: 'critical', recommendedAction: 'Schedule a mock interview' },
];

export const MOCK_STRENGTHS = ['SQL', 'Aptitude', 'Resume'];
export const MOCK_CRITICAL_GAPS = ['Tree Traversal', 'Graph Algorithms', 'System Design'];
export const MOCK_RISK_AREAS = ['Interview performance', 'DSA consistency'];

export const MOCK_MISSION_TASKS: MissionTask[] = [
  { id: '1', type: 'learn', title: 'Tree Traversal Fundamentals', description: 'Review the theory behind DFS, BFS, pre-order, and post-order traversal.', status: 'completed' },
  { id: '2', type: 'practice', title: '5 Tree Traversal Questions', description: 'Complete 5 practice questions targeting your weakest tree concepts.', status: 'active' },
  { id: '3', type: 'validate', title: 'Mini Assessment', description: 'Take a short assessment to prove mastery of Tree Traversal.', status: 'pending' }
];

export const MOCK_PRACTICE_QUESTIONS: PracticeQuestion[] = [
  {
    id: 'q1',
    question: 'Given the root of a binary tree, return the level order traversal of its nodes values.',
    topic: 'Tree Traversal',
    difficulty: 'medium',
    questionType: 'coding',
    companyTags: ['Google', 'Amazon', 'Microsoft'],
    roleTags: ['Software Engineer', 'Backend Developer'],
    codeTemplate: 'function levelOrder(root) {\n  // write your code here\n}'
  },
  {
    id: 'q2',
    question: 'Write a SQL query to find the second highest salary from the Employee table.',
    topic: 'SQL',
    difficulty: 'medium',
    questionType: 'sql',
    companyTags: ['Amazon', 'Meta'],
    roleTags: ['Data Analyst', 'Software Engineer'],
    sqlSchema: 'CREATE TABLE Employee (Id INT, Salary INT);'
  }
];

export const MOCK_MISTAKES: Mistake[] = [
  {
    id: 'm1',
    topic: 'Tree Traversal',
    question: 'Level order traversal bug',
    mistakeType: 'Conceptual Gap',
    whyItHappened: 'Did not correctly initialize the queue with the root node before starting the loop.',
    correctConcept: 'Always push the root object and manage a while(queue.length) state.',
    recommendedRemediation: 'Practice 3 BFS problems focusing strictly on state initialization.',
    attemptCount: 2,
    status: 'unresolved',
    createdAt: new Date().toISOString()
  }
];

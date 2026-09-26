import { isMockAPI, delay } from './client';
import type { DashboardData, SkillGap, PlacementRouteData, MissionData } from '../../types';
import { MOCK_DIMENSIONS, MOCK_STRENGTHS, MOCK_CRITICAL_GAPS, MOCK_RISK_AREAS, MOCK_MISSION_TASKS } from '../mock/mockData';

export async function getDashboard(): Promise<DashboardData> {
  if (isMockAPI) {
    await delay(600);
    return {
      readinessScore: 72,
      dimensions: MOCK_DIMENSIONS,
      strengths: MOCK_STRENGTHS,
      criticalGaps: MOCK_CRITICAL_GAPS,
      riskAreas: MOCK_RISK_AREAS,
      mission: {
        title: 'Improve Tree Traversal',
        description: 'Targeting your lowest dimensions based on recent practice attempts.',
        tasks: MOCK_MISSION_TASKS,
        estimatedTime: 45,
        status: 'active'
      },
      nextBestAction: 'Practice 5 Tree Traversal questions'
    };
  }
  // TODO: Add real API implementation using fetch and VITE_API_BASE_URL
  throw new Error("Real API not implemented");
}

export async function getSkillGaps(): Promise<SkillGap[]> {
  if (isMockAPI) {
    await delay(500);
    return [
      {
        topic: 'Tree Traversal',
        currentScore: 42,
        targetScore: 70,
        priority: 'High',
        status: 'critical',
        trend: 'down',
        recommendedTopics: ['Tree Fundamentals', 'DFS/BFS', 'Binary Trees', 'BST']
      },
      {
        topic: 'Graph Algorithms',
        currentScore: 55,
        targetScore: 75,
        priority: 'High',
        status: 'warning',
        trend: 'flat',
        recommendedTopics: ['Dijkstra', 'Topological Sort']
      },
      {
        topic: 'System Design',
        currentScore: 60,
        targetScore: 80,
        priority: 'Medium',
        status: 'warning',
        trend: 'up',
        recommendedTopics: ['Caching', 'Load Balancing']
      }
    ];
  }
  throw new Error("Real API not implemented");
}

export async function getPlacementRoute(): Promise<PlacementRouteData> {
  if (isMockAPI) {
    await delay(700);
    return {
      currentNode: 'Tree Fundamentals',
      nodes: [
        { id: '1', title: 'Arrays', status: 'completed' },
        { id: '2', title: 'Strings', status: 'completed' },
        { id: '3', title: 'Tree Fundamentals', status: 'active' },
        { id: '4', title: 'DFS/BFS', status: 'upcoming' },
        { id: '5', title: 'BST', status: 'upcoming' },
        { id: '6', title: 'Practice', status: 'upcoming' },
        { id: '7', title: 'Graphs', status: 'blocked' },
        { id: '8', title: 'Interview', status: 'blocked' }
      ],
      target: 'Software Engineer',
      reasonForChange: 'Tree assessment score: 42%\n\nThe preparation route has been recalculated to focus on Tree fundamentals before progressing.'
    };
  }
  throw new Error("Real API not implemented");
}

export async function getMission(): Promise<MissionData> {
  if (isMockAPI) {
    await delay(400);
    return {
      title: 'Improve Tree Traversal',
      description: 'Strengthen core understanding of trees based on the recent assessment.',
      tasks: MOCK_MISSION_TASKS,
      estimatedTime: 45,
      status: 'active'
    };
  }
  throw new Error("Real API not implemented");
}

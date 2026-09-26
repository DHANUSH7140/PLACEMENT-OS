import { isMockAPI, delay } from './client';
import type { PracticeQuestion, PracticeEvaluation } from '../../types';

export async function startAssessment(): Promise<{ assessmentId: string, totalQuestions: number, timeLimit: number }> {
  if (isMockAPI) {
    await delay(1000);
    return {
      assessmentId: 'assess_' + Date.now(),
      totalQuestions: 5,
      timeLimit: 30 // minutes
    };
  }
  throw new Error("Real API not implemented");
}

let mockOffset = 0; // simplistic mock logic

export async function getAssessmentQuestions(assessmentId: string): Promise<PracticeQuestion[]> {
  if (isMockAPI) {
    await delay(800);
    return [
      {
        id: 'a1',
        question: 'What is the worst-case time complexity of QuickSort?',
        topic: 'Algorithms',
        difficulty: 'medium',
        questionType: 'mcq',
        options: ['O(N log N)', 'O(N^2)', 'O(N)', 'O(log N)'],
        companyTags: [],
        roleTags: []
      },
      {
        id: 'a2',
        question: 'Explain the difference between clustered and non-clustered index.',
        topic: 'SQL',
        difficulty: 'medium',
        questionType: 'theory',
        companyTags: [],
        roleTags: []
      }
    ]; // Simulating paginated or full load of questions
  }
  throw new Error("Real API not implemented");
}

export async function submitAssessmentQuestionAttempt(assessmentId: string, questionId: string, answer: string): Promise<boolean> {
  if (isMockAPI) {
    await delay(500);
    return true;
  }
  throw new Error("Real API not implemented");
}

export async function submitAssessment(assessmentId: string): Promise<boolean> {
  if (isMockAPI) {
    await delay(1500);
    return true; // Assessment finalized
  }
  throw new Error("Real API not implemented");
}

export async function getAssessmentResults(assessmentId: string): Promise<{ readinessScore: number, skillGaps: string[] }> {
  if (isMockAPI) {
    await delay(1000);
    return {
      readinessScore: 72,
      skillGaps: ['Tree Traversal', 'Graph Algorithms']
    };
  }
  throw new Error("Real API not implemented");
}

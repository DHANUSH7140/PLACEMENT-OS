import { isMockAPI, delay } from './client';
import type { PracticeQuestion, Mistake, PracticeEvaluation } from '../../types';
import { MOCK_PRACTICE_QUESTIONS, MOCK_MISTAKES } from '../mock/mockData';

export async function getPracticeQuestions(topic?: string): Promise<PracticeQuestion[]> {
  if (isMockAPI) {
    await delay(600);
    if (topic) {
      return MOCK_PRACTICE_QUESTIONS.filter(q => q.topic.toLowerCase().includes(topic.toLowerCase()));
    }
    return MOCK_PRACTICE_QUESTIONS;
  }
  throw new Error("Real API not implemented");
}

export async function getPracticeQuestion(id: string): Promise<PracticeQuestion> {
  if (isMockAPI) {
    await delay(400);
    const q = MOCK_PRACTICE_QUESTIONS.find(q => q.id === id);
    if (!q) throw new Error('Question not found');
    return q;
  }
  throw new Error("Real API not implemented");
}

export async function submitQuestionAttempt(id: string, answer: string): Promise<PracticeEvaluation> {
  if (isMockAPI) {
    await delay(1200);
    return {
      score: 68,
      correctness: 72,
      approach: 64,
      understanding: 70,
      mistakeType: 'Conceptual Gap',
      whyItHappened: 'Queue initialization omitted processing root first',
      correctConcept: 'Standard BFS structure requires root pre-loading in queue',
      explanation: 'Your approach is generally on track but missed the fundamental starting parameters for BFS traversal in javascript.',
      recommendedTopic: 'Review BFS vs DFS',
      recommendedAction: 'Practice 3 BFS problems checking specifically for this initialization.'
    };
  }
  throw new Error("Real API not implemented");
}

export async function getMistakes(): Promise<Mistake[]> {
  if (isMockAPI) {
    await delay(800);
    return MOCK_MISTAKES;
  }
  throw new Error("Real API not implemented");
}

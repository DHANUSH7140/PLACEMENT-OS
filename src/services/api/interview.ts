import { isMockAPI, delay } from './client';
import type { InterviewResult } from '../../types';

export async function startInterview(type: string, role: string, difficulty: string): Promise<{ id: string, initialMessage: string }> {
  if (isMockAPI) {
    await delay(1000);
    return {
      id: 'inv_' + Date.now(),
      initialMessage: `Welcome! Let's begin your ${type} interview for the ${role} role. Can you start by telling me about a recent challenging project you worked on?`
    };
  }
  throw new Error("Real API not implemented");
}

export async function submitInterviewAnswer(id: string, answer: string): Promise<{ replyMessage: string, isRoundComplete: boolean }> {
  if (isMockAPI) {
    await delay(1500);
    return {
      replyMessage: "That sounds interesting. Could you elaborate on how you handled the conflicting requirements with the stakeholder during that project?",
      isRoundComplete: false
    };
  }
  throw new Error("Real API not implemented");
}

export async function getInterviewResults(id: string): Promise<InterviewResult> {
  if (isMockAPI) {
    await delay(1500);
    return {
      scores: {
        correctness: 82,
        technicalDepth: 75,
        clarity: 85,
        relevance: 90,
        structure: 78,
        conciseness: 72
      },
      strengths: ['Great situational awareness', 'Strong communication of trade-offs'],
      weaknesses: ['Rambled slightly on technical details without structure', 'Did not mention the testing approach'],
      recommendations: ['Use the STAR method more strictly', 'Always briefly mention testing or validation'],
      nextBestAction: 'Review the STAR method framework'
    };
  }
  throw new Error("Real API not implemented");
}

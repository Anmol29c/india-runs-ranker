import json
import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, 'sample_candidates.json'), 'r') as f:
    candidates = json.load(f)

print(f"Total candidates: {len(candidates)}")

def score_candidate(candidate):
    score = 0
    profile = candidate.get('profile', {})
    redrob = candidate.get('redrob_signals', {})
    
    # Experience (25 points)
    exp = profile.get('years_of_experience', 0)
    if 5 <= exp <= 9: score += 25
    elif exp > 9: score += 15
    elif exp >= 3: score += 10
    
    # AI/ML Skills (30 points)
    skills = [s.lower() for s in profile.get('skills', [])]
    ai_skills = ['python','machine learning','llm','nlp','pytorch',
                 'tensorflow','transformers','ai','deep learning',
                 'langchain','openai','gemini','hugging face']
    for skill in ai_skills:
        if any(skill in s for s in skills):
            score += 3
    
    # GitHub activity (15 points)
    github = redrob.get('github_activity_score', 0)
    score += min(github, 15)
    
    # Job title (15 points)
    title = profile.get('current_title', '').lower()
    summary = profile.get('summary', '').lower()
    ai_keywords = ['ai','ml','machine learning','data scientist',
                   'nlp','deep learning','llm','research']
    if any(k in title for k in ai_keywords): score += 15
    elif any(k in summary for k in ai_keywords): score += 8
    elif 'engineer' in title: score += 5
    
    # Redrob signals (15 points)
    if redrob.get('verified_email'): score += 3
    if redrob.get('linkedin_connected'): score += 3
    score += min(redrob.get('endorsements_received', 0) // 10, 5)
    score += min(redrob.get('interview_completion_rate', 0) * 4, 4)
    
    return round(score, 2)

results = []
for candidate in candidates:
    score = score_candidate(candidate)
    results.append({
        'candidate_id': candidate['candidate_id'],
        'score': score,
        'name': candidate.get('profile', {}).get('anonymized_name', 'Unknown'),
        'title': candidate.get('profile', {}).get('current_title', 'Unknown')
    })

results.sort(key=lambda x: x['score'], reverse=True)

print("\nTOP 10 CANDIDATES:")
print("-" * 60)
for i, r in enumerate(results[:10], 1):
    print(f"{i}. {r['name']} | {r['title']} | Score: {r['score']}")

output_path = os.path.join(current_dir, 'ranked_output.csv')
with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['rank', 'candidate_id', 'score'])
    for i, r in enumerate(results, 1):
        writer.writerow([i, r['candidate_id'], r['score']])

print(f"\nOutput saved: ranked_output.csv")
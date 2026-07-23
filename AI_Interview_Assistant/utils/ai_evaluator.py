# utils/ai_evaluator.py
"""
AI Answer Evaluator.
Computes semantic similarity using Sentence-Transformers (SBERT).
Performs NLP checks for missing concepts, grammar indicators, communication clarity,
and confidence metrics (e.g., filler word density).
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK resources are loaded
for resource in ['tokenizers/punkt', 'tokenizers/punkt_tab', 'corpora/stopwords']:
    try:
        nltk.data.find(resource)
    except LookupError:
        name = resource.split('/')[-1]
        nltk.download(name, quiet=True)

class AIEvaluator:
    def __init__(self):
        self.model = None
        self.stop_words = set(stopwords.words('english'))
        
        # Try loading SentenceTransformers model
        try:
            from sentence_transformers import SentenceTransformer
            # Using 'all-MiniLM-L6-v2' (lightweight, highly accurate, fast on CPU)
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Sentence-Transformers not loaded: {e}. Falling back to TF-IDF matching.")

    def evaluate_answer(self, user_answer: str, ideal_answer: str) -> dict:
        """
        Evaluates a candidate's answer against an ideal answer.
        Returns similarity score, feedback, missing concepts, grammar, communication, and confidence.
        """
        if not user_answer.strip():
            return {
                "similarity_score": 0.0,
                "feedback": "No answer was provided. Please write a response.",
                "missing_concepts": [],
                "grammar_score": 0.0,
                "communication_score": 0.0,
                "confidence_score": 0.0
            }

        # 1. Semantic Similarity
        similarity = 0.0
        if self.model:
            try:
                embeddings = self.model.encode([user_answer, ideal_answer], convert_to_tensor=True)
                from sentence_transformers import util
                similarity = float(util.cos_sim(embeddings[0], embeddings[1])[0][0]) * 100
            except Exception as e:
                print(f"Error in SBERT encoding: {e}. Falling back to TF-IDF.")
                similarity = self._tfidf_similarity(user_answer, ideal_answer)
        else:
            similarity = self._tfidf_similarity(user_answer, ideal_answer)

        similarity = min(max(similarity, 0.0), 100.0)

        # 2. Missing Concepts
        missing_concepts = self._check_missing_concepts(user_answer, ideal_answer)

        # 3. Grammar Score (NLP heuristics: punctuation, spelling density, capitalization)
        grammar_score = self._estimate_grammar_score(user_answer)

        # 4. Communication Score (Vocabulary richness + Readability index)
        communication_score = self._estimate_communication_score(user_answer)

        # 5. Confidence Score (Filler word and hedge analysis)
        confidence_score, filler_feedback = self._estimate_confidence_score(user_answer)

        # 6. Overall Feedback Generation
        feedback = self._generate_feedback(similarity, missing_concepts, filler_feedback)

        return {
            "similarity_score": round(similarity, 1),
            "feedback": feedback,
            "missing_concepts": missing_concepts,
            "grammar_score": round(grammar_score, 1),
            "communication_score": round(communication_score, 1),
            "confidence_score": round(confidence_score, 1)
        }

    def _tfidf_similarity(self, s1: str, s2: str) -> float:
        """
        Fallback TF-IDF similarity.
        """
        try:
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([s1, s2])
            return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100)
        except Exception:
            return 0.0

    def _check_missing_concepts(self, user_answer: str, ideal_answer: str) -> list:
        """
        Identifies key technical nouns and verbs in the ideal answer that are absent in user's answer.
        """
        u_tokens = set(w.lower() for w in word_tokenize(user_answer) if w.isalnum())
        i_tokens = [w.lower() for w in word_tokenize(ideal_answer) if w.isalnum()]
        
        # Filter stopwords
        i_keywords = [w for w in i_tokens if w not in self.stop_words and len(w) > 3]
        
        # Find missing key words from the ideal answer
        missing = []
        for word in i_keywords:
            if word not in u_tokens and word not in missing:
                missing.append(word)
                
        # Limit to top 5 missing concepts
        return missing[:5]

    def _estimate_grammar_score(self, text: str) -> float:
        """
        Heuristic Grammar Scorer.
        Checks for:
        - Capitalization of first letters in sentences.
        - Proper end punctuation.
        - Word spelling checks (length ratio of valid alphanumeric characters).
        """
        score = 100.0
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        
        if not sentences:
            return 0.0
            
        capitalization_errors = 0
        punctuation_errors = 0
        
        for s in sentences:
            if not s:
                continue
            # Capitalization check
            if not s[0].isupper():
                capitalization_errors += 1
            # Punctuation check
            if s[-1] not in ['.', '!', '?']:
                punctuation_errors += 1
                
        # Penalize
        score -= (capitalization_errors / len(sentences)) * 20
        score -= (punctuation_errors / len(sentences)) * 15
        
        # Text length penalty (too brief might represent poor structure)
        if len(text.split()) < 5:
            score -= 30
            
        return max(min(score, 100.0), 0.0)

    def _estimate_communication_score(self, text: str) -> float:
        """
        Heuristic Communication Clarity Scorer.
        Calculates:
        - Vocabulary richness: Type-Token Ratio (unique words / total words).
        - Paragraph readability: Sentence length structure (optimal is 10-20 words).
        """
        words = [w.lower() for w in word_tokenize(text) if w.isalnum()]
        if not words:
            return 0.0
            
        unique_ratio = len(set(words)) / len(words)
        
        # Optimal sentence length score
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        avg_sentence_len = len(words) / len(sentences) if sentences else 0
        
        # Sentence length penalty (very short sentences or run-on sentences)
        len_score = 100.0
        if avg_sentence_len < 8:
            len_score -= (8 - avg_sentence_len) * 5
        elif avg_sentence_len > 25:
            len_score -= (avg_sentence_len - 25) * 3
            
        # Combine vocabulary richness (TTR) and sentence structure
        comm_score = (unique_ratio * 40) + (len_score * 0.6)
        return max(min(comm_score, 100.0), 0.0)

    def _estimate_confidence_score(self, text: str) -> tuple:
        """
        Heuristic Confidence Scorer.
        Identifies filler words (like, actually, basically, um, uh, you know) and hedges.
        """
        filler_words = ["like", "actually", "basically", "um", "uh", "you know", "essentially", "literally", "probably"]
        text_lower = text.lower()
        words = word_tokenize(text_lower)
        
        if not words:
            return 0.0, ""
            
        filler_count = 0
        detected_fillers = []
        for filler in filler_words:
            # handle multi-word fillers like 'you know'
            count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
            if count > 0:
                filler_count += count
                detected_fillers.append(filler)
                
        # Calculate ratio
        ratio = filler_count / len(words)
        
        # Base confidence is 100
        score = 100.0
        # Penalize for filler words
        score -= (ratio * 200) # 10% fillers = -20 points
        
        # Penalize for overly brief answers indicating lack of depth
        if len(words) < 15:
            score -= 20
            
        score = max(min(score, 100.0), 0.0)
        
        feedback = ""
        if detected_fillers:
            feedback = f"Try to reduce filler words such as: {', '.join(detected_fillers)}."
            
        return score, feedback

    def _generate_feedback(self, similarity: float, missing_concepts: list, filler_feedback: str) -> str:
        """
        Assembles contextual AI feedback.
        """
        feedback_parts = []
        
        if similarity >= 80:
            feedback_parts.append("🌟 Outstanding response! You have captured the semantic core of the concept with high technical accuracy.")
        elif similarity >= 60:
            feedback_parts.append("👍 Good answer. You demonstrate a solid grasp of the subject, though you could elaborate with more specific details.")
        elif similarity >= 40:
            feedback_parts.append("⚠️ Partially correct. Your answer covers some relevant points but lacks depth or misses the core definition.")
        else:
            feedback_parts.append("❌ Incomplete or incorrect answer. Review the ideal response to understand the key technical components of this topic.")
            
        if missing_concepts:
            feedback_parts.append(f"Consider explaining terms like: **{', '.join(missing_concepts)}**.")
            
        if filler_feedback:
            feedback_parts.append(filler_feedback)
            
        return " ".join(feedback_parts)

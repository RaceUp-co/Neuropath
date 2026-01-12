"""
Analyseur de biais psychologiques utilisant l'IA
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger

from src.config import settings

# Charger la base de données des biais
BIASES_PATH = Path(__file__).parent.parent / "database" / "biases.json"

# Import OpenAI (gestion optionnelle)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


class BiasAnalyzer:
    """Analyseur de biais psychologiques pour les sites web"""
    
    def __init__(self):
        """Initialise l'analyseur"""
        self.biases_db = self._load_biases()
        if settings.openai_api_key and OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
                self.use_ai = True
            except Exception as e:
                logger.warning(f"Erreur initialisation OpenAI: {e}. Analyse basique uniquement.")
                self.use_ai = False
                self.client = None
        else:
            logger.warning("OpenAI non disponible. Analyse basique uniquement.")
            self.use_ai = False
            self.client = None
    
    def _load_biases(self) -> Dict:
        """Charge la base de données des biais"""
        try:
            with open(BIASES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement des biais: {e}")
            return {"biases": []}
    
    def analyze(self, scraped_data: Dict) -> Dict:
        """
        Analyse les données scrappées pour détecter les biais
        
        Args:
            scraped_data: Données scrappées du site
            
        Returns:
            Résultats de l'analyse
        """
        results = {
            'biases_detected': [],
            'scores': {},
            'recommendations': [],
            'priority_fixes': []
        }
        
        # Analyse basique (pattern matching)
        basic_analysis = self._basic_analysis(scraped_data)
        
        # Analyse IA si disponible
        if self.use_ai:
            ai_analysis = self._ai_analysis(scraped_data)
            # Fusionner les résultats
            results = self._merge_analyses(basic_analysis, ai_analysis)
        else:
            results = basic_analysis
        
        # Calculer les scores globaux
        results['overall_score'] = self._calculate_overall_score(results)
        
        # Générer les recommandations prioritaires
        results['priority_fixes'] = self._get_priority_fixes(results)
        
        return results
    
    def _basic_analysis(self, data: Dict) -> Dict:
        """Analyse basique avec pattern matching"""
        biases_detected = []
        scores = {}
        
        # Ancrage (prix barrés, comparaisons)
        prices = data.get('prices', [])
        if len(prices) > 1:
            biases_detected.append({
                'id': 'anchoring',
                'confidence': 0.7,
                'evidence': f"{len(prices)} prix détectés, possibilité d'ancrage"
            })
            scores['anchoring'] = 0.7
        
        # Surcharge de choix (navigation)
        nav_items = data.get('stats', {}).get('navigation_items', 0)
        if nav_items > 9:
            biases_detected.append({
                'id': 'choice_overload',
                'confidence': 0.8,
                'evidence': f"{nav_items} éléments de navigation (recommandé: <9)"
            })
            scores['choice_overload'] = 0.8
        
        # Preuve sociale (témoignages, compteurs)
        text = data.get('text', '').lower()
        social_proof_keywords = ['témoignage', 'testimonial', 'utilisateurs', 'clients', 'avis', 'review', 'étoiles', 'stars']
        social_proof_count = sum(1 for keyword in social_proof_keywords if keyword in text)
        if social_proof_count >= 3:
            biases_detected.append({
                'id': 'social_proof',
                'confidence': 0.6,
                'evidence': f"Éléments de preuve sociale détectés ({social_proof_count} mentions)"
            })
            scores['social_proof'] = 0.6
        
        # Aversion à la perte (mots d'urgence)
        urgency_keywords = ['limité', 'urgent', 'rapide', 'ne ratez pas', "dans peu de temps", 'stock limité', 'limited', 'hurry', 'don\'t miss']
        urgency_count = sum(1 for keyword in urgency_keywords if keyword in text)
        if urgency_count >= 2:
            biases_detected.append({
                'id': 'loss_aversion',
                'confidence': 0.7,
                'evidence': f"Mots d'urgence détectés ({urgency_count} occurrences)"
            })
            scores['loss_aversion'] = 0.7
        
        # Rareté (stock limité, exclusivité)
        scarcity_keywords = ['exclusif', 'limité', 'seulement', 'restant', 'exclusive', 'limited', 'only', 'remaining']
        scarcity_count = sum(1 for keyword in scarcity_keywords if keyword in text)
        if scarcity_count >= 2:
            biases_detected.append({
                'id': 'scarcity',
                'confidence': 0.7,
                'evidence': f"Éléments de rareté détectés ({scarcity_count} mentions)"
            })
            scores['scarcity'] = 0.7
        
        # Charge cognitive (nombre d'éléments)
        stats = data.get('stats', {})
        total_elements = stats.get('total_links', 0) + stats.get('total_images', 0) + stats.get('total_ctas', 0)
        if total_elements > 150:
            biases_detected.append({
                'id': 'cognitive_load',
                'confidence': 0.6,
                'evidence': f"{total_elements} éléments interactifs (potentielle surcharge)"
            })
            scores['cognitive_load'] = 0.6
        
        return {
            'biases_detected': biases_detected,
            'scores': scores
        }
    
    def _ai_analysis(self, data: Dict) -> Dict:
        """Analyse avec IA (GPT)"""
        if not self.use_ai:
            return {'biases_detected': [], 'scores': {}}
        
        try:
            # Préparer le contexte
            context = self._prepare_context(data)
            
            # Construire le prompt
            prompt = self._build_analysis_prompt(context)
            
            # Appel API OpenAI
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert en psychologie cognitive et UX design. Tu analyses des sites web pour détecter l'utilisation de biais psychologiques."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.openai_temperature,
                max_tokens=settings.max_tokens
            )
            
            # Parser la réponse (JSON attendu)
            ai_result = response.choices[0].message.content
            
            # Essayer de parser comme JSON
            try:
                parsed = json.loads(ai_result)
                return parsed
            except:
                # Si ce n'est pas du JSON, faire une analyse basique du texte
                logger.warning("Réponse IA non-JSON, utilisation de l'analyse basique")
                return {'biases_detected': [], 'scores': {}}
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse IA: {e}")
            return {'biases_detected': [], 'scores': {}}
    
    def _prepare_context(self, data: Dict) -> str:
        """Prépare le contexte pour l'IA"""
        context_parts = []
        
        # Titres
        titles = data.get('titles', {})
        if titles.get('h1'):
            context_parts.append(f"Titres H1: {', '.join(titles['h1'][:5])}")
        
        # CTAs
        ctas = data.get('ctas', [])[:20]
        cta_texts = [cta['text'] for cta in ctas if cta.get('text')]
        if cta_texts:
            context_parts.append(f"CTAs: {', '.join(cta_texts[:10])}")
        
        # Texte (extrait)
        text = data.get('text', '')[:2000]  # Limiter
        if text:
            context_parts.append(f"Texte: {text}")
        
        # Navigation
        nav = data.get('navigation', [])
        if nav:
            nav_items = []
            for nav_list in nav[:3]:
                nav_items.extend(nav_list[:10])
            if nav_items:
                context_parts.append(f"Navigation: {', '.join(nav_items[:20])}")
        
        # Prix
        prices = data.get('prices', [])[:10]
        if prices:
            context_parts.append(f"Prix: {', '.join(prices)}")
        
        return "\n".join(context_parts)
    
    def _build_analysis_prompt(self, context: str) -> str:
        """Construit le prompt d'analyse"""
        biases_list = [bias['name'] for bias in self.biases_db.get('biases', [])[:20]]
        
        prompt = f"""Analyse ce site web et détecte les biais psychologiques utilisés.

Contexte du site:
{context}

Biais à rechercher (liste non exhaustive): {', '.join(biases_list)}

Retourne un JSON avec cette structure:
{{
    "biases_detected": [
        {{
            "id": "anchoring",
            "confidence": 0.8,
            "evidence": "Description de la preuve"
        }}
    ],
    "scores": {{
        "anchoring": 0.8,
        "social_proof": 0.6
    }}
}}

Soyez précis et ne détectez que les biais clairement présents."""
        
        return prompt
    
    def _merge_analyses(self, basic: Dict, ai: Dict) -> Dict:
        """Fusionne les analyses basique et IA"""
        merged_biases = basic.get('biases_detected', [])
        ai_biases = ai.get('biases_detected', [])
        
        # Ajouter les biais IA qui ne sont pas déjà détectés
        existing_ids = {b['id'] for b in merged_biases}
        for bias in ai_biases:
            if bias['id'] not in existing_ids:
                merged_biases.append(bias)
        
        # Fusionner les scores (prendre le max)
        merged_scores = basic.get('scores', {})
        ai_scores = ai.get('scores', {})
        for bias_id, score in ai_scores.items():
            merged_scores[bias_id] = max(merged_scores.get(bias_id, 0), score)
        
        return {
            'biases_detected': merged_biases,
            'scores': merged_scores
        }
    
    def _calculate_overall_score(self, results: Dict) -> float:
        """Calcule un score global"""
        scores = results.get('scores', {})
        if not scores:
            return 0.0
        
        # Moyenne pondérée par l'impact
        total = 0.0
        weights = 0.0
        
        for bias_id, score in scores.items():
            # Trouver le biais dans la DB
            bias_info = next((b for b in self.biases_db.get('biases', []) if b['id'] == bias_id), None)
            if bias_info:
                weight = {'high': 3, 'medium': 2, 'low': 1}.get(bias_info.get('impact', 'medium'), 1)
            else:
                weight = 1
            
            total += score * weight
            weights += weight
        
        return total / weights if weights > 0 else 0.0
    
    def _get_priority_fixes(self, results: Dict) -> List[Dict]:
        """Génère les corrections prioritaires"""
        priority_fixes = []
        biases_db = {b['id']: b for b in self.biases_db.get('biases', [])}
        
        # Trier les biais par score et impact
        biases_with_scores = []
        for bias_result in results.get('biases_detected', []):
            bias_id = bias_result['id']
            score = bias_result.get('confidence', 0)
            bias_info = biases_db.get(bias_id)
            
            if bias_info:
                impact_weight = {'high': 3, 'medium': 2, 'low': 1}.get(bias_info.get('impact', 'medium'), 1)
                priority_score = score * impact_weight
                biases_with_scores.append({
                    'bias': bias_info,
                    'score': score,
                    'priority': priority_score,
                    'evidence': bias_result.get('evidence', '')
                })
        
        # Trier par priorité
        biases_with_scores.sort(key=lambda x: x['priority'], reverse=True)
        
        # Générer les recommandations
        for item in biases_with_scores[:5]:  # Top 5
            bias = item['bias']
            recommendations = bias.get('recommendations', [])
            
            priority_fixes.append({
                'bias_id': bias['id'],
                'bias_name': bias['name'],
                'priority_score': item['priority'],
                'current_score': item['score'],
                'issue': item['evidence'],
                'recommendations': recommendations,
                'impact': bias.get('impact', 'medium')
            })
        
        return priority_fixes

"""
Exemple de test simple pour Neuropath
"""
from src.scraper.web_scraper import WebScraper
from src.analyzer.bias_analyzer import BiasAnalyzer
from src.reports.report_generator import ReportGenerator

def test_basic_analysis():
    """Test basique sans API OpenAI"""
    print("Test d'analyse basique...")
    
    # Initialiser
    scraper = WebScraper()
    analyzer = BiasAnalyzer()
    report_generator = ReportGenerator()
    
    # Test URL (remplacer par une vraie URL pour tester)
    test_url = "https://example.com"
    
    try:
        # Scraping
        print(f"Scraping de {test_url}...")
        scraped_data = scraper.scrape_url(test_url, use_selenium=False)
        print(f"✓ Scraping réussi: {len(scraped_data.get('text', ''))} caractères")
        
        # Analyse
        print("Analyse des biais...")
        analysis_results = analyzer.analyze(scraped_data)
        print(f"✓ Analyse terminée: {len(analysis_results.get('biases_detected', []))} biais détectés")
        
        # Génération du rapport
        print("Génération du rapport...")
        report = report_generator.generate_report(test_url, scraped_data, analysis_results)
        print(f"✓ Rapport généré: {report.get('report_path', 'N/A')}")
        
        # Afficher le résumé
        summary = report.get('summary', {})
        print(f"\n=== Résumé ===")
        print(f"Score global: {summary.get('overall_score', 0):.2f}")
        print(f"Biais détectés: {summary.get('total_biases_detected', 0)}")
        print(f"Interprétation: {summary.get('interpretation', 'N/A')}")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_analysis()

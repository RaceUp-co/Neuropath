"""
Scraper web pour extraire le contenu HTML, CSS et texte d'un site
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Optional
import json
import time
from urllib.parse import urljoin, urlparse
from loguru import logger

from src.config import settings


class WebScraper:
    """Scraper pour extraire le contenu d'un site web"""
    
    def __init__(self, use_selenium: bool = False):
        """
        Initialise le scraper
        
        Args:
            use_selenium: Si True, utilise Selenium pour les sites JavaScript
        """
        self.use_selenium = use_selenium
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.user_agent
        })
        self.driver: Optional[webdriver.Chrome] = None
        
    def _init_selenium(self):
        """Initialise le driver Selenium si nécessaire"""
        if self.driver is None:
            chrome_options = Options()
            if settings.selenium_headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'user-agent={settings.user_agent}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                logger.warning(f"Impossible d'initialiser Selenium: {e}. Utilisation de requests uniquement.")
                self.use_selenium = False
    
    def _close_selenium(self):
        """Ferme le driver Selenium"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def scrape_url(self, url: str, use_selenium: Optional[bool] = None) -> Dict:
        """
        Scrape une URL et extrait les informations
        
        Args:
            url: URL à scraper
            use_selenium: Override pour l'utilisation de Selenium
            
        Returns:
            Dictionnaire avec le contenu extrait
        """
        if use_selenium is not None:
            self.use_selenium = use_selenium
        
        try:
            if self.use_selenium:
                return self._scrape_with_selenium(url)
            else:
                return self._scrape_with_requests(url)
        except Exception as e:
            logger.error(f"Erreur lors du scraping de {url}: {e}")
            # Fallback sur requests si Selenium échoue
            if self.use_selenium:
                logger.info("Tentative avec requests...")
                return self._scrape_with_requests(url)
            raise
    
    def _scrape_with_requests(self, url: str) -> Dict:
        """Scrape avec requests et BeautifulSoup"""
        response = self.session.get(url, timeout=settings.scraping_timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        return self._extract_content(soup, url)
    
    def _scrape_with_selenium(self, url: str) -> Dict:
        """Scrape avec Selenium pour les sites JavaScript"""
        self._init_selenium()
        
        try:
            self.driver.get(url)
            # Attendre le chargement
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)  # Attente supplémentaire pour le JS
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            return self._extract_content(soup, url)
        finally:
            self._close_selenium()
    
    def _extract_content(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extrait le contenu d'une page"""
        
        # HTML structure
        html_content = str(soup)
        
        # Texte
        # Supprimer scripts et styles
        for script in soup(["script", "style", "meta", "link"]):
            script.decompose()
        
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Titres
        titles = {
            'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
            'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
            'h3': [h.get_text(strip=True) for h in soup.find_all('h3')],
        }
        
        # CTAs (boutons et liens importants)
        ctas = []
        for button in soup.find_all(['button', 'a']):
            text = button.get_text(strip=True)
            if text:
                ctas.append({
                    'text': text,
                    'type': button.name,
                    'href': button.get('href', ''),
                    'class': button.get('class', [])
                })
        
        # Images avec alt text
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        # Liens
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                links.append({
                    'text': link.get_text(strip=True),
                    'href': full_url,
                    'internal': urlparse(full_url).netloc == urlparse(base_url).netloc
                })
        
        # CSS (styles inline et dans les balises style)
        css_content = []
        for style_tag in soup.find_all('style'):
            css_content.append(style_tag.string or '')
        
        # Styles inline (pour analyse de couleurs, etc.)
        inline_styles = []
        for element in soup.find_all(style=True):
            inline_styles.append({
                'tag': element.name,
                'style': element.get('style', ''),
                'class': element.get('class', [])
            })
        
        # Métadonnées
        meta = {}
        meta_tag = soup.find('meta', property='og:title')
        if meta_tag:
            meta['og_title'] = meta_tag.get('content', '')
        meta_tag = soup.find('meta', property='og:description')
        if meta_tag:
            meta['og_description'] = meta_tag.get('content', '')
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta['description'] = meta_tag.get('content', '')
        
        # Navigation (menus)
        navigation = []
        for nav in soup.find_all(['nav', 'ul', 'ol'], class_=lambda x: x and ('nav' in str(x).lower() or 'menu' in str(x).lower())):
            nav_items = []
            for item in nav.find_all(['li', 'a']):
                text = item.get_text(strip=True)
                if text:
                    nav_items.append(text)
            if nav_items:
                navigation.append(nav_items)
        
        # Prix (détection basique)
        prices = []
        price_patterns = soup.find_all(text=lambda x: x and ('€' in x or '$' in x or '£' in x))
        for price_text in price_patterns[:20]:  # Limiter à 20
            if any(char.isdigit() for char in price_text):
                prices.append(price_text.strip())
        
        # Formulaires
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'fields': []
            }
            for input_field in form.find_all(['input', 'textarea', 'select']):
                form_data['fields'].append({
                    'type': input_field.get('type', input_field.name),
                    'name': input_field.get('name', ''),
                    'placeholder': input_field.get('placeholder', ''),
                    'required': input_field.has_attr('required')
                })
            forms.append(form_data)
        
        return {
            'url': base_url,
            'html': html_content,
            'text': text_content,
            'titles': titles,
            'ctas': ctas[:50],  # Limiter
            'images': images[:100],
            'links': links[:200],
            'css': '\n'.join(css_content),
            'inline_styles': inline_styles[:100],
            'meta': meta,
            'navigation': navigation,
            'prices': prices,
            'forms': forms,
            'stats': {
                'total_words': len(text_content.split()),
                'total_links': len(links),
                'total_images': len(images),
                'total_ctas': len(ctas),
                'navigation_items': sum(len(nav) for nav in navigation),
                'total_forms': len(forms)
            }
        }
    
    def __del__(self):
        """Nettoyage"""
        self._close_selenium()

# Quotes Scraper

Este proyecto es un script de scraping y almacenamiento de citas, etiquetas y autores utilizando Scrapy para la extracción de datos, MySQL para el almacenamiento, y pytest para las pruebas unitarias.

## Características

- Scraping de citas, autores y etiquetas del sitio web "https://quotes.toscrape.com"
- Almacenamiento de datos en una base de datos MySQL
- Pruebas unitarias con pytest

## Requisitos

- Python 3.7+
- Scrapy
- MySQL
- mysql-connector-python
- pytest

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/AI-School-F5-P3/web_scraping_xiomara.git
   cd web_scraping_xiomara
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Configura tu base de datos MySQL y actualiza la información de conexión en `db.py`.

## Uso

### Scraping

Para ejecutar el spider de Scrapy:

```
scrapy crawl quotespider
```

### Pruebas

Para ejecutar las pruebas:

```
pytest
```

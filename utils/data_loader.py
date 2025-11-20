"""
Data Loader Module
==================

Handles loading and caching of JSON data files.
"""

import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Loads and caches JSON data files"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._cache = {}

    def load_json(self, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Load JSON file with optional caching

        Args:
            filename: Name of the JSON file
            use_cache: Whether to use cached data

        Returns:
            Dictionary containing the JSON data
        """
        if use_cache and filename in self._cache:
            return self._cache[filename]

        file_path = self.data_dir / filename

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if use_cache:
                self._cache[filename] = data

            logger.info(f"Loaded {filename} successfully")
            return data

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            raise

    def get_diseases(self) -> Dict[str, Any]:
        """Load disease database"""
        data = self.load_json('diseases.json')
        return data.get('diseases', {})

    def get_recommendations_config(self) -> Dict[str, Any]:
        """Load recommendations configuration"""
        return self.load_json('recommendations.json')

    def clear_cache(self):
        """Clear the data cache"""
        self._cache.clear()
        logger.info("Data cache cleared")

    def reload_data(self):
        """Reload all data from files"""
        self.clear_cache()
        self.get_diseases()
        self.get_recommendations_config()
        logger.info("All data reloaded")


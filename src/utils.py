import pandas as pd
import logging
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Р—Р°РіСЂСѓР·РєР° РїРµСЂРµРјРµРЅРЅС‹С… РѕРєСЂСѓР¶РµРЅРёСЏ
load_dotenv()

logger = logging.getLogger(__name__)


def load_transactions(filepath: str = "data/operations.xlsx") -> List[Dict[str, Any]]:
    """
    Р—Р°РіСЂСѓР¶Р°РµС‚ С‚СЂР°РЅР·Р°РєС†РёРё РёР· Excel С„Р°Р№Р»Р°.

    Args:
        filepath: РџСѓС‚СЊ Рє Excel С„Р°Р№Р»Сѓ

    Returns:
        РЎРїРёСЃРѕРє СЃР»РѕРІР°СЂРµР№ СЃ С‚СЂР°РЅР·Р°РєС†РёСЏРјРё
    """
    try:
        if not os.path.exists(filepath):
            logger.warning(f"Р¤Р°Р№Р» {filepath} РЅРµ РЅР°Р№РґРµРЅ. Р’РѕР·РІСЂР°С‰Р°СЋ РїСѓСЃС‚РѕР№ СЃРїРёСЃРѕРє.")
            return []

        df = pd.read_excel(filepath)
        logger.info(f"РЈСЃРїРµС€РЅРѕ РїСЂРѕС‡РёС‚Р°РЅРѕ {len(df)} С‚СЂР°РЅР·Р°РєС†РёР№ РёР· {filepath}")
        logger.info(f"РљРѕР»РѕРЅРєРё РІ РґР°РЅРЅС‹С…: {list(df.columns)}")

        # РљРѕРЅРІРµСЂС‚РёСЂСѓРµРј РґР°С‚С‹ РµСЃР»Рё РѕРЅРё РµСЃС‚СЊ
        date_columns = [col for col in df.columns if 'РґР°С‚Р°' in col.lower() or 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        return df.to_dict('records')

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё РґР°РЅРЅС‹С… РёР· {filepath}: {e}")
        return []


def load_settings(settings_file: str = ".env") -> Dict[str, str]:
    """
    Р—Р°РіСЂСѓР¶Р°РµС‚ РЅР°СЃС‚СЂРѕР№РєРё РёР· С„Р°Р№Р»Р°.

    Args:
        settings_file: РџСѓС‚СЊ Рє С„Р°Р№Р»Сѓ СЃ РЅР°СЃС‚СЂРѕР№РєР°РјРё

    Returns:
        РЎР»РѕРІР°СЂСЊ СЃ РЅР°СЃС‚СЂРѕР№РєР°РјРё
    """
    try:
        settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            settings[key.strip()] = value.strip()

        # Р”РѕР±Р°РІР»СЏРµРј РїРµСЂРµРјРµРЅРЅС‹Рµ РѕРєСЂСѓР¶РµРЅРёСЏ
        for key in ['API_KEY', 'EXCHANGE_API_KEY', 'STOCK_API_KEY']:
            env_value = os.getenv(key)
            if env_value:
                settings[key] = env_value

        logger.info(f"Р—Р°РіСЂСѓР¶РµРЅРѕ {len(settings)} РЅР°СЃС‚СЂРѕРµРє")
        return settings

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё РЅР°СЃС‚СЂРѕРµРє: {e}")
        return {}


def save_report(report_data: Dict[str, Any], filename_prefix: str) -> str:
    """
    РЎРѕС…СЂР°РЅСЏРµС‚ РѕС‚С‡РµС‚ РІ JSON С„Р°Р№Р».

    Args:
        report_data: Р”Р°РЅРЅС‹Рµ РѕС‚С‡РµС‚Р°
        filename_prefix: РџСЂРµС„РёРєСЃ РёРјРµРЅРё С„Р°Р№Р»Р°

    Returns:
        РџСѓС‚СЊ Рє СЃРѕС…СЂР°РЅРµРЅРЅРѕРјСѓ С„Р°Р№Р»Сѓ
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        logger.info(f"РћС‚С‡РµС‚ СЃРѕС…СЂР°РЅРµРЅ РІ С„Р°Р№Р»: {filename}")
        return filename

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° СЃРѕС…СЂР°РЅРµРЅРёСЏ РѕС‚С‡РµС‚Р°: {e}")
        return ""


def get_exchange_rates(currency_codes: List[str] = None) -> Dict[str, float]:
    """
    РџРѕР»СѓС‡Р°РµС‚ РєСѓСЂСЃС‹ РІР°Р»СЋС‚ (Р·Р°РіР»СѓС€РєР°).

    Args:
        currency_codes: РЎРїРёСЃРѕРє РєРѕРґРѕРІ РІР°Р»СЋС‚

    Returns:
        РЎР»РѕРІР°СЂСЊ СЃ РєСѓСЂСЃР°РјРё РІР°Р»СЋС‚
    """
    try:
        # Р—Р°РіР»СѓС€РєР° РґР»СЏ РґРµРјРѕРЅСЃС‚СЂР°С†РёРё
        # Р’ СЂРµР°Р»СЊРЅРѕРј РїСЂРёР»РѕР¶РµРЅРёРё Р·РґРµСЃСЊ Р±СѓРґРµС‚ API Р·Р°РїСЂРѕСЃ
        rates = {
            "USD": 90.5,
            "EUR": 98.2,
            "GBP": 114.3,
        }

        if currency_codes:
            rates = {code: rates.get(code, 0) for code in currency_codes}

        logger.info(f"РџРѕР»СѓС‡РµРЅС‹ РєСѓСЂСЃС‹ РґР»СЏ {len(rates)} РІР°Р»СЋС‚")
        return rates

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° РїРѕР»СѓС‡РµРЅРёСЏ РєСѓСЂСЃРѕРІ РІР°Р»СЋС‚: {e}")
        return {}


def get_stock_prices(stock_symbols: List[str] = None) -> Dict[str, float]:
    """
    РџРѕР»СѓС‡Р°РµС‚ С†РµРЅС‹ Р°РєС†РёР№ (Р·Р°РіР»СѓС€РєР°).

    Args:
        stock_symbols: РЎРїРёСЃРѕРє СЃРёРјРІРѕР»РѕРІ Р°РєС†РёР№

    Returns:
        РЎР»РѕРІР°СЂСЊ СЃ С†РµРЅР°РјРё Р°РєС†РёР№
    """
    try:
        # Р—Р°РіР»СѓС€РєР° РґР»СЏ РґРµРјРѕРЅСЃС‚СЂР°С†РёРё
        # Р’ СЂРµР°Р»СЊРЅРѕРј РїСЂРёР»РѕР¶РµРЅРёРё Р·РґРµСЃСЊ Р±СѓРґРµС‚ API Р·Р°РїСЂРѕСЃ
        prices = {
            "AAPL": 185.2,
            "GOOGL": 142.5,
            "MSFT": 374.5,
            "TSLA": 240.1,
            "AMZN": 154.9,
        }

        if stock_symbols:
            prices = {symbol: prices.get(symbol, 0) for symbol in stock_symbols}

        logger.info(f"РџРѕР»СѓС‡РµРЅС‹ С†РµРЅС‹ РґР»СЏ {len(prices)} Р°РєС†РёР№")
        return prices

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° РїРѕР»СѓС‡РµРЅРёСЏ С†РµРЅ Р°РєС†РёР№: {e}")
        return {}


def format_amount(amount: float, currency: str = "RUB") -> str:
    """
    Р¤РѕСЂРјР°С‚РёСЂСѓРµС‚ СЃСѓРјРјСѓ РґР»СЏ РІС‹РІРѕРґР°.

    Args:
        amount: РЎСѓРјРјР°
        currency: Р’Р°Р»СЋС‚Р°

    Returns:
        РћС‚С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРЅР°СЏ СЃС‚СЂРѕРєР°
    """
    return f"{amount:,.2f} {currency}".replace(",", " ").replace(".", ",")


def filter_by_date_range(
        transactions: List[Dict[str, Any]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_column: str = "Р”Р°С‚Р° РѕРїРµСЂР°С†РёРё"
) -> List[Dict[str, Any]]:
    """
    Р¤РёР»СЊС‚СЂСѓРµС‚ С‚СЂР°РЅР·Р°РєС†РёРё РїРѕ РґРёР°РїР°Р·РѕРЅСѓ РґР°С‚.

    Args:
        transactions: РЎРїРёСЃРѕРє С‚СЂР°РЅР·Р°РєС†РёР№
        start_date: РќР°С‡Р°Р»СЊРЅР°СЏ РґР°С‚Р° (YYYY-MM-DD)
        end_date: РљРѕРЅРµС‡РЅР°СЏ РґР°С‚Р° (YYYY-MM-DD)
        date_column: РќР°Р·РІР°РЅРёРµ РєРѕР»РѕРЅРєРё СЃ РґР°С‚РѕР№

    Returns:
        РћС‚С„РёР»СЊС‚СЂРѕРІР°РЅРЅС‹Р№ СЃРїРёСЃРѕРє С‚СЂР°РЅР·Р°РєС†РёР№
    """
    try:
        if not transactions:
            return []

        filtered = transactions.copy()

        if start_date:
            start = pd.to_datetime(start_date)
            filtered = [t for t in filtered if pd.to_datetime(t.get(date_column, '')) >= start]

        if end_date:
            end = pd.to_datetime(end_date)
            filtered = [t for t in filtered if pd.to_datetime(t.get(date_column, '')) <= end]

        logger.info(f"РћС‚С„РёР»СЊС‚СЂРѕРІР°РЅРѕ {len(filtered)} РёР· {len(transactions)} С‚СЂР°РЅР·Р°РєС†РёР№")
        return filtered

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° С„РёР»СЊС‚СЂР°С†РёРё РїРѕ РґР°С‚Рµ: {e}")
        return transactions


def calculate_statistics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Р Р°СЃСЃС‡РёС‚С‹РІР°РµС‚ Р±Р°Р·РѕРІСѓСЋ СЃС‚Р°С‚РёСЃС‚РёРєСѓ РїРѕ С‚СЂР°РЅР·Р°РєС†РёСЏРј.

    Args:
        transactions: РЎРїРёСЃРѕРє С‚СЂР°РЅР·Р°РєС†РёР№

    Returns:
        РЎР»РѕРІР°СЂСЊ СЃРѕ СЃС‚Р°С‚РёСЃС‚РёРєРѕР№
    """
    try:
        if not transactions:
            return {
                "total_count": 0,
                "total_amount": 0,
                "avg_amount": 0,
                "min_amount": 0,
                "max_amount": 0,
            }

        amounts = [t.get("РЎСѓРјРјР° РѕРїРµСЂР°С†РёРё", 0) for t in transactions]

        return {
            "total_count": len(transactions),
            "total_amount": sum(amounts),
            "avg_amount": sum(amounts) / len(amounts) if amounts else 0,
            "min_amount": min(amounts) if amounts else 0,
            "max_amount": max(amounts) if amounts else 0,
        }

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° СЂР°СЃС‡РµС‚Р° СЃС‚Р°С‚РёСЃС‚РёРєРё: {e}")
        return {}


def read_excel_file(file_path: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Р§РёС‚Р°РµС‚ Excel С„Р°Р№Р» Рё РІРѕР·РІСЂР°С‰Р°РµС‚ DataFrame.

    Args:
        file_path: РџСѓС‚СЊ Рє Excel С„Р°Р№Р»Сѓ

    Returns:
        DataFrame СЃ РґР°РЅРЅС‹РјРё
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Р¤Р°Р№Р» {file_path} РЅРµ РЅР°Р№РґРµРЅ")

        df = pd.read_excel(file_path)
        logger.info(f"РџСЂРѕС‡РёС‚Р°РЅ С„Р°Р№Р» {file_path}. РЎС‚СЂРѕРє: {len(df)}, РљРѕР»РѕРЅРѕРє: {len(df.columns)}")
        return df

    except Exception as e:
        logger.error(f"РћС€РёР±РєР° С‡С‚РµРЅРёСЏ С„Р°Р№Р»Р° {file_path}: {e}")
        raise

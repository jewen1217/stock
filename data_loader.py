import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
from typing import Optional


class DataLoader:
    """
    주식 데이터를 불러오는 클래스
    """
    
    def __init__(self):
        pass
    
    def fetch_stock_data(self, symbol: str, period: str = '1y') -> Optional[pd.DataFrame]:
        """
        FinanceDataReader를 사용하여 주식 데이터를 가져옵니다.
        
        Args:
            symbol (str): 주식 심볼 (예: AAPL, 005930)
            period (str): 데이터 기간 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            pd.DataFrame: 주식 데이터 (Date, Open, High, Low, Close, Volume)
        """
        try:
            end_date = datetime.now()
            
            # 기간별 시작 날짜 계산
            period_mapping = {
                '1d': 1,
                '5d': 5,
                '1mo': 30,
                '3mo': 90,
                '6mo': 180,
                '1y': 365,
                '2y': 730,
                '5y': 1825,
                '10y': 3650,
                'ytd': None  # 연초부터
            }
            
            if period == 'ytd':
                start_date = datetime(end_date.year, 1, 1)
            elif period == 'max':
                # 최대 데이터를 위해 날짜 범위 없이 가져오기
                df = fdr.DataReader(symbol)
            else:
                days = period_mapping.get(period, 365)  # 기본값 1년
                start_date = end_date - timedelta(days=days)
            
            # 날짜 범위가 있는 경우 데이터 가져오기
            if period != 'max':
                start_str = start_date.strftime('%Y-%m-%d')
                end_str = end_date.strftime('%Y-%m-%d')
                df = fdr.DataReader(symbol, start_str, end_str)
            
            if df.empty:
                print(f"No data found for symbol: {symbol}")
                return None
            
            # 데이터 전처리
            df = self._preprocess_data(df)
            
            return df
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터 전처리 (컬럼명 소문자 변환, 날짜 컬럼 생성 등)
        
        Args:
            df (pd.DataFrame): 원본 데이터
            
        Returns:
            pd.DataFrame: 전처리된 데이터
        """
        # 인덱스를 컬럼으로 변환 (날짜 보존)
        df = df.reset_index()
        
        # 컬럼명을 소문자로 변환
        df.columns = df.columns.str.lower()
        
        # 날짜 컬럼 처리
        if 'index' in df.columns:
            df['date'] = df['index']
        elif 'date' not in df.columns:
            df['date'] = df.index
            
        return df
    
    def get_data_info(self, df: pd.DataFrame) -> dict:
        """
        데이터 정보를 반환합니다.
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            dict: 데이터 정보 (시작일, 종료일, 데이터 포인트 수)
        """
        if df is None or df.empty:
            return {"error": "No data available"}
        
        return {
            "start_date": df['date'].iloc[0],
            "end_date": df['date'].iloc[-1],
            "data_points": len(df),
            "columns": df.columns.tolist()
        }
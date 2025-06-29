import pandas as pd
import numpy as np
from typing import Dict, Any


class TechnicalAnalyzer:
    """
    기술적 지표를 계산하고 매매 신호를 생성하는 클래스
    """
    
    def __init__(self):
        # 기술적 지표 파라미터 설정
        self.SHORT_EMA_PERIOD = 12
        self.LONG_EMA_PERIOD = 26
        self.RSI_PERIOD = 14
        self.BOLLINGER_PERIOD = 20
        self.BOLLINGER_STD_DEV = 2
        self.MACD_SIGNAL_PERIOD = 9
    
    def calculate_ema(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        EMA (Exponential Moving Average) 계산
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: EMA가 추가된 데이터
        """
        df['EMA_short'] = df['close'].ewm(span=self.SHORT_EMA_PERIOD, adjust=False).mean()
        df['EMA_long'] = df['close'].ewm(span=self.LONG_EMA_PERIOD, adjust=False).mean()
        return df
    
    def calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        MACD (Moving Average Convergence Divergence) 계산
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: MACD가 추가된 데이터
        """
        # EMA가 계산되지 않았다면 먼저 계산
        if 'EMA_short' not in df.columns or 'EMA_long' not in df.columns:
            df = self.calculate_ema(df)
        
        df['MACD'] = df['EMA_short'] - df['EMA_long']
        df['MACD_signal_line'] = df['MACD'].ewm(span=self.MACD_SIGNAL_PERIOD, adjust=False).mean()
        df['MACD_histogram'] = df['MACD'] - df['MACD_signal_line']
        return df
    
    def calculate_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: RSI가 추가된 데이터
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).ewm(alpha=1/self.RSI_PERIOD, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/self.RSI_PERIOD, adjust=False).mean()
        rs = gain.where(loss != 0, 0) / loss.where(loss != 0, 1)
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    def calculate_bollinger_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        볼린저 밴드 계산
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: 볼린저 밴드가 추가된 데이터
        """
        middle = df['close'].rolling(window=self.BOLLINGER_PERIOD).mean()
        std = df['close'].rolling(window=self.BOLLINGER_PERIOD).std()
        df['BB_upper'] = middle + (std * self.BOLLINGER_STD_DEV)
        df['BB_lower'] = middle - (std * self.BOLLINGER_STD_DEV)
        df['BB_middle'] = middle
        return df
    
    def calculate_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        OBV (On-Balance Volume) 계산
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: OBV가 추가된 데이터
        """
        df['OBV'] = pd.Series(
            np.where(df['close'].diff() > 0, df['volume'], 
                    np.where(df['close'].diff() < 0, -df['volume'], 0)), 
            index=df.index
        ).cumsum()
        return df
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        모든 기술적 지표를 계산합니다.
        
        Args:
            df (pd.DataFrame): 주식 데이터
            
        Returns:
            pd.DataFrame: 모든 지표가 추가된 데이터
        """
        df = self.calculate_ema(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_obv(df)
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        기술적 지표를 기반으로 매매 신호를 생성합니다.
        
        Args:
            df (pd.DataFrame): 기술적 지표가 계산된 데이터
            
        Returns:
            pd.DataFrame: 매매 신호가 추가된 데이터
        """
        # EMA 신호
        df['EMA_buy'] = np.where(df['EMA_short'] > df['EMA_long'], 1, 0)
        df['EMA_sell'] = np.where(df['EMA_short'] <= df['EMA_long'], 1, 0)
        
        # MACD 신호
        df['MACD_buy'] = np.where(df['MACD'] > df['MACD_signal_line'], 1, 0)
        df['MACD_sell'] = np.where(df['MACD'] <= df['MACD_signal_line'], 1, 0)
        
        # RSI 신호
        df['RSI_buy'] = np.where(df['RSI'] < 30, 1, 0)  # 과매도 구간에서 매수
        df['RSI_sell'] = np.where(df['RSI'] > 70, 1, 0)  # 과매수 구간에서 매도
        
        # 볼린저 밴드 신호
        df['BB_buy'] = np.where(
            (df['close'] <= df['BB_lower']) | 
            ((df['close'].shift(1) <= df['BB_lower'].shift(1)) & 
             (df['close'] > df['BB_lower'])), 1, 0
        )
        df['BB_sell'] = np.where(df['close'] >= df['BB_upper'], 1, 0)
        
        # OBV 신호
        df['OBV_buy'] = np.where(df['OBV'] > df['OBV'].rolling(window=5).mean(), 1, 0)
        df['OBV_sell'] = np.where(df['OBV'] <= df['OBV'].rolling(window=5).mean(), 1, 0)
        
        # 복합 신호
        total_buy_signals = (
            df['EMA_buy'] + df['MACD_buy'] + df['RSI_buy'] + 
            df['BB_buy'] + df['OBV_buy']
        )
        total_sell_signals = (
            df['EMA_sell'] + df['MACD_sell'] + df['RSI_sell'] + 
            df['BB_sell'] + df['OBV_sell']
        )
        
        # 종합 신호: 매수/매도 신호 개수 비교
        df['buy'] = np.where(total_buy_signals > total_sell_signals, 1, 0)
        df['sell'] = np.where(total_sell_signals > total_buy_signals, 1, 0)
        
        df['Buy_strength'] = total_buy_signals
        df['Sell_strength'] = total_sell_signals
        
        return df
    
    def analyze_stock(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        주식 데이터에 대한 완전한 기술적 분석을 수행합니다.
        
        Args:
            df (pd.DataFrame): 주식 데이터
            symbol (str): 주식 심볼
            
        Returns:
            dict: 분석 결과
        """
        if df is None or df.empty:
            return {"error": f"No data available for {symbol}"}
        
        # 모든 기술적 지표 계산
        df = self.calculate_all_indicators(df)
        df = self.generate_signals(df)
        
        # 최신 데이터 가져오기
        latest = df.iloc[-1]
        
        result = {
            "symbol": symbol,
            "date": latest['date'],
            "price": latest['close'],
            "volume": latest['volume'],
            "technical_indicators": {
                "EMA": {
                    "short": latest['EMA_short'],
                    "long": latest['EMA_long'],
                    "buy": latest['EMA_buy'],
                    "sell": latest['EMA_sell']
                },
                "MACD": {
                    "macd": latest['MACD'],
                    "signal_line": latest['MACD_signal_line'],
                    "histogram": latest['MACD_histogram'],
                    "buy": latest['MACD_buy'],
                    "sell": latest['MACD_sell']
                },
                "RSI": {
                    "value": latest['RSI'],
                    "buy": latest['RSI_buy'],
                    "sell": latest['RSI_sell']
                },
                "Bollinger_Bands": {
                    "upper": latest['BB_upper'],
                    "middle": latest['BB_middle'],
                    "lower": latest['BB_lower'],
                    "buy": latest['BB_buy'],
                    "sell": latest['BB_sell']
                },
                "OBV": {
                    "value": latest['OBV'],
                    "buy": latest['OBV_buy'],
                    "sell": latest['OBV_sell']
                }
            },
            "buy": latest['buy'],
            "sell": latest['sell'],
            "buy_strength": latest['Buy_strength'],
            "sell_strength": latest['Sell_strength'],
            "data_points": len(df)
        }
        
        return result
    
    def get_signal_explanation(self) -> Dict[str, str]:
        """
        신호에 대한 설명을 반환합니다.
        
        Returns:
            dict: 신호 설명
        """
        return {
            "EMA": "단기 EMA > 장기 EMA면 Buy=1, 반대면 Sell=1",
            "MACD": "MACD > Signal Line면 Buy=1, 반대면 Sell=1",
            "RSI": "RSI < 30(과매도)면 Buy=1, RSI > 70(과매수)면 Sell=1",
            "Bollinger_Bands": "가격이 하단밴드 근처면 Buy=1, 상단밴드 근처면 Sell=1",
            "OBV": "OBV > 5일평균면 Buy=1, 반대면 Sell=1",
            "Composite": "Buy 신호 개수 > Sell 신호 개수면 Composite_buy=1, 반대면 Composite_sell=1"
        }
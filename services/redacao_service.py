from typing import Dict, Tuple
from config import logger, openai

class RedacaoService:
    @staticmethod
    async def corrigir_redacao(texto: str) -> Tuple[Dict[str, int], str]:
        """
        Corrige uma redação usando os critérios do ENEM
        Returns: (notas por competência, feedback detalhado)
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um corretor de redações ENEM..."},
                    {"role": "user", "content": f"Corrija esta redação:\n{texto}"}
                ]
            )
            
            # Processar resposta e extrair notas
            notas = {
                "comp1": 0, "comp2": 0, "comp3": 0,
                "comp4": 0, "comp5": 0
            }
            feedback = response.choices[0].message.content
            
            return notas, feedback
            
        except Exception as e:
            logger.error(f"Erro ao corrigir redação: {e}")
            return None, "Erro ao processar a correção" 
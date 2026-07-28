from pathlib import Path
import json

class ConfiguracaoService:

    def __init__(self, caminho_arquivo):

        self.__caminho_arquivo = Path(caminho_arquivo)
        self.__som_ativo = True
        self.__tipo_impressora = "normal"
        self.__impressora = ""
        self.__quantidade_vias = 1
        self.__largura_papel = "80"
   
    @property
    def som_ativo(self):
        return self.__som_ativo
    
    @property
    def tipo_impressora(self):
        return self.__tipo_impressora

    @property
    def impressora(self):
        return self.__impressora
    
    @property
    def quantidade_vias(self):
        return self.__quantidade_vias

    @property 
    def largura_papel(self):
        return self.__largura_papel
    
    def _configuracao_padrao(self):

        return {
            "som_ativo": True,
            "tipo_impressora": "normal",
            "impressora": "",
            "quantidade_vias": 1,
            "largura_papel": "80"
        }

    def _normalizar_configuracoes(self, configuracoes):

        configuracoes_completas = {
            **self._configuracao_padrao(),
            **configuracoes
        }

        tipo_impressora = str(configuracoes_completas.get("tipo_impressora", "normal")).strip().lower()

        if tipo_impressora not in ("normal", "termica"):
            tipo_impressora = "normal"

        configuracoes_completas[ "tipo_impressora"] = tipo_impressora

        nome_impressora = str( configuracoes_completas.get("impressora", "") or "").strip()

        configuracoes_completas["impressora"] = nome_impressora

        try:
            quantidade_vias = int(configuracoes_completas.get("quantidade_vias", 1))

        except (TypeError, ValueError):
            quantidade_vias = 1

        quantidade_vias = max( 1, min(quantidade_vias, 3))

        configuracoes_completas[ "quantidade_vias"] = quantidade_vias

        largura_papel = str(configuracoes_completas.get("largura_papel","80")).replace( "mm", "").strip()

        if largura_papel not in ("58", "80"):
            largura_papel = "80"

        configuracoes_completas["largura_papel"] = largura_papel

        configuracoes_completas["som_ativo"] = bool(configuracoes_completas.get("som_ativo", True))

        return configuracoes_completas

    def _atualizar_atributos(self, configuracoes):

        self.__som_ativo = configuracoes["som_ativo" ]
        self.__tipo_impressora = configuracoes["tipo_impressora" ]
        self.__impressora = configuracoes["impressora"]
        self.__quantidade_vias = configuracoes["quantidade_vias"]
        self.__largura_papel = configuracoes["largura_papel"]

    def carregar_configuracoes(self):

        configuracao_padrao = self._configuracao_padrao()
        
        if not self.__caminho_arquivo.exists():
            self.salvar_configuracoes(configuracao_padrao)
            return configuracao_padrao
        
        try:
            with open(self.__caminho_arquivo, "r", encoding="utf-8") as arquivo:
                configuracoes_salvas = json.load(arquivo)
            
            if not isinstance(configuracoes_salvas, dict):
                raise ValueError("O arquivo de configurações não possui dicionario")
            
            configuracoes_completas = (self._normalizar_configuracoes(configuracoes_salvas))

            self._atualizar_atributos(configuracoes_completas)

            return configuracoes_completas
        except (json.JSONDecodeError, OSError, ValueError) as erro:
            print("Erro ao carregar configurações: ", erro)

            self.salvar_configuracoes(configuracao_padrao)

            return configuracao_padrao

    def salvar_configuracoes(self, configuracoes):

        if not isinstance(configuracoes, dict):

            raise TypeError("As configurações devem ser enviadas em um dicionário!")
        
        configuracoes_completas = (self._normalizar_configuracoes(configuracoes))

        self.__caminho_arquivo.parent.mkdir(parents=True, exist_ok= True)

        with open(self.__caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(configuracoes_completas, arquivo, ensure_ascii=False, indent=4)

        self._atualizar_atributos(configuracoes_completas)

        return configuracoes_completas











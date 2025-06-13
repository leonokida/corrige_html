import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import re

class AgenteCorrigeHtml:
    """
    Agente IA que corrige arquivos HTML com defeitos de sintaxe.

    Métodos:
        corrige_html(conteudo_original): Recebe uma string que contém o conteúdo de um arquivo HTML inválido e retorna uma string com o conteúdo corrigido.
    """

    def __init__(self):
        """
        Inicializa conexão com API da Azure OpenAI
        """
        load_dotenv()
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        self.deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


    def corrige_html(self, conteudo_original: str) -> str:
        """
        Input: conteúdo original do arquivo HTML, com erros de sintaxe
        Output: conteúdo corrigido do arquivo HTML
        """

        system_prompt = """
            Você é um assistente especializado em corrigir arquivos HTML. Sua tarefa crucial é apenas corrigir erros de sintaxe em tags HTML e parâmetros, como endereços de e-mail ou URLs.

            Em hipótese alguma você deve alterar o texto ou o conteúdo das páginas. Seu foco é estritamente na validação do HTML, garantindo que as tags e seus atributos estejam corretos.

            Sua resposta deve ser exclusivamente o código HTML corrigido. Se o que você receber não for um arquivo HTML válido ou se você não puder fazer as correções, retorne uma string vazia: "".
        """

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conteudo_original}
            ],
            temperature=0.3,
            max_tokens=5000
        )

        html_string = response.choices[0].message.content.strip()

        # Extrai só o HTML
        match = re.search(r'(<!DOCTYPE html[\s\S]*</html>)', html_string)
        if match:
            html_code = match.group(1)
        else:
            html_code = ""

        return html_code
from agente_corrige_html import AgenteCorrigeHtml
import sys
import os

def sanitize_filename(filename, base_dir=None):
    """
    Normaliza e sanitiza o nome do arquivo para remover componentes indesejados como './' ou '../'.
    Se base_dir for fornecido, garante que o arquivo permaneça dentro desse diretório.
    """
    # Normaliza o caminho (remove ./, resolve ../, etc)
    normalized_path = os.path.normpath(filename)

    # Opcional: força o caminho a ficar relativo (evita caminho absoluto malicioso)
    normalized_path = normalized_path.lstrip(os.sep)

    # Se quiser garantir que o caminho fique dentro de um diretório específico
    if base_dir:
        safe_path = os.path.normpath(os.path.join(base_dir, normalized_path))
        # Protege contra path traversal
        if not os.path.commonpath([os.path.abspath(safe_path), os.path.abspath(base_dir)]) == os.path.abspath(base_dir):
            raise ValueError("Caminho não permitido.")
        return safe_path

    return normalized_path

# Verifica se recebeu arquivo por argv
if len(sys.argv) < 2:
    print("Modo de utilizar: python main.py <nome do arquivo>")
    exit(-1)

# Carrega conteúdo do arquivo em string
nome_arq = sys.argv[1]
with open(nome_arq, "r", encoding="utf-8") as arq:
    conteudo = arq.read()
arq.close()
print("Arquivo HTML carregado")

# Utiliza o agente corretor de HTML para corrigir conteúdo
print("Corrigindo conteúdo...")
corretor = AgenteCorrigeHtml()
conteudo_corrigido = corretor.corrige_html(conteudo_original=conteudo)

if conteudo_corrigido == "":
    print("Houve um erro ao corrigir o arquivo HTML")
    exit(-1)

# Escreve string com conteúdo corrigido em novo arquivo
nome_arq = sanitize_filename(nome_arq)
nome_arq_corrido = nome_arq.split('.')[0] + "_corrigido." + nome_arq.split('.')[1]
with open(nome_arq_corrido, "w", encoding="utf-8") as arq:
    arq.write(conteudo_corrigido)
arq.close()
print("Arquivo HTML corrigido!")
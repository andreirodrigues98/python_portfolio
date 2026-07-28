from pathlib import Path
import shutil

def obter_categorias():
    categorias = {
    '.pdf': 'PDFs',

    '.jpg': 'Imagens',
    '.jpeg': 'Imagens',
    '.png': 'Imagens',
    '.gif': 'Imagens',
    '.webp': 'Imagens',
    '.bmp': 'Imagens',
    '.svg': 'Imagens',
    '.ico': 'Imagens',

    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.avi': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.webm': 'Videos',

    '.mp3': 'Audios',
    '.wav': 'Audios',
    '.ogg': 'Audios',
    '.m4a': 'Audios',
    '.flac': 'Audios',

    '.doc': 'Documentos',
    '.docx': 'Documentos',
    '.txt': 'Documentos',
    '.md': 'Documentos',
    '.rtf': 'Documentos',
    '.odt': 'Documentos',

    '.xls': 'Planilhas',
    '.xlsx': 'Planilhas',
    '.csv': 'Planilhas',
    '.ods': 'Planilhas',

    '.ppt': 'Apresentacoes',
    '.pptx': 'Apresentacoes',
    '.odp': 'Apresentacoes',

    '.json': 'Dados',
    '.xml': 'Dados',
    '.yaml': 'Dados',
    '.yml': 'Dados',

    '.py': 'Codigos',
    '.c': 'Codigos',
    '.cpp': 'Codigos',
    '.java': 'Codigos',
    '.js': 'Codigos',
    '.ts': 'Codigos',
    '.jsx': 'Codigos',
    '.tsx': 'Codigos',
    '.html': 'Codigos',
    '.css': 'Codigos',
    '.php': 'Codigos',
    '.sql': 'Codigos',
    '.toml': 'Codigos',

    '.zip': 'Compactados',
    '.rar': 'Compactados',
    '.7z': 'Compactados',
    '.tar': 'Compactados',
    '.gz': 'Compactados',
    '.bz2': 'Compactados',
    '.xz': 'Compactados',

    '.iso': 'Imagens_de_Disco',

    '.exe': 'Instaladores',
    '.msi': 'Instaladores',
    '.msix': 'Instaladores',
    '.appx': 'Instaladores',
    '.appxbundle': 'Instaladores',
    '.msixbundle': 'Instaladores',

    '.bat': 'Scripts',
    '.cmd': 'Scripts',
    '.ps1': 'Scripts',

    '.ttf': 'Fontes',
    '.otf': 'Fontes',
    '.woff': 'Fontes',
    '.woff2': 'Fontes',

    '.epub': 'Ebooks',
    '.mobi': 'Ebooks',

    '.stl': 'Modelos_3D',
    '.obj': 'Modelos_3D',
    '.fbx': 'Modelos_3D',
    '.blend': 'Modelos_3D',
    '.gltf': 'Modelos_3D',
    '.glb': 'Modelos_3D'
}

    return categorias

def validar_pasta():
    caminho = input('Digite o caminho da pasta(Ex: C:\\Users\\SeuNome\\Downloads): ').strip()

    if not caminho:
        print('Preencha o campo corretamente!')
        return 
    
    pasta = Path(caminho)

    if not pasta.exists():
        print('Pasta não existe')
        return 
    
    if not pasta.is_dir():
        print('Esse caminho não pertence a uma pasta')
        return 
    
    return pasta

def destino_unico(pasta_destino, item):
    destino_final = pasta_destino / item.name

    contador = 1 

    while destino_final.exists():
        novo_nome = f'{item.stem}_{contador}{item.suffix}'
        destino_final = pasta_destino / novo_nome
        contador += 1

    return destino_final

def relatorio_final(total_movidos, relatorio):
    print('\n=============== Relatorio Final ===============')

    if total_movidos == 0:
        print('Nenhum arquivo novo foi movido')
    else:
        print(f'A quantidade de arquivos movidos foi: {total_movidos}\n')

        for categoria, quantidade in relatorio.items():
            print(f'{categoria}: {quantidade} arquivo(s)')

def organizar_arquivo(item, categorias, pasta, relatorio):
            
    print(f'\nNome: {item.name}\nExtensão: {item.suffix.lower()}')
    extensao = item.suffix.lower()
    categoria = categorias.get(extensao, 'Outros')
    print(f'Categoria: {categoria}')

    if categoria not in relatorio:
        relatorio[categoria] = 0 

    pasta_destino = pasta / categoria
    pasta_destino.mkdir(exist_ok = True)

    print(f'Pasta usada/criada: {pasta_destino}')

    destino_final = destino_unico(pasta_destino, item)

    try:       
        shutil.move(item, destino_final)
        print('Arquivo movido com sucesso!')
        relatorio[categoria] += 1
        return True

    except Exception as erro:
        print(f'Não foi possivel mover o arquivo: {item.name}!')
        print(f'Erro: {erro}')
        return False

def analisar_pasta():
    
    categorias = obter_categorias()
    
    pasta = validar_pasta()

    if pasta is None:
        return 
    
    print('\nPasta encontrada com sucesso!')
    print(f'Caminho: {pasta}')

    total_movidos = 0
    relatorio = {}

    for item in pasta.iterdir():
        if item.is_file():
            organizar = organizar_arquivo(item, categorias, pasta, relatorio)
            if organizar:
                total_movidos += 1

    relatorio_final(total_movidos, relatorio)
    
if __name__ == '__main__':
    analisar_pasta()
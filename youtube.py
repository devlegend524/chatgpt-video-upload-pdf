import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'

from youtubesearchpython import CustomSearch, VideoSortOrder
from pytube import YouTube
import whisper
import re


# Metodo que realiza a busca videos referente a um assunto(parametro "procurar") no youtube
# retornando a quantidade de videos definidas (parametro "limite") ordenadas por relevancia
def find_videos(procurar, limite):
    list_video = []
    customSearch = CustomSearch(procurar, VideoSortOrder.relevance, limit=limite, language='pt-BR')
    result = customSearch.result()['result']
    total = len(result)
    if total > 0:
        for vid in result:
            list_video.append({"videos": vid['id'], "views": vid['viewCount']['short'], "titulo": vid['title']})
        if total > limite:
            list_video = list_video[:limite]
    return list_video


# Recebe uma lista de id`s e outra de nome dos videos a serem transcritos em texto
# Aqui é utilizado o modelo "whisper" que transforma audio em texto, modelo tamebm da OpenAi
# https://openai.com/research/whisper
def vid_toText(video_id, nome, dir_in, dir_out):
  # Baixar o modelo pré treinados (conforme imagem acima)
  model     = whisper.load_model('medium', download_root='./modelo_whisper/medium/', device= device)
  
  for idx, itm in enumerate(video_id):
    # Cria nome padronizado sem caracteres especiais
    nome_video = re.sub("[^A-Z]", "", nome[idx],0,re.IGNORECASE)
    # Criar o objeto de video, e realizar o download apenas do audio do video
    youtube_video = YouTube('https://youtu.be/'+ itm) 
    streams   = youtube_video.streams.filter(only_audio=True)
    stream    = streams.first()
    stream.download(filename= dir_in + nome_video + '.mp4')
    # Aplicar o modelo whisper no audio 
    output = model.transcribe(dir_in + nome_video + '.mp4')
    segments = output['segments']
    # Salvar a saida do modelo (texto do video)
    with open(dir_out + nome_video +'.txt','w', encoding='utf-8') as the_file:
        for segment in segments:
          the_file.write(segment["text"].strip() + '\n')


# Realiza a junção das duas funcoes, busca e abtem os textos do video.
def busca_youtube(q, limite):
  videos = find_videos(q, limite)
  video_id = []
  nome = []
  for v in videos:
      video_id.append(v['videos'])
      nome.append(v['titulo'])  
  vid_toText(video_id,nome)
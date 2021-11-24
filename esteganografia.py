# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:17:52 2021

@author: josec
"""

import cv2
import numpy as np


def mensagemParaBinario(mensagem):
    if type(mensagem) == str:
        return ''.join([ format(ord(i), "08b") for i in mensagem])
    elif type(mensagem) == bytes or type(mensagem) == np.ndarray:
        return [format(i,"08b") for i in mensagem]
    elif type(mensagem) == int or type(mensagem) == np.uint8:
        return format(mensagem, "08b")
    else:
        raise TypeError("Tipo nao suportado")
        
#função para esconder a mensagem na imagem

def esconderData(imagem,mensagem_secreta):
    #calcular o numero de bytes maximos para codificar
    n_bytes= imagem.shape[0] * imagem.shape[1]*3//8
    print("Numero maximo de bytes para codificar: ", n_bytes)
    
    #Checa se o numero de bytes para codificar é menor que o numero maximo de 
    #bytes da imagem
    if len(mensagem_secreta) > n_bytes:
        raise ValueError("Encontrou um numero insuficiente de bytes, precisa de uma imagem maior ou menos data!")
    mensagem_secreta+= "#####" #usando qualquer string como delimitador

    data_index=0
    #converter dados de entrada para binário
    binaria_mensagem_secreta=mensagemParaBinario(mensagem_secreta)

    data_len = len(binaria_mensagem_secreta) #encontra o tamanho da mensagem a ser escondida
    for values in imagem:
        for pixel in values:
            #converte RGB para binario
            r, g, b=mensagemParaBinario(pixel)
            #modifica o bit menos significativo se,e somente se, ainda há data para armazenar
            if data_index < data_len:
                #esconde o dado no bit menos significativo do pixel vermelho
                pixel[0]= int(r[:-1]+binaria_mensagem_secreta[data_index], 2)
                data_index+=1
            if data_index < data_len:
                #esconde o dado no bit menos significativo do pixel verde
                pixel[1]= int(g[:-1]+binaria_mensagem_secreta[data_index], 2)
                data_index+=1
            if data_index < data_len:
                #esconde o dado no bit menos significativo do pixel vermelho
                pixel[2]= int(b[:-1]+binaria_mensagem_secreta[data_index], 2)
                data_index+=1
            # se os dados já estão codificados,sai do loop
            if data_index >= data_len:
                break
    return imagem

def mostrarData(imagem):

  binaria_data = ""
  for values in imagem:
      for pixel in values:
          r, g, b = mensagemParaBinario(pixel) #converte os valores rgb para um formato binário
          binaria_data += r[-1] #extraindo data do bit menos significativo do pixel vermelho
          binaria_data += g[-1] #extraindo data do bit menos significativo do pixel verde
          binaria_data += b[-1] #extraindo data do bit menos significativo do pixel azul
  # divide por 8-bits
  todos_bytes = [ binaria_data[i: i+8] for i in range(0, len(binaria_data), 8) ]
  # converte de bits para caracteres ASCII
  decodificada_data = ""
  for byte in todos_bytes:
      decodificada_data += chr(int(byte, 2))
      if decodificada_data[-5:] == "#####": #checa se o delimitador "#####" é alcançado
          break
  #print(decodificada_data)
  return decodificada_data[:-5] #remove o delimitador para mostrar a mensagem secreta original
    
#codificar a mensagem na imagem
def codificado_texto():
    nome_imagem= input("digite o nome da imagem(com a extensão plz):")
    imagem= cv2.imread(nome_imagem)#lê a imagem usando OpenCV do Python
    
    #detalhes da imagem
    print("A forma da imagem e: ", imagem.shape)#checa a forma da imagem para calcular os bytes nela
    print("A imagem original é mostrada abaixo: ")
    redimensionada_imagem= cv2.resize(imagem, (500,500)) #redimensiona a imagem para 500 x 500
    cv2.imshow("Imagem Original",redimensionada_imagem)#mostra a imagem
    #espera o usuário apertar qualquer tecla,isso é necessario para evitar que o kernel do python crashe
    cv2.waitKey(0) 
    #fecha todas as janelas abertas
    cv2.destroyAllWindows()
    
    data= input("digite a mensagem a ser codificada na imagem: ")
    if(len(data) == 0):
        raise ValueError("Digite uma mensagem de verdade, poxa!")
    
    nome_arquivo= input("digite o nome da nova imagem codificada(com extensao plz):")
    imagem_codificada= esconderData(imagem, data) #deixa a função esconderData esconder a mensagem na imagem
    cv2.imwrite(nome_arquivo,imagem_codificada)
    
def decodificado_texto():
    # lê a imagem com o texto codificado
    nome_imagem= input("digite o nome da imagem com mensagem codificada(com extensao plz):")
    imagem= cv2.imread(nome_imagem)#lê a imagem com OpenCV

    print("A imagem com mensagem codificada e mostrada abaixo: ")
    redimensionada_imagem=cv2.resize(imagem,(500,500))
    cv2.imshow("Imagem Codificada",redimensionada_imagem)
    #espera o usuário apertar qualquer tecla,isso é necessario para evitar que o kernel do python crashe
    cv2.waitKey(0) 
    #fecha todas as janelas abertas
    cv2.destroyAllWindows()
    
    texto=  mostrarData(imagem)
    return texto    

#imagem esteganografada
def esteganografia():
    a=input("Estenografar imagem \n 1.Codificar data \n 2.Decodificar data \n Sua entrada é(1 ou 2): ")
    usuario_entrada= int(a)
    if(usuario_entrada == 1):
        print("Codificando imagem...")
        codificado_texto()
    elif(usuario_entrada == 2):
        print("Decodificando imagem...")
        print("A mensagem decodificada é: "+ decodificado_texto())
    else:
        raise Exception("digite uma entrada valida")
       
esteganografia() #chama a função principal        
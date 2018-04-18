import json, sys, os
import subprocess as s
from bs4 import BeautifulSoup as bs
import requests

class Chatbot():
    a = 0
    b = 0
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            memoria = open(nome+'.json','w')
            memoria.write('[["Michele","Almeida"],{"oi": "Oie, o que voce precisa?","obrigada":"foi um prazer ajudar"}]')
            memoria.close()
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases = json.load(memoria)
        memoria.close()
        self.historico = [None,]

    def escuta(self, frase=None):
        if frase == None:
            frase = input('>: ')
        frase = str(frase)
        frase = frase.lower()
        frase = frase.replace('é','é')
        
        return frase
  
    def pensa(self,frase):
        
        if frase in self.frases:
            if frase == 'Aprendizado' or frase == 'aprendizado':
                self.b = 1
            return self.frases[frase]
        
        if frase == 'Receitas' or frase == 'receitas':
            self.a = 1
            return 'Qual receita deseja pesquisar?'
        if self.a == 1:
            self.a = 0            
            return self.receitas(frase)
        
        #responde frases que dependem do histórico
        ultimaFrase = self.historico[-1]         
        if ultimaFrase == 'Olá, o que você precisa?':
            nome = self.pegaNome(frase)
            frase = self.respondeNome(nome)
            return frase
        if self.b == 1:
            self.chave = frase
            self.b = 2
            self.a = 0
            return 'Ohhh! Me dá a resposta: '
        if self.b == 2:
            self.b = 0
            resp = frase
            self.frases[self.chave] = resp
            self.gravaMemoria()
            return 'Ohhh, que legal! '
        if ultimaFrase == 'digite a receita':
            return receitas(frase)
        try:
            resp = str(eval(frase))
            return resp
        except:
            pass
        return 'lost'

      
    def receitas(self, pesquisa):
        pesquisa = str(pesquisa)
        pesquisa = pesquisa.split(' ')
        pesquisa = "+".join(pesquisa)
        page = requests.get("http://www.tudogostoso.com.br/busca?q="+pesquisa)
        soup = bs(page.content, "html.parser")
                   
        for link in soup.find_all('a'):
            endereco = str(link.get('href'))
            if('tudogostoso' in endereco and pesquisa in endereco):
                return str(endereco)
            
    def pegaNome(self,nome):
        if 'o meu nome é ' in nome:
            nome = nome[14:]

        nome = nome.title()
        return nome

    def respondeNome(self,nome):
        if nome in self.conhecidos:
            frase = 'Oi '
        else:
            frase = 'Muito prazer '
            self.conhecidos.append(nome)
            self.gravaMemoria()
        return frase+nome
    
    def gravaMemoria(self):
        memoria = open(self.nome+'.json','w')
        json.dump([self.conhecidos, self.frases],memoria)
        memoria.close()
            

    def fala(self,frase):
        if 'executa ' in frase:
            plataforma = sys.platform
            comando = frase.replace('executa ','')
            if 'win' in plataforma:
                os.startfile(comando)
            if 'linux' in plataforma:
                try:
                    s.Popen(comando)
                except FileNotFoundError:
                    s.Popen(['xdg-open',comando])
        else:
            print(frase)
        self.historico.append(frase)

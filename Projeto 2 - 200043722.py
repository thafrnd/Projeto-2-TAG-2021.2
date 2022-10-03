# Projeto 2 da disciplina Teoria e Aplicação de Grafos
# Universidade de Brasilia
# Departamento de Ciencia da Computacao
# Professor: Díbio Leandro Borges
# Aluna: Thaís Fernanda de Castro Garcia
# Matricula: 200043722

from pathlib import Path
from collections import defaultdict
#Função que le o arquivo txt o qual contem os dados
def ler_arquivo():
        file = Path(__file__).absolute().parent / "entradaProj2TAG.txt"
        with open(file, "r") as f:
            usable = [x for x in f.readlines() if x[0] == '(']        
        dados=[]
        projects = [x for x in usable if x[1] == 'P']
        students = [x for x in usable if x[1] == 'A']
        dados.append(projects)
        dados.append(students)
        return dados
#A função trata os dados e retorna uma lista para que possa ser usada na função de Gale-Shapley
def organiza_dados(projects, students):       
        alunos_organizados={}  
        projetos_organizados={}
        dados_organizados=[]
        
        for x in students:
            x = x.replace(' (', ';')    
            x = x.replace('(', '')      
            x = x.replace(')', '')
            
            
            a, b = x.split(':')     
            c, d = b.split(';') 
            c = c.split(', ')                            
            alunos_organizados[a] = tuple([int(d)]+[tuple(c)])
                    
        for y in projects:    
            y = y.replace('(', '')   
            y = y.replace(')', '')
            
            
            b, vagas, nota = y.split(', ')  
            nota = int(nota)                 
            a = tuple(sorted([i[0] for i in alunos_organizados.items() 
                if i[1][0] >= nota and b in i[1][1]],        
                key = lambda x: alunos_organizados[x][0], reverse=True))   
            projetos_organizados[b] = tuple([int(vagas)]+[a])
            
        dados_organizados.append(projetos_organizados)
        dados_organizados.append(alunos_organizados)
        
        
        return dados_organizados
String=[]
#Função responsável por executar o algoritmo de Gale-Shapley
def gale_shapley(projetos_organizados, alunos_organizados):
    students={}                                                   #Todo aluno começa livre
    projects={}                                                   #Os projetos começam vazios
    for i in alunos_organizados.keys():                           #Vamos iterar sobre os projetos livres
        students[i]=None                                          #Para cada projeto vamos iterar todos os alunos
    for i in projetos_organizados.keys():                         #Se tiver livre adiciona ao projeto
        projects[i]= []                                           #Se não estiver livre mas preferir esse projeto ele é retirado do projeto atual e adicionado ao novo
    projetos_livres = list(projects.keys())                       #O antigo projeto fica livre
                                                                  #Caso o projeto não esteja livre passa para o proximo da fila
                                                                  #As iterações são registradas com auxilio de uma lista que armazena 10 iterações
                                                                  #A faixa das iterações é selecionada manualmente
                                                                  #A função retorna uma lista que possibilita printar o resultado
                                                                  
    i = 0                                                         
    while projetos_livres:                                        
        p = projetos_livres.pop(0)                                
        for a in projetos_organizados[p][1]:     
            string = f"Tentativa de adicionar o aluno {a} ao projeto {p}"   
            prioridade = students[a]
            if not prioridade:         
                projects[p].append(a)  
                students[a] = p       
                string = f"O aluno {a} entrou para o projeto {p}"
            else:
                if alunos_organizados[a][1].index(p) < alunos_organizados[a][1].index(prioridade):   
                    students[a] = p   
                    projects[prioridade].remove(a)    
                    projects[p].append(a)  
                    string = f"O aluno {a} saiu do projeto {prioridade} e entrou no projeto {p}"
                    if prioridade not in projetos_livres:  
                        projetos_livres.append(prioridade)    
                elif alunos_organizados[a][1].index(p) > alunos_organizados[a][1].index(prioridade):
                    string += f", mas o aluno prefere {prioridade}"

            if 20 <= i <=30:
                String.append(string)
            i += 1

            if len(projects[p]) == projetos_organizados[p][0]:
                break

    return projects



dados = ler_arquivo()
dados_organizados=organiza_dados(dados[0],dados[1])
projetos_organizados=dados_organizados[0]
alunos_organizados=dados_organizados[1]
pares = gale_shapley(projetos_organizados, alunos_organizados)
print("\nPós Emparelhamento:")
projetos_vazios = 0
projetos_incompletos = 0

for x in pares.items():
    if x[1]:
        print(f"{x[0]}: {', '.join(x[1])}")
        
        if len(x[1]) < projetos_organizados[x[0]][0]:
            projetos_incompletos += 1
    else:
            print(f"{x[0]}: Projeto Vazio")
            projetos_vazios += 1
print("\nIterações:")

#Parte do código responsável por printar as iterações
conta=0
while conta <=10:
    print(f"Iteração {conta+20}: {String[conta]}")
    conta=conta+1

print(f"\n{projetos_vazios} Projeto(s) acabaram vazios")
print(f"{projetos_incompletos} Projeto(s) não lotaram todas suas vagas")
print(f"{30-(projetos_vazios+projetos_incompletos)} Projeto(s) foram completamente preenchidos")



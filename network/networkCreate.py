import datacreate.processingFile as dp

path = "/home/leandronascimento/Documentos/UNIVERSIDADE FEDERAL DE MINAS GERAIS/LISBOA/analiseLisboa.xlsx"

node, edges = dp.get_files(path=path, tabname="controle",
                           firstcolumn=7, lastcolumn=20,
                           corrlevel=0.8)


print(node)
print("")
print(edges)
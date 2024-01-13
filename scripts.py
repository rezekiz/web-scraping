# TODO docstrings

# Com este código criamos a função get_xml() para captura a informação da página
def get_xml(nuccore_id):

    import requests
    url = 'https://www.ncbi.nlm.nih.gov/nuccore/'+nuccore_id
    return requests.get(url)

# Declaramos funções para sistematizar este workflow

def get_ncbi_uid(nuccore_id):
    
    fonte = get_xml(nuccore_id)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(fonte.content, 'lxml-xml')
    id = soup.find_all('meta',{'name':'ncbi_uidlist'})[0].attrs['content']
    return id

def get_gb_file(nuccore_id):
    
    id = get_ncbi_uid(nuccore_id)
    src = f'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=genbank&id={id}&conwithfeat=on&withparts=on&show-sequence=on&hide-cdd=on&ncbi_phid=CE8B8E325A26C7610000000006A205E5'
    
    import requests
    r = requests.get(src)
    gb_file = r.text
    
    return gb_file

#####################################
# RESERVADO PARA A FUNÇÃO SAVE_FILE #
#####################################


def parse_genbank(nuccore_id):
    import re
    
    locus = get_gb_file(nuccore_id)
    
    i = re.match(r'LOCUS\s+(\w+)', locus)
    if i:
        id = i.group(1)
    organism = ""
    o = re.search(r'SOURCE\s+.+', locus)
    if o:
        s = re.match(r'SOURCE\s+(.+)', o[0] )
        if s:
            organism = s.group(1)
    sequencia = ""
    existe = re.findall(r'^\s+\d+ [actg ]+', locus, re.MULTILINE )
    if existe:
        for linha in existe:
            m = re.match( r'\s+\d+ (.+)', linha, re.DOTALL )
            # print( m.group(1) )
            # print( re.sub(r'\s+', '', m.group(1) ) ) 
            sequencia = sequencia + re.sub(r'\s+', '', m.group(1) )
    return (id, organism, sequencia)

######################################################################
# RESERVADO PARA FUNÇÕES:                                            #
#   - connect_db(address,user,pword)                                 #
#       implementação da criação de conectores                       #
#                                                                    # 
#   - create_table_db(db, table_name, **fields)                      #
#       criação de tabelas com campos e data-types definidos         #
#       invoca a função connect_db                                   #
#                                                                    #   
#   - insert_data_db(db,table_name,data)                             #
#       inserção de dados na base de dados                           #
#       invoca a função create_table_db se a tabela não existir      #
#       invoca a função connect_db                                   #
######################################################################